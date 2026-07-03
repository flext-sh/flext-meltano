# FLEXT Meltano Test Suite

<!-- TOC START -->

- [Overview](#overview)
- [Test Organization](#test-organization)
  - [Test Categories](#test-categories)
- [Test Execution](#test-execution)
  - [Quality Gates Integration](#quality-gates-integration)
  - [Test Configuration](#test-configuration)
- [Active Test Files](#active-test-files)
  - [Core Functionality Tests](#core-functionality-tests)
  - [Data Integration Tests](#data-integration-tests)
  - [Plugin Management Tests](#plugin-management-tests)
- [Test Standards](#test-standards)
  - [Test Documentation Requirements](#test-documentation-requirements)
  - [Test Implementation Standards](#test-implementation-standards)
- [Test Scope](#test-scope)
- [Test Organization](#test-organization)
  - [Quality Requirements](#quality-requirements)
- [Deprecated/Archived Tests](#deprecatedarchived-tests)
- [Test Development Workflow](#test-development-workflow)
  - [Adding New Tests](#adding-new-tests)
  - [Test Execution Patterns](#test-execution-patterns)
- [Integration with Quality Gates](#integration-with-quality-gates)
  - [CI/CD Integration](#cicd-integration)
  - [Pre-commit Hooks](#pre-commit-hooks)

<!-- TOC END -->

**Enterprise-Grade Testing Infrastructure**

## Overview

Comprehensive test suite for FLEXT Meltano's Go ↔ Python bridge library, implementing enterprise testing standards with 90%+ coverage requirements, comprehensive test categorization, and integration with quality gates.

## Test Organization

### Test Categories

#### **Unit Tests** (`unit/`)

- **Purpose**: Fast, isolated testing of individual components
- **Execution Time**: < 1 second per test
- **Coverage Target**: 95%+ for core modules
- **Dependencies**: None (mocked external dependencies)

#### **Integration Tests** (`integration/`)

- **Purpose**: Test component interactions and external dependencies
- **Execution Time**: < 30 seconds per test
- **Coverage**: End-to-end workflows with real dependencies
- **Dependencies**: PostgreSQL, Redis, file system access

#### **End-to-End Tests** (`e2e/`)

- **Purpose**: Complete workflow validation from API to data output
- **Execution Time**: < 5 minutes per test
- **Coverage**: Full pipeline execution scenarios
- **Dependencies**: All infrastructure services

#### **Extension Tests** (`extensions/`)

- **Purpose**: Test specialized extensions and add-ons
- **Execution Time**: Variable based on extension complexity
- **Coverage**: Oracle OIC and custom extension validation
- **Dependencies**: Extension-specific services

#### **Test Fixtures** (`fixtures/`)

- **Purpose**: Reusable test data and configuration
- **Content**: Sample data, mock configurations, test schemas
- **Format**: JSON, YAML, CSV files for test scenarios

## Test Execution

### Quality Gates Integration

```bash
# Mandatory pre-commit testing
make test                    # Run all core tests
make test-coverage          # Generate coverage report (90% minimum)
make test-integration       # Run integration tests
make test-e2e              # Run end-to-end tests (CI/CD only)

# Development workflow
pytest tests/unit/          # Fast unit tests only
pytest tests/integration/   # Integration tests with dependencies
pytest -m "not slow"       # Exclude slow tests for quick feedback
pytest --lf                # Run only last failed tests
```

### Test Configuration

```text
# conftest.py - Global test configuration
pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.meltano",
    "tests.fixtures.singer",
]

# Coverage requirements (enforced)
minimum_coverage = 90
fail_under = 90
```

## Active Test Files

### Core Functionality Tests

#### **Bridge Integration**

- **[`test_singer_integration.py`](test_singer_integration.py)** - ✅ Singer SDK re-exports and service creation
- **[`test_execution_comprehensive.py`](test_execution_comprehensive.py)** - ✅ Subprocess execution and result handling

#### **Base Components**

- **[`test_base_simple.py`](test_base_simple.py)** - ✅ Foundation classes and factory functions
- **[`test_base_coverage.py`](test_base_coverage.py)** - ✅ Comprehensive base module testing
- **[`test_core_library.py`](test_core_library.py)** - ✅ Core library functionality validation

#### **Command-Line Interface**

- **[`test_cli_comprehensive.py`](test_cli_comprehensive.py)** - ✅ CLI operations and command validation
- **[`test_cli_integration.py`](test_cli_integration.py)** - ✅ CLI integration with core services

### Data Integration Tests

#### **Singer Protocol**

- **[`test_flext_singer.py`](test_flext_singer.py)** - ✅ Singer SDK bridge and message handling
- **[`test_flext_singer_comprehensive.py`](test_flext_singer_comprehensive.py)** - ✅ Comprehensive Singer integration
- **[`test_flext_singer_coverage.py`](test_flext_singer_coverage.py)** - ✅ Complete Singer protocol coverage

#### **Meltano Integration**

- **[`test_meltano_integration.py`](test_meltano_integration.py)** - ✅ Meltano CLI integration and orchestration
- **[`test_discovery_complete.py`](test_discovery_complete.py)** - ✅ Plugin discovery and catalog management
- **[`test_real_catalog_discovery.py`](test_real_catalog_discovery.py)** - ✅ Real-world catalog discovery scenarios

#### **DBT Integration**

- **[`test_dbt_integration.py`](test_dbt_integration.py)** - ✅ DBT project management and execution
- **[`test_real_dbt_functionality.py`](test_real_dbt_functionality.py)** - ✅ Real DBT functionality validation

### Plugin Management Tests

#### **Installation & Discovery**

- **[`test_installation_simple.py`](test_installation_simple.py)** - ✅ Basic plugin installation workflows
- **[`test_installation_comprehensive.py`](test_installation_comprehensive.py)** - ✅ Complex installation scenarios
- **[`test_installation_real.py`](test_installation_real.py)** - ✅ Real plugin installation validation
- **[`test_installation_edge_cases.py`](test_installation_edge_cases.py)** - ✅ Error handling and edge cases

## Test Standards

### Test Documentation Requirements

Each test file must include:

1. **Module docstring** explaining test scope and purpose
1. **Class docstrings** describing test categories
1. **Method docstrings** with clear test descriptions
1. **Enterprise-grade commenting** for complex test logic
1. **English-only** documentation following professional standards

### Test Implementation Standards

```text
"""Test module following enterprise standards.

**Test Category**: Integration/Unit/E2E
**Coverage Target**: 90%+
**Dependencies**: List external dependencies
**Execution Time**: Expected execution time range

## Test Scope

Brief description of what this module tests and why.

## Test Organization

Description of test class organization and test method patterns.
"""


class TestModuleFunctionality:
    """Test class for specific functionality area.

    **Test Category**: Unit/Integration
    **Focus**: Specific component or workflow being tested
    """

    def test_specific_behavior(self):
        """Test specific behavior with clear expectations.

        **Given**: Initial state/conditions
        **When**: Action being tested
        **Then**: Expected outcomes
        """
        # Implementation with clear assertions
        assert result.success
        assert expected_value in result.data
```

### Quality Requirements

- **Coverage**: Minimum 90% line coverage per module
- **Performance**: Unit tests < 1s, Integration tests < 30s
- **Reliability**: Zero flaky tests allowed in CI/CD
- **Documentation**: All test files must have comprehensive docstrings
- **Isolation**: Tests must be independent and repeatable

## Deprecated/Archived Tests

The following test files are disabled or archived for historical reference:

- **`*.bak`** - Backup files from refactoring phases
- **`*.disabled`** - Temporarily disabled tests (with clear reasons)
- **`*.BROKEN`** - Known broken tests requiring investigation

These files are preserved for migration patterns and historical context but are not executed in the test suite.

## Test Development Workflow

### Adding New Tests

1. **Identify test category** (unit/integration/e2e)
1. **Create test file** following naming convention `test_<module>_<category>.py`
1. **Implement tests** following enterprise standards
1. **Add documentation** with comprehensive docstrings
1. **Verify coverage** meets 90% minimum requirement
1. **Integrate with CI/CD** via appropriate test markers

### Test Execution Patterns

```bash
# Development workflow
pytest tests/test_<module>.py -v     # Run specific test file
pytest tests/ -k "test_specific"     # Run tests matching pattern
pytest tests/ --collect-only         # Show available tests
pytest tests/ --durations=10         # Show slowest tests

# Coverage analysis (thresholds configured in pyproject.toml)
make test

# Quality validation
pytest tests/ --doctest-modules      # Validate docstring examples
pytest tests/ --mypy
```

## Integration with Quality Gates

### CI/CD Integration

```yaml
# Quality gate requirements
test_coverage_minimum: 90%
test_execution_timeout: 30m
flaky_test_tolerance: 0
documentation_coverage: aiming for 100%
```

### Pre-commit Hooks

- **Test execution**: All affected tests must pass
- **Coverage validation**: New code must meet coverage requirements
- **Documentation check**: Test docstrings must be complete
- **Performance validation**: Test execution time must be within limits

______________________________________________________________________

**Status**: ✅ **ENTERPRISE READY** - Comprehensive test suite with quality gates · 1.0.0 Release Preparation
**Coverage**: 90%+ across all test categories
**Last Updated**: 2025-08-02
**Maintainer**: FLEXT Development Team
