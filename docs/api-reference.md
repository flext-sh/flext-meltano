# flext-meltano API Reference

**Complete API documentation for flext-meltano v0.9.9**

**Last Updated**: 2025-09-17

> **⚠️ STATUS**: Development phase - Foundation patterns implemented, direct imports require abstraction

---

## 🎯 Core Services

### FlextMeltanoService

**Primary ELT orchestration service**

```python
from flext_meltano import FlextMeltanoService
from flext_core import FlextResult

service = FlextMeltanoService(service_type="tap")
result: FlextResult[dict] = service.execute()
```

**Methods**:

- `execute() -> FlextResult[dict]` - Execute configured ELT operation
- `validate_configuration() -> FlextResult[bool]` - Validate service configuration

### FlextMeltanoAdapter

**Meltano Core integration adapter**

```python
from flext_meltano import FlextMeltanoAdapter

adapter = FlextMeltanoAdapter()
result: FlextResult[dict] = adapter.run_pipeline("tap-csv", "target-jsonl")
```

**Methods**:

- `run_pipeline(tap: str, target: str) -> FlextResult[dict]` - Execute ELT pipeline
- `validate_project() -> FlextResult[bool]` - Validate Meltano project configuration
- `list_plugins() -> FlextResult[list]` - List available Meltano plugins

---

## 🔌 Singer Protocol Abstractions

### FlextTapAbstractions

**Singer tap operations wrapper**

```python
from flext_meltano import FlextTapAbstractions

tap_abstractions = FlextTapAbstractions()
catalog_result: FlextResult[dict] = await tap_abstractions.discover_catalog("tap-csv")
```

**Methods**:

- `discover_catalog(tap_name: str) -> FlextResult[dict]` - Discover Singer catalog
- `extract_data(tap_name: str, config: dict) -> FlextResult[list]` - Extract data records
- `validate_tap_config(config: dict) -> FlextResult[bool]` - Validate tap configuration

### FlextTargetAbstractions

**Singer target operations wrapper**

```python
from flext_meltano import FlextTargetAbstractions

target_abstractions = FlextTargetAbstractions()
result: FlextResult[dict] = await target_abstractions.load_data("target-jsonl", records)
```

**Methods**:

- `load_data(target_name: str, records: list) -> FlextResult[dict]` - Load data records
- `validate_target_config(config: dict) -> FlextResult[bool]` - Validate target configuration

---

## 🛠️ Transformation Services

### FlextMeltanoDbtService

**dbt transformation operations**

```python
from flext_meltano import FlextMeltanoDbtService

dbt_service = FlextMeltanoDbtService()
result: FlextResult[dict] = dbt_service.execute_dbt_operation()
```

**Current Status**: Placeholder implementation returning static data

**Methods**:

- `execute_dbt_operation() -> FlextResult[dict]` - Execute dbt transformations (placeholder)
- `validate_dbt_project() -> FlextResult[bool]` - Validate dbt project structure

---

## ⚙️ Configuration Management

### FlextMeltanoConfig

**ELT configuration management**

```python
from flext_meltano import FlextMeltanoConfig

config = FlextMeltanoConfig()
result: FlextResult[dict] = config.load_configuration("production")
```

**Methods**:

- `load_configuration(environment: str) -> FlextResult[dict]` - Load environment configuration
- `validate_config() -> FlextResult[bool]` - Validate configuration structure

### FlextMeltanoConfigBuilders

**Pipeline configuration builders**

```python
from flext_meltano import FlextMeltanoConfigBuilders

builder = FlextMeltanoConfigBuilders()
pipeline_config: FlextResult[dict] = builder.build_pipeline_config(tap_config, target_config)
```

**Methods**:

- `build_pipeline_config(tap: dict, target: dict) -> FlextResult[dict]` - Build ELT pipeline configuration
- `build_tap_config(settings: dict) -> FlextResult[dict]` - Build tap-specific configuration
- `build_target_config(settings: dict) -> FlextResult[dict]` - Build target-specific configuration

---

## 🚀 Execution Layer

### FlextMeltanoExecutor

**Command orchestration and execution**

```python
from flext_meltano import FlextMeltanoExecutor

executor = FlextMeltanoExecutor()
result: FlextResult[dict] = await executor.run_meltano_command(["install"])
```

**Methods**:

- `run_meltano_command(args: list) -> FlextResult[dict]` - Execute Meltano command
- `run_singer_command(tap: str, target: str) -> FlextResult[dict]` - Execute Singer pipeline
- `validate_execution_environment() -> FlextResult[bool]` - Validate execution environment

### FlextMeltanoBridge

**Go ↔ Python bridge communication**

```python
from flext_meltano import FlextMeltanoBridge

bridge = FlextMeltanoBridge()
response: FlextResult[dict] = bridge.handle_bridge_request(request_data)
```

**Bridge Operations**:

- `version` - Get bridge version information
- `list_plugins` - List available ELT plugins
- `run_pipeline` - Execute ELT pipeline
- `discover_catalog` - Singer catalog discovery
- `validate_project` - Meltano project validation

---

## 📊 Data Types and Protocols

### FlextSingerTypes

**Singer protocol type definitions**

```python
from flext_meltano import FlextSingerTypes

# Singer message types
record_message = FlextSingerTypes.RecordMessage(stream="users", record={"id": 1})
schema_message = FlextSingerTypes.SchemaMessage(stream="users", schema=schema_def)
state_message = FlextSingerTypes.StateMessage(value={"bookmark": "2025-01-01"})
```

### StreamDefinition

**Singer stream configuration**

```python
from flext_meltano import StreamDefinition

stream = StreamDefinition(
    name="users",
    schema={"type": "object", "properties": {...}},
    metadata={"selected": True}
)
```

### TapConfig

**Tap configuration model**

```python
from flext_meltano import TapConfig

config = TapConfig(
    name="tap-csv",
    executable="tap-csv",
    settings={"files": [{"entity": "users", "path": "users.csv"}]}
)
```

---

## 🔧 Utilities and Validators

### FlextMeltanoUtilities

**ELT helper utilities**

```python
from flext_meltano import FlextMeltanoUtilities

utils = FlextMeltanoUtilities()
validation: FlextResult[bool] = utils.validate_singer_catalog(catalog)
```

**Methods**:

- `validate_singer_catalog(catalog: dict) -> FlextResult[bool]` - Validate Singer catalog structure
- `parse_singer_messages(stream: Iterator) -> FlextResult[list]` - Parse Singer message stream
- `format_pipeline_output(result: dict) -> FlextResult[str]` - Format pipeline execution output

### FlextMeltanoValidators

**ELT data validation**

```python
from flext_meltano import FlextMeltanoValidators

validators = FlextMeltanoValidators()
result: FlextResult[bool] = validators.validate_pipeline_config(config)
```

**Methods**:

- `validate_pipeline_config(config: dict) -> FlextResult[bool]` - Validate complete pipeline configuration
- `validate_singer_schema(schema: dict) -> FlextResult[bool]` - Validate Singer schema structure
- `validate_dbt_models(models: list) -> FlextResult[bool]` - Validate dbt model definitions

---

## 📁 File Management

### FlextMeltanoFileManagers

**ELT file operations**

```python
from flext_meltano import FlextMeltanoFileManagers

file_manager = FlextMeltanoFileManagers()
result: FlextResult[str] = file_manager.read_meltano_config()
```

**Methods**:

- `read_meltano_config() -> FlextResult[str]` - Read meltano.yml configuration
- `write_singer_catalog(catalog: dict, path: str) -> FlextResult[bool]` - Write Singer catalog to file
- `backup_project_files() -> FlextResult[list]` - Backup critical project files

---

## 🚨 Error Handling

All flext-meltano operations use the FlextResult pattern for type-safe error handling:

```python
from flext_core import FlextResult

# Success case
result = FlextResult[dict].ok({"status": "success", "records": 100})

# Error case
result = FlextResult[dict].fail("Pipeline execution failed: Invalid configuration")

# Handling results
if result.is_success:
    data = result.unwrap()
    print(f"Operation successful: {data}")
else:
    print(f"Operation failed: {result.error}")
```

---

## 🔗 Integration Patterns

### With flext-core

```python
from flext_core import FlextDomainService, FlextResult
from flext_meltano import FlextMeltanoService

class CustomELTService(FlextDomainService):
    def __init__(self):
        super().__init__()
        self._meltano_service = FlextMeltanoService()

    def process_data(self) -> FlextResult[dict]:
        return self._meltano_service.execute()
```

### With flext-cli

```python
from flext_cli import FlextCliApi
from flext_meltano import FlextMeltanoExecutor

def create_elt_command():
    cli = FlextCliApi()
    executor = FlextMeltanoExecutor()

    # Use flext-cli for command interface
    # Use flext-meltano for ELT operations
```

---

## 📈 Status and Limitations

### Current Compliance Status

| Component                   | Status         | Notes                         |
| --------------------------- | -------------- | ----------------------------- |
| **FlextResult Usage**       | 🟢 Complete    | 600+ usages, 174 methods      |
| **Service Patterns**        | 🟢 Implemented | Proper flext-core inheritance |
| **Architecture Compliance** | 🔴 Blocked     | Direct meltano.core imports   |
| **dbt Integration**         | 🔴 Placeholder | Requires dbt programmatic API |

### Known Limitations

1. **Direct Import Violations**: Lines 17-25 in adapters.py require abstraction layer
2. **dbt Placeholder**: Current implementation returns static data
3. **Modern ELT Patterns**: Missing 2025 industry best practices
4. **Production Readiness**: Limited by compliance violations

### Resolution Timeline

- **Abstraction Layer**: 4-6 weeks for meltano.core wrapper implementation
- **dbt Integration**: 3-4 weeks for dbt programmatic API integration
- **Modern Patterns**: 2-3 weeks for 2025 ELT best practices
- **Total Timeline**: 8-10 weeks for complete compliance

---

**API Reference v0.9.9** - Reflects current implementation with identified compliance gaps requiring systematic resolution for full FLEXT ecosystem integration.
