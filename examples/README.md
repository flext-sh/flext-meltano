# FLEXT Meltano Examples

**Enterprise Integration Examples and Usage Patterns**

## Overview

Comprehensive collection of working examples demonstrating FLEXT Meltano's Go ↔ Python bridge library usage patterns, from basic integration to advanced enterprise scenarios. All examples are tested, documented, and follow production-ready patterns.

## Example Categories

### **Basic Usage Examples**

#### **[basic_usage.py](basic_usage.py)** - ✅ Production Ready

**Purpose**: Fundamental bridge library usage patterns
**Scope**: Configuration, basic operations, result handling
**Target Audience**: New developers learning FLEXT Meltano
**Dependencies**: None (uses mocked operations)

```python
# Basic bridge integration example
from flext_meltano import FlextMeltanoConfig, create_meltano_tap_service

# Simple configuration and service creation
config = FlextMeltanoConfig(project_root="./meltano")
result = create_meltano_tap_service(config)
```

#### **[api_usage.py](api_usage.py)** - ✅ Production Ready

**Purpose**: Public API usage patterns and best practices
**Scope**: API imports, factory functions, service interactions
**Target Audience**: API consumers and integration developers
**Dependencies**: flext-core (FlextResult patterns)

### **Advanced Integration Examples**

#### **[enterprise_examples.py](enterprise_examples.py)** - ✅ Production Ready

**Purpose**: Enterprise-grade usage patterns with full error handling
**Scope**: Complex workflows, error recovery, monitoring integration
**Target Audience**: Enterprise architects and senior developers
**Dependencies**: All infrastructure components

#### **[singer_bridge_example.py](singer_bridge_example.py)** - ✅ Production Ready

**Purpose**: Singer SDK bridge integration patterns
**Scope**: Tap/target creation, stream processing, catalog management
**Target Audience**: Data engineers working with Singer protocol
**Dependencies**: Singer SDK, Meltano CLI

#### **[real_working_examples.py](real_working_examples.py)** - ✅ Production Ready

**Purpose**: Real-world scenarios with actual data processing
**Scope**: End-to-end pipeline execution, data validation, monitoring
**Target Audience**: Operations teams and data engineers
**Dependencies**: PostgreSQL, Redis, file system access

### **Code Quality & Architecture Examples**

#### **[code_reduction_examples.py](code_reduction_examples.py)** - ✅ Production Ready

**Purpose**: Demonstrate boilerplate reduction and code efficiency gains
**Scope**: Before/after comparisons, pattern consolidation, DRY principles
**Target Audience**: Developers evaluating FLEXT Meltano adoption
**Dependencies**: Comparison frameworks (for before/after demonstrations)

#### **[code_reduction_showcase.py](code_reduction_showcase.py)** - ✅ Production Ready

**Purpose**: Showcase architectural improvements and simplification
**Scope**: Complex scenario simplification, enterprise pattern usage
**Target Audience**: Technical leaders and architects
**Dependencies**: Enterprise pattern libraries

#### **[simplified_imports_demo.py](simplified_imports_demo.py)** - ✅ Production Ready

**Purpose**: Import simplification and namespace organization
**Scope**: Clean import patterns, namespace usage, API surface
**Target Audience**: Library users optimizing imports
**Dependencies**: Core library modules only

### **Utility & Helper Examples**

#### **[constants_usage.py](constants_usage.py)** - ✅ Production Ready

**Purpose**: Constants and configuration management patterns
**Scope**: Environment variables, configuration validation, defaults
**Target Audience**: DevOps and configuration management teams
**Dependencies**: Environment configuration utilities

#### **[quick_start_guide.py](quick_start_guide.py)** - ✅ Production Ready

**Purpose**: Rapid onboarding and first-time user experience
**Scope**: Minimal setup, quick wins, basic operations
**Target Audience**: New users getting started with FLEXT Meltano
**Dependencies**: Minimal (designed for first-time setup)

## Usage Patterns

### Running Examples

```bash
# Setup environment for examples
cd examples/
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt  # If available
# OR install FLEXT Meltano
pip install -e ../

# Run basic examples
python basic_usage.py
python api_usage.py

# Run advanced examples (requires infrastructure)
docker-compose up -d postgres redis  # Start dependencies
python enterprise_examples.py
python real_working_examples.py
```

### Development Workflow

```bash
# Test all examples
pytest examples/ --doctest-modules

# Validate example code quality
ruff check examples/
mypy examples/

# Run examples in CI/CD
make test-examples
```

## Example Standards

### Documentation Requirements

Each example file must include:

1. **Module docstring** with clear purpose and scope
2. **Enterprise-grade comments** explaining complex operations
3. **Usage instructions** with setup requirements
4. **Expected output** descriptions
5. **Error handling** demonstrations where applicable

### Code Quality Standards

```python
"""Example module following enterprise documentation standards.

**Purpose**: Clear description of what this example demonstrates
**Scope**: Specific functionality or patterns covered
**Target Audience**: Who should use this example
**Dependencies**: External dependencies required

## Usage

python example_module.py

## Expected Output

Description of what users should see when running the example.
"""

from typing import Any

from flext_meltano import FlextMeltanoConfig

def demonstrate_pattern() -> dict[str, Any]:
    """Demonstrate specific pattern with clear documentation.

    Returns:
        Dictionary containing demonstration results with status and data.

    Example:
        >>> result = demonstrate_pattern()
        >>> assert result["status"] == "success"
    """
    # Implementation with enterprise patterns
    return {"status": "success", "data": "demonstration_complete"}
```

### Testing Integration

All examples are validated through:

- **Doctest validation**: Code examples in docstrings are tested
- **Static analysis**: Type checking and linting validation
- **Import validation**: All imports must resolve correctly
- **Output validation**: Expected outputs are verified in CI/CD

## Integration with Documentation

### Cross-Reference System

Examples are integrated with the comprehensive documentation system:

- **[Main Documentation](../docs/README.md)** - Complete navigation system
- **[API Documentation](../docs/api/README.md)** - API reference with examples
- **[Development Guide](../docs/guides/development.md)** - Development workflows
- **[Getting Started](../docs/guides/getting-started.md)** - First-time setup

### Example Categories in Documentation

- **🚀 New Developers**: [basic_usage.py](basic_usage.py), [quick_start_guide.py](quick_start_guide.py)
- **🏗️ Enterprise Architects**: [enterprise_examples.py](enterprise_examples.py), [code_reduction_showcase.py](code_reduction_showcase.py)
- **📊 Data Engineers**: [singer_bridge_example.py](singer_bridge_example.py), [real_working_examples.py](real_working_examples.py)
- **⚙️ Operations Teams**: [constants_usage.py](constants_usage.py), [api_usage.py](api_usage.py)

## Contributing Examples

### Adding New Examples

1. **Identify use case** - Clear problem or pattern to demonstrate
2. **Create example file** - Follow naming convention `[category]_[purpose].py`
3. **Implement with documentation** - Comprehensive docstrings and comments
4. **Add to this README** - Update appropriate category section
5. **Test integration** - Ensure example runs correctly and passes validation

### Quality Requirements

- **Executable**: All examples must run without errors
- **Documented**: Comprehensive docstrings and inline comments
- **Production-Ready**: Follow enterprise coding standards
- **Tested**: Integration with CI/CD validation pipeline
- **Cross-Referenced**: Linked to relevant documentation sections

---

**Status**: ✅ **ENTERPRISE READY** - Production-quality examples with comprehensive documentation
**Coverage**: All major usage patterns and integration scenarios
**Last Updated**: 2025-08-02
**Maintainer**: FLEXT Development Team
