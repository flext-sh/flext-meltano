#!/usr/bin/env python3
"""FLEXT-Meltano Documentation Automation Framework.

Automated scheduling, CI/CD integration, and continuous maintenance
for documentation quality assurance using complete FLEXT ecosystem integration.

ARCHITECTURAL INTEGRATION:
- FlextCore.Result[T]: Railway pattern error handling
- FlextCore.Config: Centralized configuration management
- FlextCore.Logger: Structured logging with correlation
- FlextCore.Service: Service base class with dependency injection
- FlextCli: CLI utilities for subprocess operations
- FlextQuality: Quality assurance integration
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time as time_module
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import schedule
from flext_cli import (
    FlextCliCmd,
)
from flext_core import FlextCore

from .docs_config import DocsConfig
from .docs_templates import DocsTemplates


class DocumentationAutomation(FlextCore.Service):
    """Automated documentation maintenance and CI/CD integration using FLEXT ecosystem.

    Extends FlextCore.Service with dependency injection and railway pattern error handling.
    Integrates with FlextCli for subprocess operations and FlextCore.Logger for structured logging.
    """

    def __init__(
        self,
        logger: FlextCore.Logger | None = None,
        cli_cmd: FlextCliCmd | None = None,
    ) -> None:
        """Initialize DocumentationAutomation with FLEXT ecosystem integration.

        Args:
            logger: FlextCore.Logger instance (injected via container)
            cli_cmd: FlextCliCmd instance (injected via container)

        """
        super().__init__(logger=logger)

        # Dependency injection setup
        self._container = FlextCore.Container.get_global()
        self._cli_cmd = cli_cmd or self._container.get("FlextCliCmd").unwrap_or(
            FlextCliCmd()
        )

        # Template system for content generation
        self._templates = DocsTemplates(logger=None)

        # Access configuration via singleton
        self._config = DocsConfig.get_instance()
        self.maintenance_script = Path("scripts/docs_maintenance.py")

        # Validate maintenance script exists using FlextCore.Result pattern
        if not self.maintenance_script.exists():
            error_msg = f"Maintenance script not found: {self.maintenance_script}"
            self.logger.error("Maintenance script validation failed", error=error_msg)
            raise FlextExceptions.ConfigurationError(error_msg)

    def run_ci_checks(self) -> FlextCore.Result[bool]:
        """Run documentation quality checks for CI/CD pipeline using FLEXT patterns.

        Returns:
            FlextCore.Result containing success status with detailed error information

        """
        self.logger.info("Starting CI documentation quality checks")

        # Run comprehensive audit using FlextCli
        audit_result = self._run_maintenance_audit("--comprehensive")
        if not audit_result.is_success:
            self.logger.error("Documentation audit failed", error=audit_result.error)
            return FlextCore.Result.fail(audit_result.error)

        # Check quality thresholds
        quality_check_result = self._validate_quality_thresholds()
        if not quality_check_result.is_success:
            self.logger.error(
                "Quality threshold validation failed", error=quality_check_result.error
            )
            return FlextCore.Result.fail(quality_check_result.error)

        success_status = quality_check_result.unwrap()
        if success_status:
            self.logger.info("CI documentation quality checks passed")
        else:
            self.logger.warning("CI documentation quality checks failed")

        return FlextCore.Result.ok(success_status)

    def _run_maintenance_audit(self, *args: str) -> FlextCore.Result[None]:
        """Run maintenance audit using FlextCli.

        Args:
            *args: Command line arguments for the maintenance script

        Returns:
            FlextCore.Result indicating success or failure

        """
        try:
            cmd_args = [sys.executable, str(self.maintenance_script)] + list(args)

            # Use subprocess for execution
            result = subprocess.run(
                cmd_args, cwd=Path.cwd(), capture_output=True, text=True, check=False
            )

            if result.returncode != 0:
                error_msg = (
                    f"Maintenance audit failed with exit code {result.returncode}"
                )
                if result.stderr:
                    error_msg += f": {result.stderr.strip()}"
                return FlextCore.Result.fail(FlextExceptions.OperationError(error_msg))

            return FlextCore.Result.ok(None)

        except Exception as e:
            error_msg = f"Failed to execute maintenance audit: {e}"
            self.logger.exception("Maintenance audit execution failed", error=error_msg)
            return FlextCore.Result.fail(FlextExceptions.OperationError(error_msg))

    def _validate_quality_thresholds(self) -> FlextCore.Result[bool]:
        """Validate quality thresholds against generated summary.

        Returns:
            FlextCore.Result containing validation result

        """
        try:
            summary_path = (
                Path(self._config.reports_output_dir) / "docs_quality_summary.json"
            )

            if not summary_path.exists():
                error_msg = f"Quality summary not found at {summary_path}"
                self.logger.warning("Quality summary missing", path=str(summary_path))
                return FlextCore.Result.ok(False)  # Not a failure, just no data

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
                return FlextCore.Result.fail(FlextExceptions.ValidationError(error_msg))

            # Check quality score threshold
            min_score = self._config.min_quality_score

            if quality_score < min_score:
                error_msg = f"Quality score {quality_score} below threshold {min_score}"
                self.logger.error(
                    "Quality score below threshold",
                    score=quality_score,
                    threshold=min_score,
                )
                return FlextCore.Result.fail(FlextExceptions.ValidationError(error_msg))

            self.logger.info(
                "Quality thresholds validated successfully",
                score=quality_score,
                critical_issues=critical_count,
            )
            return FlextCore.Result.ok(True)

        except Exception as e:
            error_msg = f"Quality threshold validation failed: {e}"
            self.logger.exception("Quality validation failed", error=error_msg)
            return FlextCore.Result.fail(FlextExceptions.ValidationError(error_msg))

    def schedule_maintenance(self) -> None:
        """Set up scheduled maintenance tasks."""
        automation_config = self._config.get_schedule_config()

        if not automation_config.get("enable_scheduled_audits", False):
            print("📅 Scheduled audits disabled in configuration")
            return

        schedule_type = automation_config.get("audit_schedule", "weekly")

        if schedule_type == "daily":
            self._schedule_daily(automation_config)
        elif schedule_type == "weekly":
            self._schedule_weekly(automation_config)
        elif schedule_type == "monthly":
            self._schedule_monthly(automation_config)

        print("📅 Maintenance scheduling configured")

    def _schedule_daily(self, config: dict[str, Any]) -> None:
        """Schedule daily maintenance."""
        audit_time = config.get("audit_time", "09:00")
        hour, minute = map(int, audit_time.split(":"))

        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
            self._run_scheduled_audit
        )

    def _schedule_weekly(self, config: dict[str, Any]) -> None:
        """Schedule weekly maintenance."""
        audit_day = config.get("audit_day", "monday").lower()
        audit_time = config.get("audit_time", "09:00")
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
                self._run_scheduled_audit
            )

    def _schedule_monthly(self, config: dict[str, Any]) -> None:
        """Schedule monthly maintenance."""
        # Run on the 1st of each month
        audit_time = config.get("audit_time", "09:00")
        _hour, _minute = map(int, audit_time.split(":"))

        # Monthly scheduling not supported by schedule library
        # schedule.every().month.at(f"{hour:02d}:{minute:02d}").do(
        #     self._run_scheduled_audit
        # )

    def _run_scheduled_audit(self) -> None:
        """Run scheduled documentation audit."""
        print(f"📅 Running scheduled documentation audit at {datetime.now(UTC)}")

        try:
            result = subprocess.run(
                [sys.executable, str(self.maintenance_script), "--comprehensive"],
                check=False,
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )

            if result.returncode == 0:
                print("✅ Scheduled audit completed successfully")
            else:
                print(f"⚠️  Scheduled audit completed with warnings: {result.stderr}")

        except Exception as e:
            print(f"❌ Scheduled audit failed: {e}")

    def run_continuous_monitoring(self) -> None:
        """Run continuous monitoring loop."""
        print("🔄 Starting continuous documentation monitoring...")

        self.schedule_maintenance()

        try:
            while True:
                schedule.run_pending()
                time_module.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("⏹️  Continuous monitoring stopped")

    def generate_ci_workflow(self) -> FlextCore.Result[str]:
        """Generate GitHub Actions workflow for documentation quality using templates.

        Returns:
            FlextCore.Result containing the generated workflow YAML

        """
        return self._templates.generate_ci_workflow(self._config.get_schedule_config())

    def create_maintenance_hook(self) -> FlextCore.Result[str]:
        """Create Git pre-commit hook for documentation quality using templates.

        Returns:
            FlextCore.Result containing the generated hook script

        """
        return self._templates.generate_git_hook()

    def setup_git_hooks(self) -> None:
        """Set up Git hooks for documentation quality."""
        hooks_dir = Path(".git/hooks")
        if not hooks_dir.exists():
            print("⚠️  Git hooks directory not found. Initialize git repository first.")
            return

        pre_commit_hook = hooks_dir / "pre-commit"

        # Backup existing hook if it exists
        if pre_commit_hook.exists():
            backup_hook = hooks_dir / "pre-commit.backup"
            if not backup_hook.exists():
                pre_commit_hook.rename(backup_hook)
                print(f"📋 Backed up existing pre-commit hook to {backup_hook}")

        # Create new hook using FLEXT templates
        hook_result = self.create_maintenance_hook()
        if not hook_result.is_success:
            error_msg = f"Failed to generate hook content: {hook_result.error}"
            self.logger.error("Hook generation failed", error=error_msg)
            print(f"❌ {error_msg}")
            return

        hook_content = hook_result.unwrap()
        pre_commit_hook.write_text(hook_content)
        pre_commit_hook.chmod(0o755)

        self.logger.info("Git hook installed successfully", path=str(pre_commit_hook))
        print(f"✅ Documentation quality pre-commit hook installed: {pre_commit_hook}")

    def create_makefile_targets(self) -> FlextCore.Result[str]:
        """Create Makefile targets for documentation maintenance using templates.

        Returns:
            FlextCore.Result containing the generated Makefile content

        """
        return self._templates.generate_makefile_targets()


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
        "--schedule", action="store_true", help="Start scheduled maintenance monitoring"
    )
    parser.add_argument(
        "--setup-hooks", action="store_true", help="Set up Git hooks for quality checks"
    )
    parser.add_argument(
        "--generate-workflow",
        action="store_true",
        help="Generate GitHub Actions workflow",
    )
    parser.add_argument(
        "--generate-makefile", action="store_true", help="Generate Makefile targets"
    )

    args = parser.parse_args()

    try:
        automation = DocumentationAutomation()

        if args.ci_check:
            result = automation.run_ci_checks()
            if result.is_success:
                success = result.unwrap()
                sys.exit(0 if success else 1)
            else:
                print(f"❌ CI check failed: {result.error}")
                sys.exit(1)

        elif args.schedule:
            automation.run_continuous_monitoring()

        elif args.setup_hooks:
            automation.setup_git_hooks()

        elif args.generate_workflow:
            result = automation.generate_ci_workflow()
            if result.is_success:
                print(result.unwrap())
            else:
                print(f"❌ Workflow generation failed: {result.error}")
                sys.exit(1)

        elif args.generate_makefile:
            result = automation.create_makefile_targets()
            if result.is_success:
                print(result.unwrap())
            else:
                print(f"❌ Makefile generation failed: {result.error}")
                sys.exit(1)

        else:
            parser.print_help()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
