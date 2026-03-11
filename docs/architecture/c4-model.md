# C4 Model Architecture Documentation

<!-- TOC START -->

- [📋 Table of Contents](#table-of-contents)
- [🎯 Context Diagram (Level 1)](#context-diagram-level-1)
  - [System Purpose](#system-purpose)
  - [Key Relationships](#key-relationships)
- [🏗️ Container Diagram (Level 2)](#container-diagram-level-2)
  - [Container Overview](#container-overview)
  - [Container Responsibilities](#container-responsibilities)
- [🔧 Component Diagram (Level 3)](#component-diagram-level-3)
  - [Service Layer Components](#service-layer-components)
  - [Adapter Layer Components](#adapter-layer-components)
  - [Component Interactions](#component-interactions)
- [💻 Code Diagram (Level 4)](#code-diagram-level-4)
  - [Service Layer Code Structure](#service-layer-code-structure)
  - [Key Classes and Interfaces](#key-classes-and-interfaces)
- [📋 Architecture Decision Records](#architecture-decision-records)
  - [ADR-001: Railway-Oriented Programming with r[T]](#adr-001-railway-oriented-programming-with-flextresultt)
  - [ADR-002: Clean Architecture with Domain-Driven Design](#adr-002-clean-architecture-with-domain-driven-design)
  - [ADR-003: Singer Protocol Abstraction Layer](#adr-003-singer-protocol-abstraction-layer)
- [🏆 Quality Attributes](#quality-attributes)
  - [Performance](#performance)
  - [Reliability](#reliability)
  - [Security](#security)
  - [Maintainability](#maintainability)
  - [Usability](#usability)
- [🔄 Evolution & Technical Debt](#evolution-technical-debt)
  - [Current Architecture Health](#current-architecture-health)
  - [Future Evolution Considerations](#future-evolution-considerations)

<!-- TOC END -->

**FLEXT-Meltano Enterprise Data Integration Platform**

**Framework**: C4 Model | **Version**: 1.0 | **Last Updated**: 2025-10-10

______________________________________________________________________

## 📋 Table of Contents

1. [Context Diagram (Level 1)](#context-diagram-level-1)
1. [Container Diagram (Level 2)](#container-diagram-level-2)
1. [Component Diagram (Level 3)](#component-diagram-level-3)
1. [Code Diagram (Level 4)](#code-diagram-level-4)
1. [Architecture Decision Records](#architecture-decision-records)
1. [Quality Attributes](#quality-attributes)

______________________________________________________________________

## 🎯 Context Diagram (Level 1)

### System Purpose

**FLEXT-Meltano** is an enterprise-grade data integration platform that provides comprehensive Singer protocol implementation, plugin development tools, and Meltano project management for the FLEXT ecosystem. It serves as the foundation for all ELT operations across 32+ FLEXT projects.

```plantuml
@startuml FLEXT-Meltano Context Diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

title FLEXT-Meltano - System Context Diagram

Person(user, "Data Engineer/Developer", "Creates and manages ELT pipelines")
Person(REDACTED_LDAP_BIND_PASSWORD, "Platform Administrator", "Manages Meltano infrastructure")

System(flext_meltano, "FLEXT-Meltano", "Enterprise data integration platform providing Singer protocol, plugin development, and pipeline orchestration")

System_Ext(meltano_core, "Meltano Core", "Data integration platform")
System_Ext(singer_sdk, "Singer SDK", "Protocol implementation")
System_Ext(dbt_core, "DBT Core", "Data transformation")
System_Ext(flext_core, "FLEXT-Core", "Foundation patterns and services")

System_Ext(flext_tap_star, "FLEXT-Tap-* Projects", "32+ Singer tap implementations")
System_Ext(flext_target_star, "FLEXT-Target-* Projects", "Singer target implementations")
System_Ext(flext_dbt_star, "FLEXT-DBT-* Projects", "Data transformation projects")

System_Ext(data_sources, "Data Sources", "Databases, APIs, files, cloud services")
System_Ext(data_destinations, "Data Destinations", "Data warehouses, lakes, applications")

Rel(user, flext_meltano, "Uses", "Python API, CLI, configuration")
Rel(REDACTED_LDAP_BIND_PASSWORD, flext_meltano, "Manages", "Infrastructure, monitoring, security")

Rel(flext_meltano, meltano_core, "Integrates with", "CLI operations, project management")
Rel(flext_meltano, singer_sdk, "Implements", "Tap/target protocols, state management")
Rel(flext_meltano, dbt_core, "Orchestrates", "Model execution, testing, documentation")
Rel(flext_meltano, flext_core, "Built on", "r[T], dependency injection, logging")

Rel(flext_tap_star, flext_meltano, "Depends on", "Foundation library")
Rel(flext_target_star, flext_meltano, "Depends on", "Foundation library")
Rel(flext_dbt_star, flext_meltano, "Depends on", "Foundation library")

Rel(flext_meltano, data_sources, "Extracts data from", "Singer protocol")
Rel(flext_meltano, data_destinations, "Loads data to", "Singer protocol")

@enduml
```

### Key Relationships

| Relationship                        | Description                         | Technology              |
| ----------------------------------- | ----------------------------------- | ----------------------- |
| **Users → FLEXT-Meltano**           | API usage, pipeline creation        | Python, CLI, YAML       |
| **FLEXT-Meltano → Meltano**         | CLI integration, project management | Subprocess, file system |
| **FLEXT-Meltano → Singer SDK**      | Protocol implementation             | Python inheritance      |
| **FLEXT-Meltano → DBT**             | Model orchestration                 | CLI, file system        |
| **FLEXT-Meltano → FLEXT-Core**      | Foundation patterns                 | Python imports          |
| **FLEXT Ecosystem → FLEXT-Meltano** | 32+ dependent projects              | Python dependencies     |

______________________________________________________________________

## 🏗️ Container Diagram (Level 2)

### Container Overview

FLEXT-Meltano is deployed as a Python library with multiple deployment options supporting different use cases.

```plantuml
@startuml FLEXT-Meltano Container Diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title FLEXT-Meltano - Container Diagram

Person(user, "Data Engineer", "Creates and orchestrates ELT pipelines")

System_Boundary(flext_meltano, "FLEXT-Meltano Platform") {
    Container(api, "API Layer", "Python/FastAPI", "REST API for pipeline management, plugin operations, monitoring")
    Container(service, "Service Layer", "Python", "Business logic, orchestration, error handling")
    Container(adapter, "Adapter Layer", "Python", "External system integration (Meltano, DBT, Singer)")
    Container(model, "Domain Model", "Python/Pydantic", "Data models, validation, business entities")
    Container(config, "Configuration", "Python/YAML", "Configuration management, environment settings")
    ContainerDb(state_store, "State Store", "File System/SQLite", "Pipeline state, bookmarks, execution history")
}

System_Ext(meltano_cli, "Meltano CLI", "Command Line", "Data integration orchestration")
System_Ext(dbt_cli, "DBT CLI", "Command Line", "Data transformation")
System_Ext(data_sources, "Data Sources", "Various", "APIs, databases, files, cloud services")
System_Ext(data_targets, "Data Targets", "Various", "Warehouses, databases, applications")

Rel(user, api, "Uses", "HTTP/REST, Python API")

Rel(api, service, "Orchestrates", "Method calls")
Rel(service, adapter, "Integrates", "Method calls")
Rel(service, model, "Validates", "Data binding")
Rel(service, config, "Configures", "Configuration access")

Rel(adapter, meltano_cli, "Executes", "Subprocess calls")
Rel(adapter, dbt_cli, "Orchestrates", "Subprocess calls")
Rel(adapter, state_store, "Persists", "File I/O, SQL")

Rel(meltano_cli, data_sources, "Extracts", "Singer protocol")
Rel(meltano_cli, data_targets, "Loads", "Singer protocol")
Rel(dbt_cli, data_targets, "Transforms", "SQL")

@enduml
```

### Container Responsibilities

| Container         | Technology         | Purpose              | Key Classes                                     |
| ----------------- | ------------------ | -------------------- | ----------------------------------------------- |
| **API Layer**     | FastAPI/Python     | External interface   | `FlextMeltano`, `FlextMeltanoCLI`               |
| **Service Layer** | Python             | Business logic       | `FlextMeltanoService`, `FlextMeltanoExecutor`   |
| **Adapter Layer** | Python             | External integration | `FlextMeltanoAdapter`, `FlextMeltanoDbtService` |
| **Domain Model**  | Pydantic/Python    | Data validation      | `FlextMeltanoModels`, `FlextMeltanoSettings`    |
| **Configuration** | YAML/Python        | Settings management  | `FlextMeltanoSettings`, environment variables   |
| **State Store**   | File System/SQLite | Persistence          | JSON files, SQLite database                     |

______________________________________________________________________

## 🔧 Component Diagram (Level 3)

### Service Layer Components

```plantuml
@startuml FLEXT-Meltano Service Components
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title FLEXT-Meltano - Service Layer Components

Container_Boundary(service_layer, "Service Layer") {
    Component(api_facade, "API Facade", "Python", "Unified public API for all operations")
    Component(orchestrator, "Pipeline Orchestrator", "Python", "Pipeline execution and coordination")
    Component(plugin_manager, "Plugin Manager", "Python", "Plugin discovery, installation, validation")
    Component(singer_service, "Singer Service", "Python", "Singer protocol implementation")
    Component(dbt_service, "DBT Service", "Python", "DBT model orchestration")
}

Component(config_manager, "Configuration Manager", "Python", "Configuration loading and validation")
Component(state_manager, "State Manager", "Python", "Pipeline state and bookmark management")
Component(error_handler, "Error Handler", "Python", "Railway-oriented error handling")

Rel(api_facade, orchestrator, "Delegates to", "Method calls")
Rel(api_facade, plugin_manager, "Uses", "Plugin operations")
Rel(api_facade, config_manager, "Configures", "Configuration access")

Rel(orchestrator, singer_service, "Coordinates", "Pipeline execution")
Rel(orchestrator, dbt_service, "Orchestrates", "Model execution")
Rel(orchestrator, state_manager, "Persists", "State updates")
Rel(orchestrator, error_handler, "Handles errors", "r[T]")

Rel(plugin_manager, config_manager, "Validates", "Plugin configuration")
Rel(singer_service, state_manager, "Updates", "Singer bookmarks")
Rel(dbt_service, state_manager, "Tracks", "Model execution state")

@enduml
```

### Adapter Layer Components

```plantuml
@startuml FLEXT-Meltano Adapter Components
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title FLEXT-Meltano - Adapter Layer Components

Container_Boundary(adapter_layer, "Adapter Layer") {
    Component(meltano_adapter, "Meltano Adapter", "Python", "Meltano CLI integration and execution")
    Component(dbt_adapter, "DBT Adapter", "Python", "DBT CLI orchestration and monitoring")
    Component(singer_adapter, "Singer Adapter", "Python", "Singer protocol abstraction layer")
    Component(cli_translator, "CLI Translator", "Python", "Command translation and execution")
}

Component(file_manager, "File Manager", "Python", "Configuration and state file management")
Component(process_manager, "Process Manager", "Python", "Subprocess execution and monitoring")

Rel(meltano_adapter, cli_translator, "Translates", "Command generation")
Rel(dbt_adapter, cli_translator, "Translates", "DBT command execution")
Rel(singer_adapter, cli_translator, "Implements", "Singer protocol calls")

Rel(cli_translator, process_manager, "Executes", "Subprocess management")
Rel(cli_translator, file_manager, "Manages", "Configuration files")

Rel(meltano_adapter, file_manager, "Persists", "Meltano project files")
Rel(dbt_adapter, file_manager, "Manages", "DBT project structure")

@enduml
```

### Component Interactions

| Component                 | Responsibilities               | Key Interactions                                |
| ------------------------- | ------------------------------ | ----------------------------------------------- |
| **API Facade**            | Public interface unification   | Service orchestration, configuration management |
| **Pipeline Orchestrator** | ELT pipeline coordination      | Singer service, DBT service, state management   |
| **Plugin Manager**        | Plugin lifecycle management    | Configuration validation, adapter integration   |
| **Singer Service**        | Protocol implementation        | State management, error handling                |
| **DBT Service**           | Model orchestration            | File management, process execution              |
| **Configuration Manager** | Settings management            | All components for configuration access         |
| **State Manager**         | Persistence layer              | Pipeline execution tracking, bookmark storage   |
| **Error Handler**         | Railway pattern implementation | All services for error propagation              |

______________________________________________________________________

## 💻 Code Diagram (Level 4)

### Service Layer Code Structure

```plantuml
@startuml FLEXT-Meltano Code Structure
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title FLEXT-Meltano - Code Structure (Service Layer)

Package "Service Layer" as services {
    Class FlextMeltanoService {
        +discover_plugins()
        +validate_plugins()
        +install_plugins()
        +execute_pipeline()
    }

    Class FlextMeltanoExecutor {
        +execute_tap()
        +execute_target()
        +run_pipeline()
        +monitor_execution()
    }

    Class FlextMeltanoPluginService {
        +discover_available_plugins()
        +install_plugin()
        +validate_plugin_config()
        +test_plugin()
    }
}

Package "Adapter Layer" as adapters {
    Class FlextMeltanoAdapter {
        +run_meltano_command()
        +get_meltano_version()
        +create_project()
        +add_plugin()
    }

    Class FlextMeltanoDbtService {
        +run_dbt_command()
        +validate_models()
        +generate_docs()
        +run_tests()
    }
}

Package "Domain Model" as models {
    Class FlextMeltanoModels {
        +TapRunParams
        +TargetRunParams
        +PipelineConfig
        +FlextPluginSettings
    }

    Class FlextMeltanoSettings {
        +load_from_file()
        +validate_config()
        +get_environment_vars()
    }
}

' Relationships
FlextMeltanoService --> FlextMeltanoExecutor : uses
FlextMeltanoService --> FlextMeltanoPluginService : uses
FlextMeltanoExecutor --> FlextMeltanoAdapter : integrates
FlextMeltanoExecutor --> FlextMeltanoDbtService : orchestrates
FlextMeltanoPluginService --> FlextMeltanoAdapter : manages

FlextMeltanoService --> FlextMeltanoModels : validates
FlextMeltanoService --> FlextMeltanoSettings : configures

note right of FlextMeltanoService
    Railway-oriented error handling
    with r[T] pattern
end note

@enduml
```

### Key Classes and Interfaces

| Class                    | Purpose                  | Key Methods                           | Dependencies                |
| ------------------------ | ------------------------ | ------------------------------------- | --------------------------- |
| **FlextMeltano**         | Main API facade          | Unified public interface              | All service classes         |
| **FlextMeltanoService**  | Core business logic      | Plugin management, pipeline execution | Adapters, models, config    |
| **FlextMeltanoAdapter**  | Meltano integration      | CLI operations, project management    | Meltano CLI, file system    |
| **FlextMeltanoExecutor** | Pipeline orchestration   | Tap/target execution, monitoring      | Singer service, DBT service |
| **FlextMeltanoModels**   | Data validation          | Pydantic models, type safety          | Pydantic v2                 |
| **FlextMeltanoSettings** | Configuration management | Settings loading, validation          | YAML, environment variables |

______________________________________________________________________

## 📋 Architecture Decision Records

### ADR-001: Railway-Oriented Programming with r[T]

**Status**: Accepted | **Date**: 2025-01-15

#### Context

FLEXT-Meltano needs robust error handling for complex ELT operations involving multiple external systems and potential failure points.

#### Decision

Implement railway-oriented programming using r[T] from flext-core, ensuring composable error handling throughout the entire codebase.

#### Consequences

- ✅ **Positive**: Composable error handling, type safety, consistent error propagation
- ⚠️ **Negative**: Learning curve for railway pattern, additional boilerplate
- ✅ **Mitigation**: Comprehensive documentation and examples

### ADR-002: Clean Architecture with Domain-Driven Design

**Status**: Accepted | **Date**: 2025-01-20

#### Context

The system needs to be maintainable, testable, and evolvable while integrating with complex external systems (Meltano, DBT, Singer).

#### Decision

Implement Clean Architecture with clear separation between:

- API Layer (external interfaces)
- Service Layer (business logic)
- Adapter Layer (external system integration)
- Domain Model (business entities and rules)

#### Consequences

- ✅ **Positive**: Testability, maintainability, clear boundaries
- ⚠️ **Negative**: Additional abstraction layers
- ✅ **Mitigation**: Consistent architectural patterns

### ADR-003: Singer Protocol Abstraction Layer

**Status**: Accepted | **Date**: 2025-02-01

#### Context

Direct Singer SDK usage would create tight coupling and prevent FLEXT ecosystem integration.

#### Decision

Create comprehensive abstraction layer over Singer SDK with FLEXT patterns and error handling.

#### Consequences

- ✅ **Positive**: FLEXT ecosystem consistency, type safety, error handling
- ⚠️ **Negative**: Additional complexity over direct SDK usage
- ✅ **Mitigation**: Comprehensive documentation and examples

______________________________________________________________________

## 🏆 Quality Attributes

### Performance

- **Response Time**: \<100ms for API operations, \<5s for pipeline startup
- **Throughput**: Support for concurrent pipeline execution
- **Scalability**: Horizontal scaling through stateless design
- **Resource Usage**: Memory-efficient streaming for large datasets

### Reliability

- **Availability**: 99.9% uptime target for core services
- **Error Handling**: Railway pattern with comprehensive error recovery
- **Data Consistency**: ACID compliance for state management
- **Fault Tolerance**: Graceful degradation and automatic retry mechanisms

### Security

- **Authentication**: Integration with FLEXT authentication systems
- **Authorization**: Role-based access control for pipeline operations
- **Data Protection**: Encryption at rest and in transit
- **Audit Logging**: Comprehensive security event logging

### Maintainability

- **Code Quality**: 100% type safety, zero linting violations
- **Documentation**: Comprehensive API docs and architecture documentation
- **Testing**: 95%+ code coverage with automated CI/CD
- **Modularity**: Clear separation of concerns and dependency injection

### Usability

- **API Design**: Consistent, intuitive public interfaces
- **Error Messages**: Clear, actionable error reporting
- **Configuration**: YAML-based configuration with validation
- **Monitoring**: Comprehensive logging and metrics

______________________________________________________________________

## 🔄 Evolution & Technical Debt

### Current Architecture Health

- **Technical Debt**: Low - Clean architecture implemented from start
- **Code Quality**: High - 100% type safety, comprehensive testing
- **Documentation**: Excellent - C4 model, ADRs, comprehensive guides
- **Maintainability**: High - Modular design with clear boundaries

### Future Evolution Considerations

- **Microservices Migration**: Potential split into separate services
- **Event-Driven Architecture**: Message-based pipeline coordination
- **Cloud-Native Features**: Kubernetes operators, service mesh integration
- **Multi-Cloud Support**: Cloud-agnostic deployment patterns

______________________________________________________________________

**C4 Model Documentation**: FLEXT-Meltano Enterprise Architecture
_Comprehensive system documentation following industry-standard C4 modeling approach_
