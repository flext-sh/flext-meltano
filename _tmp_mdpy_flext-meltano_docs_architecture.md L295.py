# from flext-meltano/docs/architecture.md:295
from __future__ import annotations


class FlextMeltanoError(Exception):
    """Base exception for all flext-meltano operations."""


class FlextMeltanoConfigurationError(FlextMeltanoError):
    """Configuration-related errors."""


class FlextMeltanoExecutionError(FlextMeltanoError):
    """Pipeline execution errors."""


class FlextMeltanoValidationError(FlextMeltanoError):
    """Data validation errors."""```
## 🎯 Current Status and Technical Debt

### **Architecture Compliance Status**

| Component                 | Status | Details                                            |
| ------------------------- | ------ | -------------------------------------------------- |
| **Type Safety**           | 🟢 90%  | Comprehensive Pydantic models and type annotations |
| **FLEXT Integration**     | 🟢 85%  | Strong flext-core usage with r patterns            |
| **Single Class Pattern**  | 🟢 100% | All modules follow single class architecture       |
| **External Abstractions** | 🟡 60%  | Direct imports in adapters.py need wrapping        |

### **Technical Debt**

**Priority 1 - Critical**:

- **Direct Imports**: Lines 14-25 in `adapters.py` need abstraction layer
- **Library Wrapper**: Implement `_MeltanoLibraryWrapper` pattern

**Priority 2 - Important**:

- **Integration Testing**: Expand real API integration tests
- **Bridge Communication**: Complete Go ↔ Python bridge patterns

**Priority 3 - Enhancement**:

- **Plugin Architecture**: Ecosystem-wide plugin foundation
- **Performance**: Optimize for large data volume processing

## 🚀 Future Architecture

### **Target State**

1. **Complete Abstraction**: All external libraries wrapped behind FLEXT interfaces
1. **Enhanced Integration**: Full ecosystem integration with plugin architecture
1. **Production Readiness**: 100% test coverage with real API integration
1. **Performance Optimization**: Efficient processing for enterprise data volumes

### **Migration Path**

1. **Phase 1**: Implement library wrapper for direct imports
1. **Phase 2**: Expand integration testing coverage
1. **Phase 3**: Complete plugin architecture foundation
1. **Phase 4**: Performance optimization and production hardening

______________________________________________________________________

**Architecture Summary**: flext-meltano provides a robust, type-safe foundation for ELT operations within the FLEXT ecosystem, with clear separation of concerns, comprehensive error handling, and strong integration patterns. The current architecture debt primarily involves abstracting direct library dependencies behind FLEXT-compatible interfaces.

## Related Documentation

**Within Project**:

- [Getting Started](getting-started.md) - Installation and basic usage
- [API Reference](api-reference.md) - Complete API documentation
- [Examples](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-meltano/examples/) - Working code examples

**Across Projects**:

- [flext-core Foundation](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-core/docs/architecture/overview.md) - Clean architecture and CQRS patterns
- [flext-plugin Architecture](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-plugin/docs/architecture.md) - Plugin architecture patterns
- [flext-quality Automation](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-quality/AGENTS.md) - Quality analysis and automation

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

**Design Authority**: This architecture follows FLEXT ecosystem standards and Clean Architecture principles, ensuring maintainability, testability, and integration capability across the 32-project FLEXT ecosystem.
