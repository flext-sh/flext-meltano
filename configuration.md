# flext-meltano Configuration

<!-- TOC START -->
- [🎯 Configuration Overview](#configuration-overview)
- [📋 Environment Setup](#environment-setup)
  - [Required Environment Variables](#required-environment-variables)
  - [Virtual Environment Setup](#virtual-environment-setup)
- [⚙️ Meltano Project Configuration](#meltano-project-configuration)
  - [Basic meltano.yml Structure](#basic-meltanoyml-structure)
  - [Configuration Validation](#configuration-validation)
- [🔌 Singer Plugin Configuration](#singer-plugin-configuration)
  - [Tap Configuration](#tap-configuration)
  - [Target Configuration](#target-configuration)
  - [Singer Catalog Configuration](#singer-catalog-configuration)
- [🛠️ dbt Configuration](#dbt-configuration)
  - [dbt Project Structure](#dbt-project-structure)
  - [dbt Project Configuration (dbt_project.yml)](#dbt-project-configuration-dbtprojectyml)
  - [dbt Service Configuration](#dbt-service-configuration)
- [🏗️ Pipeline Configuration](#pipeline-configuration)
  - [Complete ELT Pipeline](#complete-elt-pipeline)
  - [Configuration Validation](#configuration-validation)
- [🌍 Environment Management](#environment-management)
  - [Development Environment](#development-environment)
  - [Production Environment](#production-environment)
  - [Environment Switching](#environment-switching)
- [🔧 Configuration File Management](#configuration-file-management)
  - [Reading Configuration Files](#reading-configuration-files)
  - [Writing Configuration Files](#writing-configuration-files)
  - [Configuration Backup](#configuration-backup)
- [🔍 Configuration Validation](#configuration-validation)
  - [Schema Validation](#schema-validation)
  - [Runtime Validation](#runtime-validation)
- [🚨 Current Limitations](#current-limitations)
  - [Architecture Compliance Issues](#architecture-compliance-issues)
  - [Configuration Restrictions](#configuration-restrictions)
  - [Workarounds](#workarounds)
- [🔄 Configuration Migration](#configuration-migration)
  - [Resolution Timeline](#resolution-timeline)
  - [Migration Planning](#migration-planning)
<!-- TOC END -->

**Configuration management for FLEXT ecosystem ELT foundation library**

> **⚠️ COMPLIANCE NOTE**: Current configuration patterns require abstraction layer for full FLEXT compliance due to direct meltano.core usage.

______________________________________________________________________

## 🎯 Configuration Overview

flext-meltano provides enterprise-grade configuration management for ELT operations, supporting:

- **Meltano Project Configuration** - Complete meltano.yml management
- **Singer Plugin Configuration** - Tap and target settings validation
- **dbt Project Configuration** - Model and transformation settings
- **Environment Management** - Development, staging, and production configurations
- **FLEXT Integration** - flext-core pattern compliance and validation

______________________________________________________________________

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
cd ../..
source .venv/bin/activate
cd flext-meltano

# Install dependencies
poetry install --with dev,test
```

______________________________________________________________________

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

```python notest
from flext_meltano import FlextMeltanoSettings
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u

settings = FlextMeltanoSettings()
validation_result: p.Result[bool] = settings.validate_meltano_config()

if validation_result.success:
    u.Cli.print("Meltano configuration is valid")
else:
    u.Cli.print(f"Configuration error: {validation_result.error}")
```

______________________________________________________________________

## 🔌 Singer Plugin Configuration

### Tap Configuration

```python notest
from flext_meltano import TapConfig, FlextMeltanoSettingsBuilders

# Create tap configuration
tap_config = TapConfig(
    name="tap-csv",
    executable="tap-csv",
    settings={"files": [{"entity": "users", "path": "data/users.csv", "keys": ["id"]}]},
)

# Build pipeline configuration
builder = FlextMeltanoSettingsBuilders()
pipeline_config = builder.build_tap_config(tap_config.dict())
```

### Target Configuration

```python notest
from flext_meltano import FlextMeltanoSettingsBuilders

target_settings = {
    "destination_path": "output/",
    "file_naming_scheme": "{stream_name}.jsonl",
}

builder = FlextMeltanoSettingsBuilders()
target_config = builder.build_target_config(target_settings)
```

### Singer Catalog Configuration

```python notest
from flext_meltano import StreamDefinition

# Define stream configuration
stream = StreamDefinition(
    name="users",
    schema={
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"},
        },
    },
    metadata={
        "selected": True,
        "replication-method": "INCREMENTAL",
        "replication-key": "updated_at",
    },
)
```

______________________________________________________________________

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

```python notest
from flext_meltano import FlextMeltanoDbtService

# Note: Current implementation is placeholder
dbt_service = FlextMeltanoDbtService()
result = dbt_service.execute_dbt_operation()

# Returns placeholder data:
# {"dbt_status": "ready", "models": []}
```

______________________________________________________________________

## 🏗️ Pipeline Configuration

### Complete ELT Pipeline

```python notest
from flext_meltano import FlextMeltanoService, FlextMeltanoSettingsBuilders

# Build complete pipeline configuration
builder = FlextMeltanoSettingsBuilders()

# Tap configuration
tap_config = {
    "name": "tap-csv",
    "settings": {"files": [{"entity": "users", "path": "data/users.csv"}]},
}

# Target configuration
target_config = {"name": "target-jsonl", "settings": {"destination_path": "output/"}}

# Build pipeline
pipeline_config = builder.build_pipeline_config(tap_config, target_config)

# Initialize service
service = FlextMeltanoService(service_type="pipeline")
execution_result = service.execute()
```

### Configuration Validation

```python notest
from flext_meltano import FlextMeltanoValidators

validators = FlextMeltanoValidators()

# Validate complete pipeline
validation_result = validators.validate_pipeline_config({
    "tap": tap_config,
    "target": target_config,
    "transform": dbt_config,
})

if validation_result.failure:
    u.Cli.print(f"Pipeline validation failed: {validation_result.error}")
```

______________________________________________________________________

## 🌍 Environment Management

### Development Environment

```yaml
# meltano.yml - development settings
environments:
  - name: dev
    settings:
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
    settings:
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

```python notest
from flext_meltano import FlextMeltanoSettings

settings = FlextMeltanoSettings()

# Load development configuration
dev_config = settings.load_configuration("dev")

# Load production configuration
prod_config = settings.load_configuration("prod")
```

______________________________________________________________________

## 🔧 Configuration File Management

### Reading Configuration Files

```python notest
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

```python notest
# Write Singer catalog
catalog_data = {
    "streams": [{"tap_stream_id": "users", "schema": {...}, "metadata": [...]}]
}

write_result = file_manager.write_singer_catalog(catalog_data, "output/catalog.json")
```

### Configuration Backup

```python notest
# Backup critical configuration files
backup_result = file_manager.backup_project_files()

if backup_result.success:
    backup_files = backup_result.unwrap()
    u.Cli.print(f"Backed up {len(backup_files)} configuration files")
```

______________________________________________________________________

## 🔍 Configuration Validation

### Schema Validation

```python notest
from flext_meltano import FlextMeltanoValidators

validators = FlextMeltanoValidators()

# Validate Singer schema
schema_validation = validators.validate_singer_schema({
    "type": "object",
    "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
})

# Validate dbt models
model_validation = validators.validate_dbt_models([
    {"name": "stg_users", "path": "models/staging/stg_users.sql"},
    {"name": "dim_users", "path": "models/marts/dim_users.sql"},
])
```

### Runtime Validation

```python notest
from flext_meltano import FlextMeltanoExecutor

executor = FlextMeltanoExecutor()

# Validate execution environment
env_validation = executor.validate_execution_environment()

if env_validation.failure:
    u.Cli.print(f"Environment validation failed: {env_validation.error}")
```

______________________________________________________________________

## 🚨 Current Limitations

### Architecture Compliance Issues

1. **Direct Import Violations**: Configuration system uses direct meltano.core imports
1. **Abstraction Layer Missing**: Requires wrapper implementation for full FLEXT compliance
1. **dbt Integration**: Current configuration returns placeholder data

### Configuration Restrictions

Due to compliance issues:

- **Production Use**: Not recommended until abstraction layer implemented
- **Full Configuration**: Limited by direct library import violations
- **Modern Patterns**: Missing 2025 ELT configuration best practices

### Workarounds

1. **Use Abstractions**: Leverage existing FlextMeltanoSettings where possible
1. **Monitor Progress**: Track abstraction layer implementation
1. **Plan Migration**: Prepare for wrapper layer adoption
1. **Validate Patterns**: Use r patterns consistently

______________________________________________________________________

## 🔄 Configuration Migration

### Resolution Timeline

- **Phase 1**: Abstraction layer for meltano.core imports (4-6 weeks)
- **Phase 2**: Modern configuration patterns integration (3-4 weeks)
- **Phase 3**: Production-ready configuration management (2 weeks)

### Migration Planning

1. **Current State**: Document existing configuration patterns
1. **Target Architecture**: Plan abstraction layer implementation
1. **Transition Strategy**: Gradual migration with backward compatibility
1. **Validation**: Ensure all configuration patterns maintain functionality

______________________________________________________________________

**Configuration Guide v0.12.0-dev** - Reflects current configuration capabilities with identified compliance gaps requiring systematic resolution for full FLEXT ecosystem integration.
