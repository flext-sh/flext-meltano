# FLEXT Meltano Quick Start Guide

Get up and running with FLEXT Meltano in minutes.

## 🚀 Installation & Setup

### Prerequisites

- Python 3.13
- Poetry 1.8+
- Git

### Quick Setup

```bash
# Clone or navigate to the project
cd flext-meltano

# Complete development setup
make setup

# Verify installation
make check
```

## 📝 Basic Usage Examples

### 1. Simple Pipeline Execution

```python
import flext_meltano
from flext_meltano.flext_meltano_execution import flext_meltano_execute_job

# Execute a CSV pipeline
result = flext_meltano_execute_job("tap-csv", "target-csv")

if result.success:
    print("✅ Pipeline completed successfully!")
    print(f"Output: {result.output}")
else:
    print("❌ Pipeline failed!")
    print(f"Error: {result.error}")
```

### 2. Meltano Command Execution

```python
from flext_meltano.flext_meltano_execution import flext_meltano_run_command

# Get Meltano version
version_result = flext_meltano_run_command(["--version"])
print(f"Meltano version: {version_result.output.strip()}")

# List installed plugins
plugins_result = flext_meltano_run_command(["invoke", "--list"])
if plugins_result.success:
    print("Installed plugins:")
    print(plugins_result.output)
```

### 3. Plugin Discovery

```python
from flext_meltano.flext_meltano_discovery import (
    flext_meltano_discover_plugins,
    flext_meltano_discover_catalog
)

# Discover available plugins
plugins = flext_meltano_discover_plugins()
print(f"Available plugins: {plugins}")

# Discover schema from a tap
catalog = flext_meltano_discover_catalog("tap-csv")
print(f"Catalog: {catalog}")
```

### 4. Plugin Installation

```python
from flext_meltano.flext_meltano_installation import (
    flext_meltano_install_plugin,
    FlextMeltanoInstaller
)

# Install plugins using function
csv_result = flext_meltano_install_plugin("extractor", "tap-csv")
target_result = flext_meltano_install_plugin("loader", "target-csv")

# Or using installer class
installer = FlextMeltanoInstaller()
postgres_result = installer.install_plugin("extractor", "tap-postgres")

if all([csv_result.success, target_result.success]):
    print("✅ Plugins installed successfully!")
```

## 🌉 Go Bridge Integration

### Using the Bridge Script

```bash
# Get Meltano version
python scripts/flext_meltano_bridge.py version

# Execute pipeline
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv

# Add plugins
python scripts/flext_meltano_bridge.py add_plugin extractor tap-postgres
python scripts/flext_meltano_bridge.py add_plugin loader target-postgres

# Discover catalog
python scripts/flext_meltano_bridge.py discover tap-postgres
```

### JSON Response Format

All bridge operations return JSON responses:

```json
{
  "success": true,
  "output": "meltano, version 3.8.0\n",
  "returncode": 0,
  "command": "--version"
}
```

## 🧪 Testing Your Setup

### Run Quality Gates

```bash
# Complete validation (all must pass)
make validate

# Individual checks
make lint                    # Code linting
make type-check              # Type checking
make test                    # Run tests with coverage
make security                # Security scanning
```

### Test Basic Pipeline

```bash
# Initialize Meltano project (if needed)
make meltano-init

# Add test plugins
make meltano-add-extractor NAME=tap-csv
make meltano-add-loader NAME=target-csv

# Test basic pipeline
make test-pipeline
```

### Verify Bridge Integration

```python
# Test bridge functionality
from flext_meltano.flext_meltano_execution import flext_meltano_run_command

# This simulates what the Go service would call
result = flext_meltano_run_command(["--version"])
assert result.success
assert "meltano" in result.output.lower()
print("✅ Bridge integration working!")
```

## 🏗️ Project Structure Overview

```
flext-meltano/
├── src/flext_meltano/           # Core library
│   ├── __init__.py              # 249 exports
│   ├── base.py                  # Base classes
│   ├── core.py                  # Enterprise services
│   ├── flext_meltano_execution.py  # Primary API
│   └── ...                      # Other modules
├── scripts/                     # Bridge scripts
│   └── flext_meltano_bridge.py  # Go integration
├── tests/                       # Test suite (90%+ coverage)
├── docs/                        # Documentation
├── dbt/                         # DBT configurations
└── examples/                    # Usage examples
```

## 🎯 Common Patterns

### Error Handling

```python
from flext_meltano.flext_meltano_execution import flext_meltano_execute_job

def safe_pipeline_execution(extractor, loader):
    """Execute pipeline with proper error handling."""
    try:
        result = flext_meltano_execute_job(extractor, loader)
        
        if result.success:
            return {"status": "success", "data": result.output}
        else:
            return {"status": "error", "message": result.error}
            
    except Exception as e:
        return {"status": "exception", "message": str(e)}

# Usage
pipeline_result = safe_pipeline_execution("tap-csv", "target-csv")
print(pipeline_result)
```

### Configuration Management

```python
from flext_meltano.base import FlextMeltanoConfig

# Create configuration
config = FlextMeltanoConfig(
    meltano_project_root="./my-project",
    environment="production"
)

# Use with services
from flext_meltano.core import FlextMeltanoOrchestrationService
orchestrator = FlextMeltanoOrchestrationService(config=config)
```

### Factory Pattern Usage

```python
from flext_meltano.base import create_tap, create_target

# Create tap instance
oracle_tap = create_tap("oracle", 
    host="localhost", 
    port=1521, 
    database="xe"
)

# Create target instance
postgres_target = create_target("postgres",
    host="localhost",
    port=5432,
    database="warehouse"
)
```

## 🔧 Development Workflow

### Setting Up Development Environment

```bash
# Install development dependencies
make dev-install

# Set up pre-commit hooks
make pre-commit

# Run tests in watch mode (if available)
pytest --watch
```

### Adding New Functionality

1. **Write Tests First**: Add tests to appropriate test directory
2. **Implement Feature**: Follow existing patterns in modules
3. **Run Quality Gates**: `make validate` must pass
4. **Update Documentation**: Keep docs current
5. **Test Bridge Integration**: Ensure Go compatibility

### Quality Checklist

Before committing:

- [ ] `make validate` passes (all quality gates)
- [ ] Tests added for new functionality
- [ ] 90%+ test coverage maintained
- [ ] Type hints added (MyPy strict mode)
- [ ] Documentation updated
- [ ] Bridge integration tested (if applicable)

## 🚨 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure proper Python path
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
```

**Meltano Not Found:**
```bash
# Initialize Meltano project
make meltano-init
```

**Poetry Issues:**
```bash
# Reinstall dependencies
rm -rf .venv
poetry install --all-extras
```

**Test Failures:**
```bash
# Run specific test with verbose output
pytest tests/test_specific.py -v -s
```

## 📚 Next Steps

1. **Explore [API Reference](../api/README.md)** for detailed function documentation
2. **Review [Architecture Guide](../architecture/README.md)** for system design
3. **Check [Advanced Examples](advanced-examples.md)** for complex scenarios
4. **Read [Development Guide](../guides/development.md)** for contribution guidelines

---

*Quick Start Guide - Version 2.0.0-enterprise*
*Last Updated: 2025-01-29*