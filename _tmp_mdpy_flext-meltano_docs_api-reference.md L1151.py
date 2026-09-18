# from flext-meltano/docs/api-reference.md:1151
from flext_meltano import FlextPluginService

# Initialize plugin service
plugin_service = FlextPluginService()

# Install plugin
install_result = plugin_service.install_plugin("tap-gitlab")
if install_result.success:
    u.Cli.print(f"Installed {install_result.unwrap().plugin_name}")

# List available taps
taps = plugin_service.discover_plugins()
available_taps = [p for p in taps.unwrap() if p.plugin_type == "tap"]```
______________________________________________________________________

**Document Status**: ✅ Complete | **Last Reviewed**: 2026-04-14

## Related Documentation

**Within Project**:

- [Getting Started](getting-started.md) - Installation and basic usage
- [Architecture](architecture.md) - Architecture and design patterns
- [Examples](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-meltano/examples/) - Working code examples

**Across Projects**:

- [flext-core Foundation](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-core/docs/api-reference/foundation.md) - Core APIs and patterns
- [flext-plugin API](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-plugin/docs/api-reference.md) - Plugin API reference
- [flext-quality Automation](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-quality/AGENTS.md) - Quality analysis and automation

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
