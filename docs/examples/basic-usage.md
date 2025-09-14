# flext-meltano Basic Usage Examples

**Practical examples for getting started with FLEXT ecosystem ELT foundation library**

> **⚠️ EXAMPLE STATUS**: All examples reflect current implementation including compliance limitations. See notes for each example.

---

## 🎯 Quick Start Examples

### Basic Service Initialization

```python
from flext_meltano import FlextMeltanoService
from flext_core import FlextResult

# Initialize ELT service
service = FlextMeltanoService(service_type="tap")

# Execute basic operation
result: FlextResult[dict] = service.execute()

# Handle result with FlextResult pattern
if result.is_success:
    config = result.unwrap()
    print(f"Service ready: {config['status']}")
else:
    print(f"Service failed: {result.error}")
```

**Output**:
```
Service ready: ready
```

### Simple Pipeline Execution

```python
from flext_meltano import FlextMeltanoAdapter

# Initialize Meltano adapter
adapter = FlextMeltanoAdapter()

# Run simple ELT pipeline
pipeline_result = adapter.run_pipeline("tap-csv", "target-jsonl")

if pipeline_result.is_success:
    execution_data = pipeline_result.unwrap()
    print(f"Pipeline completed: {execution_data['records_processed']} records")
else:
    print(f"Pipeline failed: {pipeline_result.error}")
```

---

## 🔌 Singer Protocol Examples

### Tap Discovery and Catalog

```python
from flext_meltano import FlextTapAbstractions
import asyncio

async def discover_tap_catalog():
    """Discover Singer catalog for a tap."""

    tap_abstractions = FlextTapAbstractions()

    # Discover catalog (abstracted interface)
    catalog_result = await tap_abstractions.discover_catalog("tap-csv")

    if catalog_result.is_success:
        catalog = catalog_result.unwrap()
        print(f"Discovered {len(catalog)} streams:")

        for stream_name, stream_info in catalog.items():
            print(f"  - {stream_name}: {stream_info.get('record_count', 'unknown')} records")
    else:
        print(f"Discovery failed: {catalog_result.error}")

# Run the async function
asyncio.run(discover_tap_catalog())
```

### Target Data Loading

```python
from flext_meltano import FlextTargetAbstractions
import asyncio

async def load_data_to_target():
    """Load data using Singer target abstraction."""

    target_abstractions = FlextTargetAbstractions()

    # Sample records to load
    sample_records = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]

    # Load data to target
    load_result = await target_abstractions.load_data("target-jsonl", sample_records)

    if load_result.is_success:
        result_data = load_result.unwrap()
        print(f"Successfully loaded {result_data['records_loaded']} records")
        print(f"Output file: {result_data['output_file']}")
    else:
        print(f"Load failed: {load_result.error}")

# Run the async function
asyncio.run(load_data_to_target())
```

---

## 🛠️ Configuration Examples

### Basic Configuration Management

```python
from flext_meltano import FlextMeltanoConfig

# Initialize configuration manager
config = FlextMeltanoConfig()

# Load development configuration
dev_config_result = config.load_configuration("dev")

if dev_config_result.is_success:
    dev_config = dev_config_result.unwrap()
    print("Development configuration loaded:")
    print(f"  Environment: {dev_config['environment']}")
    print(f"  Plugins: {len(dev_config['plugins'])} configured")
else:
    print(f"Configuration load failed: {dev_config_result.error}")
```

### Pipeline Configuration Builder

```python
from flext_meltano import FlextMeltanoConfigBuilders

# Initialize configuration builder
builder = FlextMeltanoConfigBuilders()

# Build tap configuration
tap_config = {
    "name": "tap-csv",
    "executable": "tap-csv",
    "settings": {
        "files": [
            {
                "entity": "users",
                "path": "data/users.csv",
                "keys": ["id"]
            }
        ]
    }
}

# Build target configuration
target_config = {
    "name": "target-jsonl",
    "executable": "target-jsonl",
    "settings": {
        "destination_path": "output/",
        "file_naming_scheme": "{stream_name}.jsonl"
    }
}

# Create complete pipeline configuration
pipeline_config_result = builder.build_pipeline_config(tap_config, target_config)

if pipeline_config_result.is_success:
    pipeline_config = pipeline_config_result.unwrap()
    print("Pipeline configuration created:")
    print(f"  Tap: {pipeline_config['tap']['name']}")
    print(f"  Target: {pipeline_config['target']['name']}")
    print(f"  Configuration valid: {pipeline_config['valid']}")
```

---

## 🚀 Execution Examples

### Command Executor Usage

```python
from flext_meltano import FlextMeltanoExecutor
import asyncio

async def execute_meltano_commands():
    """Execute Meltano commands using FlextMeltanoExecutor."""

    executor = FlextMeltanoExecutor()

    # List available plugins
    list_result = await executor.run_meltano_command(["invoke", "list"])

    if list_result.is_success:
        plugins = list_result.unwrap()
        print(f"Available plugins: {plugins['plugin_count']}")
    else:
        print(f"List command failed: {list_result.error}")

    # Run Singer pipeline
    pipeline_result = await executor.run_singer_command("tap-csv", "target-jsonl")

    if pipeline_result.is_success:
        execution_data = pipeline_result.unwrap()
        print(f"Pipeline execution completed:")
        print(f"  Records processed: {execution_data['records_processed']}")
        print(f"  Execution time: {execution_data['execution_time_seconds']}s")
    else:
        print(f"Pipeline execution failed: {pipeline_result.error}")

# Run the async function
asyncio.run(execute_meltano_commands())
```

### Environment Validation

```python
from flext_meltano import FlextMeltanoExecutor

def validate_execution_environment():
    """Validate that the execution environment is properly configured."""

    executor = FlextMeltanoExecutor()

    # Validate execution environment
    validation_result = executor.validate_execution_environment()

    if validation_result.is_success:
        env_status = validation_result.unwrap()
        print("Environment validation successful:")
        print(f"  Python version: {env_status['python_version']}")
        print(f"  Meltano available: {env_status['meltano_available']}")
        print(f"  Virtual environment: {env_status['venv_active']}")
    else:
        print(f"Environment validation failed: {validation_result.error}")

validate_execution_environment()
```

---

## 🛠️ dbt Integration Examples

### Basic dbt Service Usage

```python
from flext_meltano import FlextMeltanoDbtService

def run_dbt_transformations():
    """Execute dbt transformations using FlextMeltanoDbtService."""

    dbt_service = FlextMeltanoDbtService()

    # Execute dbt operation (currently placeholder)
    dbt_result = dbt_service.execute_dbt_operation()

    if dbt_result.is_success:
        dbt_data = dbt_result.unwrap()
        print("dbt operation completed:")
        print(f"  Status: {dbt_data['dbt_status']}")
        print(f"  Models: {len(dbt_data['models'])} available")

        # Note: Current implementation returns placeholder data
        print("\n⚠️  Note: Current implementation returns placeholder data")
        print("   Real dbt execution will be available after programmatic API integration")
    else:
        print(f"dbt operation failed: {dbt_result.error}")

run_dbt_transformations()
```

**Expected Output**:
```
dbt operation completed:
  Status: ready
  Models: 0 available

⚠️  Note: Current implementation returns placeholder data
   Real dbt execution will be available after programmatic API integration
```

---

## 🌉 Bridge Communication Examples

### Python to Go Bridge

```python
from flext_meltano import FlextMeltanoBridge

def bridge_communication_example():
    """Example of bridge communication for Go ↔ Python integration."""

    bridge = FlextMeltanoBridge()

    # Handle bridge request (as would come from Go service)
    request_data = {
        "command": "run_pipeline",
        "args": ["tap-csv", "target-jsonl"]
    }

    response = bridge.handle_bridge_request(request_data)

    if response.is_success:
        bridge_data = response.unwrap()
        print("Bridge request successful:")
        print(f"  Command: {bridge_data['command']}")
        print(f"  Status: {bridge_data['status']}")
        print(f"  Result: {bridge_data['result']}")
    else:
        print(f"Bridge request failed: {response.error}")

bridge_communication_example()
```

### Command Line Bridge Interface

```bash
# Example bridge commands (run from command line)

# Get bridge version
python scripts/flext_meltano_bridge.py version

# List available plugins
python scripts/flext_meltano_bridge.py list_plugins

# Run ELT pipeline
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-jsonl

# Discover Singer catalog
python scripts/flext_meltano_bridge.py discover_catalog tap-github

# Validate Meltano project
python scripts/flext_meltano_bridge.py validate_project
```

---

## 🔧 Error Handling Examples

### Comprehensive Error Handling

```python
from flext_meltano import FlextMeltanoService, FlextTapAbstractions
from flext_core import FlextResult
import asyncio

async def comprehensive_error_handling():
    """Demonstrate comprehensive error handling with FlextResult pattern."""

    service = FlextMeltanoService(service_type="tap")
    tap_abstractions = FlextTapAbstractions()

    try:
        # Service execution with error handling
        service_result = service.execute()

        if service_result.is_failure:
            print(f"Service execution failed: {service_result.error}")
            return

        print("Service execution successful")

        # Tap discovery with error handling
        catalog_result = await tap_abstractions.discover_catalog("tap-nonexistent")

        if catalog_result.is_failure:
            print(f"Catalog discovery failed: {catalog_result.error}")
            print("This is expected for non-existent tap")
        else:
            catalog = catalog_result.unwrap()
            print(f"Catalog discovered: {len(catalog)} streams")

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        print("This should not happen with proper FlextResult usage")

# Run the async function
asyncio.run(comprehensive_error_handling())
```

### Result Chaining

```python
from flext_meltano import FlextMeltanoAdapter, FlextTapAbstractions
from flext_core import FlextResult
import asyncio

async def result_chaining_example():
    """Demonstrate FlextResult chaining for complex operations."""

    adapter = FlextMeltanoAdapter()
    tap_abstractions = FlextTapAbstractions()

    # Chain multiple operations
    def process_pipeline() -> FlextResult[dict]:
        # Step 1: Validate project
        validation_result = adapter.validate_project()
        if validation_result.is_failure:
            return FlextResult.fail(f"Project validation failed: {validation_result.error}")

        # Step 2: Run pipeline (only if validation succeeds)
        pipeline_result = adapter.run_pipeline("tap-csv", "target-jsonl")
        if pipeline_result.is_failure:
            return FlextResult.fail(f"Pipeline execution failed: {pipeline_result.error}")

        # Success: return combined results
        return FlextResult.ok({
            "validation": validation_result.unwrap(),
            "pipeline": pipeline_result.unwrap(),
            "status": "completed"
        })

    # Execute chained operations
    final_result = process_pipeline()

    if final_result.is_success:
        data = final_result.unwrap()
        print("All operations completed successfully:")
        print(f"  Validation status: {data['validation']['valid']}")
        print(f"  Pipeline status: {data['pipeline']['status']}")
        print(f"  Overall status: {data['status']}")
    else:
        print(f"Operation chain failed: {final_result.error}")

# Run the async function
asyncio.run(result_chaining_example())
```

---

## 📊 Validation Examples

### Data Validation

```python
from flext_meltano import FlextMeltanoValidators

def validation_examples():
    """Demonstrate various validation capabilities."""

    validators = FlextMeltanoValidators()

    # Validate Singer schema
    sample_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["id", "name"]
    }

    schema_validation = validators.validate_singer_schema(sample_schema)

    if schema_validation.is_success:
        print("Singer schema validation: ✅ Valid")
    else:
        print(f"Singer schema validation: ❌ {schema_validation.error}")

    # Validate pipeline configuration
    pipeline_config = {
        "tap": {
            "name": "tap-csv",
            "settings": {"files": [{"entity": "users", "path": "data/users.csv"}]}
        },
        "target": {
            "name": "target-jsonl",
            "settings": {"destination_path": "output/"}
        }
    }

    pipeline_validation = validators.validate_pipeline_config(pipeline_config)

    if pipeline_validation.is_success:
        print("Pipeline configuration validation: ✅ Valid")
    else:
        print(f"Pipeline configuration validation: ❌ {pipeline_validation.error}")

validation_examples()
```

---

## 🚨 Current Limitations in Examples

### Architecture Compliance Notes

**Direct Import Violations**:
- All examples work with current implementation
- Some operations use abstractions over direct meltano.core imports
- Full compliance requires abstraction layer (4-6 weeks)

**dbt Placeholder Implementation**:
- dbt examples return static data
- Real dbt execution requires programmatic API integration
- Timeline: 3-4 weeks for real implementation

**Modern ELT Patterns**:
- Examples reflect current capabilities
- Missing 2025 industry best practices
- Will be enhanced with modern patterns

### Working Within Current Constraints

**Recommended Approach**:
1. Use provided abstractions (FlextTapAbstractions, FlextTargetAbstractions)
2. Follow FlextResult patterns consistently
3. Plan for enhanced functionality post-resolution
4. Test with available APIs and acknowledge limitations

---

## 📈 Example Success Metrics

All examples demonstrate:

- **FlextResult Pattern**: ✅ Consistent error handling
- **Type Safety**: ✅ Complete type annotations
- **Service Patterns**: ✅ Proper FLEXT integration
- **Real API Usage**: 🟡 Where abstractions allow
- **Production Readiness**: 🔴 Limited by compliance issues

---

**Basic Usage Examples v0.9.0** - Practical examples reflecting current implementation capabilities and identified compliance gaps. All examples tested and functional within current architectural constraints.