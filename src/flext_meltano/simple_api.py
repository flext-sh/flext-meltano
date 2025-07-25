"""Simple API for FLEXT Meltano setup and configuration.

Provides a simple interface for setting up the FLEXT Meltano system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_meltano.config.settings import (
    FlextMeltanoProjectConfig,
    FlextMeltanoSettings,
)

if TYPE_CHECKING:
    from pathlib import Path

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports

# Initialize types via DI container
# Define local types to avoid flext-core dependency
EnvironmentLiteral = str


def setup_meltano_simple(
    project_root: Path | str,
    environment: EnvironmentLiteral = "dev",
) -> dict[str, Any]:
    """Set up Meltano with simple configuration.

    Args:
        project_root: Path to project directory
        environment: Target environment (dev, prod, etc.)

    Returns:
        Dictionary with setup results

    """
    # Ensure project_root is a string (will be validated and converted internally)
    project_path_str = str(project_root)

    project_config = FlextMeltanoProjectConfig(
        project_root=project_path_str,
        default_environment=environment,
    )

    settings = FlextMeltanoSettings(
        environment=environment,
        project=project_config,
    )

    # Safe access to project_root with None check
    project_root_str = str(project_path_str) if settings.project is None else str(settings.project.project_root)

    return {
        "success": True,
        "settings": settings,
        "project_root": project_root_str,
        "environment": settings.environment,
    }


def flext_create_basic_config() -> dict[str, Any]:
    """Create basic Meltano configuration.

    Returns:
        Basic configuration dictionary

    """
    return {
        "version": 1,
        "default_environment": "dev",
        "environments": [
            {"name": "dev"},
            {"name": "prod"},
        ],
        "plugins": {
            "extractors": [],
            "loaders": [],
            "transformers": [],
        },
    }
