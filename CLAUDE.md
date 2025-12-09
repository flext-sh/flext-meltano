# flext-meltano - FLEXT Data Integration

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-07

---

## Project Overview

**FLEXT-Meltano** is the enterprise Meltano data integration and ELT pipeline orchestration foundation for the FLEXT ecosystem. It provides comprehensive Singer protocol implementation, plugin development tools, and Meltano project management.

**Version**: 0.9.0  
**Status**: 88% Complete - Production-capable  
**Python**: 3.13+

**CURRENT CAPABILITIES**:

- ✅ Complete Singer Protocol Implementation
- ✅ Meltano Integration
- ✅ DBT Operations
- ✅ Plugin Development Framework
- ✅ Enterprise Pipeline Orchestration
- ✅ FLEXT-Core Integration

**ECOSYSTEM INTEGRATION**:

- Foundation for 32+ FLEXT Projects (all flext-tap-_, flext-target-_, flext-dbt-\* projects)
- Zero Custom ELT Code - ABSOLUTE prohibition of custom Meltano/Singer/DBT implementations
- Enterprise Data Pipelines - Production-ready ELT orchestration

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests

# Meltano-specific
make meltano-install          # Install Meltano plugins
make meltano-run              # Run Meltano pipeline
```

---

## Key Patterns

### Singer Protocol Implementation

```python
from flext_core import FlextResult
from flext_meltano import FlextMeltano

meltano = FlextMeltano()

# Singer tap execution
result = meltano.run_tap("tap-ldap", config={...})
if result.is_success:
    records = result.unwrap()
```

### Meltano Project Management

```python
from flext_meltano import FlextMeltanoProject

project = FlextMeltanoProject("my-project")
result = project.initialize()
if result.is_success:
    print("Project initialized")
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:

- ❌ Custom Meltano/Singer/DBT implementations
- ❌ Direct Singer SDK imports outside flext-meltano
- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types

**MANDATORY**:

- ✅ Use `FlextResult[T]` for all operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations
- ✅ All ELT operations flow through flext-meltano

---

**See Also**:

- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-plugin Patterns](../flext-plugin/CLAUDE.md)
