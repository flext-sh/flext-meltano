"""FLEXT Meltano plugin discovery helpers."""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult


def flext_meltano_discover_plugins(
    plugin_type: str | None = None,
) -> FlextResult[list[dict[str, Any]]]:
    """Discover available Meltano plugins.

    Args:
        plugin_type: Optional filter by plugin type (extractors, loaders, etc.)

    Returns:
        FlextResult containing list of discovered plugins

    """
    try:
        # Basic plugin discovery - can be extended with actual Meltano discovery
        plugins = [
            {
                "name": "tap-csv",
                "type": "extractors",
                "namespace": "tap_csv",
                "pip_url": "pipelinewise-tap-csv",
            },
            {
                "name": "target-jsonl",
                "type": "loaders",
                "namespace": "target_jsonl",
                "pip_url": "target-jsonl",
            },
        ]

        if plugin_type:
            plugins = [p for p in plugins if p["type"] == plugin_type]

        return FlextResult.ok(plugins)

    except Exception as e:
        return FlextResult.fail(f"Failed to discover plugins: {e}")
