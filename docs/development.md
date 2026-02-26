# Development Guide

<!-- TOC START -->

- [🎯 Project Overview](#project-overview)
- [🛠️ Development Setup](#development-setup)
  - [**Prerequisites**](#prerequisites)
  - [**Initial Setup**](#initial-setup)
- [🔧 Development Workflow](#development-workflow)
  - [**Quality Gates**](#quality-gates)
  - [**Code Standards**](#code-standards)
  - [**Testing Strategy**](#testing-strategy)
- [🏗️ Architecture Constraints](#architecture-constraints)
  - [**Current Compliance Issues**](#current-compliance-issues)
  - [**FLEXT Ecosystem Requirements**](#flext-ecosystem-requirements)
- [📊 Code Metrics](#code-metrics)
  - [**Current Implementation**](#current-implementation)
  - [**Priority Improvements**](#priority-improvements)
- [🧪 Testing Guidelines](#testing-guidelines)
  - [**Test Organization**](#test-organization)
  - [**Running Tests**](#running-tests)
- [🔍 Debugging and Development](#debugging-and-development)
  - [**Common Issues**](#common-issues)
  - [**Development Tools**](#development-tools)
- [📚 Contributing Guidelines](#contributing-guidelines)
  - [**Code Review Checklist**](#code-review-checklist)
  - [**Architecture Compliance**](#architecture-compliance)
- [🎯 Development Priorities](#development-priorities)
  - [**Immediate (Next Sprint)**](#immediate-next-sprint)
  - [**Short Term (Next Month)**](#short-term-next-month)
  - [**Long Term (Next Quarter)**](#long-term-next-quarter)

<!-- TOC END -->

**Development workflow for the flext-meltano project**

**Last Updated**: 2025-09-17

---

## 🎯 Project Overview

This is a dual-purpose project:

- **Meltano ELT Project**: Working pipeline with tap-csv configuration
- **Python Library**: Abstractions for FLEXT ecosystem integration

**Current Status**: 7,286 lines of source code with 13,970 lines of tests. Architecture compliance needs improvement.

---

## 🛠️ Development Setup

### **Prerequisites**

- Python 3.13+
- Poetry for dependency management
- Access to FLEXT workspace virtual environment

### **Initial Setup**

```bash
# Navigate to project
cd ..flext-meltano

# Activate FLEXT workspace environment
source ../.venv/bin/activate

# Install dependencies
poetry install --with dev,test

# Verify setup
make lint type-check test
```

---

## 🔧 Development Workflow

### **Quality Gates**

```bash
# Pre-commit checks (must pass)
make validate           # Complete validation pipeline
make lint               # Ruff linting
make type-check         # MyPy strict mode
make test               # Test suite execution
```

### **Code Standards**

- **Architecture**: Single class per module with nested helpers
- **Error Handling**: FlextResult pattern for all operations
- **Type Safety**: Comprehensive type annotations with Pydantic
- **Import Policy**: Root-level imports only from flext_meltano

### **Testing Strategy**

- **Unit Tests**: Component-level validation
- **Integration Tests**: Real API integration where possible
- **Test Coverage**: Current 2:1 test-to-source ratio (comprehensive)

---

## 🏗️ Architecture Constraints

### **Current Compliance Issues**

- **Direct Imports**: `src/flext_meltano/adapters.py` contains meltano.core imports
- **Abstraction Layer**: Needs implementation to wrap external dependencies
- **Plugin Integration**: Limited beyond basic tap-csv configuration

### **FLEXT Ecosystem Requirements**

- Use only flext-core foundation patterns
- Implement FlextResult railway-oriented programming
- Follow single responsibility principle
- Maintain comprehensive type safety

---

## 📊 Code Metrics

### **Current Implementation**

| Component   | Lines  | Quality        |
| ----------- | ------ | -------------- |
| Source Code | 7,286  | Substantial    |
| Test Code   | 13,970 | Comprehensive  |
| Modules     | 20     | Well-organized |

### **Priority Improvements**

1. Resolve direct import violations
1. Implement abstraction layer for external libraries
1. Expand Meltano plugin configuration
1. Complete integration testing coverage

---

## 🧪 Testing Guidelines

### **Test Organization**

```bash
tests/
├── unit/           # Component unit tests
├── integration/    # API integration tests
├── e2e/           # End-to-end workflow tests
└── fixtures/      # Test data and utilities
```

### **Running Tests**

```bash
# All tests
make test

# Specific categories
pytest tests/unit/ -v
pytest tests/integration/ -v

# With coverage
pytest --cov=src --cov-report=html
```

---

## 🔍 Debugging and Development

### **Common Issues**

- **Import Errors**: Ensure PYTHONPATH includes src directory
- **Type Errors**: Run `make type-check` for detailed MyPy output
- **Test Failures**: Check test isolation and fixture setup

### **Development Tools**

```bash
# Format code
make format

# Quick checks
make l          # lint
make t          # test
make c         # type-check
```

---

## 📚 Contributing Guidelines

### **Code Review Checklist**

- [ ] All quality gates pass
- [ ] Type annotations present
- [ ] FlextResult pattern used for error handling
- [ ] No direct external library imports
- [ ] Tests updated for new functionality

### **Architecture Compliance**

- Use only FLEXT ecosystem imports
- Follow single class per module pattern
- Implement proper error handling with FlextResult
- Maintain comprehensive documentation

---

## 🎯 Development Priorities

### **Immediate (Next Sprint)**

1. Implement abstraction layer for meltano.core imports
1. Expand integration test coverage
1. Document actual vs claimed functionality

### **Short Term (Next Month)**

1. Complete plugin architecture foundation
1. Resolve all architecture compliance issues
1. Expand Meltano project configuration

### **Long Term (Next Quarter)**

1. Production deployment readiness
1. Performance optimization
1. Comprehensive ecosystem integration

---

**Development Status**: Active development with focus on architecture compliance and realistic capability documentation.
