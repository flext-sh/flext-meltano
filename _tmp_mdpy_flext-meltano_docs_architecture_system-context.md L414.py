# from flext-meltano/docs/architecture/system-context.md:414
from __future__ import annotations
class PluginManager:
    """Plugin management system for ecosystem extensibility."""

    def __init__(self):
        self.plugin_registry: Dict[str, PluginInfo] = {}
        self.plugin_loaders: List[PluginLoader] = []

    def register_plugin(self, plugin_info: PluginInfo) -> p.Result[bool]:
        """Register a plugin in the ecosystem."""
        if plugin_info.name in self.plugin_registry:
            return r.fail(
                PluginError(f"Plugin {plugin_info.name} already registered")
            )

        # Validate plugin compatibility
        validation_result = self.validate_plugin_compatibility(plugin_info)
        if validation_result.failure:
            return validation_result

        self.plugin_registry[plugin_info.name] = plugin_info
        self.logger.info(f"Registered plugin: {plugin_info.name}")
        return r.| ok(value=True)

    def load_plugin(self, name: str) -> p.Result[Plugin]:
        """Load and initialize a plugin."""
        if name not in self.plugin_registry:
            return r.fail(
                PluginError(f"Plugin {name} not found in registry")
            )

        plugin_info = self.plugin_registry[name]

        # Load plugin using appropriate loader
        for loader in self.plugin_loaders:
            if loader.can_load(plugin_info):
                return loader.load_plugin(plugin_info)

        return r.fail(
            PluginError(f"No loader found for plugin {name}")
        )```
______________________________________________________________________

## 🌐 Ecosystem Architecture

### FLEXT Ecosystem Structure

