# from flext-meltano/docs/api-reference.md:557
from __future__ import annotations


def update_plugin(
    self, plugin_name: str, version: str | None = None
) -> p.Result[FlextMeltanoModels.PluginUpdateResult]:
    """Update a plugin.

    Args:
        plugin_name: Name of the plugin to update
        version: Specific version to update to

    Returns:
        r containing update result

    """```
### FlextPluginRegistry

**Plugin registry and discovery system**

