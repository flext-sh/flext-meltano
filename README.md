# FLEXT-Meltano

Meltano integration for the FLEXT platform providing project management, pipeline orchestration, and Go-Python bridge functionality.

**Part of the FLEXT Ecosystem**: This module integrates with the FLEXT platform, using flext-core for foundation patterns and flext-observability for monitoring.

## Overview

FLEXT-Meltano is a modern wrapper around Meltano that integrates with the FLEXT ecosystem. It provides:

- **Project Management**: Create, configure and manage Meltano projects
- **Pipeline Orchestration**: Execute and monitor data pipelines  
- **Go Integration**: HTTP API bridge for Go applications
- **FLEXT Integration**: Uses FLEXT patterns (ServiceResult, domain events, etc.)

## Status

| Component | Status | Notes |
|-----------|--------|--------|
| **Core APIs** | ✅ Working | Project creation, plugin management |
| **Go Bridge** | ✅ Working | HTTP API approach using JSON responses |
| **Pipeline Execution** | ✅ Working | Basic tap-target pipelines via Meltano CLI |
| **FLEXT Integration** | ✅ Working | ServiceResult patterns, observability |

## Quick Start

### Installation

**Installation**:

```bash
# Install in development mode
cd flext-meltano
pip install -e .

# Install Meltano CLI
pip install meltano

# Verify installation
python -c "
from flext_meltano import MeltanoBridge
bridge = MeltanoBridge('.')
print('✅ Available:', bridge.is_available())
"
```

### Basic Usage

```python
import asyncio
from flext_meltano import MeltanoBridge

async def basic_pipeline():
    bridge = MeltanoBridge('.')
    
    # Create project
    await bridge.init_project('my_project', '.')
    
    # Add plugins
    await bridge.add_plugin('my_project', 'extractor', 'tap-csv')
    await bridge.add_plugin('my_project', 'loader', 'target-csv')
    
    # Run pipeline
    result = await bridge.run_pipeline('my_project', 'tap-csv', 'target-csv')
    print(result)

asyncio.run(basic_pipeline())
```

### Go Integration

The Go integration uses HTTP API communication:

```python
from flext_meltano.integrations import GoIntegration

integration = GoIntegration()
components = integration.generate_http_api_components()
# Generates: FastAPI server, Go HTTP client, documentation
```

## Architecture

```
flext_meltano/
├── integrations/
│   ├── bridge.py              # Main Go-Python bridge
│   └── gopy_integration.py    # HTTP API generation
├── project_manager.py         # Meltano project operations
├── orchestrator.py           # Pipeline orchestration  
├── models.py                 # Data models
├── event_bridge.py           # Event handling
└── unified_anti_corruption_layer.py  # Clean boundaries
```

**Key Components**:

- **MeltanoBridge**: Main API for external integration
- **MeltanoProjectManager**: Project lifecycle management
- **FlextMeltanoOrchestrator**: Pipeline execution and monitoring
- **UnifiedMeltanoAntiCorruptionLayer**: Clean architecture boundary

## Configuration

**Environment Configuration**:

```bash
# .env
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

## Testing

The project includes comprehensive testing setup:

```bash
# Run tests
pytest

# With coverage
pytest --cov=flext_meltano

# Specific test categories
pytest -m unit
pytest -m integration
pytest -m "requires_meltano"
```

## Development

### Code Quality

The project uses modern Python tooling:

- **ruff**: Linting and formatting
- **mypy**: Static type checking  
- **pytest**: Testing framework
- **pre-commit**: Git hooks

```bash
# Run quality checks
ruff check src/
mypy src/
```

### Dependencies

**FLEXT Integration**:
- **flext-core**: Foundation framework (ServiceResult, domain patterns)
- **flext-observability**: Logging and monitoring
- **meltano**: Data platform integration
- **sqlalchemy**: Database operations

**Key Features**:
- ServiceResult pattern for consistent error handling
- HTTP API bridge for Go integration
- Async/await support throughout
- Clean architecture with anti-corruption layers

## Documentation

- **[Getting Started](./docs/guides/getting-started.md)** - Setup and first pipeline
- **[API Reference](./docs/api/core.md)** - Complete API documentation
- **[Examples](./docs/examples/basic-pipeline.md)** - Working code examples
- **[Production Guide](./docs/deployment/production.md)** - Deployment patterns

## Limitations

**Known Limitations**:

- **Go Integration**: HTTP API only, not native Go bindings
- **Testing**: Basic operations tested, complex scenarios need more validation
- **Production**: Deployment patterns provided but not production-validated
- **Extensions**: Oracle/LDAP integration code present but minimally tested

## Contributing

**Development Standards**:

1. **Type Safety**: Python 3.13+ with comprehensive type hints
2. **Testing**: Maintain 90%+ test coverage
3. **Architecture**: Clean Architecture and DDD patterns
4. **Error Handling**: Use ServiceResult pattern for consistent error handling
5. **Code Quality**: Ruff linting, MyPy type checking
6. **Documentation**: Keep docs updated with API changes

## CLI

The project provides a CLI interface:

```bash
# Available through poetry scripts
flext-meltano --help

# Or direct module execution
python -m flext_meltano.cli --help
```

---

**Project**: flext-meltano | **Framework**: FLEXT 0.7.0 | **Python**: 3.13+ | **Status**: Development