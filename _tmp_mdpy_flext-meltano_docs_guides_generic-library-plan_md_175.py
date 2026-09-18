# from flext-meltano_docs/guides/generic-library-plan.md:175
# Plugin operations (no CLI dependency)
service = FlextMeltanoService()
plugins = service.discover_plugins()
result = service.install_plugin("tap-gitlab")

# Pipeline execution (protocol-based)
tap_result = service.execute_tap("tap-gitlab", settings={"api_url": "..."})
target_result = service.execute_target(
    "target-postgres", records, settings={"host": "..."}
)```
#### FlextPluginService (Plugin Management)

**Self-Contained Plugin Management:**

