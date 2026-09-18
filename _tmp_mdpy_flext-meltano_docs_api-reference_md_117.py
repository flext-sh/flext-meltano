# from flext-meltano_docs/api-reference.md:117
from __future__ import annotations


def discover_plugins(self) -> p.Result[Sequence[FlextMeltanoModels.PluginInfo]]:
    """Discover all available plugins in the project.

    Returns:
        r containing list of discovered plugins or error

    Example:
        >>> service = FlextMeltanoService()
        >>> result = service.discover_plugins()
        >>> if result.success:
        ...     plugins = result.unwrap()
        ...     u.Cli.print(f"Found {len(plugins)} plugins")

    """```
##### install_plugin(plugin_name, version=None)

**Install a Meltano plugin**

