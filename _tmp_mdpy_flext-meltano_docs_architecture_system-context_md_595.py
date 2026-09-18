# from flext-meltano_docs/architecture/system-context.md:595
from __future__ import annotations
class FLEXTPluginRegistry:
    """Central plugin registry for ecosystem coordination."""

    def __init__(self):
        self.registered_plugins: Dict[str, PluginMetadata] = {}

    def register_flext_plugin(self, plugin: FLEXTPlugin) -> p.Result[bool]:
        """Register a FLEXT plugin in the ecosystem."""

        # Validate plugin compatibility
        compatibility_result = self.validate_plugin_compatibility(plugin)
        if compatibility_result.failure:
            return compatibility_result

        # Register with FLEXT-Meltano
        registration_result = self.meltano_adapter.register_plugin(plugin)
        if registration_result.failure:
            return registration_result

        # Add to ecosystem registry
        self.registered_plugins[plugin.name] = PluginMetadata(
            name=plugin.name,
            version=plugin.version,
            type=plugin.plugin_type,
            dependencies=plugin.dependencies,
            capabilities=plugin.capabilities
        )

        return r.| ok(value=True)

    def discover_compatible_plugins(self, requirements: PluginRequirements) -> List[PluginMetadata]:
        """Discover plugins that meet specific requirements."""
        compatible = []

        for plugin_meta in self.registered_plugins.values():
            if self.plugin_meets_requirements(plugin_meta, requirements):
                compatible.append(plugin_meta)

        return sorted(compatible, key=lambda p: p.version, reverse=True)```
______________________________________________________________________

## 🔲 System Boundaries

### Functional Boundaries

#### Data Integration Boundary

- **Inside**: Singer protocol implementation, Meltano orchestration, DBT execution
- **Outside**: Specific data source/target implementations (handled by domain projects)
- **Interface**: Plugin API, configuration schemas, execution results

#### Application Boundary

- **Inside**: Business logic, validation, error handling, state management
- **Outside**: User interfaces, external APIs, infrastructure concerns
- **Interface**: REST APIs, CLI commands, plugin interfaces

#### Infrastructure Boundary

- **Inside**: Application code, business rules, data models
- **Outside**: Operating system, network, storage, external services
- **Interface**: Environment variables, configuration files, service contracts

### Security Boundaries

