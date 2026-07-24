# ADR-003: Singer Protocol Abstraction Layer

<!-- TOC START -->
- [Context](#context)
- [Decision](#decision)
- [Rationale](#rationale)
  - [Why Abstraction Layer](#why-abstraction-layer)
  - [Why Not Direct SDK Usage](#why-not-direct-sdk-usage)
- [Consequences](#consequences)
  - [Positive](#positive)
  - [Negative](#negative)
  - [Risks](#risks)
  - [Mitigation Strategies](#mitigation-strategies)
- [Alternatives Considered](#alternatives-considered)
  - [1. Direct Singer SDK Usage](#1-direct-singer-sdk-usage)
  - [2. Thin Wrapper Only](#2-thin-wrapper-only)
  - [3. Complete Protocol Reimplementation](#3-complete-protocol-reimplementation)
- [Implementation Details](#implementation-details)
  - [Abstraction Hierarchy](#abstraction-hierarchy)
  - [Error Handling Integration](#error-handling-integration)
  - [State Management](#state-management)
- [Related ADRs](#related-adrs)
- [Notes](#notes)
<!-- TOC END -->

**Status**: Accepted | **Date**: 2025-02-01 | **Category**: 🏗️ Architecture

## Context

FLEXT-Meltano needs to integrate with the Singer protocol for data extraction and loading, but direct use of the Singer SDK would create tight coupling and prevent FLEXT ecosystem integration. The system must:

- Implement Singer taps and targets following FLEXT patterns
- Provide type-safe interfaces for Singer operations
- Handle Singer-specific error conditions appropriately
- Maintain consistency with FLEXT error handling and logging
- Support both custom and existing Singer plugins
- Enable testing without external Singer dependencies

## Decision

Create a comprehensive abstraction layer over the Singer SDK that provides FLEXT ecosystem integration while maintaining protocol compliance.

**Key Abstractions:**

1. **FlextMeltanoTap** - Abstract base class for Singer taps
1. **FlextMeltanoTarget** - Abstract base class for Singer targets
1. **FlextMeltanoStream** - Stream abstraction with FLEXT patterns
1. **SingerProtocolService** - Protocol coordination and state management

## Rationale

### Why Abstraction Layer

**FLEXT Ecosystem Consistency**: Ensures all Singer implementations follow FLEXT patterns

```python
from __future__ import annotations


# FLEXT pattern - Railway-oriented, type-safe
class MyCustomTap(FlextMeltanoTap):
    def discover_streams(self) -> p.Result[List[FlextMeltanoStream]]:
        return r.ok([MyStream(self)])
```

**Error Handling**: Consistent error handling across all Singer operations

```python
# Automatic error wrapping and context preservation
result = tap.discover_streams()
if result.failure:
    # FLEXT error handling patterns
    logger.error(f"Stream discovery failed: {result.error}")
```

**Testability**: Singer components can be tested in isolation

```python
from __future__ import annotations


# Mock Singer SDK for unit testing
@pytest.fixture
def mock_singer_sdk():
    with patch("singer_sdk.Tap"):
        yield
```

### Why Not Direct SDK Usage

**Tight Coupling**: Direct Singer SDK usage creates external dependencies
**Inconsistent Patterns**: SDK patterns don't align with FLEXT error handling
**Testing Challenges**: External dependencies make testing difficult
**Evolution Barriers**: SDK changes could break FLEXT integrations

## Consequences

### Positive

- **Consistency**: All Singer implementations follow FLEXT patterns
- **Maintainability**: Changes to Singer SDK isolated to abstraction layer
- **Testability**: Components can be tested without external dependencies
- **Type Safety**: Full type annotations for Singer operations
- **Error Handling**: Consistent error patterns across all operations

### Negative

- **Abstraction Overhead**: Additional layer between FLEXT and Singer
- **Maintenance Burden**: Abstraction layer must be kept in sync with SDK
- **Learning Curve**: Developers need to understand both layers
- **Performance Impact**: Slight overhead from abstraction

### Risks

- **SDK Changes**: Singer SDK evolution could break abstractions
- **Feature Lag**: New SDK features take time to abstract
- **Complexity**: Understanding both FLEXT and Singer patterns

### Mitigation Strategies

- **Automated Testing**: Comprehensive tests for abstraction layer
- **SDK Monitoring**: Track Singer SDK changes and releases
- **Documentation**: Clear guidance on when to use abstractions
- **Code Generation**: Tools to generate boilerplate code

## Alternatives Considered

### 1. Direct Singer SDK Usage

- **Pros**: No abstraction overhead, direct access to features
- **Cons**: Tight coupling, inconsistent patterns, testing issues
- **Rejected**: Violates FLEXT ecosystem consistency requirements

### 2. Thin Wrapper Only

- **Pros**: Minimal overhead, close to direct usage
- **Cons**: Still exposes SDK patterns, limited FLEXT integration
- **Rejected**: Doesn't provide sufficient FLEXT ecosystem benefits

### 3. Complete Protocol Reimplementation

- **Pros**: Full control, no external dependencies
- **Cons**: Massive effort, protocol compliance risks
- **Rejected**: Unnecessary complexity, maintenance burden too high

## Implementation Details

### Abstraction Hierarchy

```python
from __future__ import annotations


# Base abstractions
class FlextMeltanoSingerBase:
    """Base class for all Singer operations with FLEXT patterns."""


class FlextMeltanoTap(FlextMeltanoSingerBase, SingerTap):
    """FLEXT tap abstraction with railway-oriented error handling."""


class FlextMeltanoTarget(FlextMeltanoSingerBase, SingerTarget):
    """FLEXT target abstraction with railway-oriented error handling."""


class FlextMeltanoStream(FlextMeltanoSingerBase):
    """Stream abstraction with FLEXT state management."""
```

### Error Handling Integration

```python
from __future__ import annotations


class FlextMeltanoTap(FlextMeltanoSingerBase):
    def discover_streams(self) -> p.Result[List[FlextMeltanoStream]]:
        try:
            # Singer SDK operations
            streams = super().discover_streams()
            # Convert to FLEXT streams
            flext_streams = [FlextMeltanoStream.from_sdk(stream) for stream in streams]
            return r.ok(flext_streams)
        except Exception as e:
            return r.fail(SingerError(f"Stream discovery failed: {e}"))

    def run_tap(self, settings: dict, state: dict) -> p.Result[TapResult]:
        # Railway pattern for tap execution
        return (
            self
            .validate_config(settings)
            .flat_map(lambda _: self.initialize_state(state))
            .flat_map(lambda _: self.execute_streams())
            .map(lambda result: TapResult.from_execution(result))
        )
```

### State Management

```python
from __future__ import annotations


class FlextMeltanoStream:
    def get_records(self, context: Optional[dict]) -> Iterator[dict]:
        """Get records with FLEXT state management."""
        try:
            # Singer SDK record retrieval
            for record in super().get_records(context):
                # FLEXT state updates
                self.update_bookmark(record)
                yield record
        except Exception as e:
            # FLEXT error handling
            logger.error(f"Record retrieval failed: {e}")
            raise SingerStreamError(f"Stream {self.name} failed: {e}")
```

## Related ADRs

- [ADR-001](001-railway-oriented-programming.md) - Error handling patterns
- [ADR-002](002-clean-architecture-ddd.md) - Architecture layering
- [ADR-004](004-type-safety-first.md) - Type safety requirements

## Notes

**SDK Compatibility:**

- Tested with Singer SDK v0.44.0
- Compatibility layer for major version changes
- Automated testing against multiple SDK versions

**Performance Considerations:**

- Minimal overhead for normal operations
- Error paths optimized for fast failure
- Memory usage within acceptable limits

**Migration Path:**

- Existing direct SDK usage migrated incrementally
- New implementations use abstraction layer exclusively
- Legacy code wrapped with compatibility adapters
