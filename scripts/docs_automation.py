#!/usr/bin/env python3
"""FLEXT-Meltano Documentation Automation Framework.

Automated scheduling, CI/CD integration, and continuous maintenance
for documentation quality assurance using complete FLEXT ecosystem integration.

ARCHITECTURAL INTEGRATION:
- r[T]: Railway pattern error handling
- FlextSettings: Centralized configuration management
- FlextLogger: Structured logging with correlation
- FlextService: Service base class with dependency injection
- FlextCli: CLI utilities for subprocess operations
- FlextQuality: Quality assurance integration
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time as time_module
from collections.abc import Callable
from pathlib import Path

import schedule
from flext_cli import (
    FlextCliCmd,
)
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextTypes as t,
    e,
    r,
    s,
)

from flext_meltano.docs_config import DocsConfig
from flext_meltano.docs_templates import DocsTemplates


class DocumentationAutomation(s):
    """Automated documentation maintenance and CI/CD integration using FLEXT ecosystem.

    Extends FlextService with dependency injection and railway pattern error handling.
    Integrates with FlextCli for subprocess operations and FlextLogger for structured logging.
    """

    def __init__(
        self,
        logger: FlextLogger | None = None,
        cli_cmd: FlextCliCmd | None = None,
    ) -> None:
        """Initialize DocumentationAutomation with FLEXT ecosystem integration.

        Args:
            logger: FlextLogger instance (injected via container)
            cli_cmd: FlextCliCmd instance (injected via container)

        """
        super().__init__(logger=logger)

        # Dependency injection setup
        self._container = FlextContainer.get_global()
        self._cli_cmd = cli_cmd or self._container.get("FlextCliCmd").unwrap_or(
            FlextCliCmd(),
        )

        # Template system for content generation
        self._templates = DocsTemplates(logger=None)

        # Access configuration via singleton
        self._config = DocsConfig.get_instance()
        self.maintenance_script = Path("scripts/docs_maintenance.py")

        # Validate maintenance script exists using r pattern
        if not self.maintenance_script.exists():
            error_msg = f"Maintenance script not found: {self.maintenance_script}"
            self.logger.error("Maintenance script validation failed", error=error_msg)
            raise e.ConfigurationError(error_msg)

    def run_ci_checks(self) -> r[bool]:
        """Run documentation quality checks for CI/CD pipeline using FLEXT patterns.

        Returns:
            r containing success status with detailed error information

        """
        self.logger.info("Starting CI documentation quality checks")

        # Run comprehensive audit using FlextCli
        audit_result = self._run_maintenance_audit("--comprehensive")
        if not audit_result.is_success:
            self.logger.error("Documentation audit failed", error=audit_result.error)
            return r.fail(audit_result.error or "Documentation audit failed")

        # Check quality thresholds
        quality_check_result = self._validate_quality_thresholds()
        if not quality_check_result.is_success:
            self.logger.error(
                "Quality threshold validation failed",
                error=quality_check_result.error,
            )
            return r.fail(
                quality_check_result.error or "Quality threshold validation failed",
            )

        success_status = quality_check_result.value
        if success_status:
            self.logger.info("CI documentation quality checks passed")
        else:
            self.logger.warning("CI documentation quality checks failed")

        return r.ok(success_status)

    def _run_maintenance_audit(self, *args: str) -> r[None]:
        """Run maintenance audit using FlextCli.

        Args:
            *args: Command line arguments for the maintenance script

        Returns:
            r indicating success or failure

        """
        try:
            # Import maintenance module directly instead of subprocess call
            maintenance_spec = importlib.util.spec_from_file_location(
                "maintenance_audit",
                self.maintenance_script,
            )
            if not maintenance_spec or not maintenance_spec.loader:
                return r.fail(
                    f"Could not load maintenance script: {self.maintenance_script}",
                )

            maintenance_module = importlib.util.module_from_spec(maintenance_spec)
            sys.modules["maintenance_audit"] = maintenance_module
            maintenance_spec.loader.exec_module(maintenance_module)

            # Call maintenance audit function directly
            if hasattr(maintenance_module, "run_comprehensive_audit"):
                result = maintenance_module.run_comprehensive_audit(*args)
                if isinstance(result, dict) and result.get("success", False):
                    return r.ok(True)
                if result:
                    return r.ok(True)
                return r.fail("Maintenance audit completed with warnings")
            return r.fail(
                f"No run_comprehensive_audit function found in {self.maintenance_script}",
            )

        except Exception as e:
            error_msg = f"Failed to execute maintenance audit: {e}"
            self.logger.exception("Maintenance audit execution failed", error=error_msg)
            return r.fail(error_msg)

    def _validate_quality_thresholds(self) -> r[bool]:
        """Validate quality thresholds against generated summary.

        Returns:
            r containing validation result

        """
        try:
            summary_path = (
                Path(self._config.reports_output_dir) / "docs_quality_summary.json"
            )

            if not summary_path.exists():
                error_msg = f"Quality summary not found at {summary_path}"
                self.logger.warning("Quality summary missing", path=str(summary_path))
                return r.ok(False)  # Not a failure, just no data

            with Path(summary_path).open(encoding="utf-8") as f:
                summary = json.load(f)

            quality_score = summary.get("quality_score", 0)
            issues = summary.get("issues", {})

            # Check critical issues
            critical_count = issues.get("by_severity", {}).get("critical", 0)
            fail_on_critical = self._config.fail_on_critical_issues

            if critical_count > 0 and fail_on_critical:
                error_msg = f"Critical documentation issues found: {critical_count}"
                self.logger.error("Critical issues detected", count=critical_count)
                return r.fail(error_msg)

            # Check quality score threshold
            min_score = self._config.min_quality_score

            if quality_score < min_score:
                error_msg = f"Quality score {quality_score} below threshold {min_score}"
                self.logger.error(
                    "Quality score below threshold",
                    score=quality_score,
                    threshold=min_score,
                )
                return r.fail(error_msg)

            self.logger.info(
                "Quality thresholds validated successfully",
                score=quality_score,
                critical_issues=critical_count,
            )
            return r.ok(True)

        except Exception as e:
            error_msg = f"Quality threshold validation failed: {e}"
            self.logger.exception("Quality validation failed", error=error_msg)
            return r.fail(error_msg)

    def schedule_maintenance(self) -> None:
        """Set up scheduled maintenance tasks."""
        automation_config = self._config.get_schedule_config()

        if not automation_config.get("enable_scheduled_audits", False):
            return

        schedule_type = automation_config.get("audit_schedule", "weekly")

        if schedule_type == "daily":
            self._schedule_daily(automation_config)
        elif schedule_type == "weekly":
            self._schedule_weekly(automation_config)
        elif schedule_type == "monthly":
            self._schedule_monthly(automation_config)

    def _schedule_daily(self, config: dict[str, t.GeneralValueType]) -> None:
        """Schedule daily maintenance."""
        if schedule is None:
            self.logger.warning("Schedule library not available, skipping scheduling")
            return

        audit_time = str(config.get("audit_time", "09:00"))
        hour, minute = map(int, audit_time.split(":"))

        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
            self._run_scheduled_audit,
        )

    def _schedule_weekly(self, config: dict[str, t.GeneralValueType]) -> None:
        """Schedule weekly maintenance."""
        if schedule is None:
            self.logger.warning("Schedule library not available, skipping scheduling")
            return

        audit_day = str(config.get("audit_day", "monday")).lower()
        audit_time = str(config.get("audit_time", "09:00"))
        hour, minute = map(int, audit_time.split(":"))

        # Map day names to schedule methods
        day_methods = {
            "monday": schedule.every().monday,
            "tuesday": schedule.every().tuesday,
            "wednesday": schedule.every().wednesday,
            "thursday": schedule.every().thursday,
            "friday": schedule.every().friday,
            "saturday": schedule.every().saturday,
            "sunday": schedule.every().sunday,
        }

        if audit_day in day_methods:
            day_methods[audit_day].at(f"{hour:02d}:{minute:02d}").do(
                self._run_scheduled_audit,
            )

    @staticmethod
    def _schedule_monthly(config: dict[str, t.GeneralValueType]) -> None:
        """Schedule monthly maintenance."""
        # Run on the 1st of each month
        audit_time = str(config.get("audit_time", "09:00"))
        _hour, _minute = map(int, audit_time.split(":"))

        # Monthly scheduling not supported by schedule library
        # schedule.every().month.at(f"{hour:02d}:{minute:02d}").do(
        #     self._run_scheduled_audit
        # )

    def _run_scheduled_audit(self) -> None:
        """Run scheduled documentation audit using direct module import."""
        try:
            # Import maintenance module directly instead of subprocess call
            maintenance_spec = importlib.util.spec_from_file_location(
                "scheduled_audit",
                self.maintenance_script,
            )
            if not maintenance_spec or not maintenance_spec.loader:
                self.logger.error(
                    "maintenance_script_load_failed",
                    path=str(self.maintenance_script),
                )
                return

            maintenance_module = importlib.util.module_from_spec(maintenance_spec)
            sys.modules["scheduled_audit"] = maintenance_module
            maintenance_spec.loader.exec_module(maintenance_module)

            # Call comprehensive audit function directly
            if hasattr(maintenance_module, "run_comprehensive_audit"):
                maintenance_module.run_comprehensive_audit("--comprehensive")
            else:
                self.logger.warning(
                    "maintenance_function_not_found",
                    function="run_comprehensive_audit",
                    script=str(self.maintenance_script),
                )

        except Exception as e:
            self.logger.exception("scheduled_audit_execution_failed", error=str(e))

    def run_continuous_monitoring(self) -> None:
        """Run continuous monitoring loop."""
        if schedule is None:
            self.logger.warning(
                "Schedule library not available, cannot run continuous monitoring",
            )
            return

        self.schedule_maintenance()

        try:
            while True:
                schedule.run_pending()
                time_module.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            pass

    def generate_ci_workflow(self) -> r[str]:
        """Generate GitHub Actions workflow for documentation quality using templates.

        Returns:
            r containing the generated workflow YAML

        """
        return self._templates.generate_ci_workflow(self._config.get_schedule_config())

    def create_maintenance_hook(self) -> r[str]:
        """Create Git pre-commit hook for documentation quality using templates.

        Returns:
            r containing the generated hook script

        """
        return self._templates.generate_git_hook()

    def setup_git_hooks(self) -> None:
        """Set up Git hooks for documentation quality."""
        hooks_dir = Path(".git/hooks")
        if not hooks_dir.exists():
            return

        pre_commit_hook = hooks_dir / "pre-commit"

        # Backup existing hook if it exists
        if pre_commit_hook.exists():
            backup_hook = hooks_dir / "pre-commit.backup"
            if not backup_hook.exists():
                pre_commit_hook.rename(backup_hook)

        # Create new hook using FLEXT templates
        hook_result = self.create_maintenance_hook()
        if not hook_result.is_success:
            error_msg = f"Failed to generate hook content: {hook_result.error}"
            self.logger.error("Hook generation failed", error=error_msg)
            return

        hook_content = hook_result.value
        pre_commit_hook.write_text(hook_content)
        pre_commit_hook.chmod(0o755)

        self.logger.info("Git hook installed successfully", path=str(pre_commit_hook))

    def create_makefile_targets(self) -> r[str]:
        """Create Makefile targets for documentation maintenance using templates.

        Returns:
            r containing the generated Makefile content

        """
        return self._templates.generate_makefile_targets()


def _handle_ci_check(automation: DocumentationAutomation) -> int:
    """Handle CI check command."""
    result = automation.run_ci_checks()
    if result.is_success:
        success = result.value
        return 0 if success else 1
    return 1


def _handle_generate_workflow(automation: DocumentationAutomation) -> int:
    """Handle generate workflow command."""
    result = automation.generate_ci_workflow()
    return 0 if result.is_success else 1


def _handle_generate_makefile(automation: DocumentationAutomation) -> int:
    """Handle generate makefile command."""
    result = automation.create_makefile_targets()
    return 0 if result.is_success else 1


def main() -> None:
    """Main entry point for documentation automation."""
    parser = argparse.ArgumentParser(
        description="FLEXT-Meltano Documentation Automation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/docs_automation.py --ci-check
  python scripts/docs_automation.py --schedule
  python scripts/docs_automation.py --setup-hooks
  python scripts/docs_automation.py --generate-workflow
        """,
    )

    parser.add_argument("--ci-check", action="store_true", help="Run CI quality checks")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Start scheduled maintenance monitoring",
    )
    parser.add_argument(
        "--setup-hooks",
        action="store_true",
        help="Set up Git hooks for quality checks",
    )
    parser.add_argument(
        "--generate-workflow",
        action="store_true",
        help="Generate GitHub Actions workflow",
    )
    parser.add_argument(
        "--generate-makefile",
        action="store_true",
        help="Generate Makefile targets",
    )

    args = parser.parse_args()

    try:
        automation = DocumentationAutomation()

        command_handlers: dict[str, Callable[[DocumentationAutomation], int | None]] = {
            "ci_check": _handle_ci_check,
            "schedule": lambda a: (a.run_continuous_monitoring(), None)[1],
            "setup_hooks": lambda a: (a.setup_git_hooks(), None)[1],
            "generate_workflow": _handle_generate_workflow,
            "generate_makefile": _handle_generate_makefile,
        }

        for arg_name, handler in command_handlers.items():
            if getattr(args, arg_name, False):
                exit_code = handler(automation)
                if exit_code is not None:
                    sys.exit(exit_code)
                return

        parser.print_help()

    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
