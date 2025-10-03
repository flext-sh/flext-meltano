"""FLEXT Meltano Configuration - Unified configuration management and builders.

This module consolidates all Meltano configuration functionality including:
- Configuration management with Pydantic validation
- Configuration building utilities
- Environment-specific configurations

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import SettingsConfigDict

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

# Type alias for configuration dictionaries
ConfigDict = FlextTypes.Dict


class FlextMeltanoConfigBuilders:
    """UNIFIED configuration builders class - SINGLE RESPONSIBILITY.

    Handles ALL Meltano configuration building operations in one cohesive class
    following SOLID principles and eliminating nested class violations.

    SOLID Principles Compliance:
    - Single Responsibility: ONE class with unified configuration building purpose
    - Open/Closed: Extensible through method addition, closed for structural modification
    - Liskov Substitution: All configuration methods return consistent FlextResult types
    - Interface Segregation: Clear method separation by configuration type
    - Dependency Inversion: Depends on flext-core abstractions, not implementations
    """

    # =================================================================
    # UNIFIED CONFIGURATION BUILDING METHODS - NO NESTED CLASSES
    # =================================================================

    def __init__(self) -> None:
        """Initialize unified configuration builders."""
        self._logger = FlextLogger(__name__)

    # DBT Configuration Methods

    def create_dbt_config(
        self,
        project_name: str,
        profile_name: str = "",
    ) -> FlextResult[ConfigDict]:
        """Create DBT project configuration.

        Args:
            project_name: Name of the DBT project
            profile_name: Optional profile name override

        Returns:
            FlextResult with DBT configuration dictionary

        """
        try:
            profile = profile_name or f"{project_name}_profile"
            config: ConfigDict = {
                "name": project_name,
                "version": "1.0.0",
                "config-version": 2,
                "profile": profile,
                "model-paths": ["models"],
                "analysis-paths": ["analyses"],
                "test-paths": ["tests"],
                "seed-paths": ["seeds"],
                "macro-paths": ["macros"],
                "snapshot-paths": ["snapshots"],
                "target-path": "target",
                "clean-targets": ["target", "dbt_packages"],
                "vars": {},
            }
            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Failed to create DBT config: {e}")

    def create_dbt_profile_config(
        self,
        profile_name: str,
        target_name: str,
        connection_config: ConfigDict,
    ) -> FlextResult[ConfigDict]:
        """Create DBT profile configuration.

        Args:
            profile_name: Name of the DBT profile
            target_name: Name of the default target
            connection_config: Database connection configuration

        Returns:
            FlextResult with DBT profile configuration

        """
        try:
            profile_config: ConfigDict = {
                profile_name: {
                    "target": target_name,
                    "outputs": {target_name: connection_config},
                }
            }
            return FlextResult[ConfigDict].ok(profile_config)
        except Exception as e:
            return FlextResult[ConfigDict].fail(
                f"Failed to create DBT profile config: {e}"
            )

    # Meltano Configuration Methods

    def create_meltano_config(
        self,
        project_name: str,
        version: str = "1.0.0",
        environment: str = "dev",
    ) -> FlextResult[ConfigDict]:
        """Create Meltano project configuration.

        Args:
            project_name: Name of the Meltano project
            version: Project version
            environment: Default environment

        Returns:
            FlextResult with Meltano configuration

        """
        try:
            config: ConfigDict = {
                "version": version,
                "project_id": project_name,
                "default_environment": environment,
                "environments": [
                    {
                        "name": environment,
                        "config": {},
                        "state": {},
                    }
                ],
                "plugins": {
                    "extractors": [],
                    "loaders": [],
                    "transforms": [],
                    "orchestrators": [],
                },
            }
            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Failed to create Meltano config: {e}")

    def add_plugin_to_config(
        self,
        config: ConfigDict,
        plugin_type: str,
        plugin_name: str,
        plugin_config: ConfigDict | None = None,
    ) -> FlextResult[ConfigDict]:
        """Add plugin to Meltano configuration.

        Args:
            config: Meltano configuration dictionary
            plugin_type: Type of plugin (extractors, loaders, etc.)
            plugin_name: Name of the plugin
            plugin_config: Optional plugin configuration

        Returns:
            FlextResult with updated configuration

        """
        try:
            if "plugins" not in config:
                config["plugins"] = {}
            if plugin_type not in config["plugins"]:
                config["plugins"][plugin_type] = []
            plugin_entry = {"name": plugin_name}
            if plugin_config:
                plugin_entry["config"] = plugin_config

            config["plugins"][plugin_type].append(plugin_entry)
            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Failed to add plugin to config: {e}")


class FlextMeltanoConfig(FlextConfig):
    """Meltano ELT configuration management with enterprise-grade validation.

    Extends FlextConfig to provide comprehensive Meltano-specific configuration
    with validation using flext-core patterns. This class serves as the single
    source of truth for all Meltano configuration across the application.

    Features:
    - Uses Pydantic 2.11+ features (SettingsConfigDict, SecretStr for sensitive data)
    - Enhanced singleton pattern with get_or_create_shared_instance()
    - Complete type annotations with Python 3.13+ syntax
    - Environment-specific factory methods for different deployment contexts

    """

    # Model configuration using Pydantic 2.11+ SettingsConfigDict
    model_config = SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        case_sensitive=False,
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=False,
    )

    # =========================================================================
    # MELTANO-SPECIFIC CONFIGURATION FIELDS
    # =========================================================================

    # Project Configuration
    project_id: str = Field(
        default="meltano-project",
        description="Unique identifier for the Meltano project",
        min_length=1,
        max_length=255,
    )

    project_name: str = Field(
        default="Meltano ELT Project",
        description="Human-readable name for the project",
        min_length=1,
        max_length=255,
    )

    version: str = Field(
        default="1.0.0",
        description="Project version following semantic versioning",
        pattern=r"^\d+\.\d+\.\d+.*$",
    )

    # Environment Configuration
    default_environment: str = Field(
        default="dev",
        description="Default Meltano environment for operations",
        min_length=1,
        max_length=50,
    )

    meltano_version: str = Field(
        default="3.0.0",
        description="Target Meltano version for compatibility",
        pattern=r"^\d+\.\d+\.\d+.*$",
    )

    # Database Configuration (sensitive data)
    database_url: SecretStr | None = Field(
        default=None,
        description="Database connection URL for Meltano system database",
    )

    # Plugin Configuration
    enable_plugin_discovery: bool = Field(
        default=True,
        description="Enable automatic plugin discovery and installation",
    )

    plugin_cache_dir: Path | None = Field(
        default=None,
        description="Directory for caching plugin installations",
    )

    # Pipeline Configuration
    default_batch_size: int = Field(
        default=FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
        description="Default batch size for data processing",
        gt=0,
        le=FlextConstants.Performance.BatchProcessing.MAX_ITEMS,
    )

    max_concurrent_pipelines: int = Field(
        default=5,
        description="Maximum number of concurrent pipeline executions",
        gt=0,
        le=50,
    )

    # Logging Configuration
    enable_structured_logging: bool = Field(
        default=True,
        description="Enable structured JSON logging for ELT operations",
    )

    log_level: str = Field(
        default="INFO",
        description="Logging level for Meltano operations",
    )

    # Security Configuration
    enable_encryption: bool = Field(
        default=True,
        description="Enable encryption for sensitive configuration data",
    )

    # =========================================================================
    # PYDANTIC VALIDATORS (DOMAIN-SPECIFIC BUSINESS RULES)
    # =========================================================================

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, v: str) -> str:
        """Validate project ID follows Meltano naming conventions."""
        if not v.replace("-", "").replace("_", "").isalnum():
            message = "project_id must contain only alphanumeric characters, hyphens, and underscores"
            raise ValueError(message)
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid Python logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            valid_levels_str = ", ".join(valid_levels)
            message = f"log_level must be one of: {valid_levels_str}"
            raise ValueError(message)
        return v.upper()

    # =========================================================================
    # CLASS VARIABLES AND SINGLETON PATTERN
    # =========================================================================

    _global_instance: ClassVar[FlextMeltanoConfig | None] = None

    # =========================================================================
    # INITIALIZATION AND SINGLETON METHODS
    # =========================================================================

    def __init__(self, **data: object) -> None:
        """Initialize Meltano configuration with enhanced validation."""
        super().__init__(**data)

        # Set default plugin cache directory if not provided
        if self.plugin_cache_dir is None:
            self.plugin_cache_dir = Path.home() / ".meltano" / "cache" / "plugins"

    @classmethod
    def get_global_instance(cls) -> FlextMeltanoConfig:
        """Get or create the global Meltano configuration instance."""
        if cls._global_instance is None:
            cls._global_instance = cls()
        return cls._global_instance

    @classmethod
    def get_or_create_shared_instance(
        cls,
        **kwargs: object,
    ) -> FlextMeltanoConfig:
        """Get existing global instance or create new shared instance with kwargs."""
        if cls._global_instance is None:
            cls._global_instance = cls(**kwargs)
        else:
            # Update existing instance with new values
            for key, value in kwargs.items():
                if hasattr(cls._global_instance, key):
                    setattr(cls._global_instance, key, value)
        return cls._global_instance

    # =========================================================================
    # ENVIRONMENT-SPECIFIC FACTORY METHODS
    # =========================================================================

    @classmethod
    def create_development_config(
        cls,
        project_id: str = "meltano-dev",
        **kwargs: object,
    ) -> FlextMeltanoConfig:
        """Create configuration optimized for development environment."""
        return cls(
            project_id=project_id,
            default_environment="dev",
            enable_structured_logging=False,
            log_level="DEBUG",
            max_concurrent_pipelines=2,
            **kwargs,
        )

    @classmethod
    def create_production_config(
        cls,
        project_id: str,
        database_url: str,
        **kwargs: object,
    ) -> FlextMeltanoConfig:
        """Create configuration optimized for production environment."""
        return cls(
            project_id=project_id,
            default_environment="prod",
            database_url=SecretStr(database_url),
            enable_encryption=True,
            enable_structured_logging=True,
            log_level="WARNING",
            max_concurrent_pipelines=10,
            **kwargs,
        )

    @classmethod
    def create_testing_config(
        cls,
        project_id: str = "meltano-test",
        **kwargs: object,
    ) -> FlextMeltanoConfig:
        """Create configuration optimized for testing environment."""
        return cls(
            project_id=project_id,
            default_environment="test",
            enable_structured_logging=False,
            log_level="DEBUG",
            max_concurrent_pipelines=1,
            enable_encryption=False,
            **kwargs,
        )

    # =========================================================================
    # CONFIGURATION MANAGEMENT METHODS
    # =========================================================================

    def get_plugin_cache_path(self) -> Path:
        """Get the plugin cache directory path."""
        return self.plugin_cache_dir or Path.home() / ".meltano" / "cache" / "plugins"

    def get_database_url(self) -> str | None:
        """Safely get database URL from SecretStr."""
        return self.database_url.get_secret_value() if self.database_url else None

    def to_meltano_dict(self) -> dict[str, str | bool]:
        """Convert configuration to Meltano-compatible dictionary format."""
        return {
            "project_id": self.project_id,
            "version": self.version,
            "default_environment": self.default_environment,
            "meltano_version": self.meltano_version,
            "send_anonymous_usage_stats": False,
            "database_uri": self.get_database_url() or "sqlite:///meltano.db",
        }

    def validate_compatibility(self) -> FlextResult[None]:
        """Validate configuration compatibility with Meltano version."""
        try:
            # Basic compatibility check
            if not self.meltano_version.startswith("3."):
                return FlextResult.fail(
                    f"Meltano version {self.meltano_version} may not be fully compatible. "
                    "Recommended: 3.0.0+"
                )
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Compatibility validation failed: {e}")

    # =========================================================================
    # METADATA AND SERIALIZATION METHODS
    # =========================================================================

    def get_metadata(self) -> dict[str, str | bool]:
        """Get configuration metadata for logging and debugging."""
        return {
            "app_name": self.project_name,
            "version": self.version,
            "environment": self.default_environment,
            "meltano_version": self.meltano_version,
            "debug": self.log_level == "DEBUG",
            "trace": self.log_level == "DEBUG",
            "structured_logging": self.enable_structured_logging,
            "encryption_enabled": self.enable_encryption,
        }

    def to_json(self) -> str:
        """Serialize configuration to JSON (excluding secrets)."""
        data = self.model_dump(exclude={"database_url"})
        return FlextUtilities.Json.serialize(data)

    @classmethod
    def from_json(cls, json_str: str) -> FlextResult[FlextMeltanoConfig]:
        """Deserialize configuration from JSON."""
        try:
            data = FlextUtilities.Json.deserialize(json_str)
            return FlextResult.ok(cls(**data))
        except Exception as e:
            return FlextResult.fail(f"Failed to load config from JSON: {e}")

    def __str__(self) -> str:
        """String representation of configuration (safe, no secrets)."""
        return (
            f"FlextMeltanoConfig(project_id='{self.project_id}', "
            f"environment='{self.default_environment}', "
            f"version='{self.version}')"
        )

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return (
            f"FlextMeltanoConfig("
            f"project_id={self.project_id!r}, "
            f"project_name={self.project_name!r}, "
            f"version={self.version!r}, "
            f"default_environment={self.default_environment!r}, "
            f"meltano_version={self.meltano_version!r}, "
            f"enable_plugin_discovery={self.enable_plugin_discovery!r}, "
            f"default_batch_size={self.default_batch_size!r}, "
            f"max_concurrent_pipelines={self.max_concurrent_pipelines!r}, "
            f"enable_structured_logging={self.enable_structured_logging!r}, "
            f"log_level={self.log_level!r}, "
            f"enable_encryption={self.enable_encryption!r}"
            f")"
        )


__all__ = [
    "FlextMeltanoConfig",
    "FlextMeltanoConfigBuilders",
]
