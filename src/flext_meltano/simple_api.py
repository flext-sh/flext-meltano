"""Simple API for FLEXT Meltano setup and configuration.

Provides a simple interface for setting up the FLEXT Meltano system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_meltano.config.settings import FlextMeltanoSettings

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports

if TYPE_CHECKING:
    from pathlib import Path

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
    from pathlib import Path

    from flext_meltano.config.settings import FlextMeltanoProjectConfig

    # Ensure project_root is a Path object
    project_path = Path(project_root) if isinstance(project_root, str) else project_root

    project_config = FlextMeltanoProjectConfig(
        project_root=project_path,
        default_environment=environment,
    )

    settings = FlextMeltanoSettings(
        environment=environment,
        project=project_config,
    )

    return {
        "success": True,
        "settings": settings,
        "project_root": str(settings.project.project_root),
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
