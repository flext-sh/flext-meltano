# FLEXT Meltano API Reference

Complete API documentation for the FLEXT Meltano enterprise data integration library.

## 📚 API Overview

FLEXT Meltano provides **249 exports** through a comprehensive public interface, organized into logical groups for different use cases.

## 🔑 Core APIs

### Primary Import Pattern

```python
import flext_meltano

# Access all functionality through the main module
# 249 exports available including:
# - Execution functions
# - Base classes
# - Core services
# - Singer SDK re-exports
# - DBT integration
# - Configuration management
```

## 🚀 Execution Layer

### Primary Execution Functions

#### `flext_meltano_execute_job(extractor, loader, **kwargs)`

Execute a complete Meltano pipeline job.

```python
from flext_meltano.flext_meltano_execution import flext_meltano_execute_job

# Execute CSV pipeline
result = flext_meltano_execute_job("tap-csv", "target-csv")

if result.success:
    print(f"Pipeline completed successfully: {result.output}")
    print(f"Return code: {result.returncode}")
else:
    print(f"Pipeline failed: {result.error}")
```

**Parameters:**
- `extractor` (str): Meltano extractor plugin name
- `loader` (str): Meltano loader plugin name
- `**kwargs`: Additional arguments passed to Meltano

**Returns:** `FlextMeltanoResult`

#### `flext_meltano_run_command(args, **kwargs)`

Execute generic Meltano CLI commands.

```python
from flext_meltano.flext_meltano_execution import flext_meltano_run_command

# Get Meltano version
result = flext_meltano_run_command(["--version"])

# List installed plugins
result = flext_meltano_run_command(["invoke", "--list"])

# Run with environment
result = flext_meltano_run_command(["run", "my-job"], env={"MELTANO_ENVIRONMENT": "prod"})
```

**Parameters:**
- `args` (List[str]): Meltano command arguments
- `**kwargs`: Additional subprocess arguments

**Returns:** `FlextMeltanoResult`

### Result Handling

#### `FlextMeltanoResult`

Standard result object for all operations.

```python
from flext_meltano.flext_meltano_execution import FlextMeltanoResult

# Result properties
result.success: bool          # Operation success status
result.output: str           # Command output (stdout)
result.error: str            # Error output (stderr)
result.returncode: int       # Process return code
result.command: str          # Executed command
```

## 🔧 Discovery & Installation

### Plugin Discovery

#### `flext_meltano_discover_catalog(tap_name, **kwargs)`

Discover schema catalog from a tap.

```python
from flext_meltano.flext_meltano_discovery import flext_meltano_discover_catalog

# Discover catalog from tap
catalog = flext_meltano_discover_catalog("tap-csv")
```

#### `flext_meltano_discover_plugins(**kwargs)`

Discover available Meltano plugins.

```python
from flext_meltano.flext_meltano_discovery import flext_meltano_discover_plugins

# Get available plugins
plugins = flext_meltano_discover_plugins()
```

### Plugin Installation

#### `flext_meltano_install_plugin(plugin_type, plugin_name, **kwargs)`

Install and configure Meltano plugins.

```python
from flext_meltano.flext_meltano_installation import flext_meltano_install_plugin

# Install extractor
result = flext_meltano_install_plugin("extractor", "tap-csv")

# Install loader
result = flext_meltano_install_plugin("loader", "target-csv")
```

#### `FlextMeltanoInstaller`

Service class for plugin management.

```python
from flext_meltano.flext_meltano_installation import FlextMeltanoInstaller

installer = FlextMeltanoInstaller()
result = installer.install_plugin("extractor", "tap-postgres")
```

## 🧪 Validation & Testing

### Validation Functions

#### `flext_meltano_validate_project(**kwargs)`

Validate Meltano project configuration.

```python
from flext_meltano.flext_meltano_validation import flext_meltano_validate_project

# Validate current project
result = flext_meltano_validate_project()
```

#### `flext_meltano_test_tap_connection(tap_name, **kwargs)`

Test tap connection and configuration.

```python
from flext_meltano.flext_meltano_validation import flext_meltano_test_tap_connection

# Test tap connection
result = flext_meltano_test_tap_connection("tap-postgres")
```

## 🏗️ Base Classes & Factories

### Base Classes

#### `FlextMeltanoTap`

Base class for Singer tap implementations.

```python
from flext_meltano.base import FlextMeltanoTap

class MyCustomTap(FlextMeltanoTap):
    def execute(self):
        # Custom tap implementation
        pass
```

#### `FlextMeltanoTarget`

Base class for Singer target implementations.

```python
from flext_meltano.base import FlextMeltanoTarget

class MyCustomTarget(FlextMeltanoTarget):
    def execute(self):
        # Custom target implementation
        pass
```

#### `FlextMeltanoDbt`

Base class for DBT integrations.

```python
from flext_meltano.base import FlextMeltanoDbt

dbt_service = FlextMeltanoDbt(project_dir="./dbt")
```

### Factory Functions

#### `create_tap(tap_type, **config)`

Factory function for creating tap instances.

```python
from flext_meltano.base import create_tap

# Create Oracle tap
oracle_tap = create_tap("oracle", host="localhost", database="xe")
```

#### `create_target(target_type, **config)`

Factory function for creating target instances.

```python
from flext_meltano.base import create_target

# Create CSV target
csv_target = create_target("csv", output_dir="./output")
```

#### `create_dbt_service(project_dir)`

Factory function for creating DBT services.

```python
from flext_meltano.base import create_dbt_service

# Create DBT service
dbt = create_dbt_service("./dbt")
result = dbt.run_models()
```

## 🏢 Enterprise Services

### Core Services

#### `FlextMeltanoOrchestrationService`

Pipeline orchestration and management.

```python
from flext_meltano.core import FlextMeltanoOrchestrationService

orchestrator = FlextMeltanoOrchestrationService()
result = orchestrator.execute_pipeline("my-pipeline")
```

#### `FlextMeltanoDbtService`

DBT operations and project management.

```python
from flext_meltano.core import FlextMeltanoDbtService

dbt_service = FlextMeltanoDbtService(project_dir="./dbt")
result = dbt_service.run_models(["model1", "model2"])
```

#### `FlextMeltanoSingerService`

Singer protocol handling and stream management.

```python
from flext_meltano.core import FlextMeltanoSingerService

singer_service = FlextMeltanoSingerService()
streams = singer_service.discover_streams("tap-postgres")
```

## 🌉 Bridge Integration

### CLI Bridge Interface

The bridge script provides a CLI interface for Go service integration:

```bash
# Bridge script usage
python scripts/flext_meltano_bridge.py version
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv
python scripts/flext_meltano_bridge.py add_plugin extractor tap-csv
python scripts/flext_meltano_bridge.py discover tap-postgres
```

### Bridge Operations

Available bridge operations:
- `version`: Get Meltano version
- `run_pipeline <extractor> <loader>`: Execute pipeline
- `add_plugin <type> <name>`: Install plugin
- `discover <tap_name>`: Discover catalog
- `list_plugins`: List installed plugins

## 🎵 Singer SDK Re-exports

FLEXT Meltano re-exports key Singer SDK components:

```python
# Available Singer SDK imports
from flext_meltano import (
    Stream,           # Singer stream class
    Tap,             # Singer tap base class
    Target,          # Singer target base class
    Sink,            # Singer sink base class
    SQLSink,         # SQL-specific sink
    BatchSink,       # Batch processing sink
    PropertiesList,  # Schema properties
    Property,        # Individual property
    th               # Typing helpers
)
```

## 🔧 Configuration Management

### `FlextMeltanoConfig`

Configuration management class.

```python
from flext_meltano.base import FlextMeltanoConfig

config = FlextMeltanoConfig(
    meltano_project_root="./",
    environment="dev"
)
```

## 📊 Error Handling

All FLEXT Meltano operations use the FlextResult pattern from flext-core:

```python
from flext_core import FlextResult
from flext_meltano.flext_meltano_execution import flext_meltano_execute_job

# Standard error handling pattern
result = flext_meltano_execute_job("tap-csv", "target-csv")

if result.success:
    # Handle success case
    data = result.value
else:
    # Handle error case
    error = result.error
    print(f"Operation failed: {error}")
```

## 🧪 Testing Utilities

Testing helpers and utilities:

```python
# Test markers for pytest
pytest -m unit               # Unit tests
pytest -m integration        # Integration tests
pytest -m e2e                # End-to-end tests

# Coverage requirements
pytest --cov=src/flext_meltano --cov-fail-under=90
```

---

*API Reference - Version 2.0.0-enterprise*
*Last Updated: 2025-01-29*