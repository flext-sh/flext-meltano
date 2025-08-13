# flext-meltano

**Type**: Infrastructure Library | **Status**: Active Development | **Dependencies**: flext-core

Meltano/Singer integration library providing data pipeline orchestration for the FLEXT ecosystem.

> ⚠️ Development Status: Go-Python bridge working; core functionality largely complete; ~74% coverage (90% target).

## Quick Start

```bash
# Install dependencies
poetry install

# Test basic functionality
python -c "from flext_meltano import FlextMeltanoBridge; bridge = FlextMeltanoBridge(); print('✅ Working')"

# Development setup
make setup
```

## Current Reality

**What Actually Works:**

- Go-Python bridge integration via FlextMeltanoBridge
- Meltano CLI execution through subprocess patterns
- Singer SDK integration (taps, targets, transformations)
- DBT project management and execution
- Plugin discovery and installation

**What Needs Work:**

- Test coverage improvement (74% → 90% target)
- Quality gate compliance (coverage requirement blocking)
- Monitoring stack integration
- Production deployment patterns

## Architecture Role in FLEXT Ecosystem

### **Infrastructure Component**

FLEXT Meltano provides data pipeline orchestration between Go services and Python data ecosystem:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (32 Projects)                 │
├─────────────────────────────────────────────────────────────────┤
│ Services: FlexCore(Go) | FLEXT Service(Go/Python) | Clients     │
├─────────────────────────────────────────────────────────────────┤
│ Applications: API | Auth | Web | CLI | Quality | Observability  │
├═════════════════════════════════════════════════════════════════┤
│ Infrastructure: Oracle | LDAP | LDIF | gRPC | [FLEXT-MELTANO]   │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem: Taps(5) | Targets(5) | DBT(4) | Extensions(1) │
├─────────────────────────────────────────────────────────────────┤
│ Foundation: FLEXT-CORE (FlextResult | DI | Domain Patterns)     │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Responsibilities**

1. **Go-Python Bridge**: Enable Go services to execute Meltano operations via subprocess
2. **Pipeline Orchestration**: ELT pipeline management using Meltano runtime
3. **Singer Integration**: Complete integration with Singer SDK for taps/targets

## Key Features

### **Current Capabilities**

- **Go-Python Bridge**: FlextMeltanoBridge class for Go service integration
- **Meltano Integration**: Subprocess-based CLI execution with FlextResult patterns
- **Singer SDK**: Complete tap/target/transformation support
- **DBT Integration**: Project management and transformation execution

### **FLEXT Core Integration**

- **FlextResult Pattern**: Type-safe error handling for all operations
- **Subprocess Orchestration**: Reliable command execution with result handling
- **Enterprise Patterns**: Clean Architecture and dependency injection

## Installation & Usage

### Installation

```bash
# Clone and install
cd /path/to/flext-meltano
poetry install

# Development setup
make setup
make meltano-init
```

### Basic Usage

```python
from flext_meltano import FlextMeltanoBridge
from flext_meltano.execution import execute_meltano_command, run_pipeline

# Go-Python bridge
bridge = FlextMeltanoBridge()
version_result = bridge.get_version()
if version_result.success:
    print(f"Meltano version: {version_result.data['meltano']}")

# Direct Meltano execution
result = execute_meltano_command(["--version"])
if result.success:
    print(f"Output: {result.data}")

# Pipeline execution
pipeline_result = run_pipeline("tap-csv", "target-csv")
```

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation pipeline (run before commits)
make validate              # Full validation (lint + type + security + test)
make check                 # Quick lint + type check
make test                  # Run all tests (90% coverage requirement)
make lint                  # Code linting
make type-check            # Type checking
make format                # Code formatting
make security              # Security scanning
```

### Meltano Operations

```bash
# Meltano setup and operations
make meltano-init          # Initialize Meltano project
make meltano-install       # Install Meltano plugins
make meltano-run JOB=job-name  # Run specific pipeline
make meltano-test          # Test Meltano configuration
make test-pipeline         # Run basic CSV test pipeline
```

## Configuration

### Environment Variables

```bash
# Meltano configuration
export MELTANO_ENVIRONMENT=dev
export MELTANO_PROJECT_ROOT=$(PWD)

# Python path setup
export PYTHONPATH=$(PWD)/src:$(PYTHONPATH)
```

## Quality Standards

### **Quality Targets**

- **Coverage**: 90% target (currently ~74%)
- **Type Safety**: MyPy strict mode adopted (work in progress)
- **Linting**: Ruff with comprehensive rules (minor issues may remain)
- **Security**: Bandit + pip-audit scanning

## Integration with FLEXT Ecosystem

### **FLEXT Core Patterns**

```python
# FlextResult for all operations
from flext_meltano.execution import FlextMeltanoExecutionResult

result = execute_meltano_command(["--version"])
if result.success:
    print(f"Output: {result.data}")
else:
    print(f"Error: {result.error_message}")
```

### **Service Integration**

- **FlexCore (Go)**: Bridge integration via subprocess calls
- **FLEXT Service**: Python library integration for pipeline orchestration
- **Singer Ecosystem**: Native tap/target support with 15 Singer projects

## Current Status

**Version**: 2.0.0-enterprise (Development)

**Completed**:

- ✅ Go-Python bridge integration (FlextMeltanoBridge)
- ✅ Meltano CLI execution with subprocess patterns
- ✅ Singer SDK integration and DBT project management
- ✅ Type safety baseline in place; strict compliance in progress

**In Progress**:

- 🔄 Test coverage improvement (74% → 90%)
- 🔄 Quality gate compliance
- 🔄 Production deployment patterns

**Planned**:

- 📋 Enhanced monitoring integration
- 📋 Performance optimization
- 📋 Advanced pipeline orchestration

## Contributing

### Development Standards

- **FLEXT Core Integration**: Use established patterns
- **Type Safety**: All code must pass MyPy
- **Testing**: Maintain 90% coverage
- **Code Quality**: Follow linting rules

### Development Workflow

```bash
# Setup and validate
make setup
make validate
make test
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Links

- **[flext-core](../flext-core)**: Foundation library
- **[CLAUDE.md](CLAUDE.md)**: Development guidance
- **[Documentation](docs/)**: Complete documentation

---

 
