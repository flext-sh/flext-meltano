"""Dependency injection container for FLEXT-MELTANO.

REFACTORED:
    Uses flext-core dependency injection patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from flext_meltano.config.settings import FlextMeltanoSettings
from flext_meltano.infrastructure.di_container import get_container

T = TypeVar("T")

if TYPE_CHECKING:
    from collections.abc import Callable


# Simple singleton implementation since not available from di_container
def singleton[T](cls: type[T]) -> Callable[..., T]:
    """Simple singleton decorator."""
    instances: dict[type, Any] = {}

    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]  # type: ignore[no-any-return]

    return get_instance


@singleton
class FlextMeltanoContainerConfig:
    """Meltano container configuration using flext-core patterns."""

    def __init__(self, settings: FlextMeltanoSettings) -> None:
        self.settings = settings

    def configure_dependencies(self) -> None:
        """Configure Meltano dependency injection container.

        Registers all Meltano-specific services and configurations with the
        flext-core dependency injection container.
        """
        # Get container
        container = get_container()
        # Register settings
        container.register(FlextMeltanoSettings, self.settings)

        # Register this config instance
        container.register(FlextMeltanoContainerConfig, self)


def setup_meltano_container(
    settings: FlextMeltanoSettings | None = None,
) -> FlextMeltanoContainerConfig:
    """Set up Meltano dependency injection container."""
    if settings is None:
        settings = FlextMeltanoSettings(
            project_name="flext-infrastructure.plugins.flext-meltano",
            project_version="0.7.0",
            environment="development",
        )

    config = FlextMeltanoContainerConfig(settings)
    config.configure_dependencies()

    return config


def get_meltano_container() -> FlextMeltanoContainerConfig:
    """Get configured Meltano container."""
    container = get_container()
    return container.resolve(FlextMeltanoContainerConfig)  # type: ignore[no-any-return]
