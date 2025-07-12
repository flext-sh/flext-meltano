# FLEXT Ecosystem Integration Guide

**Document Purpose**: Integration guide for FLEXT-Meltano with FLEXT platform components

**Last Updated**: 2025-07-12  
**FLEXT Version**: 0.7.0  
**Python**: 3.13+

---

## FLEXT Integration Overview

FLEXT-Meltano integrates with the FLEXT platform, leveraging flext-core for foundation patterns and flext-observability for monitoring capabilities.

### Core Integration Components

**Primary Dependencies**:
- **flext-core**: Foundation framework with ServiceResult patterns
- **flext-observability**: Logging and monitoring capabilities

**Optional Integrations**:
- **flext-db-oracle**: Oracle database operations (when available)
- **flext-ldap**: LDAP integration (when available)

---

## Core FLEXT Dependencies

### flext-core Integration

**Relationship**: Foundation dependency  
**Usage**: Core patterns, ServiceResult, Clean Architecture, DDD

```python
# ServiceResult Pattern (from flext-core)
from flext_core.domain import ServiceResult
from flext_meltano import MeltanoProjectManager

async def create_project_with_flext_patterns():
    manager = MeltanoProjectManager('.')
    
    # Returns ServiceResult[T] for type-safe error handling
    result: ServiceResult[dict] = await manager.create_project('my_project', 'dev')
    
    if result.is_success:
        project_info = result.value
        print(f"✅ Project created: {project_info['project_path']}")
    else:
        print(f"❌ Error: {result.error}")
```

**Key Integrations**:
- **ServiceResult**: All operations return ServiceResult[T] for consistent error handling
- **Domain Events**: Pipeline events published via flext-core event system
- **Clean Architecture**: Anti-corruption layers follow flext-core patterns
- **Type Safety**: Python 3.13+ strict typing from flext-core standards

### flext-observability Integration

**Relationship**: Monitoring dependency  
**Usage**: Logging, metrics, health checks, telemetry

```python
# Observability Integration
from flext_observability import health, metrics, logger
from flext_meltano import MeltanoBridge

async def monitored_pipeline_execution():
    # Health check integration
    health_status = health.check_component("meltano")
    
    # Metrics collection
    with metrics.timer("pipeline_execution"):
        bridge = MeltanoBridge('.')
        result = await bridge.run_pipeline('project', 'tap-csv', 'target-csv')
    
    # Structured logging
    logger.info("Pipeline executed", 
                project="project",
                result=result,
                health=health_status)
```

**Key Integrations**:
- **Health Checks**: Meltano availability monitoring
- **Metrics Collection**: Pipeline execution timing and success rates
- **Structured Logging**: Comprehensive audit trails
- **Telemetry**: Integration with FLEXT workspace monitoring

---

## Optional FLEXT Integrations

### flext-db-oracle Integration

**Relationship**: Optional database dependency  
**Usage**: Oracle database operations for enterprise data pipelines

```python
# Oracle Integration (when available)
from flext_meltano import MeltanoBridge
try:
    from flext_db_oracle import OracleConnection
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False

async def oracle_pipeline_example():
    if not ORACLE_AVAILABLE:
        print("⚠️ Oracle integration not available")
        return
    
    # Use Oracle connection for Meltano tap configuration
    oracle_conn = OracleConnection()
    
    # Configure Meltano with Oracle credentials
    bridge = MeltanoBridge('.')
    result = await bridge.configure_oracle_tap(oracle_conn.get_config())
```

### flext-ldap Integration

**Relationship**: Optional LDAP dependency  
**Usage**: LDAP operations for authentication and directory services

```python
# LDAP Integration (when available)
from flext_meltano import MeltanoBridge
try:
    from flext_ldap import LDAPClient
    LDAP_AVAILABLE = True
except ImportError:
    LDAP_AVAILABLE = False

async def ldap_pipeline_example():
    if not LDAP_AVAILABLE:
        print("⚠️ LDAP integration not available")
        return
    
    # Use LDAP for user directory data extraction
    ldap_client = LDAPClient()
    
    # Configure Meltano LDAP tap
    bridge = MeltanoBridge('.')
    result = await bridge.configure_ldap_tap(ldap_client.get_config())
```

### flext-api Integration

**Relationship**: Optional REST API dependency  
**Usage**: REST endpoints for pipeline management

```python
# API Integration (when building REST services)
from flext_meltano import MeltanoBridge, MeltanoProjectManager
try:
    from flext_api import APIRouter
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False

if API_AVAILABLE:
    router = APIRouter()
    
    @router.post("/pipelines/create")
    async def create_pipeline(project_name: str):
        manager = MeltanoProjectManager('.')
        result = await manager.create_project(project_name, 'prod')
        
        if result.is_success:
            return {"status": "success", "project": result.value}
        else:
            return {"status": "error", "message": result.error}
```

---

## FLEXT Workspace Patterns

### Environment Configuration

**FLEXT Namespace Conventions**:

```bash
# .env (FLEXT workspace standards)

# FLEXT workspace coordination
FLEXT_WORKSPACE_ROOT=/home/marlonsc/flext
PYTHON_VENV=/home/marlonsc/flext/.venv
FLEXT_CORE_VERSION=0.7.0

# FLEXT ecosystem integration
FLEXT_LOG_LEVEL=INFO
FLEXT_OBSERVABILITY_ENABLED=true
FLEXT_TOKEN_FILE=/home/marlonsc/flext/.token

# FLEXT-Meltano specific (MELTANO_* namespace)
MELTANO_PROJECT_ROOT=./projects
MELTANO_ENVIRONMENT=dev

# Singer protocol (SINGER_* namespace)
SINGER_SDK_LOG_LEVEL=ERROR
SINGER_SDK_DISABLE_WARNINGS=true
```

### Multi-Agent Coordination

**FLEXT .token Protocol**:

```python
# Multi-agent coordination following FLEXT workspace patterns
from pathlib import Path
import json

def coordinate_with_flext_workspace():
    """Read and update FLEXT workspace coordination token."""
    
    workspace_root = Path(os.getenv('FLEXT_WORKSPACE_ROOT', '/home/marlonsc/flext'))
    token_file = workspace_root / '.token'
    
    # Read current workspace state
    if token_file.exists():
        with token_file.open('r') as f:
            workspace_state = json.load(f)
        print(f"✅ FLEXT workspace state: {workspace_state}")
    
    # Update with FLEXT-Meltano activity
    new_state = {
        "active_agent": "claude_flext_meltano",
        "activity": "pipeline_management",
        "timestamp": "2025-07-12T10:00:00Z",
        "module": "flext-meltano"
    }
    
    with token_file.open('w') as f:
        json.dump(new_state, f, indent=2)
    
    print("✅ FLEXT workspace coordination updated")
```

### Testing Integration

**FLEXT Ecosystem Testing**:

```python
# Testing within FLEXT ecosystem
import pytest
from flext_core.domain import ServiceResult
from flext_observability import health
from flext_meltano import MeltanoBridge

@pytest.mark.integration
@pytest.mark.requires_flext_core
@pytest.mark.requires_flext_observability
async def test_flext_ecosystem_integration():
    """Test FLEXT-Meltano integration with core ecosystem."""
    
    # Test flext-core integration
    bridge = MeltanoBridge('.')
    result = await bridge.init_project('test_project', '.')
    assert isinstance(result, str)  # JSON response
    
    # Test flext-observability integration
    health_status = health.check_component("meltano")
    assert health_status["status"] in ["healthy", "degraded"]

@pytest.mark.integration
@pytest.mark.requires_flext_db_oracle
async def test_oracle_integration():
    """Test Oracle integration when available."""
    pytest.importorskip("flext_db_oracle")
    
    # Oracle-specific testing
    pass

@pytest.mark.integration
@pytest.mark.requires_flext_ldap
async def test_ldap_integration():
    """Test LDAP integration when available."""
    pytest.importorskip("flext_ldap")
    
    # LDAP-specific testing
    pass
```

---

## Architecture Patterns

### Clean Architecture Boundaries

FLEXT-Meltano maintains clean boundaries with other FLEXT modules:

```python
# Anti-corruption layer for FLEXT ecosystem
from flext_meltano.unified_anti_corruption_layer import UnifiedMeltanoAntiCorruptionLayer
from flext_core.domain import ServiceResult

class FlextEcosystemAdapter:
    """Adapter for FLEXT ecosystem integration."""
    
    def __init__(self):
        self.acl = UnifiedMeltanoAntiCorruptionLayer()
    
    async def translate_oracle_operation(self, oracle_op) -> ServiceResult:
        """Translate Oracle operations to Meltano operations."""
        try:
            # Transform Oracle domain concepts to Meltano concepts
            meltano_op = self.acl.translate_external_operation(oracle_op)
            return ServiceResult.success(meltano_op)
        except Exception as e:
            return ServiceResult.failure(f"Oracle translation failed: {e}")
    
    async def translate_ldap_operation(self, ldap_op) -> ServiceResult:
        """Translate LDAP operations to Meltano operations."""
        try:
            # Transform LDAP domain concepts to Meltano concepts
            meltano_op = self.acl.translate_external_operation(ldap_op)
            return ServiceResult.success(meltano_op)
        except Exception as e:
            return ServiceResult.failure(f"LDAP translation failed: {e}")
```

### Domain Events Integration

```python
# Domain events following FLEXT ecosystem patterns
from flext_core.domain.events import DomainEvent
from flext_meltano import MeltanoEventBridge

class PipelineExecutedEvent(DomainEvent):
    """Pipeline execution event for FLEXT ecosystem."""
    
    def __init__(self, project_id: str, pipeline_id: str, result: dict):
        super().__init__(
            event_type="pipeline_executed",
            aggregate_id=project_id,
            data={
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "result": result,
                "module": "flext-meltano"
            }
        )

# Event publishing to FLEXT ecosystem
event_bridge = MeltanoEventBridge()
event = PipelineExecutedEvent("project_1", "pipeline_1", {"status": "success"})
await event_bridge.publish(event)
```

---

## Development Workflow

### FLEXT Workspace Setup

1. **Environment Activation**:
   ```bash
   cd /home/marlonsc/flext
   source .venv/bin/activate
   ```

2. **Dependency Installation**:
   ```bash
   # Install FLEXT-Meltano with ecosystem dependencies
   cd flext-meltano
   pip install -e .
   
   # Verify ecosystem integration
   python -c "
   from flext_meltano import MeltanoBridge
   from flext_core.domain import ServiceResult
   from flext_observability import health
   print('✅ FLEXT ecosystem integration verified')
   "
   ```

3. **Quality Checks**:
   ```bash
   # Run FLEXT workspace quality standards
   make lint      # Ruff with FLEXT patterns
   make test      # Pytest with ecosystem markers
   make type-check # MyPy strict typing
   ```

### Code Style Integration

FLEXT-Meltano follows FLEXT ecosystem code standards:

- **Python 3.13+**: Modern type system features
- **ServiceResult**: Error handling pattern from flext-core
- **Clean Architecture**: DDD patterns and bounded contexts
- **Namespace Conventions**: Environment variable prefixes
- **Quality Standards**: 90%+ test coverage, strict typing

---

## Production Considerations

### Deployment Patterns

1. **Shared Environment**: Use FLEXT workspace venv for consistency
2. **Configuration**: Follow FLEXT namespace conventions
3. **Monitoring**: Integrate with flext-observability
4. **Error Handling**: Use ServiceResult patterns throughout
5. **Coordination**: Respect .token protocol for multi-agent systems

### Performance Integration

```python
# Performance monitoring with FLEXT observability
from flext_observability import metrics
from flext_meltano import MeltanoBridge

async def monitored_pipeline():
    with metrics.timer("flext_meltano.pipeline_execution"):
        bridge = MeltanoBridge('.')
        
        # Track pipeline metrics
        metrics.increment("flext_meltano.pipeline_started")
        
        try:
            result = await bridge.run_pipeline('project', 'tap', 'target')
            metrics.increment("flext_meltano.pipeline_success")
            return result
        except Exception as e:
            metrics.increment("flext_meltano.pipeline_error")
            raise
```

### Security Integration

```python
# Security integration with FLEXT ecosystem
from flext_auth import SecurityContext
from flext_meltano import MeltanoProjectManager

async def secure_project_creation(user_context: SecurityContext):
    """Create project with FLEXT security integration."""
    
    # Verify permissions through FLEXT auth
    if not user_context.has_permission("meltano:project:create"):
        return ServiceResult.failure("Insufficient permissions")
    
    # Create project with audit trail
    manager = MeltanoProjectManager('.')
    result = await manager.create_project(
        project_name="secure_project",
        environment="prod",
        created_by=user_context.user_id
    )
    
    return result
```

---

## Troubleshooting

### Common Integration Issues

1. **Missing FLEXT Dependencies**:
   ```bash
   cd /home/marlonsc/flext
   source .venv/bin/activate
   pip install -e ./flext-core
   pip install -e ./flext-observability
   ```

2. **Environment Variables Not Set**:
   ```bash
   export FLEXT_WORKSPACE_ROOT=/home/marlonsc/flext
   export PYTHON_VENV=/home/marlonsc/flext/.venv
   ```

3. **Import Errors**:
   ```python
   # Graceful degradation for optional dependencies
   try:
       from flext_db_oracle import OracleConnection
       ORACLE_AVAILABLE = True
   except ImportError:
       ORACLE_AVAILABLE = False
       print("⚠️ Oracle integration not available")
   ```

---

## Summary

FLEXT-Meltano is designed as an integral part of the FLEXT ecosystem while maintaining clean architectural boundaries. It leverages:

- **flext-core**: Foundation patterns and ServiceResult error handling
- **flext-observability**: Comprehensive monitoring and logging
- **Optional modules**: Oracle, LDAP, API, and other FLEXT components
- **Workspace patterns**: Shared environment and coordination protocols
- **Quality standards**: Consistent with FLEXT ecosystem requirements

This integration approach ensures FLEXT-Meltano works seamlessly within the broader FLEXT platform while remaining independently functional and maintainable.

**For more details**: See individual module documentation in the FLEXT workspace.