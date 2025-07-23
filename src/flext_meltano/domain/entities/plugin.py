"""Meltano Plugin Domain Entity - NEW SEMANTIC ARCHITECTURE.

MeltanoPlugin represents a Meltano plugin (extractor, loader, etc.)
with its configuration and business rules.
"""

from __future__ import annotations

from typing import Any, ClassVar

from flext_core import ServiceResult
from pydantic import BaseModel, Field, field_validator

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_meltano.infrastructure.di_container import (
    get_domain_entity,
    get_field,
    get_service_result,
)

DomainEntity = BaseModel




class MeltanoPlugin(DomainEntity):
    """Meltano plugin domain entity with business rules."""

    # Identity
    name: str = Field(..., description="Plugin name")
    namespace: str = Field(..., description="Plugin namespace")

    # Plugin metadata
    plugin_type: str = Field(..., description="Plugin type")
    variant: str = Field(default="original", description="Plugin variant")
    pip_url: str | None = Field(default=None, description="Plugin pip URL")

    # Configuration
    settings: dict[str, Any] = Field(
        default_factory=dict,
        description="Plugin settings",
    )
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Plugin configuration",
    )

    # Status
    is_installed: bool = Field(default=False, description="Whether plugin is installed")
    is_configured: bool = Field(
        default=False,
        description="Whether plugin is configured",
    )
    is_enabled: bool = Field(default=True, description="Whether plugin is enabled")

    # Metadata
    description: str | None = Field(default=None, description="Plugin description")
    version: str | None = Field(default=None, description="Plugin version")

    # Business rules
    VALID_PLUGIN_TYPES: ClassVar[set[str]] = {
        "extractors",
        "loaders",
        "transformers",
        "orchestrators",
        "utilities",
        "files",
        "mappers",
    }

    @field_validator("plugin_type")
    @classmethod
    def validate_plugin_type(cls, v: str) -> str:
        """Validate plugin type."""
        if v not in cls.VALID_PLUGIN_TYPES:
            msg = f"Invalid plugin type '{v}'. Must be one of: {cls.VALID_PLUGIN_TYPES}"
            raise ValueError(msg)
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate plugin name."""
        if not v or len(v.strip()) == 0:
            msg = "Plugin name cannot be empty"
            raise ValueError(msg)

        # Business rule: plugin names follow naming convention
        import re

        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            msg = "Plugin name must contain only alphanumeric characters, dashes, and underscores"
            raise ValueError(msg)

        return v.strip()

    def install(self) -> ServiceResult[None]:
        """Mark plugin as installed."""
        if self.is_installed:
            return ServiceResult.fail("Plugin is already installed")

        self.is_installed = True
        return ServiceResult.ok(None)

    def uninstall(self) -> ServiceResult[None]:
        """Mark plugin as uninstalled."""
        if not self.is_installed:
            return ServiceResult.fail("Plugin is not installed")

        self.is_installed = False
        self.is_configured = False  # Cannot be configured if not installed
        return ServiceResult.ok(None)

    def configure(self, settings: dict[str, Any]) -> ServiceResult[None]:
        """Configure the plugin with settings."""
        if not self.is_installed:
            return ServiceResult.fail("Cannot configure plugin that is not installed")

        # Business rule: validate required settings based on plugin type
        if self.plugin_type == "extractors" and not settings.get("connection"):
            return ServiceResult.fail("Extractors must have connection settings")

        if self.plugin_type == "loaders" and not settings.get("target"):
            return ServiceResult.fail("Loaders must have target settings")

        self.settings.update(settings)
        self.is_configured = True
        return ServiceResult.ok(None)

    def enable(self) -> ServiceResult[None]:
        """Enable the plugin."""
        if not self.is_installed:
            return ServiceResult.fail("Cannot enable plugin that is not installed")

        if self.is_enabled:
            return ServiceResult.fail("Plugin is already enabled")

        self.is_enabled = True
        return ServiceResult.ok(None)

    def disable(self) -> ServiceResult[None]:
        """Disable the plugin."""
        if not self.is_enabled:
            return ServiceResult.fail("Plugin is already disabled")

        self.is_enabled = False
        return ServiceResult.ok(None)

    def is_ready_for_execution(self) -> bool:
        """Check if plugin is ready for execution."""
        return self.is_installed and self.is_configured and self.is_enabled

    def get_full_name(self) -> str:
        """Get the full plugin name including namespace."""
        return (
            f"{self.namespace}:{self.name}"
            if self.namespace != self.name
            else self.name
        )

    def update_settings(self, new_settings: dict[str, Any]) -> ServiceResult[None]:
        """Update plugin settings."""
        if not self.is_installed:
            return ServiceResult.fail("Cannot update settings for uninstalled plugin")

        self.settings.update(new_settings)
        return ServiceResult.ok(None)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting value."""
        return self.settings.get(key, default)
