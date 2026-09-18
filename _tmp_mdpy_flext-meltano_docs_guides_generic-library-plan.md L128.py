# from flext-meltano/docs/guides/generic-library-plan.md:128
# Generic plugin registry
registry = FlextPluginRegistry()
plugins = registry.discover_plugins()  # No Meltano dependency
tap_info = registry.find_plugin("tap-gitlab")```
## Architecture Transformation

### Before: CLI-Centric Architecture```
┌─────────────────────────────────────┐
│ FLEXT-Meltano (CLI-Dependent)      │
├─────────────────────────────────────┤
│ 🔧 Meltano CLI Commands             │ ← Direct CLI execution
│ 📦 Plugin Installation              │ ← CLI-based installation
│ 🚀 Pipeline Execution               │ ← CLI command execution
│ 📁 Project Management              │ ← Meltano YAML parsing
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ External Dependencies               │
├─────────────────────────────────────┤
│ meltano package (runtime)           │
│ meltano.yml structure              │
│ Singer CLI tools                   │
└─────────────────────────────────────┘```
### After: Generic Library Architecture```
┌─────────────────────────────────────┐
│ FLEXT-Meltano (Generic Library)    │
├─────────────────────────────────────┤
│ 🔧 Plugin Management Services       │ ← Programmatic APIs
│ 📦 Singer Protocol Implementation   │ ← Direct protocol handling
│ 🚀 Pipeline Orchestration           │ ← Service-based execution
│ 📁 Generic Configuration           │ ← Abstracted settings management
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Core Dependencies Only             │
├─────────────────────────────────────┤
│ flext-core (foundation)            │
│ singer-python (protocol)           │
│ pydantic (validation)              │
└─────────────────────────────────────┘```
### Service Architecture

#### FlextMeltanoService (Primary Interface)

**Generic Operations:**

