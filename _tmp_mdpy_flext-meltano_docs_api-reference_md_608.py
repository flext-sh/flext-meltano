# from flext-meltano_docs/api-reference.md:608
from __future__ import annotations


def find_plugin(
    self, plugin_name: str, plugin_type: str | None = None
) -> p.Result[FlextMeltanoModels.PluginInfo | None]:
    """Find a plugin by name and optional type.

    Args:
        plugin_name: Name of the plugin to find
        plugin_type: Type of plugin (tap, target, transformer)

    Returns:
        r containing plugin info or None

    """```
##### list_plugins_by_type(plugin_type)

**List plugins by type**

