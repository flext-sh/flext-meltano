"""FLEXT Meltano configuration helpers."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from flext_meltano.helpers.execution import FlextMeltanoResult
else:
    from flext_meltano.helpers.execution import FlextMeltanoResult

# Logger removed due to missing FlextLoggerFactory


def flext_meltano_load_config(
    config_path: str | Path | None = None,
) -> FlextMeltanoResult:
    """Load Meltano configuration from file or environment.

    Args:
        config_path: Optional path to configuration file

    Returns:
        FlextMeltanoResult containing loaded configuration

    """
    try:
        config = {
            "project_root": str(Path.cwd()),
            "environment": "dev",
            "log_level": "info",
            "timeout": 300,  # 5 minutes default
            "meltano": {
                "project_root": str(Path.cwd()),
                "environment": "dev",
            },
        }

        if config_path:
            # Load actual meltano.yml configuration file
            try:
                with Path(config_path).open(encoding="utf-8") as f:
                    file_config = yaml.safe_load(f)

                # Merge file config with default config
                if isinstance(file_config, dict):
                    config.update(file_config)

                config["config_file"] = str(config_path)
            except (ValueError, TypeError, RuntimeError, OSError):
                # Continue with default config if file loading fails
                pass

        return FlextMeltanoResult.ok(config)

    except (ValueError, TypeError, RuntimeError, OSError) as e:
        return FlextMeltanoResult.fail(f"Failed to load configuration: {e}")
