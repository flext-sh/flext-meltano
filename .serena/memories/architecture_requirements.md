# FLEXT Architecture Requirements

## Foundation Architecture (Mandatory)

- **flext-core 0.9.9 RC**: Foundation library with 79% test coverage
- **Clean Architecture**: Layered structure with clear dependencies
- **Domain-Driven Design**: Entity/Value/AggregateRoot patterns
- **CQRS**: Command Query Responsibility Segregation
- **Railway Pattern**: FlextResult[T] for error handling

## Layer Structure (Copy to All Projects)

```
src/project_namespace/
├── Foundation Layer (Core Patterns)
│   ├── result.py              # FlextResult[T] railway pattern
│   ├── container.py           # Dependency injection
│   ├── exceptions.py          # Exception hierarchy
│   ├── constants.py           # FlextConstants, enums
│   └── protocols.py           # Interface definitions
│
├── Domain Layer (DDD Patterns)
│   ├── models.py              # Pydantic models
│   ├── service.py     # Domain services
│   └── root_models.py         # RootModel patterns
│
├── Application Layer (CQRS/Handlers)
│   ├── cqrs.py                # CQRS foundation
│   ├── handlers.py            # Handler implementations
│   ├── bus.py                 # Command routing
│   └── validation.py          # Validation framework
│
├── Infrastructure Layer
│   ├── config.py              # Configuration management
│   ├── loggings.py            # Structured logging
│   └── context.py             # Request context
│
└── Support Modules
    ├── mixins.py              # Reusable behaviors
    ├── utilities.py           # Helper functions
    └── services.py            # Service abstractions
```

## Domain Separation

- **flext-core**: Foundation library (result, container, models)
- **flext-cli**: CLI framework (wraps click/rich)
- **flext-api**: REST API services
- **flext-auth**: Authentication/authorization
- **flext-web**: Web interface
- **flext-ldap**: LDAP integration
- **flext-meltano**: Meltano integration
- **flext-grpc**: gRPC services
- **Singer Ecosystem**: Taps, targets, DBT transformations

## Dependency Rules

- **Use flext-core directly**: No wrappers, aliases, helpers
- **Domain boundaries**: Move logic to proper flext-\* library
- **Single responsibility**: One class per module
- **FlextContainer.get_global()**: Dependency injection
- **FlextResult[T]**: All operations return this for error handling
