# from flext-meltano_docs/guides/generic-library-plan.md:190
# Independent plugin registry
plugin_service = FlextPluginService()
registry = plugin_service.get_plugin_registry()

# Direct plugin operations
tap_plugin = registry.load_plugin("tap-gitlab")
settings = tap_plugin.validate_configuration(user_config)```
#### FlextSingerService (Protocol Implementation)

**Direct Singer Protocol Handling:**

