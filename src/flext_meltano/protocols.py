"""Protocols and abstract interfaces for flext-meltano.

All abstract contracts are centralized here and, when possible, reuse
interfaces from `flext_core` root API. New protocols here should extend
or compose those to avoid duplication.

This module provides comprehensive Protocol definitions following Python 3.13
typing standards and SOLID principles for all FLEXT Meltano components.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

# Reuse core plugin interfaces to avoid duplication

if TYPE_CHECKING:
    from pathlib import Path

    from flext_core import FlextResult

    from .config import FlextMeltanoConfig
    from .singer_unified import (
        FlextSingerUnifiedConfig,
        FlextSingerUnifiedResult,
    )


# =============================================================================
# PLUGIN PROTOCOLS (re-exported from flext-core)
# =============================================================================

# FlextPluginContext and FlextPlugin are imported from flext_core and re-exported via __all__


# =============================================================================
# CORE SERVICE PROTOCOLS
# =============================================================================


@runtime_checkable
class FlextMeltanoServiceProtocol(Protocol):
    """Protocol for all FLEXT Meltano services."""

    def initialize(self) -> FlextResult[bool]:
        """Initialize the service after validating state."""
        ...

    def validate_service(self) -> FlextResult[bool]:
        """Validate service-specific requirements."""
        ...

    def get_health_status(self) -> FlextResult[dict[str, object]]:
        """Return health information for monitoring."""
        ...


@runtime_checkable
class FlextMeltanoBridgeProtocol(Protocol):
    """Protocol for bridge integration with Go services."""

    def get_version(self) -> FlextResult[dict[str, object]]:
        """Get version information."""
        ...

    def list_plugins(self) -> FlextResult[list[dict[str, object]]]:
        """List available plugins."""
        ...

    def run_pipeline(self, tap_name: str, target_name: str) -> FlextResult[dict[str, object]]:
        """Run pipeline between tap and target."""
        ...

    def discover_catalog(self, tap_name: str) -> FlextResult[dict[str, object]]:
        """Discover catalog for a tap."""
        ...


@runtime_checkable
class FlextMeltanoExecutorProtocol(Protocol):
    """Protocol for command execution."""

    def execute_command(self, command: list[str]) -> FlextResult[dict[str, object]]:
        """Execute a command and return result."""
        ...

    def run_pipeline(self, tap_name: str, target_name: str) -> FlextResult[dict[str, object]]:
        """Execute a pipeline."""
        ...


# =============================================================================
# SINGER COMPONENT PROTOCOLS
# =============================================================================


class FlextSingerUnifiedInterface(ABC):
    """Unified abstract interface for Singer components.

    Extends core patterns while remaining independent of concrete SDKs.
    """

    @abstractmethod
    def initialize(self, config: FlextSingerUnifiedConfig) -> FlextResult[None]:
        """Initialize component with unified configuration."""
        ...

    @abstractmethod
    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover and return Singer catalog."""
        ...

    @abstractmethod
    def execute(self, input_data: object | None = None) -> FlextResult[FlextSingerUnifiedResult]:
        """Execute operation and return unified result."""
        ...

    @abstractmethod
    def validate_configuration(self) -> FlextResult[None]:
        """Validate current configuration."""
        ...


@runtime_checkable
class FlextSingerTapProtocol(Protocol):
    """Protocol for Singer tap implementations."""

    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover schema catalog."""
        ...

    def set_tap_class(self, tap_class: type) -> FlextResult[None]:
        """Set Singer tap class."""
        ...

    def validate_ready_for_use(self) -> FlextResult[bool]:
        """Validate if tap is ready for use."""
        ...


@runtime_checkable
class FlextSingerTargetProtocol(Protocol):
    """Protocol for Singer target implementations."""

    def set_target_class(self, target_class: type) -> FlextResult[None]:
        """Set Singer target class."""
        ...

    def validate_ready_for_use(self) -> FlextResult[bool]:
        """Validate if target is ready for use."""
        ...


# =============================================================================
# DBT INTEGRATION PROTOCOLS
# =============================================================================


@runtime_checkable
class FlextMeltanoDbtProtocol(Protocol):
    """Protocol for DBT service implementations."""

    async def run_models(
        self,
        models: list[str] | None = None,
        exclude: list[str] | None = None,
    ) -> FlextResult[list[dict[str, object]]]:
        """Run DBT models."""
        ...

    async def test_models(
        self,
        models: list[str] | None = None,
        exclude: list[str] | None = None,
    ) -> FlextResult[list[dict[str, object]]]:
        """Test DBT models."""
        ...

    def get_dbt_version(self) -> str:
        """Get DBT version."""
        ...


# =============================================================================
# PLUGIN MANAGEMENT PROTOCOLS
# =============================================================================


@runtime_checkable
class FlextMeltanoPluginProtocol(Protocol):
    """Protocol for plugin implementations."""

    def install(self) -> FlextResult[None]:
        """Install the plugin."""
        ...

    def configure(self, config: dict[str, object]) -> FlextResult[None]:
        """Configure the plugin."""
        ...

    def validate(self) -> FlextResult[bool]:
        """Validate plugin configuration."""
        ...


@runtime_checkable
class FlextMeltanoDiscoveryProtocol(Protocol):
    """Protocol for discovery services."""

    def discover_plugins(self) -> FlextResult[list[dict[str, object]]]:
        """Discover available plugins."""
        ...

    def discover_catalog(self, plugin_name: str) -> FlextResult[dict[str, object]]:
        """Discover catalog for a plugin."""
        ...


@runtime_checkable
class FlextMeltanoInstallationProtocol(Protocol):
    """Protocol for installation services."""

    def install_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        config: dict[str, object] | None = None,
    ) -> FlextResult[None]:
        """Install a plugin."""
        ...

    def validate_installation(self, plugin_name: str) -> FlextResult[bool]:
        """Validate plugin installation."""
        ...


# =============================================================================
# CONFIGURATION PROTOCOLS
# =============================================================================


@runtime_checkable
class FlextMeltanoConfigurableProtocol(Protocol):
    """Protocol for configurable components."""

    config: FlextMeltanoConfig

    def validate_configuration(self) -> FlextResult[None]:
        """Validate current configuration."""
        ...

    def reload_configuration(self, config: FlextMeltanoConfig) -> FlextResult[None]:
        """Reload configuration."""
        ...


# =============================================================================
# VALIDATION PROTOCOLS
# =============================================================================


@runtime_checkable
class FlextMeltanoValidationProtocol(Protocol):
    """Protocol for validation services."""

    def validate_project(self, project_path: Path | None = None) -> FlextResult[bool]:
        """Validate Meltano project."""
        ...

    def validate_plugin_config(
        self,
        plugin_name: str,
        config: dict[str, object],
    ) -> FlextResult[bool]:
        """Validate plugin configuration."""
        ...

    def test_connection(self, plugin_name: str) -> FlextResult[bool]:
        """Test plugin connection."""
        ...


__all__ = [
    "FlextMeltanoBridgeProtocol",
    # Configuration protocols
    "FlextMeltanoConfigurableProtocol",
    # DBT protocols
    "FlextMeltanoDbtProtocol",
    "FlextMeltanoDiscoveryProtocol",
    "FlextMeltanoExecutorProtocol",
    "FlextMeltanoInstallationProtocol",
    # Plugin protocols
    "FlextMeltanoPluginProtocol",
    # Core protocols
    "FlextMeltanoServiceProtocol",
    # Validation protocols
    "FlextMeltanoValidationProtocol",
    "FlextSingerTapProtocol",
    "FlextSingerTargetProtocol",
    # Singer protocols
    "FlextSingerUnifiedInterface",
]
