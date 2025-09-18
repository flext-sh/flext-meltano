# flext-meltano Configuration

**Configuration management for FLEXT ecosystem ELT foundation library**

> **⚠️ COMPLIANCE NOTE**: Current configuration patterns require abstraction layer for full FLEXT compliance due to direct meltano.core usage.

---

## 🎯 Configuration Overview

flext-meltano provides enterprise-grade configuration management for ELT operations, supporting:

- **Meltano Project Configuration** - Complete meltano.yml management
- **Singer Plugin Configuration** - Tap and target settings validation
- **dbt Project Configuration** - Model and transformation settings
- **Environment Management** - Development, staging, and production configurations
- **FLEXT Integration** - flext-core pattern compliance and validation

---

## 📋 Environment Setup

### Required Environment Variables

```bash
# Meltano Configuration
export MELTANO_ENVIRONMENT=dev
export MELTANO_PROJECT_ROOT=/path/to/project
export MELTANO_DATABASE_URI=sqlite:///meltano.db

# FLEXT Ecosystem Integration
export PYTHONPATH=/path/to/project/src:$PYTHONPATH
export FLEXT_LOG_LEVEL=INFO
export FLEXT_ENVIRONMENT=development

# Singer Protocol Configuration
export SINGER_CATALOG_FORMAT=json
export SINGER_STREAM_BUFFER_SIZE=8192

# dbt Configuration
export DBT_PROFILES_DIR=/path/to/profiles
export DBT_PROJECT_DIR=/path/to/transform
```

### Virtual Environment Setup

```bash
# Use FLEXT workspace virtual environment
cd /home/marlonsc/flext
source .venv/bin/activate
cd flext-meltano

# Install dependencies
poetry install --with dev,test
```

---

## ⚙️ Meltano Project Configuration

### Basic meltano.yml Structure

```yaml
version: 1
default_environment: dev

project_id: flext-elt-pipeline
environments:
  - name: dev
  - name: prod

extractors:
  - name: tap-csv
    executable: tap-csv
    settings:
      files:
        - entity: users
          path: data/users.csv
          keys: [id]

loaders:
  - name: target-jsonl
    executable: target-jsonl
    settings:
      destination_path: output

transforms:
  - name: dbt-transform
    executable: dbt-core
    settings:
      project_dir: transform/
      profiles_dir: profiles/
```

### Configuration Validation

```python
from flext_meltano import FlextMeltanoConfig
from flext_core import FlextResult

config = FlextMeltanoConfig()
validation_result: FlextResult[bool] = config.validate_meltano_config()

if validation_result.is_success:
    print("Meltano configuration is valid")
else:
    print(f"Configuration error: {validation_result.error}")
```

---

## 🔌 Singer Plugin Configuration

### Tap Configuration

```python
from flext_meltano import TapConfig, FlextMeltanoConfigBuilders

# Create tap configuration
tap_config = TapConfig(
    name="tap-csv",
    executable="tap-csv",
    settings={
        "files": [
            {
                "entity": "users",
                "path": "data/users.csv",
                "keys": ["id"]
            }
        ]
    }
)

# Build pipeline configuration
builder = FlextMeltanoConfigBuilders()
pipeline_config = builder.build_tap_config(tap_config.dict())
```

### Target Configuration

```python
from flext_meltano import FlextMeltanoConfigBuilders

target_settings = {
    "destination_path": "output/",
    "file_naming_scheme": "{stream_name}.jsonl"
}

builder = FlextMeltanoConfigBuilders()
target_config = builder.build_target_config(target_settings)
```

### Singer Catalog Configuration

```python
from flext_meltano import StreamDefinition

# Define stream configuration
stream = StreamDefinition(
    name="users",
    schema={
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"}
        }
    },
    metadata={
        "selected": True,
        "replication-method": "INCREMENTAL",
        "replication-key": "updated_at"
    }
)
```

---

## 🛠️ dbt Configuration

### dbt Project Structure

```
transform/
├── dbt_project.yml
├── profiles/
│   └── profiles.yml
├── models/
│   ├── staging/
│   │   └── stg_users.sql
│   └── marts/
│       └── dim_users.sql
├── tests/
│   └── assert_user_id_unique.sql
└── macros/
    └── custom_macros.sql
```

### dbt Project Configuration (dbt_project.yml)

```yaml
name: "flext_transform"
version: "1.0.0"

profile: "flext_profile"

model-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  flext_transform:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

### dbt Service Configuration

```python
from flext_meltano import FlextMeltanoDbtService

# Note: Current implementation is placeholder
dbt_service = FlextMeltanoDbtService()
result = dbt_service.execute_dbt_operation()

# Returns placeholder data:
# {"dbt_status": "ready", "models": []}
```

---

## 🏗️ Pipeline Configuration

### Complete ELT Pipeline

```python
from flext_meltano import FlextMeltanoService, FlextMeltanoConfigBuilders

# Build complete pipeline configuration
builder = FlextMeltanoConfigBuilders()

# Tap configuration
tap_config = {
    "name": "tap-csv",
    "settings": {"files": [{"entity": "users", "path": "data/users.csv"}]}
}

# Target configuration
target_config = {
    "name": "target-jsonl",
    "settings": {"destination_path": "output/"}
}

# Build pipeline
pipeline_config = builder.build_pipeline_config(tap_config, target_config)

# Initialize service
service = FlextMeltanoService(service_type="pipeline")
execution_result = service.execute()
```

### Configuration Validation

```python
from flext_meltano import FlextMeltanoValidators

validators = FlextMeltanoValidators()

# Validate complete pipeline
validation_result = validators.validate_pipeline_config({
    "tap": tap_config,
    "target": target_config,
    "transform": dbt_config
})

if validation_result.is_failure:
    print(f"Pipeline validation failed: {validation_result.error}")
```

---

## 🌍 Environment Management

### Development Environment

```yaml
# meltano.yml - development settings
environments:
  - name: dev
    config:
      plugins:
        extractors:
          - name: tap-csv
            settings:
              files:
                - entity: users
                  path: data/sample_users.csv
        loaders:
          - name: target-jsonl
            settings:
              destination_path: dev_output/
```

### Production Environment

```yaml
# meltano.yml - production settings
environments:
  - name: prod
    config:
      plugins:
        extractors:
          - name: tap-csv
            settings:
              files:
                - entity: users
                  path: /data/production/users.csv
        loaders:
          - name: target-jsonl
            settings:
              destination_path: /output/production/
```

### Environment Switching

```python
from flext_meltano import FlextMeltanoConfig

config = FlextMeltanoConfig()

# Load development configuration
dev_config = config.load_configuration("dev")

# Load production configuration
prod_config = config.load_configuration("prod")
```

---

## 🔧 Configuration File Management

### Reading Configuration Files

```python
from flext_meltano import FlextMeltanoFileManagers

file_manager = FlextMeltanoFileManagers()

# Read meltano.yml
meltano_config = file_manager.read_meltano_config()

# Read Singer catalog
catalog_result = file_manager.read_singer_catalog("catalog.json")

# Read dbt profiles
dbt_profiles = file_manager.read_dbt_profiles()
```

### Writing Configuration Files

```python
# Write Singer catalog
catalog_data = {
    "streams": [
        {
            "tap_stream_id": "users",
            "schema": {...},
            "metadata": [...]
        }
    ]
}

write_result = file_manager.write_singer_catalog(catalog_data, "output/catalog.json")
```

### Configuration Backup

```python
# Backup critical configuration files
backup_result = file_manager.backup_project_files()

if backup_result.is_success:
    backup_files = backup_result.unwrap()
    print(f"Backed up {len(backup_files)} configuration files")
```

---

## 🔍 Configuration Validation

### Schema Validation

```python
from flext_meltano import FlextMeltanoValidators

validators = FlextMeltanoValidators()

# Validate Singer schema
schema_validation = validators.validate_singer_schema({
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"}
    }
})

# Validate dbt models
model_validation = validators.validate_dbt_models([
    {"name": "stg_users", "path": "models/staging/stg_users.sql"},
    {"name": "dim_users", "path": "models/marts/dim_users.sql"}
])
```

### Runtime Validation

```python
from flext_meltano import FlextMeltanoExecutor

executor = FlextMeltanoExecutor()

# Validate execution environment
env_validation = executor.validate_execution_environment()

if env_validation.is_failure:
    print(f"Environment validation failed: {env_validation.error}")
```

---

## 🚨 Current Limitations

### Architecture Compliance Issues

1. **Direct Import Violations**: Configuration system uses direct meltano.core imports
2. **Abstraction Layer Missing**: Requires wrapper implementation for full FLEXT compliance
3. **dbt Integration**: Current configuration returns placeholder data

### Configuration Restrictions

Due to compliance issues:

- **Production Use**: Not recommended until abstraction layer implemented
- **Full Configuration**: Limited by direct library import violations
- **Modern Patterns**: Missing 2025 ELT configuration best practices

### Workarounds

1. **Use Abstractions**: Leverage existing FlextMeltanoConfig where possible
2. **Monitor Progress**: Track abstraction layer implementation
3. **Plan Migration**: Prepare for wrapper layer adoption
4. **Validate Patterns**: Use FlextResult patterns consistently

---

## 🔄 Configuration Migration

### Resolution Timeline

- **Phase 1**: Abstraction layer for meltano.core imports (4-6 weeks)
- **Phase 2**: Modern configuration patterns integration (3-4 weeks)
- **Phase 3**: Production-ready configuration management (2 weeks)

### Migration Planning

1. **Current State**: Document existing configuration patterns
2. **Target Architecture**: Plan abstraction layer implementation
3. **Transition Strategy**: Gradual migration with backward compatibility
4. **Validation**: Ensure all configuration patterns maintain functionality

---

**Configuration Guide v0.9.9** - Reflects current configuration capabilities with identified compliance gaps requiring systematic resolution for full FLEXT ecosystem integration.
