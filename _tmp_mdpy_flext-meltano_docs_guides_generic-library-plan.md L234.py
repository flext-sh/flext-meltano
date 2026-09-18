# from flext-meltano/docs/guides/generic-library-plan.md:234
from __future__ import annotations


def install_plugin(
    plugin_name: str, version: str | None = None, source: str | None = None
) -> p.Result[PluginInstallResult]:
    """Install plugin from specified source.

    Args:
        plugin_name: Name of the plugin to install
        version: Specific version to install
        source: Installation source (pip, git, local)

    Returns:
        Installation result with success/failure status

    """```
### Singer Protocol API

#### Tap Execution API

