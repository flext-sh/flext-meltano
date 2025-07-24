"""FLEXT Meltano configuration helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core import FlextConstants, FlextResult


def flext_meltano_load_config(
    config_path: str | Path | None = None,
) -> FlextResult[dict[str, Any]]:
    """Load Meltano configuration from file or environment.

    Args:
        config_path: Optional path to configuration file

    Returns:
        FlextResult containing loaded configuration

    """
    try:
        config = {
            "project_root": str(Path.cwd()),
            "environment": "dev",
            "log_level": "info",
            "timeout": FlextConstants.DEFAULT_TIMEOUT,
            "meltano": {
                "project_root": str(Path.cwd()),
                "environment": "dev",
            },
        }

        if config_path:
            # TODO: Load actual config file when implemented
            config["config_file"] = str(config_path)

        return FlextResult.ok(config)

    except Exception as e:
        return FlextResult.fail(f"Failed to load configuration: {e}")
