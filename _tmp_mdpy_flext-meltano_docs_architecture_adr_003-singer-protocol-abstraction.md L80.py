# from flext-meltano/docs/architecture/adr/003-singer-protocol-abstraction.md:80
from __future__ import annotations


# Mock Singer SDK for unit testing
@pytest.fixture
def mock_singer_sdk():
    with patch("singer_sdk.Tap"):
        yield```
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

