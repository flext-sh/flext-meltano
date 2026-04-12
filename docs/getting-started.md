# Getting Started with flext-meltano

<!-- TOC START -->
- [🎯 Overview](#overview)
- [📋 Prerequisites](#prerequisites)
  - [**Environment Requirements**](#environment-requirements)
  - [**FLEXT Ecosystem Setup**](#flext-ecosystem-setup)
- [⚡ Quick Installation](#quick-installation)
- [🚀 First Steps](#first-steps)
  - [**Basic Service Usage**](#basic-service-usage)
  - [**Singer Protocol Operations**](#singer-protocol-operations)
  - [**r Pattern**](#r-pattern)
- [🔧 Development Workflow](#development-workflow)
  - [**Quality Gates**](#quality-gates)
  - [**Common Commands**](#common-commands)
- [📚 Next Steps](#next-steps)
- [⚠️ Important Notes](#important-notes)
  - [**Architecture Compliance**](#architecture-compliance)
  - [**Current Status**](#current-status)
- [Related Documentation](#related-documentation)
<!-- TOC END -->

**ELT foundation library for the FLEXT ecosystem** providing Meltano, dbt, and Singer integration.

______________________________________________________________________

## 🎯 Overview

flext-meltano serves as the ELT foundation library for the FLEXT ecosystem, abstracting Meltano project management, Singer protocol operations, and dbt transformations behind flext-core compatible interfaces.

______________________________________________________________________

## 📋 Prerequisites

### **Environment Requirements**

- **Python**: 3.13+
- **FLEXT Workspace**: Access to shared virtual environment
- **Dependencies**: Poetry for dependency management

### **FLEXT Ecosystem Setup**

```bash
# Navigate to FLEXT workspace
cd ../..

# Activate shared virtual environment
source .venv/bin/activate

# Navigate to flext-meltano
cd flext-meltano
```

______________________________________________________________________

## ⚡ Quick Installation

```bash
# Install development dependencies
poetry install --with dev,test

# Verify installation
python -c "from flext_meltano import FlextMeltanoService; print('✅ Installation successful')"
```

______________________________________________________________________

## 🚀 First Steps

### **Basic Service Usage**

```python
from flext_meltano import FlextMeltanoService
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
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u

# Initialize ELT service
service = FlextMeltanoService()

# Service is ready for ELT operations
print("flext-meltano service initialized")
```

### **Singer Protocol Operations**

```python
from flext_meltano import FlextMeltanoTapAbstractions

# Initialize tap abstractions
tap_abstractions = FlextMeltanoTapAbstractions()

# Example catalog discovery (requires configured tap)
# catalog_result = tap_abstractions.discover_catalog("tap-csv")
```

### **r Pattern**

```python
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
from flext_core import r
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


# All flext-meltano operations return r[T]
def example_operation() -> r[str]:
    try:
        # Your operation logic
        return r.ok("Operation successful")
    except Exception as e:
        return r.fail(f"Operation failed: {e}")


# Usage pattern
result = example_operation()
if result.is_success:
    data = result.unwrap()
    print(f"Success: {data}")
else:
    print(f"Error: {result.error}")
```

______________________________________________________________________

## 🔧 Development Workflow

### **Quality Gates**

```bash
# Run before any commit
make validate           # Complete validation pipeline
make lint               # Code linting
make type-check         # Type safety validation
make test               # Test execution
```

### **Common Commands**

```bash
# Development setup
make install-dev        # Install development dependencies

# Testing
make test               # Run test suite
pytest tests/unit/      # Unit tests only

# Code quality
make format             # Auto-format code
make check-imports      # Validate import compliance
```

______________________________________________________________________

## 📚 Next Steps

- **[Architecture](architecture.md)** - Understand the design patterns
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Development](development.md)** - Contributing guidelines
- **[Integration](guides/integration.md)** - Ecosystem integration patterns

______________________________________________________________________

## ⚠️ Important Notes

### **Architecture Compliance**

- **Import Restrictions**: Only use root-level imports from `flext_meltano`
- **Error Handling**: Always use `r[T]` pattern
- **Service Pattern**: Follow flext-core domain service patterns

### **Current Status**

- **Architecture Compliance**: Direct meltano imports in `adapters.py` require abstraction
- **Quality Gates**: All checks must pass before commits
- **Integration**: Use only flext-core compatible patterns

______________________________________________________________________

**Next**: Review the [Architecture Guide](architecture.md) to understand flext-meltano's design patterns and FLEXT ecosystem integration.

## Related Documentation

**Within Project**:

- [Architecture](architecture.md) - Architecture and design patterns
- [API Reference](api-reference.md) - Complete API documentation
- [Examples](../examples/) - Working code examples

**Across Projects**:

- [flext-core Foundation](https://github.com/organization/flext/tree/main/flext-core/docs/architecture/overview.md) - Clean architecture and CQRS patterns
- [flext-core Service Patterns](https://github.com/organization/flext/tree/main/flext-core/docs/guides/service-patterns.md) - Service patterns and dependency injection
- [flext-plugin Architecture](https://github.com/organization/flext/tree/main/flext-plugin/docs/architecture.md) - Plugin architecture patterns

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
