# from flext-meltano_docs/guides/generic-library-plan.md:214
from __future__ import annotations


# Generic plugin discovery
def discover_plugins(
    plugin_type: str | None = None, source: PluginSource = PluginSource.AUTO
) -> p.Result[Sequence[PluginInfo]]:
    """Discover plugins from multiple sources.

    Args:
        plugin_type: Filter by plugin type (tap, target, transformer)
        source: Plugin source (MELTANO_HUB, LOCAL_REGISTRY, GIT_REPO)

    Returns:
        List of discovered plugins with metadata

    """```
#### Plugin Installation API

