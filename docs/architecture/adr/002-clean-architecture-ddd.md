# ADR-002: Clean Architecture with Domain-Driven Design

<!-- TOC START -->

- [Context](#context)
- [Decision](#decision)
- [Rationale](#rationale)
  - [Why Clean Architecture](#why-clean-architecture)
  - [Why Domain-Driven Design](#why-domain-driven-design)
- [Consequences](#consequences)
  - [Positive](#positive)
  - [Negative](#negative)
  - [Risks](#risks)
  - [Mitigation Strategies](#mitigation-strategies)
- [Alternatives Considered](#alternatives-considered)
  - [1. Traditional Layered Architecture](#1-traditional-layered-architecture)
  - [2. Hexagonal Architecture (Ports & Adapters)](#2-hexagonal-architecture-ports-adapters)
  - [3. Microservices Architecture](#3-microservices-architecture)
  - [4. Event-Driven Architecture](#4-event-driven-architecture)
- [Implementation Details](#implementation-details)
  - [Layer Structure](#layer-structure)
  - [Layer Interaction Rules](#layer-interaction-rules)
  - [Dependency Injection](#dependency-injection)
- [Related ADRs](#related-adrs)
- [Notes](#notes)

<!-- TOC END -->

**Status**: Accepted | **Date**: 2025-01-20 | **Category**: 🏗️ Architecture

## Context

FLEXT-Meltano integrates with complex external systems (Meltano, DBT, Singer SDK) while needing to remain maintainable, testable, and evolvable. The system must:

- Handle frequent changes in external APIs and protocols
- Support testing of business logic without external dependencies
- Allow independent evolution of different system parts
- Maintain clear boundaries between business rules and external concerns
- Support multiple deployment scenarios and use cases

Traditional layered architecture approaches often lead to tight coupling between business logic and external systems, making testing difficult and evolution challenging.

## Decision

Implement Clean Architecture with Domain-Driven Design, establishing clear boundaries between:

1. **API Layer** - External interfaces and adapters
1. **Application Layer** - Use cases and application logic
1. **Domain Layer** - Business rules and entities
1. **Infrastructure Layer** - External system integration

**Key Architectural Elements:**

- **Dependency Inversion**: Inner layers don't depend on outer layers
- **Single Responsibility**: Each class/module has one reason to change
- **Explicit Boundaries**: Clear interfaces between layers
- **Domain-Centric Design**: Business logic drives architectural decisions

## Rationale

### Why Clean Architecture

**Testability**: Business logic can be tested without external dependencies

```python
# Domain logic testable in isolation
def test_pipeline_validation():
    validator = PipelineValidator()
    result = validator.validate_config(invalid_config)
    assert result.is_failure
```

**Maintainability**: Changes to external systems don't affect business logic

```python
# Adapter pattern allows external system changes
class MeltanoAdapter:
    def run_tap(self, config) -> FlextResult[TapResult]:
        # Implementation can change without affecting callers
```

**Evolvability**: System can evolve independently in each layer

- Domain rules can change without affecting external integrations
- External APIs can change without affecting business logic
- New delivery mechanisms can be added without changing core logic

### Why Domain-Driven Design

**Business Alignment**: Architecture reflects business domain structure

- `Pipeline` as a domain concept
- `Plugin` as a domain entity
- `SingerProtocol` as a domain service

**Ubiquitous Language**: Shared vocabulary between technical and business teams

- "Tap" and "Target" as domain terms
- "Pipeline execution" as a business process
- "State management" as a domain concern

## Consequences

### Positive

- **Separation of Concerns**: Clear boundaries between different aspects
- **Testability**: High test coverage possible due to isolation
- **Flexibility**: Easy to change external dependencies
- **Maintainability**: Changes localized to specific layers
- **Evolvability**: Independent evolution of different system parts
- **Business Focus**: Architecture reflects business domain

### Negative

- **Complexity**: Additional abstraction layers and interfaces
- **Indirection**: More classes and interfaces to navigate
- **Learning Curve**: Understanding layered architecture patterns
- **Upfront Cost**: More initial design and implementation effort
- **Communication Overhead**: Coordination between layers

### Risks

- **Over-Engineering**: Creating unnecessary abstractions
- **Layer Leaks**: Dependencies creeping through layer boundaries
- **Performance Overhead**: Indirection affecting performance
- **Team Resistance**: Pushback against additional complexity

### Mitigation Strategies

- **Iterative Application**: Start with simpler structure, add layers as needed
- **Clear Guidelines**: Document layer responsibilities and interaction patterns
- **Automated Checks**: Linting rules to prevent layer violations
- **Refactoring**: Ability to simplify architecture if complexity not justified

## Alternatives Considered

### 1. Traditional Layered Architecture

- **Pros**: Simple, familiar, less abstraction
- **Cons**: Business logic coupled to infrastructure, hard to test
- **Rejected**: Doesn't provide sufficient isolation for complex integrations

### 2. Hexagonal Architecture (Ports & Adapters)

- **Pros**: Very clean separation, excellent testability
- **Cons**: Complex for this domain, overkill for current needs
- **Rejected**: Clean Architecture provides similar benefits with less complexity

### 3. Microservices Architecture

- **Pros**: Independent deployment, scalability
- **Cons**: Operational complexity, distributed system challenges
- **Rejected**: Single deployable unit better suits current requirements

### 4. Event-Driven Architecture

- **Pros**: Loose coupling, scalability
- **Cons**: Complexity for synchronous operations
- **Rejected**: Request-response patterns dominate current use cases

## Implementation Details

### Layer Structure

```
src/flext_meltano/
├── api.py                    # 🚪 API Layer - External interfaces
├── services.py               # 🎯 Application Layer - Use cases
├── adapters.py               # 🔌 Infrastructure Layer - External integrations
├── models.py                 # 📦 Domain Layer - Business entities
├── config.py                 # ⚙️ Infrastructure Layer - Configuration
├── exceptions.py             # 🚨 Domain Layer - Business errors
└── __init__.py               # 🚪 API Layer - Public interface
```

### Layer Interaction Rules

**API Layer → Application Layer**

```python
# api.py
def create_pipeline(config: dict) -> FlextResult[Pipeline]:
    return FlextMeltanoService().create_pipeline(config)
```

**Application Layer → Domain Layer**

```python
# services.py
def create_pipeline(self, config: dict) -> FlextResult[Pipeline]:
    validated_config = self.config_validator.validate(config)
    return validated_config.map(lambda cfg: Pipeline.create(cfg))
```

**Application Layer → Infrastructure Layer**

```python
# services.py
def execute_pipeline(self, pipeline: Pipeline) -> FlextResult[ExecutionResult]:
    return self.meltano_adapter.run_pipeline(pipeline)
```

### Dependency Injection

```python
# Service initialization with dependencies
@dataclass
class FlextMeltanoService:
    config_validator: ConfigValidator
    meltano_adapter: MeltanoAdapter
    dbt_adapter: FlextMeltanoAdapter.Dbt

    def execute_pipeline(self, pipeline: Pipeline) -> FlextResult[ExecutionResult]:
        # Use injected dependencies
        return (
            self.config_validator.validate(pipeline.config)
            .flat_map(lambda _: self.meltano_adapter.run_pipeline(pipeline))
            .flat_map(lambda result: self.dbt_adapter.run_transformations(result))
        )
```

## Related ADRs

- [ADR-001](001-railway-oriented-programming.md) - Error handling patterns
- [ADR-003](003-singer-protocol-abstraction.md) - Protocol abstraction layer

## Notes

**Evolution Considerations:**

- Start with basic layered structure
- Add complexity only when justified by use cases
- Monitor for over-engineering and simplify when possible
- Consider hexagonal architecture for future growth

**Performance Impact:**

- Minimal impact on normal operation paths
- Test performance improved due to isolation
- Development velocity improved due to clear boundaries

**Team Adoption:**

- Training provided on layered architecture concepts
- Code reviews enforce layer boundary rules
- Automated tools validate architectural compliance
