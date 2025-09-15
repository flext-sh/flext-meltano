# flext-meltano Documentation

**Documentation for the FLEXT ecosystem ELT foundation library** providing Meltano, dbt, and Singer integration.

**Version**: 0.9.0 | **Last Updated**: 2025-09-17

---

## 📋 Documentation Index

### **Getting Started**

- **[Getting Started](getting-started.md)** - Installation and first steps
- **[Architecture](architecture.md)** - Design patterns and structure
- **[API Reference](api-reference.md)** - Complete API documentation

### **Development**

- **[Development Guide](development.md)** - Contributing and workflows
- **[Integration Patterns](integration.md)** - Ecosystem integration
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

### **Examples**

- **[Examples](examples/)** - Working code examples and patterns

---

## 🎯 Purpose and Architecture

flext-meltano serves as the ELT foundation library for the FLEXT ecosystem, abstracting Meltano project management, Singer protocol operations, and dbt transformations behind flext-core compatible interfaces.

### **Current Status**

| Component             | Status       | Details                                    |
| --------------------- | ------------ | ------------------------------------------ |
| **Architecture**      | 🟢 Compliant | Single class per module pattern            |
| **FLEXT Integration** | 🟢 Strong    | Extensive flext-core usage                 |
| **Library Imports**   | ⚠️ Issue     | Direct meltano imports require abstraction |
| **Type Safety**       | 🟢 Good      | MyPy compliance in src/                    |

## 🏗️ Implementation Details

### **Source Code Structure**

- **Total Lines**: 7,266 across 20 Python modules
- **Architecture**: Single unified class per module (FLEXT compliant)
- **Error Handling**: FlextResult pattern implementation (95% coverage)
- **Service Pattern**: FlextDomainService implementations (90% coverage)

### **Key Components**

- **FlextMeltanoService**: Core ELT orchestration
- **FlextTapAbstractions**: Singer tap integration
- **FlextTargetAbstractions**: Singer target integration
- **FlextMeltanoAdapter**: Meltano project management (requires abstraction work)
- **FlextMeltanoExecutor**: Command execution engine

### **Architecture Compliance Issues**

- **Direct Library Imports**: Lines 14-25 in `adapters.py` contain direct `meltano.core.*` imports
- **Abstraction Layer**: Requires FlextMeltanoLibraryRunner to wrap meltano operations
- **Library Integration**: Migration from CLI subprocess patterns to programmatic APIs needed

## 🚀 Quick Navigation

### **Essential Documentation**

- **[Getting Started](getting-started.md)** - Installation and first steps with flext-meltano
- **[Architecture](architecture.md)** - Design patterns and FLEXT integration
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Development](development.md)** - Contributing guidelines and workflows
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

### **Advanced Topics**

- **[Integration Patterns](integration.md)** - Ecosystem integration with other FLEXT projects
- **[Examples](examples/)** - Working code examples and usage patterns

---

## 📋 Development Workflow

### **Quality Gates**

All development must pass these quality gates:

```bash
make validate           # Complete validation pipeline
make lint               # Ruff linting with zero tolerance
make type-check         # MyPy strict mode validation
make test               # Test suite execution
```

### **FLEXT Compliance Requirements**

- **Import Restrictions**: Only root-level imports from `flext_meltano`
- **Error Handling**: FlextResult pattern for all operations
- **Service Pattern**: Follow flext-core domain service patterns
- **Architecture**: Single class per module compliance

---

## 📞 Support and Resources

### **Development Support**

- **Architecture Questions**: Review [architecture.md](architecture.md)
- **Integration Support**: Check [integration.md](integration.md)
- **Development Issues**: See [troubleshooting.md](troubleshooting.md)

### **FLEXT Ecosystem Links**

- **[FLEXT Workspace](../../README.md)** - Complete ecosystem overview
- **[FLEXT Standards](../../CLAUDE.md)** - Development standards
- **[Root TODO.md](../TODO.md)** - Current roadmap and critical issues

---

**flext-meltano Documentation v0.9.0** - Last updated 2025-09-17

**Purpose**: Comprehensive documentation for the FLEXT ecosystem ELT foundation library supporting Meltano, dbt, and Singer integration patterns.
