# from flext-meltano/docs/api-reference.md:259
from __future__ import annotations


def list_plugins(
    self, plugin_type: str | None = None
) -> p.Result[Sequence[FlextMeltanoModels.PluginInfo]]:
    """List available Meltano plugins.

    Args:
        plugin_type: Filter by plugin type (tap, target, transformer)

    Returns:
        r containing list of plugins or error

    """```
### FlextMeltanoExecutor

**Advanced pipeline execution engine**

