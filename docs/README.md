# FLEXT-Meltano Documentation

Documentation for FLEXT-Meltano, a modern Meltano integration for the FLEXT platform.

**FLEXT Integration**: Integrates with flext-core for foundation patterns and flext-observability for monitoring.

## Documentation Structure

### Core Documentation

| Document | Purpose | Status |
|----------|---------|--------|
| [**Getting Started**](./guides/getting-started.md) | Installation and basic usage | ✅ Current |
| [**API Reference**](./api/core.md) | Complete API documentation | ✅ Current |
| [**Examples**](./examples/basic-pipeline.md) | Working code examples | ✅ Verified |
| [**FLEXT Integration**](./FLEXT_ECOSYSTEM_INTEGRATION.md) | FLEXT platform integration | ✅ Current |

## What This Project Provides

### Working Features

- **MeltanoBridge API**: Project creation, plugin management, pipeline execution
- **Project Management**: Create, configure, and validate Meltano projects
- **Go Integration**: HTTP API bridge for Go applications
- **FLEXT Integration**: ServiceResult patterns, structured logging

### Limited/Untested Features

- **Complex Pipelines**: Multi-step orchestration needs more testing
- **External Integrations**: Oracle/LDAP extension code present but minimal testing
- **Performance**: No comprehensive load testing performed

## Key Components Overview

### MeltanoBridge
Main API for external integration, especially Go applications:

```python
from flext_meltano import MeltanoBridge

bridge = MeltanoBridge('.')
await bridge.init_project('my_project', '.')
await bridge.add_plugin('my_project', 'extractor', 'tap-csv')
```

### MeltanoProjectManager  
Core project lifecycle management:

```python
from flext_meltano import MeltanoProjectManager

manager = MeltanoProjectManager('.')
result = await manager.create_project('test', 'dev')
validation = await manager.validate_project('test')
```

### FlextMeltanoOrchestrator
Pipeline execution and monitoring:

```python
from flext_meltano import FlextMeltanoOrchestrator

orchestrator = FlextMeltanoOrchestrator(project_manager, state_manager, event_bus)
result = await orchestrator.run_pipeline('project', pipeline_def)
```

## Architecture Patterns

### FLEXT Integration
The project follows FLEXT architectural patterns:

- **ServiceResult**: Consistent error handling from flext-core
- **Clean Architecture**: Anti-corruption layers for external systems
- **Type Safety**: Python 3.13+ type hints throughout
- **Structured Logging**: Integration with flext-observability

### Anti-Corruption Layer
Clean boundary between FLEXT and Meltano:

```python
from flext_meltano import UnifiedMeltanoAntiCorruptionLayer

acl = UnifiedMeltanoAntiCorruptionLayer()
result = await acl.translate_meltano_operation(operation)
```

## Development Workflow

### Testing Strategy
**Testing Standards**:

```bash
# Unit tests
pytest -m unit

# Integration tests (requires Meltano)
pytest -m integration -m requires_meltano

# Meltano-specific tests
pytest -m meltano

# Coverage requirements (90% minimum)
pytest --cov=flext_meltano --cov-fail-under=90
```

### Code Quality
**Quality Standards**:

- **ruff**: Linting with ALL rules enabled (sensible exceptions)
- **mypy**: Strict type checking
- **pre-commit**: Automated quality checks
- **bandit**: Security analysis
- **pytest**: 90%+ coverage requirement
- **ServiceResult**: Consistent error handling pattern

## Configuration Management

### Environment Variables
**Configuration Standards**:

```bash
# Basic configuration
MELTANO_PROJECT_ROOT=./projects
MELTANO_ENVIRONMENT=dev

# FLEXT integration
FLEXT_LOG_LEVEL=INFO
FLEXT_OBSERVABILITY_ENABLED=true

# Singer protocol (suppress warnings)
SINGER_SDK_LOG_LEVEL=ERROR
SINGER_SDK_DISABLE_WARNINGS=true
PYTHONWARNINGS=ignore::DeprecationWarning
```

### Pydantic Models
Configuration uses typed Pydantic models:

```python
from flext_meltano.models import MeltanoProjectConfig

config = MeltanoProjectConfig(
    project_id="my_project",
    version=1,
    plugins=MeltanoPlugins(...)
)
```

## Go Integration Details

### HTTP API Approach
Rather than native bindings, the project generates HTTP APIs:

```python
from flext_meltano.integrations import GoIntegration

integration = GoIntegration()
components = integration.generate_http_api_components()

# Generates:
# - FastAPI server (Python)
# - HTTP client (Go)
# - OpenAPI documentation
```

This approach provides:
- **Reliability**: No complex FFI or binding issues
- **Maintainability**: Standard HTTP protocols
- **Debugging**: Easy to trace and monitor
- **Deployment**: Can be containerized separately

## Documentation Standards

### Example Verification
All code examples in documentation should be:

1. **Tested**: Actually executed to verify they work
2. **Complete**: Include necessary imports and setup
3. **Realistic**: Use actual data and configurations
4. **Current**: Updated when APIs change

### Status Indicators
Documentation uses clear status indicators:

- ✅ **Verified**: Tested and working
- ⚠️ **Limited**: Partially tested or theoretical
- ❌ **Untested**: Code exists but not validated
- 🚧 **In Progress**: Currently being developed

## Getting Help

### Common Issues
1. **Import Errors**: Ensure FLEXT dependencies are installed
2. **Meltano Not Found**: Install Meltano CLI (`pip install meltano`)
3. **Type Errors**: Check Python 3.13+ is being used
4. **Singer Warnings**: Configure warning suppression in environment

### Development Support
- Check existing tests for usage patterns
- Review API documentation for complete interfaces
- Use type hints and IDE support for guidance
- Follow FLEXT patterns used in other projects

---

**Framework**: FLEXT 0.7.0 | **Python**: 3.13+ | **Updated**: 2025-07-12