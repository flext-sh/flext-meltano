# flext-db-oracle Tech Stack and Dependencies

## Core Tech Stack
- **Python**: 3.13+ with Pydantic v2
- **Database**: Oracle Database (Oracle XE 21c for testing)
- **ORM**: SQLAlchemy 2.0
- **Oracle Driver**: python-oracledb (modern Oracle driver)
- **Architecture**: Clean Architecture with Domain-Driven Design

## FLEXT Ecosystem Dependencies (MANDATORY)
- **flext-core**: Foundation library (FlextResult, FlextContainer, FlextDomainService, get_logger)
- **flext-cli**: CLI patterns and utilities (integrated with Click)
- **flext-observability**: Oracle monitoring, metrics, and database performance tracking

## Python Dependencies
- **SQLAlchemy**: 2.0+ for ORM and database toolkit (INTERNAL - wrapped by FlextDbOracleApi)
- **oracledb**: Python Oracle driver (INTERNAL - managed by flext-db-oracle)
- **pydantic**: Data validation and Oracle model management
- **click**: CLI framework (INTERNAL - wrapped by FlextDbOracleClient)

## Development Dependencies  
- **pytest**: Testing framework
- **mypy**: Type checking
- **ruff**: Linting and formatting
- **pyright**: Additional type checking
- **bandit**: Security scanning

## Oracle Environment
- **Oracle XE 21c**: Container-based development environment
- **Connection Pooling**: Optimized Oracle connection pools
- **Transaction Management**: ACID compliance
- **Schema Introspection**: Complete metadata extraction
- **SSL/TLS**: Secure connections support