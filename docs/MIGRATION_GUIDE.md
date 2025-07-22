# FLEXT-Meltano Migration Guide - NEW SEMANTIC ARCHITECTURE

**Date**: 2025-07-22  
**Version**: 1.0  
**Target**: flext-meltano v1.0.0

## Overview

This guide helps you migrate from the old flext-meltano API to the **new semantic architecture** built on flext-core foundation patterns.

## Key Changes

### 1. New Semantic Structure

```
OLD STRUCTURE (Deprecated)         →    NEW STRUCTURE (Recommended)
├── project_manager.py            →    ├── domain/
├── orchestrator.py               →    │   ├── entities/
├── models.py                     →    │   │   ├── project.py
├── unified_anti_corruption_layer →    │   │   ├── plugin.py
                                  →    │   │   ├── job.py
                                  →    │   │   └── state.py
                                  →    ├── application/
                                  →    │   ├── services/
                                  →    │   │   └── project_service.py
                                  →    │   └── interfaces/
                                  →    └── infrastructure/
                                  →        └── meltano/
```

### 2. Import Changes

#### Domain Entities

```python
# ❌ OLD (Deprecated)
from flext_meltano.models import MeltanoProject, MeltanoPlugin

# ✅ NEW (Recommended)
from flext_meltano.domain.entities import MeltanoProject, MeltanoPlugin, MeltanoJob, MeltanoState
```

#### Application Services

```python
# ❌ OLD (Deprecated)
from flext_meltano import FlextMeltanoProjectManager

# ✅ NEW (Recommended)
from flext_meltano.application.services import ProjectApplicationService
```

#### Anti-Corruption Layer

```python
# ❌ OLD (Deprecated)
from flext_meltano import MeltanoAntiCorruptionLayer

# ✅ NEW (Recommended)
from flext_meltano.infrastructure.meltano import MeltanoCLIAdapter
```

### 3. API Changes

#### Project Management

**OLD API:**
```python
# ❌ Deprecated
manager = FlextMeltanoProjectManager(meltano_cli)
result = manager.create_project("my-project", "/path/to/project")
```

**NEW API:**
```python
# ✅ Recommended
from flext_meltano.application.services import ProjectApplicationService
from flext_meltano.infrastructure.meltano import MeltanoCLIAdapter
from flext_meltano.infrastructure.persistence import ProjectRepositoryImpl

# Dependency injection (using flext-core patterns)
cli_adapter = MeltanoCLIAdapter()
repository = ProjectRepositoryImpl()
service = ProjectApplicationService(repository, cli_adapter)

# Type-safe API with ServiceResult
result = await service.create_project("my-project", Path("/path/to/project"))
if result.is_success:
    project = result.data
    print(f"Created project: {project.name}")
else:
    print(f"Failed: {result.error}")
```

#### Plugin Management

**OLD API:**
```python
# ❌ Deprecated
plugin_manager = PluginManager()
plugin_manager.install_plugin("tap-postgres", "extractors")
```

**NEW API:**
```python
# ✅ Recommended
from flext_meltano.application.services import PluginApplicationService
from flext_meltano.domain.entities import MeltanoPlugin

service = PluginApplicationService(plugin_repository, cli_adapter)
result = await service.install_plugin(
    name="tap-postgres",
    plugin_type="extractors",
    project_name="my-project"
)
```

#### Job Execution

**OLD API:**
```python
# ❌ Deprecated
orchestrator = FlextMeltanoOrchestrator()
orchestrator.run_job("my-job", {"environment": "dev"})
```

**NEW API:**
```python
# ✅ Recommended
from flext_meltano.application.services import JobApplicationService
from flext_meltano.domain.entities import MeltanoJob

service = JobApplicationService(job_repository, cli_adapter)
result = await service.execute_job(
    job_name="my-job",
    project_name="my-project",
    environment="dev"
)
```

## Migration Steps

### Step 1: Update Imports

Replace all deprecated imports with new semantic imports:

```python
# Update your imports gradually
from flext_meltano.domain.entities import (
    MeltanoProject,
    MeltanoPlugin, 
    MeltanoJob,
    MeltanoState,
)
from flext_meltano.application.services import (
    ProjectApplicationService,
    PluginApplicationService,
    JobApplicationService,
)
```

### Step 2: Update Service Instantiation

Use dependency injection pattern:

```python
# OLD: Direct instantiation
manager = FlextMeltanoProjectManager(cli)

# NEW: Dependency injection
from flext_meltano.infrastructure.meltano import MeltanoCLIAdapter
from flext_meltano.infrastructure.persistence import ProjectRepositoryImpl

cli_adapter = MeltanoCLIAdapter()
repository = ProjectRepositoryImpl()
service = ProjectApplicationService(repository, cli_adapter)
```

### Step 3: Handle ServiceResult Pattern

Update error handling to use ServiceResult:

```python
# OLD: Exception-based
try:
    project = manager.create_project("test")
    print(f"Success: {project}")
except Exception as e:
    print(f"Error: {e}")

# NEW: ServiceResult-based
result = await service.create_project("test", Path("/path"))
if result.is_success:
    project = result.data
    print(f"Success: {project}")
else:
    print(f"Error: {result.error}")
```

### Step 4: Use Domain Methods

Leverage rich domain entities:

```python
# NEW: Rich domain entities with business logic
project = MeltanoProject(name="test", directory=Path("/path"))

# Business rules enforced by domain
result = project.activate()
if result.is_success:
    print("Project activated")

result = project.change_environment("prod")
if result.is_success:
    print("Environment changed")
```

## Breaking Changes

### 1. Synchronous → Asynchronous

All new APIs are async by default:

```python
# OLD: Synchronous
result = manager.create_project("test")

# NEW: Asynchronous
result = await service.create_project("test", Path("/path"))
```

### 2. Exception → ServiceResult

Error handling changed from exceptions to ServiceResult:

```python
# OLD: Exception-based
try:
    result = operation()
except SomeError as e:
    handle_error(e)

# NEW: ServiceResult-based
result = await operation()
if not result.is_success:
    handle_error(result.error)
```

### 3. Direct Access → Repository Pattern

Data access changed to repository pattern:

```python
# OLD: Direct access
projects = get_projects_from_somewhere()

# NEW: Repository pattern
projects = await project_repository.find_all()
```

## Deprecation Timeline

- **v0.7.0**: New semantic architecture introduced, old API marked deprecated
- **v0.8.0**: Deprecation warnings become more prominent
- **v0.9.0**: Old API moved to deprecated module
- **v1.0.0**: Old API completely removed

## Benefits of Migration

### 1. Better Semantic Organization
- **Quick navigation**: Clear semantic structure
- **Maintainability**: Proper separation of concerns
- **Testability**: Clean dependencies enable easy testing

### 2. Type Safety
- **ServiceResult pattern**: Type-safe error handling
- **Rich domain models**: Business rules enforced at compile time
- **Interface contracts**: Clear boundaries between layers

### 3. Foundation Patterns
- **Built on flext-core**: Consistent patterns across FLEXT ecosystem
- **Clean Architecture**: Proper dependency inversion
- **Domain-Driven Design**: Rich business models

### 4. Future-Proof
- **Extensible**: Plugin architecture for new features
- **Maintainable**: Clear boundaries and responsibilities
- **Testable**: Dependency injection enables comprehensive testing

## Getting Help

1. **Deprecation warnings**: Follow the guidance in deprecation messages
2. **Documentation**: Check `docs/SEMANTIC_ARCHITECTURE_REDESIGN.md`
3. **Examples**: See `examples/` directory for migration examples
4. **Tests**: Check `tests/` for usage patterns

## Example: Complete Migration

**Before (Old API):**
```python
from flext_meltano import FlextMeltanoProjectManager, MeltanoAntiCorruptionLayer

# Old way
cli = MeltanoAntiCorruptionLayer()
manager = FlextMeltanoProjectManager(cli)

try:
    project = manager.create_project("test-project", "/tmp/test")
    manager.install_plugin(project, "tap-postgres", "extractors")
    manager.run_job(project, "extract-load")
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")
```

**After (New API):**
```python
from flext_meltano.domain.entities import MeltanoProject
from flext_meltano.application.services import ProjectApplicationService, PluginApplicationService
from flext_meltano.infrastructure.meltano import MeltanoCLIAdapter
from flext_meltano.infrastructure.persistence import ProjectRepositoryImpl, PluginRepositoryImpl

# New way with dependency injection
async def main():
    # Setup dependencies
    cli_adapter = MeltanoCLIAdapter()
    project_repo = ProjectRepositoryImpl()
    plugin_repo = PluginRepositoryImpl()
    
    project_service = ProjectApplicationService(project_repo, cli_adapter)
    plugin_service = PluginApplicationService(plugin_repo, cli_adapter)
    
    # Create project
    result = await project_service.create_project("test-project", Path("/tmp/test"))
    if not result.is_success:
        print(f"Failed to create project: {result.error}")
        return
    
    project = result.data
    
    # Install plugin
    result = await plugin_service.install_plugin(
        name="tap-postgres",
        plugin_type="extractors", 
        project_name=project.name
    )
    if not result.is_success:
        print(f"Failed to install plugin: {result.error}")
        return
    
    # Run job
    result = await job_service.execute_job("extract-load", project.name)
    if result.is_success:
        print("Success!")
    else:
        print(f"Failed: {result.error}")

# Run with asyncio
import asyncio
asyncio.run(main())
```

The new API provides better error handling, type safety, and clear semantic organization while maintaining all the functionality of the old API.