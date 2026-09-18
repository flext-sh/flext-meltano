# from flext-meltano/docs/api-reference.md:139
from __future__ import annotations


def install_plugin(
    self, plugin_name: str, version: str | None = None
) -> p.Result[FlextMeltanoModels.PluginInstallResult]:
    """Install a Meltano plugin.

    Args:
        plugin_name: Name of the plugin to install
        version: Specific version to install (optional)

    Returns:
        r containing installation result or error

    """```
##### execute_tap(tap_name, settings=None, state=None)

**Execute a Singer tap**

