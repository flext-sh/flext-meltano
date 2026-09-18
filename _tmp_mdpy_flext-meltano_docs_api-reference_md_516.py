# from flext-meltano_docs/api-reference.md:516
from __future__ import annotations


def install_plugin(
    self, plugin_name: str, version: str | None = None
) -> p.Result[FlextMeltanoModels.PluginInstallResult]:
    """Install a plugin.

    Args:
        plugin_name: Name of the plugin to install
        version: Specific version to install

    Returns:
        r containing installation result

    """```
##### uninstall_plugin(plugin_name)

**Uninstall a plugin**

