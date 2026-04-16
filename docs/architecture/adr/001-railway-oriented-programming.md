# ADR-001: Railway-Oriented Programming with r[T]

<!-- TOC START -->
- [Context](#context)
- [Decision](#decision)
- [Rationale](#rationale)
  - [Why Railway-Oriented Programming](#why-railway-oriented-programming)
  - [Why r[T] from flext-core](#why-rt-from-flext-core)
- [Consequences](#consequences)
  - [Positive](#positive)
  - [Negative](#negative)
  - [Risks](#risks)
  - [Mitigation Strategies](#mitigation-strategies)
- [Alternatives Considered](#alternatives-considered)
  - [1. Traditional Exception Handling](#1-traditional-exception-handling)
  - [2. Custom Result Type](#2-custom-result-type)
  - [3. Async Exception Handling](#3-async-exception-handling)
  - [4. Callback-Based Error Handling](#4-callback-based-error-handling)
- [Implementation Details](#implementation-details)
  - [Error Type Hierarchy](#error-type-hierarchy)
  - [Railway Pattern Usage](#railway-pattern-usage)
  - [Testing Error Scenarios](#testing-error-scenarios)
- [Related ADRs](#related-adrs)
- [Notes](#notes)
<!-- TOC END -->

**Status**: Accepted | **Date**: 2025-01-15 | **Category**: 🏗️ Architecture

## Context

FLEXT-Meltano needs robust error handling for complex ELT operations involving multiple external systems (Meltano CLI, DBT, Singer SDK) and potential failure points. Traditional exception-based error handling becomes unwieldy in complex pipelines where:

- Multiple operations need to be chained together
- Partial failures need graceful handling
- Error context needs to be preserved through the pipeline
- Type safety needs to be maintained throughout error flows

The system needs to handle:

- Network failures when calling external CLIs
- Configuration validation errors
- Data transformation failures
- Resource allocation issues
- State persistence problems

## Decision

Implement railway-oriented programming using `r[T]` from flext-core, ensuring composable error handling throughout the entire codebase.

**Key Implementation Points:**

1. **All public APIs return `r[T]`**
1. **Internal methods may use exceptions for programming errors**
1. **Error types are specific and actionable**
1. **Railway pattern used for operation chaining**
1. **Type safety maintained in error flows**

## Rationale

### Why Railway-Oriented Programming

**Composability**: Operations can be chained safely without exception handling clutter

```python
result = (
    service
    .discover_plugins()
    .flat_map(lambda plugins: service.validate_plugins(plugins))
    .map(lambda valid_plugins: service.install_plugins(valid_plugins))
)
```

**Type Safety**: Error types are preserved through the entire flow

```python
def process_pipeline(settings: dict) -> p.Result[PipelineResult]:
    # Type checker knows result is either Success[PipelineResult] or Failure[Error]
    return r.ok(PipelineResult(...))
```

**Clarity**: Error handling is explicit and visible in the code structure

### Why r[T] from flext-core

**Consistency**: Aligns with FLEXT ecosystem patterns
**Maturity**: Proven implementation with comprehensive features
**Integration**: Works seamlessly with other FLEXT libraries

## Consequences

### Positive

- **Improved Reliability**: Explicit error handling prevents silent failures
- **Better Developer Experience**: Clear error types and messages
- **Type Safety**: Compile-time error checking for error flows
- **Testability**: Errors can be easily tested and asserted
- **Maintainability**: Error handling logic is centralized and consistent
- **Debugging**: Error context is preserved through operation chains

### Negative

- **Learning Curve**: Developers need to understand railway patterns
- **Boilerplate**: Additional code for result wrapping/unwrapping
- **Migration Effort**: Converting existing exception-based code
- **Performance**: Slight overhead from result object creation

### Risks

- **Adoption Resistance**: Team may resist pattern change
- **Inconsistent Usage**: Mix of result and exception handling
- **Error Type Proliferation**: Too many specific error types

### Mitigation Strategies

- **Training**: Comprehensive documentation and examples
- **Gradual Adoption**: Migrate modules incrementally
- **Code Generation**: Tools to automate result wrapping
- **Linting Rules**: Enforce consistent usage patterns

## Alternatives Considered

### 1. Traditional Exception Handling

- **Pros**: Familiar, built-in language feature
- **Cons**: Not composable, can cause silent failures, hard to test
- **Rejected**: Doesn't meet requirements for complex pipeline error handling

### 2. Custom Result Type

- **Pros**: Tailored to FLEXT-Meltano needs
- **Cons**: Reinventing the wheel, ecosystem fragmentation
- **Rejected**: Better to use proven flext-core implementation

### 3. Async Exception Handling

- **Pros**: Modern Python patterns
- **Cons**: Still not composable for complex flows
- **Rejected**: Same issues as traditional exceptions

### 4. Callback-Based Error Handling

- **Pros**: Explicit error paths
- **Cons**: Callback hell, hard to follow control flow
- **Rejected**: Poor readability and maintainability

## Implementation Details

### Error Type Hierarchy

```python
class FlextMeltanoError(Exception):
    """Base error for all FLEXT-Meltano operations."""


class ConfigurationError(FlextMeltanoError):
    """Configuration-related errors."""


class PluginError(FlextMeltanoError):
    """Plugin operation errors."""


class PipelineError(FlextMeltanoError):
    """Pipeline execution errors."""
```

### Railway Pattern Usage

```python
def create_and_run_pipeline(settings: PipelineConfig) -> p.Result[PipelineResult]:
    return (
        validate_config(settings)
        .flat_map(lambda cfg: discover_plugins(cfg))
        .flat_map(lambda plugins: validate_plugins(plugins))
        .flat_map(lambda valid_plugins: install_plugins(valid_plugins))
        .flat_map(lambda installed: run_pipeline(installed, settings))
        .map(lambda result: PipelineResult.from_execution(result))
    )
```

### Testing Error Scenarios

```python
def test_pipeline_failure_handling():
    # Given
    invalid_config = PipelineConfig(invalid_param="test")

    # When
    result = service.create_pipeline(invalid_config)

    # Then
    assert result.failure
    assert isinstance(result.error_value, ConfigurationError)
    assert "invalid_param" in str(result.error_value)
```

## Related ADRs

- [ADR-002](002-clean-architecture-ddd.md) - Clean Architecture patterns
- [ADR-008](008-error-handling-strategy.md) - Detailed error handling strategy
- [ADR-010](010-testing-strategy.md) - Testing strategy for error scenarios

## Notes

**Migration Plan:**

1. Phase 1: Core services (Completed)
1. Phase 2: Adapter layer (Completed)
1. Phase 3: API layer (Completed)
1. Phase 4: Legacy code cleanup (In Progress)

**Performance Impact:**

- Minimal overhead for success paths
- Error path performance acceptable for enterprise use cases
- Memory usage within acceptable limits

**Monitoring:**

- Error rates tracked via application metrics
- Common error patterns identified for improvement
- Error context preserved for debugging
