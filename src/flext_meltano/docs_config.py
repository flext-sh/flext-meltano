"""FLEXT-Meltano Documentation Configuration Service.

Centralized configuration management for documentation automation using FlextConfig.
All hardcoded values and thresholds are centralized here for maintainability and consistency.

ARCHITECTURAL INTEGRATION:
- FlextConfig: Base configuration class with validation and environment variable support
- FlextContainer: Singleton pattern for global configuration access
- Railway Pattern: r[T] for configuration loading and validation
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, cast

import yaml
from flext_core import FlextConfig, FlextContainer, FlextResult, u

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
r = FlextResult
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels


class DocsConfig(FlextConfig):
    """Centralized configuration for documentation automation.

    Extends FlextConfig with documentation-specific settings.
    All hardcoded values from throughout the codebase are centralized here.

    Attributes:
        # File Paths
        config_path: Default configuration file path
        reports_output_dir: Directory for quality reports

        # Scheduling
        enable_scheduled_audits: Whether to enable automated audits
        audit_schedule: Schedule type ('daily', 'weekly', 'monthly')
        audit_day: Day of week for weekly audits (monday, tuesday, etc.)
        audit_time: Time for scheduled audits (HH:MM format)

        # Quality Thresholds
        min_quality_score: Minimum acceptable quality score (0-100)
        max_file_age_days: Maximum age in days before content is considered stale
        min_words_per_file: Minimum word count required per file
        max_broken_links_ratio: Maximum ratio of broken links (0.0-1.0)
        max_line_length: Maximum characters per line
        fail_on_critical_issues: Whether to fail CI on critical issues

        # Link Validation
        link_validation_timeout: Timeout in seconds for link validation
        link_validation_retries: Number of retries for failed link validation

        # Content Requirements
        required_sections: List of required heading patterns

    """

    # File Paths
    config_path: str = "docs/.maintenance_config.yaml"
    reports_output_dir: str = "docs/reports"

    # Scheduling Configuration
    enable_scheduled_audits: bool = True
    audit_schedule: str = "weekly"
    audit_day: str = "monday"
    audit_time: str = "09:00"

    # Quality Thresholds
    min_quality_score: int = 80
    max_file_age_days: int = 90
    min_words_per_file: int = 50
    max_broken_links_ratio: float = 0.05
    max_line_length: int = 120
    fail_on_critical_issues: bool = True

    # Link Validation Settings
    link_validation_timeout: int = 10
    link_validation_retries: int = 2

    # Content Requirements
    required_sections: ClassVar[list[str]] = ["##", "###"]

    @classmethod
    def get_instance(cls) -> DocsConfig:
        """Get singleton instance through FlextContainer."""
        container = FlextContainer.get_global()
        config_result = container.get("DocsConfig")

        if config_result.is_success:
            return cast("DocsConfig", config_result.unwrap())

        # Create and register new instance
        instance = cls()
        container.register_service("DocsConfig", instance)
        return instance

    def load_from_file(self, config_path: str | Path | None = None) -> r[DocsConfig]:
        """Load configuration from YAML file using FlextConfig patterns.

        Args:
            config_path: Path to configuration file (uses self.config_path if None)

        Returns:
            r containing loaded configuration or error

        """
        file_path = Path(config_path or self.config_path)

        if not file_path.exists():
            # Return default configuration
            return r.ok(self)

        try:
            with file_path.open(encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            config_guard = u.guard(config_data, dict, return_value=True)
            if config_guard is None:
                error_msg = f"Invalid configuration format: expected dict, got {type(config_data)}"
                return r[DocsConfig].fail(error_msg)
            config_data = config_guard

            # Update instance with loaded values
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)

            return r.ok(self)

        except Exception as e:
            error_msg = f"Failed to load configuration from {file_path}: {e}"
            return r[DocsConfig].fail(error_msg)

    def get_schedule_config(self) -> dict[str, object]:
        """Get scheduling configuration as dictionary for backward compatibility.

        Returns:
            Dictionary with automation scheduling settings

        """
        return {
            "enable_scheduled_audits": self.enable_scheduled_audits,
            "audit_schedule": self.audit_schedule,
            "audit_day": self.audit_day,
            "audit_time": self.audit_time,
        }

    def get_quality_thresholds(self) -> dict[str, object]:
        """Get quality thresholds as dictionary for backward compatibility.

        Returns:
            Dictionary with quality threshold settings

        """
        return {
            "min_quality_score": self.min_quality_score,
            "max_file_age_days": self.max_file_age_days,
            "min_words_per_file": self.min_words_per_file,
            "max_broken_links_ratio": self.max_broken_links_ratio,
            "max_line_length": self.max_line_length,
            "fail_on_critical_issues": self.fail_on_critical_issues,
        }

    def get_reporting_config(self) -> dict[str, object]:
        """Get reporting configuration as dictionary for backward compatibility.

        Returns:
            Dictionary with reporting settings

        """
        return {
            "output_directory": self.reports_output_dir,
        }

    def get_link_validation_config(self) -> dict[str, object]:
        """Get link validation configuration as dictionary for backward compatibility.

        Returns:
            Dictionary with link validation settings

        """
        return {
            "timeout": self.link_validation_timeout,
            "retries": self.link_validation_retries,
        }

    def get_audit_thresholds(self) -> dict[str, object]:
        """Get audit thresholds as dictionary for backward compatibility.

        Returns:
            Dictionary with audit threshold settings

        """
        return {
            "max_file_age_days": self.max_file_age_days,
            "min_words_per_file": self.min_words_per_file,
            "max_broken_links_ratio": self.max_broken_links_ratio,
            "required_sections": self.required_sections,
            "max_line_length": self.max_line_length,
        }
