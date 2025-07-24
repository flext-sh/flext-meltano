"""FLEXT Meltano configuration loader module."""

from __future__ import annotations

from typing import Any

from flext_core import FlextConstants, FlextResult

from flext_meltano.config.settings import FlextMeltanoSettings


class FlextMeltanoConfigLoader:
    """Configuration loader for FLEXT Meltano settings.

    Loads and validates Meltano configuration from various sources
    following Clean Architecture patterns.
    """

    def __init__(self) -> None:
        """Initialize configuration loader."""
        self.settings = FlextMeltanoSettings()

    def load_config(
        self,
        config_path: str | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Load configuration from specified path or environment.

        Args:
            config_path: Optional path to configuration file

        Returns:
            FlextResult containing loaded configuration

        """
        try:
            config = {
                "project_root": self.settings.project.project_root,
                "environment": self.settings.environment,
                "log_level": self.settings.meltano_monitoring.log_level,
                "timeout": FlextConstants.DEFAULT_TIMEOUT,
            }

            if config_path:
                # TODO: Load from file when implemented
                config["config_path"] = config_path

            return FlextResult.ok(config)

        except Exception as e:
            return FlextResult.fail(f"Failed to load configuration: {e}")

    def validate_config(
        self,
        config: dict[str, Any],
    ) -> FlextResult[bool]:
        """Validate configuration structure and values.

        Args:
            config: Configuration dictionary to validate

        Returns:
            FlextResult indicating validation success

        """
        required_keys = ["project_root", "environment", "log_level"]

        for key in required_keys:
            if key not in config:
                return FlextResult.fail(f"Missing required config key: {key}")

        return FlextResult.ok(True)
