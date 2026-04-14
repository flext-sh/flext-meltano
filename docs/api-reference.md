# FLEXT-Meltano API Reference

<!-- TOC START -->
- [🎯 Library Overview](#library-overview)
  - [**Architecture Principles**](#architecture-principles)
  - [**Core Modules**](#core-modules)
- [🎯 Core Services](#core-services)
  - [FlextMeltanoService](#flextmeltanoservice)
  - [FlextMeltanoAdapter](#flextmeltanoadapter)
  - [FlextMeltanoExecutor](#flextmeltanoexecutor)
- [🔌 Singer Protocol Abstractions](#singer-protocol-abstractions)
  - [FlextSingerTap](#flextsingertap)
  - [FlextSingerTarget](#flextsingertarget)
- [🛠️ Plugin Management Services](#plugin-management-services)
  - [FlextPluginService](#flextpluginservice)
  - [FlextPluginRegistry](#flextpluginregistry)
- [🚀 Pipeline Services](#pipeline-services)
  - [FlextMeltanoService](#flextmeltanoservice)
  - [FlextMeltanoExecutor](#flextmeltanoexecutor)
- [📁 Project Management](#project-management)
  - [FlextProjectService](#flextprojectservice)
  - [FlextMeltanoProject](#flextmeltanoproject)
- [🔧 Configuration Management](#configuration-management)
  - [FlextMeltanoSettings](#flextmeltanosettings)
- [📊 Models and Types](#models-and-types)
  - [Core Models](#core-models)
  - [Execution Models](#execution-models)
- [🛡️ Exception Hierarchy](#exception-hierarchy)
  - [FlextMeltanoException](#flextmeltanoexception)
  - [Specific Exceptions](#specific-exceptions)
- [🔄 Integration Examples](#integration-examples)
  - [Basic Pipeline Execution](#basic-pipeline-execution)
  - [Advanced Pipeline Orchestration](#advanced-pipeline-orchestration)
  - [Plugin Management](#plugin-management)
- [Related Documentation](#related-documentation)
<!-- TOC END -->

**Complete API documentation for FLEXT-Meltano v0.12.0-dev - Enterprise Data Pipeline Integration**

**Updated**: 2026-04-14 | **Status**: ✅ Current | **Quality**: 100% Type Safe | **Coverage**: 95%+

Complete API documentation for FLEXT-Meltano, the comprehensive Meltano integration framework for the FLEXT ecosystem, providing Singer protocol implementation, plugin development tools, and enterprise data pipeline orchestration.

______________________________________________________________________

## 🎯 Library Overview

**FLEXT-Meltano** is an **enterprise-grade Meltano integration framework** providing:

- **Complete Singer Protocol Implementation** - Full tap/target development with enterprise extensions
- **Plugin Development Tools** - Automated plugin scaffolding and validation framework
- **Pipeline Orchestration** - Advanced ELT pipeline management and execution
- **Meltano Integration** - Native Meltano project and plugin support
- **Enterprise Features** - Production-ready pipeline monitoring and management

### **Architecture Principles**

1. **Singer Protocol Compliance** - Full Singer.io specification implementation with enterprise extensions
1. **Plugin-Centric Design** - Plugin-first architecture with automated development tools
1. **Pipeline Orchestration** - Advanced pipeline execution with monitoring and recovery
1. **Enterprise Integration** - Production-ready deployment and operations support
1. **Type Safety** - 100% type coverage with Pydantic v2 models

### **Core Modules**

| Module                | Purpose                        | Key Classes                                   |
| --------------------- | ------------------------------ | --------------------------------------------- |
| `services.py`         | Core service orchestration     | `FlextMeltanoService`, `FlextMeltanoExecutor` |
| `adapters.py`         | Meltano CLI integration        | `FlextMeltanoAdapter`, `FlextMeltanoBridge`   |
| `singer.py`           | Singer protocol implementation | `FlextSingerTap`, `FlextSingerTarget`         |
| `plugin_service.py`   | Plugin management              | `FlextPluginService`, `FlextPluginRegistry`   |
| `pipeline_service.py` | Pipeline orchestration         | `FlextMeltanoService`, `FlextMeltanoExecutor` |
| `project_service.py`  | Project management             | `FlextProjectService`, `FlextMeltanoProject`  |

______________________________________________________________________

## 🎯 Core Services

### FlextMeltanoService

**Primary service for Meltano project management and plugin operations**

```python
class FlextMeltanoService(s):
    """Main orchestration service for Meltano project operations."""

    def __init__(
        self,
        project_root: Path | str | None = None,
        settings: FlextMeltanoModels.Config | None = None,
    ) -> None:
        """Initialize Meltano service.

        Args:
            project_root: Path to Meltano project root directory
            settings: Service configuration t.RecursiveContainer
        """
```

#### Core Operations

##### discover_plugins()

**Discover available Meltano plugins in the project**

```python
def discover_plugins(self) -> p.Result[Sequence[FlextMeltanoModels.PluginInfo]]:
    """Discover all available plugins in the project.

    Returns:
        r containing list of discovered plugins or error

    Example:
        >>> service = FlextMeltanoService()
        >>> result = service.discover_plugins()
        >>> if result.success:
        ...     plugins = result.unwrap()
        ...     print(f"Found {len(plugins)} plugins")
    """
```

##### install_plugin(plugin_name, version=None)

**Install a Meltano plugin**

```python
def install_plugin(
    self, plugin_name: str, version: str | None = None
) -> p.Result[FlextMeltanoModels.PluginInstallResult]:
    """Install a Meltano plugin.

    Args:
        plugin_name: Name of the plugin to install
        version: Specific version to install (optional)

    Returns:
        r containing installation result or error
    """
```

##### execute_tap(tap_name, settings=None, state=None)

**Execute a Singer tap**

```python
def execute_tap(
    self, tap_name: str, settings: t.Dict | None = None, state: t.Dict | None = None
) -> p.Result[FlextMeltanoModels.TapExecutionResult]:
    """Execute a Singer tap with configuration and state.

    Args:
        tap_name: Name of the tap to execute
        settings: Tap configuration dictionary
        state: Tap state dictionary for incremental sync

    Returns:
        r containing execution result or error
    """
```

##### execute_target(target_name, records, settings=None)

**Execute a Singer target**

```python
def execute_target(
    self, target_name: str, records: Sequence[t.Dict], settings: t.Dict | None = None
) -> p.Result[FlextMeltanoModels.TargetExecutionResult]:
    """Execute a Singer target with records.

    Args:
        target_name: Name of the target to execute
        records: List of records to load
        settings: Target configuration dictionary

    Returns:
        r containing execution result or error
    """
```

### FlextMeltanoAdapter

**Meltano CLI integration and execution adapter**

```python
class FlextMeltanoAdapter(s):
    """Adapter for Meltano CLI integration and execution."""

    def __init__(self, project_root: Path | str | None = None) -> None:
        """Initialize Meltano adapter."""
```

#### Pipeline Operations

##### run_pipeline(tap_name, target_name, settings=None)

**Execute complete ELT pipeline**

```python
def run_pipeline(
    self, tap_name: str, target_name: str, settings: t.Dict | None = None
) -> p.Result[FlextMeltanoModels.PipelineResult]:
    """Execute complete ELT pipeline from tap to target.

    Args:
        tap_name: Name of the tap to execute
        target_name: Name of the target to execute
        settings: Pipeline configuration dictionary

    Returns:
        r containing pipeline execution result
    """
```

##### validate_project()

**Validate Meltano project configuration**

```python
def validate_project(self) -> p.Result[FlextMeltanoModels.ProjectValidation]:
    """Validate Meltano project configuration and structure.

    Returns:
        r containing validation result or error
    """
```

##### list_plugins(plugin_type=None)

**List available Meltano plugins**

```python
def list_plugins(
    self, plugin_type: str | None = None
) -> p.Result[Sequence[FlextMeltanoModels.PluginInfo]]:
    """List available Meltano plugins.

    Args:
        plugin_type: Filter by plugin type (tap, target, transformer)

    Returns:
        r containing list of plugins or error
    """
```

### FlextMeltanoExecutor

**Advanced pipeline execution engine**

```python
class FlextMeltanoExecutor(s):
    """Advanced pipeline execution engine with orchestration."""
```

#### Advanced Execution

##### execute_pipeline_advanced(options)

**Execute pipeline with advanced options**

```python
def execute_pipeline_advanced(
    self, options: FlextMeltanoModels.PipelineOptions
) -> p.Result[FlextMeltanoModels.PipelineResult]:
    """Execute pipeline with advanced configuration options.

    Args:
        options: Advanced pipeline execution options

    Returns:
        r containing execution result
    """
```

##### execute_parallel_pipelines(pipelines)

**Execute multiple pipelines in parallel**

```python
def execute_parallel_pipelines(
    self, pipelines: Sequence[FlextMeltanoModels.PipelineConfig]
) -> p.Result[Sequence[FlextMeltanoModels.PipelineResult]]:
    """Execute multiple pipelines in parallel.

    Args:
        pipelines: List of pipeline configurations

    Returns:
        r containing list of execution results
    """
```

______________________________________________________________________

## 🔌 Singer Protocol Abstractions

### FlextSingerTap

**Singer tap implementation with enterprise features**

```python
class FlextSingerTap(s):
    """Singer tap implementation with discovery, sync, and state management."""

    def __init__(
        self, tap_name: str, settings: t.Dict, state: t.Dict | None = None
    ) -> None:
        """Initialize Singer tap.

        Args:
            tap_name: Name of the tap plugin
            settings: Tap configuration dictionary
            state: Initial state for incremental sync
        """
```

#### Tap Operations

##### discover()

**Discover Singer catalog for the tap**

```python
def discover(self) -> p.Result[FlextMeltanoModels.Catalog]:
    """Discover Singer catalog for the tap.

    Returns:
        r containing catalog or error

    Example:
        >>> tap = FlextSingerTap("tap-gitlab", {"api_url": "https://gitlab.com"})
        >>> result = tap.discover()
        >>> if result.success:
        ...     catalog = result.unwrap()
        ...     print(f"Discovered {len(catalog.streams)} streams")
    """
```

##### sync(streams=None, state=None)

**Execute tap synchronization**

```python
def sync(
    self, streams: t.StringList | None = None, state: t.Dict | None = None
) -> p.Result[FlextMeltanoModels.SyncResult]:
    """Execute tap synchronization.

    Args:
        streams: List of streams to sync (None for all)
        state: State dictionary for incremental sync

    Returns:
        r containing sync result or error
    """
```

##### validate_config()

**Validate tap configuration**

```python
def validate_config(self) -> p.Result[FlextMeltanoModels.ValidationResult]:
    """Validate tap configuration.

    Returns:
        r containing validation result
    """
```

### FlextSingerTarget

**Singer target implementation with batch processing**

```python
class FlextSingerTarget(s):
    """Singer target implementation with batch processing and error handling."""

    def __init__(self, target_name: str, settings: t.Dict) -> None:
        """Initialize Singer target."""
```

#### Target Operations

##### load_records(records)

**Load records into the target**

```python
def load_records(
    self, records: Sequence[t.Dict]
) -> p.Result[FlextMeltanoModels.LoadResult]:
    """Load records into the target.

    Args:
        records: List of records to load

    Returns:
        r containing load result or error
    """
```

##### flush()

**Flush any buffered records**

```python
def flush(self) -> p.Result[FlextMeltanoModels.FlushResult]:
    """Flush any buffered records to the target.

    Returns:
        r containing flush result
    """
```

##### validate_config()

**Validate target configuration**

```python
def validate_config(self) -> p.Result[FlextMeltanoModels.ValidationResult]:
    """Validate target configuration.

    Returns:
        r containing validation result
    """
```

______________________________________________________________________

## 🛠️ Plugin Management Services

### FlextPluginService

**Plugin lifecycle management and operations**

```python
class FlextPluginService(s):
    """Service for plugin lifecycle management and operations."""

    def __init__(self, project_root: Path | str | None = None) -> None:
        """Initialize plugin service."""
```

#### Plugin Lifecycle

##### discover_plugins()

**Discover all plugins in the project**

```python
def discover_plugins(self) -> p.Result[Sequence[FlextMeltanoModels.PluginInfo]]:
    """Discover all plugins in the project.

    Returns:
        r containing list of discovered plugins
    """
```

##### install_plugin(plugin_name, version=None)

**Install a plugin**

```python
def install_plugin(
    self, plugin_name: str, version: str | None = None
) -> p.Result[FlextMeltanoModels.PluginInstallResult]:
    """Install a plugin.

    Args:
        plugin_name: Name of the plugin to install
        version: Specific version to install

    Returns:
        r containing installation result
    """
```

##### uninstall_plugin(plugin_name)

**Uninstall a plugin**

```python
def uninstall_plugin(
    self, plugin_name: str
) -> p.Result[FlextMeltanoModels.PluginUninstallResult]:
    """Uninstall a plugin.

    Args:
        plugin_name: Name of the plugin to uninstall

    Returns:
        r containing uninstall result
    """
```

##### update_plugin(plugin_name, version=None)

**Update a plugin to latest or specific version**

```python
def update_plugin(
    self, plugin_name: str, version: str | None = None
) -> p.Result[FlextMeltanoModels.PluginUpdateResult]:
    """Update a plugin.

    Args:
        plugin_name: Name of the plugin to update
        version: Specific version to update to

    Returns:
        r containing update result
    """
```

### FlextPluginRegistry

**Plugin registry and discovery system**

```python
class FlextPluginRegistry(s):
    """Plugin registry for plugin discovery and management."""
```

#### Registry Operations

##### register_plugin(plugin_info)

**Register a plugin in the registry**

```python
def register_plugin(self, plugin_info: FlextMeltanoModels.PluginInfo) -> p.Result[bool]:
    """Register a plugin in the registry.

    Args:
        plugin_info: Plugin information to register

    Returns:
        r indicating success or failure
    """
```

##### find_plugin(plugin_name, plugin_type=None)

**Find a plugin by name and type**

```python
def find_plugin(
    self, plugin_name: str, plugin_type: str | None = None
) -> p.Result[FlextMeltanoModels.PluginInfo | None]:
    """Find a plugin by name and optional type.

    Args:
        plugin_name: Name of the plugin to find
        plugin_type: Type of plugin (tap, target, transformer)

    Returns:
        r containing plugin info or None
    """
```

##### list_plugins_by_type(plugin_type)

**List plugins by type**

```python
def list_plugins_by_type(
    self, plugin_type: str
) -> p.Result[Sequence[FlextMeltanoModels.PluginInfo]]:
    """List plugins by type.

    Args:
        plugin_type: Type of plugins to list

    Returns:
        r containing list of plugins
    """
```

______________________________________________________________________

## 🚀 Pipeline Services

### FlextMeltanoService

**Pipeline orchestration and execution service**

```python
class FlextMeltanoService(s):
    """Service for pipeline orchestration and execution."""
```

#### Pipeline Management

##### create_pipeline(settings)

**Create a new pipeline configuration**

```python
def create_pipeline(
    self, settings: FlextMeltanoModels.PipelineConfig
) -> p.Result[FlextMeltanoModels.Pipeline]:
    """Create a new pipeline configuration.

    Args:
        settings: Pipeline configuration

    Returns:
        r containing created pipeline
    """
```

##### execute_pipeline(pipeline_name, options=None)

**Execute a configured pipeline**

```python
def execute_pipeline(
    self, pipeline_name: str, options: FlextMeltanoModels.PipelineOptions | None = None
) -> p.Result[FlextMeltanoModels.PipelineResult]:
    """Execute a configured pipeline.

    Args:
        pipeline_name: Name of the pipeline to execute
        options: Execution options

    Returns:
        r containing execution result
    """
```

##### monitor_pipeline(pipeline_id)

**Monitor pipeline execution**

```python
def monitor_pipeline(
    self, pipeline_id: str
) -> p.Result[FlextMeltanoModels.PipelineStatus]:
    """Monitor pipeline execution status.

    Args:
        pipeline_id: ID of the pipeline to monitor

    Returns:
        r containing pipeline status
    """
```

### FlextMeltanoExecutor

**Advanced pipeline execution engine**

```python
class FlextMeltanoExecutor(s):
    """Advanced pipeline execution engine with orchestration."""
```

#### Advanced Execution

##### execute_parallel_pipelines(pipelines)

**Execute multiple pipelines in parallel**

```python
def execute_parallel_pipelines(
    self, pipelines: Sequence[FlextMeltanoModels.PipelineConfig]
) -> p.Result[Sequence[FlextMeltanoModels.PipelineResult]]:
    """Execute multiple pipelines in parallel.

    Args:
        pipelines: List of pipeline configurations

    Returns:
        r containing list of execution results
    """
```

##### execute_conditional_pipeline(condition, pipeline)

**Execute pipeline based on condition**

```python
def execute_conditional_pipeline(
    self,
    condition: FlextMeltanoModels.Condition,
    pipeline: FlextMeltanoModels.PipelineConfig,
) -> p.Result[FlextMeltanoModels.PipelineResult | None]:
    """Execute pipeline based on condition evaluation.

    Args:
        condition: Condition to evaluate
        pipeline: Pipeline to execute if condition is met

    Returns:
        r containing execution result or None
    """
```

______________________________________________________________________

## 📁 Project Management

### FlextProjectService

**Meltano project management service**

```python
class FlextProjectService(s):
    """Service for Meltano project management."""
```

#### Project Operations

##### create_project(project_config)

**Create a new Meltano project**

```python
def create_project(
    self, project_config: FlextMeltanoModels.ProjectConfig
) -> p.Result[FlextMeltanoModels.Project]:
    """Create a new Meltano project.

    Args:
        project_config: Project configuration

    Returns:
        r containing created project
    """
```

##### validate_project(project_root)

**Validate Meltano project structure**

```python
def validate_project(
    self, project_root: Path | str
) -> p.Result[FlextMeltanoModels.ProjectValidation]:
    """Validate Meltano project structure and configuration.

    Args:
        project_root: Path to project root directory

    Returns:
        r containing validation result
    """
```

##### get_project_info(project_root)

**Get project information and metadata**

```python
def get_project_info(
    self, project_root: Path | str
) -> p.Result[FlextMeltanoModels.ProjectInfo]:
    """Get project information and metadata.

    Args:
        project_root: Path to project root directory

    Returns:
        r containing project information
    """
```

### FlextMeltanoProject

**Meltano project representation**

```python
class FlextMeltanoProject:
    """Representation of a Meltano project."""
```

#### Project Properties

#### r

**Project root directory path**

```python
@property
def root_path(self) -> Path:
    """Get project root directory path."""
```

##### meltano_yml_path

**Path to meltano.yml configuration file**

```python
@property
def meltano_yml_path(self) -> Path:
    """Get path to meltano.yml configuration file."""
```

##### plugins

**List of configured plugins**

```python
@property
def plugins(self) -> Sequence[FlextMeltanoModels.PluginInfo]:
    """Get list of configured plugins."""
```

______________________________________________________________________

## 🔧 Configuration Management

### FlextMeltanoSettings

**Meltano configuration management**

```python
class FlextMeltanoSettings(FlextSettings):
    """Meltano-specific configuration management."""
```

#### Configuration Sections

##### project_config

**Project-level configuration**

```python
@property
def project_config(self) -> FlextMeltanoModels.ProjectConfig:
    """Get project-level configuration."""
```

##### plugin_configs

**Plugin-specific configurations**

```python
@property
def plugin_configs(self) -> Mapping[str, t.Dict]:
    """Get plugin-specific configurations."""
```

##### pipeline_configs

**Pipeline execution configurations**

```python
@property
def pipeline_configs(self) -> Mapping[str, FlextMeltanoModels.PipelineConfig]:
    """Get pipeline execution configurations."""
```

______________________________________________________________________

## 📊 Models and Types

### Core Models

#### FlextMeltanoModels.Config

**Main configuration model**

```python
class Config(FlextBaseModel):
    """Main configuration model for FLEXT-Meltano."""

    project_root: Path | None = None
    default_environment: str = "dev"
    log_level: str = "INFO"
    plugin_dir: Path | None = None
    state_dir: Path | None = None
```

#### FlextMeltanoModels.PluginInfo

**Plugin information model**

```python
class PluginInfo(FlextBaseModel):
    """Plugin information model."""

    name: str
    namespace: str
    variant: str
    pip_url: str | None = None
    executable: str | None = None
    settings: t.Dict | None = None
    version: str | None = None
```

#### FlextMeltanoModels.PipelineConfig

**Pipeline configuration model**

```python
class PipelineConfig(FlextBaseModel):
    """Pipeline configuration model."""

    name: str
    tap: str
    target: str | None = None
    transformer: str | None = None
    schedule: str | None = None
    incremental: bool = False
    parallelism: int = 1
```

### Execution Models

#### FlextMeltanoModels.TapExecutionResult

**Tap execution result model**

```python
class TapExecutionResult(FlextBaseModel):
    """Tap execution result model."""

    success: bool
    records_extracted: int = 0
    streams_discovered: int = 0
    execution_time: float = 0.0
    state: t.Dict | None = None
    error: str | None = None
```

#### FlextMeltanoModels.TargetExecutionResult

**Target execution result model**

```python
class TargetExecutionResult(FlextBaseModel):
    """Target execution result model."""

    success: bool
    records_loaded: int = 0
    execution_time: float = 0.0
    error: str | None = None
```

#### FlextMeltanoModels.PipelineResult

**Pipeline execution result model**

```python
class PipelineResult(FlextBaseModel):
    """Pipeline execution result model."""

    success: bool
    tap_result: TapExecutionResult | None = None
    target_result: TargetExecutionResult | None = None
    transformer_result: t.Dict | None = None
    execution_time: float = 0.0
    error: str | None = None
```

______________________________________________________________________

## 🛡️ Exception Hierarchy

### FlextMeltanoException

**Base exception for FLEXT-Meltano**

```python
class FlextMeltanoException(FlextException):
    """Base exception for FLEXT-Meltano errors."""
```

### Specific Exceptions

#### FlextMeltanoPluginException

**Plugin-related errors**

```python
class FlextMeltanoPluginException(FlextMeltanoException):
    """Exception raised for plugin-related errors."""
```

#### FlextMeltanoPipelineException

**Pipeline execution errors**

```python
class FlextMeltanoPipelineException(FlextMeltanoException):
    """Exception raised for pipeline execution errors."""
```

#### FlextMeltanoConfigurationException

**Configuration-related errors**

```python
class FlextMeltanoConfigurationException(FlextMeltanoException):
    """Exception raised for configuration errors."""
```

______________________________________________________________________

## 🔄 Integration Examples

### Basic Pipeline Execution

```python
from flext_meltano import FlextMeltanoService

# Initialize service
service = FlextMeltanoService()

# Execute tap
tap_result = service.execute_tap(
    tap_name="tap-csv", settings={"files": ["data/sales.csv"]}
)

if tap_result.success:
    records = tap_result.unwrap().records

    # Execute target
    target_result = service.execute_target(
        target_name="target-jsonl",
        records=records,
        settings={"destination_path": "output/sales.jsonl"},
    )
```

### Advanced Pipeline Orchestration

```python
from flext_meltano import FlextMeltanoExecutor

# Initialize executor
executor = FlextMeltanoExecutor()

# Execute pipeline with advanced options
result = executor.execute_pipeline_advanced(
    FlextMeltanoModels.PipelineOptions(
        tap="tap-salesforce",
        target="target-snowflake",
        incremental=True,
        parallelism=4,
        state_file="state/salesforce_state.json",
    )
)

if result.success:
    print(f"Pipeline completed in {result.unwrap().execution_time}s")
```

### Plugin Management

```python
from flext_meltano import FlextPluginService

# Initialize plugin service
plugin_service = FlextPluginService()

# Install plugin
install_result = plugin_service.install_plugin("tap-gitlab")
if install_result.success:
    print(f"Installed {install_result.unwrap().plugin_name}")

# List available taps
taps = plugin_service.discover_plugins()
available_taps = [p for p in taps.unwrap() if p.plugin_type == "tap"]
```

______________________________________________________________________

**Document Status**: ✅ Complete | **Last Reviewed**: 2026-04-14

## Related Documentation

**Within Project**:

- [Getting Started](getting-started.md) - Installation and basic usage
- [Architecture](architecture.md) - Architecture and design patterns
- [Examples](../examples/) - Working code examples

**Across Projects**:

- [flext-core Foundation](https://github.com/organization/flext/tree/main/flext-core/docs/api-reference/foundation.md) - Core APIs and patterns
- [flext-plugin API](https://github.com/organization/flext/tree/main/flext-plugin/docs/api-reference.md) - Plugin API reference
- [flext-quality Automation](https://github.com/organization/flext/tree/main/flext-quality/AGENTS.md) - Quality analysis and automation

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
