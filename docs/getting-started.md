# Getting Started with flext-meltano

**ELT foundation library for the FLEXT ecosystem** providing Meltano, dbt, and Singer integration.

---

## 🎯 Overview

flext-meltano serves as the ELT foundation library for the FLEXT ecosystem, abstracting Meltano project management, Singer protocol operations, and dbt transformations behind flext-core compatible interfaces.

---

## 📋 Prerequisites

### **Environment Requirements**

- **Python**: 3.13+
- **FLEXT Workspace**: Access to shared virtual environment
- **Dependencies**: Poetry for dependency management

### **FLEXT Ecosystem Setup**

```bash
# Navigate to FLEXT workspace
cd /home/marlonsc/flext

# Activate shared virtual environment
source .venv/bin/activate

# Navigate to flext-meltano
cd flext-meltano
```

---

## ⚡ Quick Installation

```bash
# Install development dependencies
poetry install --with dev,test

# Verify installation
python -c "from flext_meltano import FlextMeltanoService; print('✅ Installation successful')"
```

---

## 🚀 First Steps

### **Basic Service Usage**

```python
from flext_meltano import FlextMeltanoService
from flext_core import FlextResult

# Initialize ELT service
service = FlextMeltanoService()

# Service is ready for ELT operations
print("flext-meltano service initialized")
```

### **Singer Protocol Operations**

```python
from flext_meltano import FlextTapAbstractions

# Initialize tap abstractions
tap_abstractions = FlextTapAbstractions()

# Example catalog discovery (requires configured tap)
# catalog_result = await tap_abstractions.discover_catalog("tap-csv")
```

### **FlextResult Pattern**

```python
from flext_core import FlextResult

# All flext-meltano operations return FlextResult[T]
def example_operation() -> FlextResult[str]:
    try:
        # Your operation logic
        return FlextResult.ok("Operation successful")
    except Exception as e:
        return FlextResult.fail(f"Operation failed: {e}")

# Usage pattern
result = example_operation()
if result.is_success:
    data = result.unwrap()
    print(f"Success: {data}")
else:
    print(f"Error: {result.error}")
```

---

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

---

## 📚 Next Steps

- **[Architecture](architecture.md)** - Understand the design patterns
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Development](development.md)** - Contributing guidelines
- **[Integration](integration.md)** - Ecosystem integration patterns

---

## ⚠️ Important Notes

### **Architecture Compliance**

- **Import Restrictions**: Only use root-level imports from `flext_meltano`
- **Error Handling**: Always use `FlextResult[T]` pattern
- **Service Pattern**: Follow flext-core domain service patterns

### **Current Status**

- **Architecture Compliance**: Direct meltano imports in `adapters.py` require abstraction
- **Quality Gates**: All checks must pass before commits
- **Integration**: Use only flext-core compatible patterns

---

**Next**: Review the [Architecture Guide](architecture.md) to understand flext-meltano's design patterns and FLEXT ecosystem integration.
