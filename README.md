# flext-meltano

**ELT foundation library for the FLEXT ecosystem** providing Meltano, dbt, and Singer integration using **library API patterns** with FlextResult error handling.

> **⚠️ STATUS**: Architecture compliance issues - Direct meltano imports require abstraction layer

---

## 🎯 Purpose and Role in FLEXT Ecosystem

### **For the FLEXT Ecosystem**

flext-meltano serves as the ELT foundation library for all data integration operations across the 32-project FLEXT ecosystem. It abstracts Meltano project management, Singer protocol operations, and dbt transformations behind flext-core compatible interfaces.

### **Key Responsibilities**

1. **Meltano Integration** - Project lifecycle management and plugin orchestration
2. **Singer Protocol** - Tap and target abstractions with message handling
3. **dbt Operations** - Transformation execution and model management

### **Integration Points**

- **flext-core** → Foundation patterns, FlextResult, service base classes
- **flext-tap-*** → Singer tap implementations using FlextTapAbstractions
- **flext-target-*** → Singer target implementations using FlextTargetAbstractions
- **All 32 FLEXT Projects** → ELT operations through flext-meltano foundation

---

## 🏗️ Architecture and Patterns

### **FLEXT-Core Integration Status**

| Pattern             | Status     | Description                      |
| ------------------- | ---------- | -------------------------------- |
| **FlextResult<T>**  | 🟢 95%     | Railway-oriented error handling  |
| **FlextService**    | 🟢 90%     | Domain service implementations   |
| **FlextContainer**  | 🟢 85%     | Dependency injection usage       |
| **Domain Patterns** | 🟡 70%     | Clean architecture compliance    |

> **Status**: 🔴 Critical | 🟡 Partial | 🟢 Complete

### **Architecture Compliance Issues**

- **Direct Library Imports**: Lines 14-25 in `adapters.py` contain forbidden `meltano.core.*` imports
- **Abstraction Layer**: Need FlextMeltanoLibraryRunner to wrap meltano operations
- **Library Integration**: Current CLI subprocess patterns require migration to programmatic APIs

---

## 🚀 Quick Start

### **Installation**

```bash
# FLEXT workspace development
cd /home/marlonsc/flext/flext-meltano
source ../venv/bin/activate  # Use shared FLEXT workspace venv
poetry install --with dev,test
```

### **Basic Usage**

```python
from flext_meltano import FlextMeltanoService, FlextTapAbstractions
from flext_core import FlextResult

# ELT service initialization
service = FlextMeltanoService()

# Singer tap operations
tap_abstractions = FlextTapAbstractions()
catalog_result = await tap_abstractions.discover_catalog("tap-csv")

if catalog_result.is_success:
    catalog = catalog_result.unwrap()
    # Process catalog...
else:
    print(f"Discovery failed: {catalog_result.error}")
```

## 🔧 Development

### **Essential Commands**

```bash
# Quality gates (must pass before commits)
make validate           # Complete validation pipeline
make lint               # Ruff linting with zero tolerance
make type-check         # MyPy strict mode validation
make test               # Test suite execution
make format             # Code auto-formatting

# Development workflow
make install-dev        # Install development dependencies
make run-tests          # Run tests with coverage
make check-imports      # Validate import compliance
```

### **Quality Gates**

- **Zero Tolerance**: No direct meltano/dbt/singer imports outside abstractions
- **Type Safety**: MyPy strict mode with zero errors in src/
- **Test Coverage**: Current focus on functional testing with real APIs
- **Import Compliance**: Only flext-core and flext-meltano root imports allowed

## 🧪 Testing

### **Test Structure**

```bash
tests/
├── unit/              # Unit tests for individual components
├── integration/       # Integration tests with real APIs
└── e2e/              # End-to-end pipeline tests
```

### **Testing Commands**

```bash
# Run all tests with coverage
make test

# Run specific test categories
pytest tests/unit/                    # Unit tests only
pytest tests/integration/             # Integration tests
pytest -m "not slow"                  # Skip slow tests
pytest --cov=src --cov-report=html    # Generate HTML coverage report
```

## 📊 Status and Metrics

### **Quality Standards**

- **Coverage**: Working toward 90% minimum (currently functional testing focus)
- **Type Safety**: MyPy strict mode compliance in src/
- **Security**: Bandit security scanning integrated
- **FLEXT-Core Compliance**: 85% (needs abstraction layer completion)

### **Ecosystem Integration**

- **Direct Dependencies**: flext-tap-*, flext-target-*, flext-dbt-* projects depend on this library
- **Service Dependencies**: Depends on flext-core for foundation patterns
- **Integration Points**: 20+ FLEXT projects use flext-meltano for ELT operations

### **Current Implementation**

- **Source Code**: 7,266 lines across 20 Python modules
- **Architecture**: Single class per module pattern (compliant)
- **Error Handling**: FlextResult pattern implementation (95% coverage)
- **Service Pattern**: FlextDomainService implementations (90% coverage)

## 🗺️ Roadmap

### **Current Version (v0.9.0)**

- Foundation library with comprehensive ELT abstractions
- FlextResult pattern implementation across all operations
- Singer protocol support through tap and target abstractions
- Meltano project management capabilities

### **Next Version (v0.10.0)**

- Resolve architecture compliance issues (direct imports)
- Implement dbtRunner programmatic API integration
- Enhanced abstraction layer for external library dependencies
- Improved test coverage with real API integration

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Installation and setup
- **[Architecture](docs/architecture.md)** - Design patterns and structure
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Development](docs/development.md)** - Contributing and workflows
- **[Integration](docs/integration.md)** - Ecosystem integration patterns
- **[Examples](docs/examples/)** - Working code examples
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues

---

## 🤝 Contributing

### **FLEXT-Core Compliance Checklist**

- [ ] Use only flext-core and flext-meltano root imports
- [ ] Implement FlextResult pattern for error handling
- [ ] Follow single class per module architecture
- [ ] Pass all quality gates (lint, type-check, test)

### **Quality Standards**

```bash
# Pre-commit validation (must pass)
make validate           # Complete validation pipeline
make check-imports      # Verify no direct library imports
make test               # Run test suite with coverage
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext/issues)
- **Security**: Report security issues privately to maintainers

---

**flext-meltano v0.9.0** - ELT foundation library enabling data integration operations across the FLEXT ecosystem.

**Mission**: Provide comprehensive Meltano, dbt, and Singer abstractions with flext-core patterns for enterprise data integration workflows.