"""Dependency injection container for FLEXT-MELTANO.

REFACTORED:
    Uses flext-core dependency injection patterns.
"""

from __future__ import annotations

from flext_core import get_container, singleton

from flext_meltano.config import MeltanoSettings


@singleton
class MeltanoContainerConfig:
    """Meltano container configuration using flext-core patterns."""

    def __init__(self, settings: MeltanoSettings) -> None:
        self.settings = settings

    def configure_dependencies(self) -> None:
        """Configure Meltano dependency injection container.

        Registers all Meltano-specific services and configurations with the
        flext-core dependency injection container.
        """
        container = get_container()

        # Register settings
        container.register(MeltanoSettings, self.settings)

        # Register this config instance
        container.register(MeltanoContainerConfig, self)


def setup_meltano_container(
    settings: MeltanoSettings | None = None,
) -> MeltanoContainerConfig:
    """Set up Meltano dependency injection container."""
    if settings is None:
        settings = MeltanoSettings(
            project_name="flext-infrastructure.plugins.flext-meltano",
            project_version="0.7.0",
            environment="development",
            debug=False,
        )

    config = MeltanoContainerConfig(settings)
    config.configure_dependencies()

    return config


def get_meltano_container() -> MeltanoContainerConfig:
    """Get configured Meltano container."""
    container = get_container()
    return container.resolve(MeltanoContainerConfig)
