# from flext-meltano/docs/api-reference.md:501
from __future__ import annotations


def discover_plugins(self) -> p.Result[Sequence[FlextMeltanoModels.PluginInfo]]:
    """Discover all plugins in the project.

    Returns:
        r containing list of discovered plugins

    """```
##### install_plugin(plugin_name, version=None)

**Install a plugin**

