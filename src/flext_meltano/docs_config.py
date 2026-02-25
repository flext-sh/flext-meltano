"""FLEXT-Meltano Documentation Configuration Service.

Centralized configuration management for documentation automation using FlextSettings.
All hardcoded values and thresholds are centralized here for maintainability and consistency.

ARCHITECTURAL INTEGRATION:
- FlextSettings: Base configuration class with validation and environment variable support
- FlextContainer: Singleton pattern for global configuration access
- Railway Pattern: r[T] for configuration loading and validation
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar

import yaml
from flext_core import FlextContainer, FlextSettings, r, u

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes as t

# Import aliases for simplified usage
m = FlextMeltanoModels


class DocsConfig(FlextSettings):
    """Centralized configuration for documentation automation.

    Extends FlextSettings with documentation-specific settings.
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

        if config_result.is_success and config_result.value is not None:
            # Type narrowing: verify instance type before returning
            value = config_result.value
            if u.Guards.is_type(value, cls):
                return value

        # Create and return new instance
        return cls()

    def load_from_file(self, config_path: str | Path | None = None) -> r[DocsConfig]:
        """Load configuration from YAML file using FlextSettings patterns.

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

            # Update instance with loaded values via model normalization
            config_values = m.Meltano.ConfigMappingPayload.model_validate(
                {"values": config_guard},
            ).values
            for key, value in config_values.items():
                if key in self.__class__.model_fields:
                    setattr(self, key, value)

            return r.ok(self)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            error_msg = f"Failed to load configuration from {file_path}: {e}"
            return r[DocsConfig].fail(error_msg)

    def get_schedule_config(self) -> Mapping[str, t.GeneralValueType]:
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

    def get_quality_thresholds(self) -> Mapping[str, t.GeneralValueType]:
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

    def get_reporting_config(self) -> Mapping[str, t.GeneralValueType]:
        """Get reporting configuration as dictionary for backward compatibility.

        Returns:
            Dictionary with reporting settings

        """
        return {
            "output_directory": self.reports_output_dir,
        }

    def get_link_validation_config(self) -> Mapping[str, t.GeneralValueType]:
        """Get link validation configuration as dictionary for backward compatibility.

        Returns:
            Dictionary with link validation settings

        """
        return {
            "timeout": self.link_validation_timeout,
            "retries": self.link_validation_retries,
        }

    def get_audit_thresholds(self) -> Mapping[str, t.GeneralValueType]:
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
