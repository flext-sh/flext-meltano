# from flext-meltano/docs/architecture/adr/002-clean-architecture-ddd.md:79
from __future__ import annotations
# Adapter pattern allows external system changes
class MeltanoAdapter:
    def run_tap(self, settings) -> p.Result[TapResult]:
        # Implementation can change without affecting callers```
**Evolvability**: System can evolve independently in each layer

- Domain rules can change without affecting external integrations
- External APIs can change without affecting business logic
- New delivery mechanisms can be added without changing core logic

### Why Domain-Driven Design

**Business Alignment**: Architecture reflects business domain structure

- `Pipeline` as a domain concept
- `Plugin` as a domain entity
- `Singer` as a domain service

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

### Layer Structure```
src/flext_meltano/
├── api.py                    # 🚪 API Layer - External interfaces
├── services.py               # 🎯 Application Layer - Use cases
├── adapters.py               # 🔌 Infrastructure Layer - External integrations
├── models.py                 # 📦 Domain Layer - Business entities
├── settings.py                 # ⚙️ Infrastructure Layer - Configuration
├── exceptions.py             # 🚨 Domain Layer - Business errors
└── __init__.py               # 🚪 API Layer - Public interface```
### Layer Interaction Rules

**API Layer → Application Layer**

