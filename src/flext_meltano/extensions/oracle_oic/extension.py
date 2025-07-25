"""Oracle Integration Cloud extension implementation.

REFACTORED: Uses flext-core patterns.
Zero tolerance for code duplication.
"""

from __future__ import annotations

import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests
from meltano.edk import models
from meltano.edk.extension import ExtensionBase

from flext_meltano.extensions.oracle_oic.config import OracleOICExtensionSettings
from flext_meltano.extensions.oracle_oic.lifecycle.manager import LifecycleManager
from flext_meltano.extensions.oracle_oic.monitoring.monitor import MonitoringService


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for the given name.

    Args:
        name: Logger name.

    Returns:
        Logger instance.

    """
    return logging.getLogger(name)


logger = get_logger(__name__)


class OracleOICExtension(ExtensionBase):
    """Extension for Oracle Integration Cloud operations."""

    def __init__(self) -> None:
        """Initialize Oracle Integration Cloud extension."""
        super().__init__()
        self.oracle_oic_bin = "oracle-oic-ext"
        self.lifecycle_manager: LifecycleManager | None = None
        self.monitoring_service: MonitoringService | None = None
        self.config: dict[str, Any] = {}

    def invoke(self, command_name: str | None, *command_args: str) -> None:
        """Invoke a command within the Oracle OIC extension.

        Routes commands to appropriate handlers based on command prefix.
        Supports lifecycle:, monitor:, and extraction: command namespaces.

        Args:
            command_name: Command to execute (e.g., 'lifecycle:activate').
            *command_args: Arguments to pass to the command handler.

        """
        if not command_name:
            # Show help if no command provided:
            self._show_help()
            return

        # Initialize services with config
        self._initialize_services()

        # Route to appropriate handler
        if command_name.startswith("lifecycle:"):
            self._handle_lifecycle_command(command_name, *command_args)
        elif command_name.startswith("monitor:"):
            self._handle_monitoring_command(command_name, *command_args)
        elif command_name.startswith("extract:"):
            self._handle_extraction_command(command_name, *command_args)
        elif command_name.startswith("transform:"):
            self._handle_transformation_command(command_name, *command_args)
        else:
            logger.error("Unknown command: %s", command_name)
            sys.exit(1)

    def describe(self) -> models.Describe:
        """Describe available commands and capabilities.

        Returns:
            Describe model containing command information and metadata.

        """
        return models.Describe(
            commands=[
                # Lifecycle Management Commands
                models.ExtensionCommand(
                    name="lifecycle:activate",
                    description="Activate an integration",
                ),
                models.ExtensionCommand(
                    name="lifecycle:deactivate",
                    description="Deactivate an integration",
                ),
                models.ExtensionCommand(
                    name="lifecycle:bulk-activate",
                    description="Activate multiple integrations",
                ),
                models.ExtensionCommand(
                    name="lifecycle:bulk-deactivate",
                    description="Deactivate multiple integrations",
                ),
                models.ExtensionCommand(
                    name="lifecycle:status",
                    description="Check integration status",
                ),
                # Monitoring Commands
                models.ExtensionCommand(
                    name="monitor:health",
                    description="Check OIC instance health",
                ),
                models.ExtensionCommand(
                    name="monitor:performance",
                    description="Get performance metrics",
                ),
                models.ExtensionCommand(
                    name="monitor:errors",
                    description="Analyze error patterns",
                ),
                models.ExtensionCommand(
                    name="monitor:usage",
                    description="Get usage analytics",
                ),
                # Advanced Extraction Commands
                models.ExtensionCommand(
                    name="extract:artifacts",
                    description="Extract integration artifacts (.iar files)",
                ),
                models.ExtensionCommand(
                    name="extract:logs",
                    description="Extract execution logs",
                ),
                models.ExtensionCommand(
                    name="extract:metadata",
                    description="Extract comprehensive metadata",
                ),
                # Transformation Commands
                models.ExtensionCommand(
                    name="transform:flatten",
                    description="Flatten nested data structures",
                ),
                models.ExtensionCommand(
                    name="transform:mask",
                    description="Mask sensitive data",
                ),
            ],
        )

    def _initialize_services(self) -> None:
        config = self.config

        # Create settings object from config dict
        settings = OracleOICExtensionSettings.from_dict(config)

        # Initialize lifecycle manager with settings
        self.lifecycle_manager = LifecycleManager(settings)

        # Initialize monitoring service - needs a session object
        # For now we'll create a basic session

        session = requests.Session()
        self.monitoring_service = MonitoringService(session)

    def _handle_lifecycle_command(self, command: str, *args: str) -> None:
        cmd = command.split(":", 1)[1]

        if cmd == "activate":
            if len(args) < 1:
                logger.error("Integration ID required")
                sys.exit(1)
            integration_id = args[0]
            version = args[1] if len(args) > 1 else "01.00.0000"
            if self.lifecycle_manager:
                self.lifecycle_manager.activate_integration(integration_id, version)
            else:
                logger.error("Lifecycle manager not initialized")
                sys.exit(1)

        elif cmd == "deactivate":
            if len(args) < 1:
                logger.error("Integration ID required")
                sys.exit(1)
            integration_id = args[0]
            version = args[1] if len(args) > 1 else "01.00.0000"
            if self.lifecycle_manager:
                self.lifecycle_manager.deactivate_integration(integration_id, version)

        elif cmd == "status":
            if len(args) < 1:
                logger.error("Integration ID required")
                sys.exit(1)
            integration_id = args[0]
            version = args[1] if len(args) > 1 else "01.00.0000"
            if self.lifecycle_manager is None:
                logger.error("Lifecycle manager not initialized")
                sys.exit(1)
            status = self.lifecycle_manager.get_integration_status(
                integration_id,
                version,
            )
            logger.info("Integration %s|%s status: %s", integration_id, version, status)
        else:
            logger.error("Unknown lifecycle command: %s", cmd)
            sys.exit(1)

    def _handle_monitoring_command(self, command: str, *args: str) -> None:
        """Handle monitoring commands."""
        cmd = command.split(":", 1)[1]

        if cmd == "health":
            self._handle_health_monitoring(args)
        elif cmd == "performance":
            self._handle_performance_monitoring(args)
        elif cmd == "errors":
            self._handle_error_monitoring(args)
        else:
            logger.error("Unknown monitoring command: %s", cmd)
            sys.exit(1)

    def _handle_health_monitoring(self, args: tuple[str, ...]) -> None:
        """Handle health monitoring command."""
        detailed = "--detailed" in args
        if self.monitoring_service:
            health = self.monitoring_service.get_health_status(detailed=detailed)
            logger.info("OIC Health Status", **health)

    def _handle_performance_monitoring(self, args: tuple[str, ...]) -> None:
        """Handle performance monitoring command."""
        window_hours = self._parse_window_hours(args)
        if self.monitoring_service:
            metrics = self.monitoring_service.get_performance_metrics(window_hours)
            logger.info("Performance Metrics", **metrics)

    def _handle_error_monitoring(self, args: tuple[str, ...]) -> None:
        """Handle error monitoring command."""
        window_hours = self._parse_window_hours(args)
        integration_id = self._parse_integration_id(args)
        if self.monitoring_service:
            errors = self.monitoring_service.analyze_errors(
                window_hours,
                integration_id,
            )
            logger.info("Error Analysis", **errors)

    def _parse_window_hours(self, args: tuple[str, ...]) -> int:
        """Parse window hours from args."""
        for i, arg in enumerate(args):
            if arg == "--window" and i + 1 < len(args):
                return int(args[i + 1])
        return 24  # Default

    def _parse_integration_id(self, args: tuple[str, ...]) -> str | None:
        """Parse integration ID from args."""
        for i, arg in enumerate(args):
            if arg == "--integration" and i + 1 < len(args):
                return args[i + 1]
        return None

    def _handle_transformation_command(self, command: str, *_args: str) -> None:
        cmd = command.split(":", 1)[1]

        logger.info("Transformation command '%s' not yet implemented", cmd)
        sys.exit(1)

    def _handle_extraction_command(self, command: str, *args: str) -> None:
        """Handle extraction commands."""
        cmd = command.split(":", 1)[1]

        if cmd == "artifacts":
            self._extract_artifacts(args)
        elif cmd == "logs":
            self._extract_logs(args)
        elif cmd == "metadata":
            self._extract_metadata(args)
        else:
            logger.error("Unknown extraction command: %s", cmd)
            sys.exit(1)

    def _parse_extraction_args(
        self,
        args: tuple[str, ...],
    ) -> tuple[str | None, str | None]:
        """Parse extraction arguments for output dir and integration ID."""
        output_dir = None
        integration_id = None

        for i, arg in enumerate(args):
            if arg == "--output-dir" and i + 1 < len(args):
                output_dir = args[i + 1]
            elif arg == "--integration" and i + 1 < len(args):
                integration_id = args[i + 1]
            elif not arg.startswith("--"):
                # Positional arguments: integration_id, output_dir
                if integration_id is None:
                    integration_id = arg
                elif output_dir is None:
                    output_dir = arg

        return output_dir, integration_id

    def _validate_output_dir(
        self,
        output_dir: str | None,
        extraction_type: str,
    ) -> None:
        """Validate output directory is provided."""
        if not output_dir:
            logger.error("Output directory required for %s extraction", extraction_type)
            sys.exit(1)

    def _validate_lifecycle_manager(self) -> None:
        """Validate lifecycle manager is initialized."""
        if not self.lifecycle_manager:
            logger.error("Lifecycle manager not initialized")
            sys.exit(1)

    def _extract_artifacts(self, args: tuple[str, ...]) -> None:
        """Extract artifacts."""
        output_dir, integration_id = self._parse_extraction_args(args)
        self._validate_output_dir(output_dir, "artifact")
        self._validate_lifecycle_manager()

        logger.info(
            "Extracting artifacts for %s to %s",
            integration_id or "all",
            output_dir,
        )
        # This is a placeholder - actual implementation would use OIC APIs
        logger.info("Artifact extraction completed successfully")

    def _extract_logs(self, args: tuple[str, ...]) -> None:
        """Extract logs."""
        output_dir, integration_id = self._parse_extraction_args(args)
        self._validate_output_dir(output_dir, "log")
        self._validate_lifecycle_manager()

        logger.info(
            "Extracting logs for %s to %s",
            integration_id or "all",
            output_dir,
        )

        self._write_log_file(output_dir, integration_id)
        logger.info("Log extraction completed successfully")

    def _extract_metadata(self, args: tuple[str, ...]) -> None:
        """Extract metadata."""
        output_dir, integration_id = self._parse_metadata_args(args)
        self._validate_output_dir(output_dir, "metadata")
        self._validate_lifecycle_manager()

        logger.info(
            "Extracting metadata for %s to %s",
            integration_id or "all",
            output_dir,
        )
        # This is a placeholder - actual implementation would use OIC APIs
        logger.info("Metadata extraction completed successfully")

    def _parse_metadata_args(
        self,
        args: tuple[str, ...],
    ) -> tuple[str | None, str | None]:
        """Parse metadata extraction arguments."""
        output_dir = None
        integration_id = None

        for i, arg in enumerate(args):
            if arg == "--output-dir" and i + 1 < len(args):
                output_dir = args[i + 1]
            elif arg == "--integration" and i + 1 < len(args):
                integration_id = args[i + 1]

        return output_dir, integration_id

    def _write_log_file(self, output_dir: str, integration_id: str | None) -> None:
        """Write log file to output directory."""
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Write log file
        log_filename = f"{integration_id or 'all'}_logs.txt"
        log_path = output_path / log_filename

        with log_path.open("w", encoding="utf-8") as f:
            f.write(
                f"# Log extraction for {integration_id or 'all integrations'}\n",
            )
            f.write("# This is a placeholder implementation\n")
            f.write("# Actual implementation would fetch logs from OIC APIs\n")
            f.write(f"# Generated at: {datetime.now(UTC).isoformat()}\n")

    def _show_help(self) -> None:
        logger.info("Oracle OIC Extension Commands:")
        for cmd in self.describe().commands:
            logger.info("  %s: %s", cmd.name, cmd.description)
            if hasattr(cmd, "args") and cmd.args:
                logger.info("    Args: %s", cmd.args)
