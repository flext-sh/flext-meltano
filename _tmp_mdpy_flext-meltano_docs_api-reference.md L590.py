# from flext-meltano/docs/api-reference.md:590
from __future__ import annotations


def register_plugin(self, plugin_info: FlextMeltanoModels.PluginInfo) -> p.Result[bool]:
    """Register a plugin in the registry.

    Args:
        plugin_info: Plugin information to register

    Returns:
        r indicating success or failure

    """```
##### find_plugin(plugin_name, plugin_type=None)

**Find a plugin by name and type**

