# from flext-meltano_docs/api-reference.md:537
from __future__ import annotations


def uninstall_plugin(
    self, plugin_name: str
) -> p.Result[FlextMeltanoModels.PluginUninstallResult]:
    """Uninstall a plugin.

    Args:
        plugin_name: Name of the plugin to uninstall

    Returns:
        r containing uninstall result

    """```
##### update_plugin(plugin_name, version=None)

**Update a plugin to latest or specific version**

