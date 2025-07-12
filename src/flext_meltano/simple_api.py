"""Simple API for FLEXT Meltano setup and configuration.

Provides a simple interface for setting up the FLEXT Meltano system.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core.config import get_container
from flext_core.domain.result import ServiceResult
from flext_meltano.config import MeltanoSettings


def setup_meltano(settings: MeltanoSettings | None = None) -> ServiceResult[bool]:
    """Set up FLEXT Meltano system with configuration and logging.

    Args:
    ----
        settings: Optional MeltanoSettings instance. If None, defaults are used.

    Returns:
    -------
        ServiceResult[bool]: Success/failure result of setup operation.

    """
    try:
        if settings is None:
            settings = MeltanoSettings()

        # Configure DI container
        container = get_container()

        # Register settings with container
        container.register(MeltanoSettings, settings)

        return ServiceResult.ok(True)

    except Exception as e:
        return ServiceResult.fail(f"Failed to setup meltano: {e}")


def create_development_meltano_config(**overrides: Any) -> MeltanoSettings:
    """Create development-friendly Meltano configuration.

    Args:
    ----
        **overrides: Configuration overrides to apply.

    Returns:
    -------
        MeltanoSettings: Configured settings instance for development.

    """
    # Development defaults
    defaults = {
        "project_root": Path.cwd() / "meltano_projects_dev",
        "log_level": "DEBUG",
        "log_structured": False,
        "environment": "development",
        "debug": True,
    }

    # Merge defaults with overrides
    config = {**defaults, **overrides}

    return MeltanoSettings(**config)


def get_meltano_settings() -> MeltanoSettings:
    """Get current Meltano settings from DI container.

    Returns
    -------
        MeltanoSettings: Current settings instance.

    Raises
    ------
        RuntimeError: If settings not found in container.

    """
    try:
        container = get_container()
        return container.resolve(MeltanoSettings)
    except Exception as e:
        msg = f"Meltano settings not configured. Call setup_meltano() first: {e}"
        raise RuntimeError(msg) from e
