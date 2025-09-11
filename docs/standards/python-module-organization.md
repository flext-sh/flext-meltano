# Python Module Organization & Semantic Patterns

**FLEXT Meltano Module Architecture & Best Practices for Bridge Integration**

---

## 🚨 Current Architecture Status

**⚠️ CRITICAL**: This documentation describes the **intended architecture**. The current project has **3 critical issues** that must be resolved before this organization can be fully implemented:

| Issue                  | Status             | Blocker                            |
| ---------------------- | ------------------ | ---------------------------------- |
| **Bridge Integration** | ❌ **BROKEN**      | `FlextMeltanoBridge` class missing |
| **Module Overload**    | ⚠️ **PROBLEMATIC** | 290+ exports in `__init__.py`      |
| **Quality Gates**      | ❌ **FAILING**     | 3 MyPy errors, 1 test failure      |

See [TODO.md](TODO.md) for immediate fixes required.

---

## 🏗️ **Module Architecture Overview**

FLEXT Meltano implements a **bridge-focused module architecture** that enables seamless Go ↔ Python integration for data pipeline orchestration. This structure follows enterprise patterns while maintaining simplicity for subprocess execution.

### **Core Design Principles**

1. **Bridge-First Design**: Primary focus on Go service integration
2. **Subprocess Orchestration**: Direct Meltano CLI execution patterns
3. **Enterprise Standards**: FlextResult, dependency injection, type safety
4. **Consolidated Structure**: Flat module organization (post-reorganization)
5. **Quality Enforcement**: 90% coverage, strict typing, security scanning

---

## 📁 **Current Module Structure & Responsibilities**

### **Actual Module Layout (17 Modules)**

```python
# Current implementation structure
src/flext_meltano/
├── __init__.py              # ⚠️ OVERLOADED: 290+ exports (needs refactoring)
├── base.py                  # ✅ Foundation classes and factory functions
├── cli.py                   # ❌ TYPE ERROR: line 157 object has no strip()
├── common.py                # ✅ Common utilities and shared functionality
├── common_schemas.py        # ✅ Shared data schemas and models
├── container.py             # ✅ Dependency injection container
├── core.py                  # ✅ Core enterprise functionality and services
├── dbt.py                   # ✅ DBT integration and project management
├── discovery.py             # ✅ Plugin discovery and catalog management
├── exceptions.py            # ✅ Custom exception classes
├── execution.py             # ✅ Subprocess execution helpers (core functionality)
├── flext_singer.py          # ✅ Singer SDK integration and stream handling
├── installation.py          # ✅ Plugin installation utilities and management
├── singer.py                # ✅ Core Singer protocol implementation
├── singer_base.py           # ✅ Singer base classes and utilities
├── singer_unified.py        # ✅ Unified Singer interface
└── validation.py            # ❌ TYPE ERRORS: lines 250, 344
```

**Missing Critical Module**:

```python
# REQUIRED: Bridge integration module
└── simple_bridge.py         # ❌ MISSING: FlextMeltanoBridge class
```

---

## 🎯 **Ideal Module Organization (Target Architecture)**

### **Foundation Layer** (Core Infrastructure)

```python
# Foundation - enterprise patterns and utilities
src/flext_meltano/
├── __init__.py              # 🎯 Public API gateway (streamlined exports)
├── exceptions.py            # 🎯 Exception hierarchy for error handling
├── common.py                # 🎯 Pure utility functions and helpers
├── common_schemas.py        # 🎯 Shared data models and schemas
└── container.py             # 🎯 Dependency injection container
```

**Responsibility**: Establish foundational contracts for enterprise patterns.

**Import Pattern**:

```python
# Foundation imports - used by all other modules
from flext_meltano import FlextMeltanoError, FlextMeltanoConfig
from flext_core import FlextResult, FlextContainer
```

### **Configuration & Base Classes Layer**

```python
# Configuration and base abstractions
├── base.py                  # 🚀 Base classes and factory functions
├── config.py                # 🚀 Configuration management (future)
└── interfaces.py            # 🚀 Protocol definitions (future)
```

**Responsibility**: Provide configuration management and base abstractions.

**Configuration Pattern**:

```python
from flext_meltano.base import FlextMeltanoConfig, FlextMeltanoBaseService

class CustomTapService(FlextMeltanoBaseService):
    def __init__(self, config: FlextMeltanoConfig) -> None:
        super().__init__(config)

    def discover_streams(self) -> FlextResult[List[Stream]]:
        return FlextResult[None].ok([])
```

### **Bridge Integration Layer** (CRITICAL - MISSING)

```python
# Go ↔ Python bridge integration (MISSING)
├── simple_bridge.py         # 🌉 MISSING: FlextMeltanoBridge class
├── bridge_models.py         # 🌉 Bridge request/response models (future)
└── bridge_utils.py          # 🌉 Bridge utility functions (future)
```

**Responsibility**: Enable Go services to execute Meltano operations via subprocess.

**Bridge Pattern** (TO BE IMPLEMENTED):

```python
from flext_meltano.simple_bridge import FlextMeltanoBridge
from flext_core import FlextResult

class FlextMeltanoBridge:
    """Bridge class for Go service integration."""

    def get_version(self) -> FlextResult[Dict[str, str]]:
        """Get Meltano version information."""
        # Implementation needed

    def run_pipeline(self, tap: str, target: str) -> FlextResult[Dict[str, object]]:
        """Execute pipeline between tap and target."""
        # Implementation needed
```

### **Core Operations Layer**

```python
# Core business operations
├── core.py                  # 🏛️ Enterprise services and orchestration
├── execution.py             # 🏛️ Subprocess execution helpers (PRIMARY)
├── cli.py                   # 🏛️ CLI interface and command handling
└── validation.py            # 🏛️ Pipeline validation and compliance
```

**Responsibility**: Implement core Meltano operations and enterprise patterns.

**Execution Pattern**:

```python
from flext_meltano.execution import execute_meltano_command, run_pipeline
from flext_core import FlextResult

# Direct subprocess execution
result = execute_meltano_command(["--version"])
if result.success:
    print(f"Meltano version: {result.data}")

# Pipeline orchestration
pipeline_result = run_pipeline("tap-csv", "target-csv")
```

### **Plugin Management Layer**

```python
# Plugin discovery and installation
├── discovery.py             # 📦 Plugin discovery and catalog management
├── installation.py          # 📦 Plugin installation utilities
└── plugin_utils.py          # 📦 Plugin utility functions (future)
```

**Responsibility**: Handle Meltano plugin lifecycle management.

**Discovery Pattern**:

```python
from flext_meltano.discovery import discover_plugins, discover_catalog
from flext_meltano.installation import install_plugin

# Plugin discovery
plugins = discover_plugins()
if plugins.success:
    print(f"Found {len(plugins.data)} plugins")

# Plugin installation
result = install_plugin("extractor", "tap-csv")
```

### **Singer Integration Layer**

```python
# Singer SDK integration and stream handling
├── singer.py                # 🎵 Core Singer protocol implementation
├── singer_base.py           # 🎵 Singer base classes and utilities
├── singer_unified.py        # 🎵 Unified Singer interface
└── flext_singer.py          # 🎵 Singer SDK integration and stream handling
```

**Responsibility**: Provide Singer protocol integration and stream handling.

**Singer Pattern**:

```python
from flext_meltano.singer import FlextSingerTap, FlextSingerTarget
from flext_meltano.flext_singer import FlextSingerService

class CustomTap(FlextSingerTap):
    def discover_streams(self) -> FlextResult[List[Stream]]:
        # Implementation using Singer SDK patterns
        return FlextResult[None].ok(streams)
```

### **Data Transformation Layer**

```python
# DBT integration and data transformation
├── dbt.py                   # 🔄 DBT integration and project management
├── dbt_models.py            # 🔄 DBT model utilities (future)
└── dbt_utils.py             # 🔄 DBT helper functions (future)
```

**Responsibility**: Handle DBT operations and data transformation workflows.

**DBT Pattern**:

```python
from flext_meltano.dbt import FlextMeltanoDbtService

dbt_service = FlextMeltanoDbtService(project_dir="./dbt")
result = dbt_service.run_models()
if result.success:
    print("DBT models executed successfully")
```

---

## 🎯 **Semantic Naming Conventions**

### **Public API Naming (FlextMeltanoXxx)**

All public exports use the `FlextMeltano` prefix for clear namespace separation:

```python
# Core patterns
FlextMeltanoConfig           # Configuration management
FlextMeltanoBaseService      # Base service class
FlextMeltanoBridge          # Go ↔ Python bridge (MISSING)
FlextMeltanoError           # Base exception class
FlextMeltanoResult          # Local result type (uses FlextResult)

# Service patterns
FlextMeltanoTapService      # Base tap service class
FlextMeltanoTargetService   # Base target service class
FlextMeltanoDbtService      # DBT operations service
FlextMeltanoOrchestrationService  # Pipeline orchestration

# Execution patterns
FlextMeltanoExecutor        # Command execution service
FlextMeltanoCli             # CLI interface wrapper
FlextMeltanoValidator       # Validation service

# Discovery patterns
FlextMeltanoDiscovery       # Plugin discovery service
FlextMeltanoInstaller       # Plugin installation service
```

**Rationale**: Clear namespace prevents conflicts and identifies FLEXT Meltano components.

### **Module-Level Naming**

```python
# Module names reflect primary responsibility
simple_bridge.py            # Bridge integration (Go ↔ Python)
execution.py                # Subprocess execution and command handling
discovery.py                # Plugin discovery and catalog management
validation.py               # Pipeline validation and compliance checking
core.py                     # Enterprise services and orchestration
base.py                     # Foundation classes and factory functions
```

**Pattern**: One primary domain per module with related utilities.

### **Function Naming Conventions**

```python
# Subprocess execution functions
execute_meltano_command()   # Generic command execution
run_pipeline()              # Pipeline-specific execution
invoke_dbt()                # DBT-specific execution

# Discovery functions
discover_plugins()          # Plugin discovery
discover_catalog()          # Schema catalog discovery
list_extractors()           # Extractor listing

# Installation functions
install_plugin()            # Plugin installation
add_extractor()             # Extractor-specific installation
configure_plugin()          # Plugin configuration

# Factory functions
create_meltano_tap_service()      # Tap service factory
create_meltano_target_service()   # Target service factory
create_meltano_dbt_service()      # DBT service factory
```

**Pattern**: Verb + noun structure describing the operation clearly.

---

## 📦 **Import Patterns & Best Practices**

### **Recommended Import Styles**

#### **1. Primary Pattern (Recommended for Go Bridge)**

```python
# Import from main package - streamlined for bridge usage
import flext_meltano

# Bridge operations (after implementation)
bridge = flext_meltano.FlextMeltanoBridge()
result = bridge.get_version()

# Direct function usage
result = flext_meltano.execute_meltano_command(["--version"])
```

#### **2. Specific Module Pattern (For Library Usage)**

```python
# Import from specific modules for clarity
from flext_meltano.execution import execute_meltano_command, run_pipeline
from flext_meltano.discovery import discover_plugins
from flext_meltano.base import FlextMeltanoConfig

# More explicit and efficient
result = execute_meltano_command(["--version"])
```

#### **3. Enterprise Pattern (For Advanced Integration)**

```python
# Enterprise service composition
from flext_meltano.core import FlextMeltanoOrchestrationService
from flext_meltano.base import FlextMeltanoConfig
from flext_core import FlextResult, FlextContainer

# Service-oriented usage
config = FlextMeltanoConfig(project_root="./")
orchestrator = FlextMeltanoOrchestrationService(config)
result = orchestrator.execute_pipeline("tap-csv target-csv")
```

### **Bridge-Specific Import Patterns** (After Implementation)

```python
# For Go subprocess execution
from flext_meltano.simple_bridge import FlextMeltanoBridge

# Bridge instantiation and usage
bridge = FlextMeltanoBridge()
version_result = bridge.get_version()
pipeline_result = bridge.run_pipeline("tap-csv", "target-csv")

# JSON serializable results for Go communication
import json
response = json.dumps({
    "success": result.success,
    "data": result.data,
    "error": result.error_message if result.is_failure else None
})
```

### **Anti-Patterns (Forbidden)**

```python
# ❌ Don't import everything (breaks namespace clarity)
from flext_meltano import *

# ❌ Don't create custom result types (breaks ecosystem consistency)
class MeltanoResult:  # Use FlextResult instead
    pass

# ❌ Don't bypass bridge for Go integration
# Use FlextMeltanoBridge, not direct execution imports

# ❌ Don't import internal implementation details
from flext_meltano._internal_utils import _private_function

# ❌ Don't alias core types (confusing across ecosystem)
from flext_meltano import FlextMeltanoBridge as Bridge
```

---

## 🏛️ **Architectural Patterns**

### **Layer Separation (Clean Architecture)**

```python
# Clear architectural boundaries
┌─────────────────────────────────────┐
│      Bridge Integration Layer       │
│   (Go ↔ Python Communication)       │
├─────────────────────────────────────┤
│       Application Layer             │  # core.py, cli.py
│    (Services, Orchestration)        │
├─────────────────────────────────────┤
│        Domain Layer                 │  # execution.py, validation.py
│   (Business Logic, Operations)      │  # discovery.py, installation.py
├─────────────────────────────────────┤
│     Infrastructure Layer            │  # singer.py, dbt.py
│   (External Integrations)           │  # flext_singer.py
├─────────────────────────────────────┤
│       Foundation Layer              │  # base.py, common.py
│   (Base Classes, Utilities)         │  # exceptions.py, container.py
└─────────────────────────────────────┘
```

### **Dependency Direction**

```python
# Dependencies flow inward (Clean Architecture)
Bridge Layer → Application Layer → Domain Layer → Foundation Layer
     ↓               ↓                ↓              ↓
Infrastructure Layer → Domain Layer → Foundation Layer (OK)
```

**Rule**: Higher layers can depend on lower layers, never the reverse.

### **Bridge Integration Architecture** (TO BE IMPLEMENTED)

```python
# Bridge pattern for Go service integration
┌─────────────────┐    subprocess    ┌─────────────────┐    import     ┌─────────────────┐
│   Go Services   │ ──────────────── │  Bridge Script  │ ───────────── │ FLEXT Meltano   │
│ (FlexCore, etc) │                  │ (Python CLI)    │               │ (Library)       │
└─────────────────┘                  └─────────────────┘               └─────────────────┘
                                              │                                   │
                                              ▼                                   ▼
                                    ┌─────────────────┐               ┌─────────────────┐
                                    │ FlextMeltano    │               │ Meltano Runtime │
                                    │ Bridge          │               │ Singer Plugins  │
                                    │ (TO IMPLEMENT)  │               │ DBT Projects    │
                                    └─────────────────┘               └─────────────────┘
```

---

## 🚀 **Enterprise Patterns & Best Practices**

### **FlextResult Chain Patterns**

```python
from flext_core import FlextResult
from flext_meltano.execution import execute_meltano_command

# Pipeline execution with error handling
def execute_complete_pipeline(tap: str, target: str) -> FlextResult[str]:
    """Execute complete pipeline with validation and monitoring."""
    return (
        validate_pipeline_config(tap, target)
        .flat_map(lambda config: execute_meltano_command(["run", f"{tap}:{target}"]))
        .map(lambda result: extract_execution_metrics(result))
        .map(lambda metrics: format_pipeline_report(metrics))
    )

# Error aggregation pattern
def validate_pipeline_inputs(
    tap_name: str,
    target_name: str,
    config: dict
) -> FlextResult[dict]:
    """Validate all pipeline inputs with comprehensive error reporting."""
    errors = []

    if not tap_name or not tap_name.startswith("tap-"):
        errors.append("Invalid tap name format")
    if not target_name or not target_name.startswith("target-"):
        errors.append("Invalid target name format")
    if not config.get("database_url"):
        errors.append("Database URL is required")

    return FlextResult[None].fail(errors) if errors else FlextResult[None].ok({
        "tap": tap_name,
        "target": target_name,
        "config": config
    })
```

### **Service Composition Patterns**

```python
from flext_meltano.core import FlextMeltanoOrchestrationService
from flext_meltano.base import FlextMeltanoConfig
from flext_core import FlextContainer

class FlextMeltanoPipelineService:
    """Enterprise pipeline service with dependency injection."""

    def __init__(self, container: FlextContainer) -> None:
        self._container = container
        self._config = container.get("meltano_config").unwrap()
        self._orchestrator = container.get("orchestration_service").unwrap()

    def execute_data_pipeline(
        self,
        pipeline_spec: dict
    ) -> FlextResult[PipelineExecutionResult]:
        """Execute data pipeline with enterprise patterns."""
        return (
            self._validate_pipeline_spec(pipeline_spec)
            .flat_map(lambda spec: self._prepare_pipeline_environment(spec))
            .flat_map(lambda env: self._orchestrator.execute_pipeline(env))
            .map(lambda result: self._generate_execution_report(result))
        )

    def _validate_pipeline_spec(self, spec: dict) -> FlextResult[dict]:
        """Validate pipeline specification."""
        # Implementation with FlextResult pattern
        return FlextResult[None].ok(spec)
```

### **Configuration Management Patterns**

```python
from flext_core.config import FlextConfig
from flext_meltano.base import FlextMeltanoConfig

class FlextMeltanoSettings(FlextConfig):
    """FLEXT Meltano configuration with environment variables."""

    # Meltano configuration
    meltano_project_root: str = "."
    meltano_environment: str = "dev"
    meltano_log_level: str = "INFO"

    # Bridge configuration
    bridge_timeout: int = 300
    bridge_max_retries: int = 3

    # Plugin configuration
    auto_install_plugins: bool = True
    plugin_discovery_cache_ttl: int = 3600

    class Config:
        env_prefix = "FLEXT_MELTANO_"
        env_file = ".env"

class FlextMeltanoBridgeConfig(FlextConfig):
    """Bridge-specific configuration for Go integration."""

    # Subprocess configuration
    subprocess_timeout: int = 300
    subprocess_shell: bool = False
    subprocess_capture_output: bool = True

    # Result formatting
    result_format: str = "json"
    error_format: str = "detailed"

    class Config:
        env_prefix = "FLEXT_BRIDGE_"
```

---

## 🔧 **Module Implementation Patterns**

### **Base Service Pattern**

```python
# base.py - Foundation classes
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from flext_core import FlextResult, FlextConfig

class FlextMeltanoConfig(FlextConfig):
    """Base configuration for all FLEXT Meltano services."""

    project_root: str = "."
    environment: str = "dev"
    debug: bool = False

    class Config:
        env_prefix = "MELTANO_"

class FlextMeltanoBaseService(ABC):
    """Base service class for all FLEXT Meltano services."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        self._config = config
        self._logger = self._setup_logging()

    @abstractmethod
    def validate_configuration(self) -> FlextResult[None]:
        """Validate service configuration."""
        pass

    def _setup_logging(self):
        """Setup structured logging for the service."""
        # Implementation
        pass

class FlextMeltanoTapService(FlextMeltanoBaseService):
    """Base class for tap services."""

    @abstractmethod
    def discover_streams(self) -> FlextResult[List[object]]:
        """Discover available streams."""
        pass

    @abstractmethod
    def read_stream(self, stream_name: str) -> FlextResult[object]:
        """Read data from specific stream."""
        pass
```

### **Execution Service Pattern**

```python
# execution.py - Core execution functionality
import subprocess
from typing import Dict, List, Optional

from flext_core import FlextResult

class FlextMeltanoExecutor:
    """Asyncio-based Meltano command executor (recommended)."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        self._config = config
        self._timeout = config.subprocess_timeout

    async def execute_command(self, args: List[str]) -> FlextResult[Dict[str, object]]:
        """Execute Meltano command with error handling using asyncio."""
        try:
            process = await asyncio.create_subprocess_exec(
                "meltano",
                *args,
                cwd=self._config.project_root,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self._timeout)
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return FlextResult[None].fail("Command timed out")

            if process.returncode == 0:
                return FlextResult[None].ok({
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode(),
                    "returncode": process.returncode
                })
            return FlextResult[None].fail(
                f"Command failed with return code {process.returncode}: {stderr.decode()}"
            )
        except Exception as e:
            return FlextResult[None].fail(f"Command execution failed: {e}")

    def run_pipeline(self, tap: str, target: str) -> FlextResult[Dict[str, object]]:
        """Execute pipeline between tap and target."""
        return self.execute_command(["run", f"{tap}:{target}"])

# Convenience functions for direct usage
def execute_meltano_command(args: List[str]) -> FlextResult[Dict[str, object]]:
    """Execute Meltano command with default configuration."""
    config = FlextMeltanoConfig()
    executor = FlextMeltanoExecutor(config)
    return executor.execute_command(args)

def run_pipeline(tap: str, target: str) -> FlextResult[Dict[str, object]]:
    """Execute pipeline with default configuration."""
    config = FlextMeltanoConfig()
    executor = FlextMeltanoExecutor(config)
    return executor.run_pipeline(tap, target)
```

### **Bridge Implementation Pattern** (TO BE IMPLEMENTED)

```python

import json
from typing import Dict, List, Optional

from flext_core import FlextResult
from flext_meltano.execution import FlextMeltanoExecutor
from flext_meltano.base import FlextMeltanoConfig

class FlextMeltanoBridge:
    """Bridge class for Go service integration.

    Provides a simple interface for Go services to execute
    Meltano operations via subprocess calls with proper
    error handling and result formatting.
    """

    def __init__(self, config: Optional[FlextMeltanoConfig] = None) -> None:
        self._config = config or FlextMeltanoConfig()
        self._executor = FlextMeltanoExecutor(self._config)

    def get_version(self) -> FlextResult[Dict[str, str]]:
        """Get Meltano version information.

        Returns:
            FlextResult containing version information
        """
        result = self._executor.execute_command(["--version"])
        if result.success:
            version_output = result.data["stdout"].strip()
            return FlextResult[None].ok({
                "meltano": version_output,
                "python": sys.version.split()[0],
                "flext_meltano": "0.9.0"
            })
        return result

    def list_plugins(self) -> FlextResult[List[Dict[str, object]]]:
        """List all available plugins."""
        result = self._executor.execute_command(["discover", "all"])
        if result.success:
            # Parse plugin information from output
            plugins = self._parse_plugin_list(result.data["stdout"])
            return FlextResult[None].ok(plugins)
        return result

    def add_plugin(
        self,
        plugin_type: str,
        name: str,
        *,
        variant: Optional[str] = None,
        pip_url: Optional[str] = None
    ) -> FlextResult[str]:
        """Add plugin to Meltano project."""
        args = ["add", plugin_type, name]
        if variant:
            args.extend(["--variant", variant])
        if pip_url:
            args.extend(["--pip-url", pip_url])

        result = self._executor.execute_command(args)
        if result.success:
            return FlextResult[None].ok(f"Plugin {name} added successfully")
        return result

    def discover_catalog(self, tap_name: str) -> FlextResult[Dict[str, object]]:
        """Discover catalog from tap."""
        result = self._executor.execute_command(["invoke", tap_name, "--discover"])
        if result.success:
            try:
                catalog = json.loads(result.data["stdout"])
                return FlextResult[None].ok(catalog)
            except json.JSONDecodeError as e:
                return FlextResult[None].fail(f"Failed to parse catalog: {e}")
        return result

    def run_pipeline(
        self,
        tap: str,
        target: str,
        *,
        environment: Optional[str] = None,
        job_id: Optional[str] = None
    ) -> FlextResult[Dict[str, object]]:
        """Execute pipeline between tap and target."""
        args = ["run"]
        if environment:
            args.extend(["--environment", environment])
        args.append(f"{tap}:{target}")

        result = self._executor.execute_command(args)
        if result.success:
            return FlextResult[None].ok({
                "tap": tap,
                "target": target,
                "environment": environment or "dev",
                "job_id": job_id,
                "execution_time": self._extract_execution_time(result.data),
                "status": "completed"
            })
        return result

    def invoke_dbt(
        self,
        command: str,
        *args: str,
        **kwargs: object
    ) -> FlextResult[Dict[str, object]]:
        """Execute DBT command."""
        dbt_args = ["invoke", "dbt", command] + list(args)
        result = self._executor.execute_command(dbt_args)
        if result.success:
            return FlextResult[None].ok({
                "command": command,
                "args": args,
                "output": result.data["stdout"],
                "status": "completed"
            })
        return result

    def _parse_plugin_list(self, output: str) -> List[Dict[str, object]]:
        """Parse plugin list from Meltano output."""
        # Implementation to parse plugin information
        return []

    def _extract_execution_time(self, result_data: Dict[str, object]) -> Optional[str]:
        """Extract execution time from command output."""
        # Implementation to extract timing information
        return None

# Factory function for bridge creation
def create_flext_meltano_bridge(
    config: Optional[FlextMeltanoConfig] = None
) -> FlextMeltanoBridge:
    """Create FlextMeltanoBridge instance with configuration."""
    return FlextMeltanoBridge(config)
```

---

## 📋 **Refactoring Roadmap**

### **Phase 1: Critical Module Fixes** (1-2 days)

1. **Implement missing bridge module**:

   ```bash
   touch src/flext_meltano/simple_bridge.py
   # Implement complete FlextMeltanoBridge class
   ```

2. **Fix type errors**:

   ```python
   # Fix cli.py:157, validation.py:250,344
   # Ensure proper type annotations
   ```

3. **Refactor **init**.py exports** (PRIORITY):

   ```python
   # Current: 290+ exports in single file
   # Target: Organized exports by functional area

   # Bridge integration
   __all__: FlextTypes.Core.StringList = [
       "FlextMeltanoBridge",  # After implementation

       # Core execution
       "execute_meltano_command",
       "run_pipeline",
       "FlextMeltanoExecutor",

       # Base classes
       "FlextMeltanoConfig",
       "FlextMeltanoBaseService",
       "FlextMeltanoTapService",
       "FlextMeltanoTargetService",

       # Service classes
       "FlextMeltanoOrchestrationService",
       "FlextMeltanoDbtService",

       # Discovery and installation
       "discover_plugins",
       "discover_catalog",
       "install_plugin",

       # Singer integration (selective re-exports)
       "Stream", "Tap", "Target", "Sink",

       # Configuration and utilities
       "FlextMeltanoError",
       "FlextMeltanoResult",
   ]
   ```

### **Phase 2: Module Organization** (1-2 weeks)

1. **Split overloaded modules**:

   ```python
   # Break large modules into focused components
   singer/ # Directory for Singer-related modules
   ├── __init__.py
   ├── base.py       # Singer base classes
   ├── stream.py     # Stream handling
   └── unified.py    # Unified interface

   bridge/ # Directory for bridge components
   ├── __init__.py
   ├── core.py       # FlextMeltanoBridge
   ├── models.py     # Request/response models
   └── utils.py      # Bridge utilities
   ```

2. **Standardize naming conventions**:

   ```python
   # Consistent FlextMeltano prefix
   FlextMeltanoTapService      → keep
   FlextSingerTap              → FlextMeltanoSingerTap
   create_tap()                → create_meltano_tap()
   flext_meltano_execute_job() → execute_meltano_job()
   ```

### **Phase 3: Enterprise Enhancement** (2-4 weeks)

1. **Add configuration management**:

   ```python
   # config.py - Centralized configuration
   class FlextMeltanoEnterpriseConfig(FlextConfig):
       # Bridge settings
       bridge: FlextMeltanoBridgeConfig

       # Execution settings
       execution: FlextMeltanoExecutionConfig

       # Plugin settings
       plugins: FlextMeltanoPluginConfig
   ```

2. **Implement monitoring patterns**:

   ```python
   # monitoring.py - Observability integration
   from flext_observability import FlextMetrics, FlextTracing

   class FlextMeltanoMonitoringService:
       def track_pipeline_execution(self, pipeline_id: str) -> None:
           # Implementation
   ```

3. **Add security hardening**:

   ```python
   # security.py - Security patterns
   class FlextMeltanoSecurityService:
       def validate_subprocess_args(self, args: List[str]) -> FlextResult[List[str]]:
           # Implementation
   ```

---

## 🧪 **Testing Organization**

### **Test Structure (Mirrors Module Organization)**

```python
# Test structure reflecting ideal module organization
tests/
├── unit/                           # Unit tests (isolated)
│   ├── test_base.py               # Tests for base.py
│   ├── test_execution.py          # Tests for execution.py
│   ├── test_simple_bridge.py      # Tests for bridge (after implementation)
│   ├── test_discovery.py          # Tests for discovery.py
│   └── test_core.py               # Tests for core.py
├── integration/                    # Integration tests
│   ├── test_meltano_integration.py # Real Meltano operations
│   ├── test_bridge_integration.py  # Bridge ↔ library integration
│   └── test_subprocess_execution.py # Subprocess execution
├── e2e/                           # End-to-end tests
│   ├── test_pipeline_execution.py  # Complete pipeline tests
│   └── test_go_bridge_simulation.py # Go integration simulation
├── conftest.py                    # Test configuration
└── fixtures/                      # Test data and fixtures
    ├── meltano_configs/           # Sample Meltano configurations
    ├── pipeline_specs/            # Pipeline test specifications
    └── bridge_responses/          # Expected bridge responses
```

### **Bridge Testing Patterns** (After Implementation)

```python
import pytest
from flext_meltano.simple_bridge import FlextMeltanoBridge
from flext_meltano.base import FlextMeltanoConfig

class TestFlextMeltanoBridge:
    """Test bridge functionality for Go integration."""

    @pytest.fixture
    def bridge(self):
        """Provide bridge instance for testing."""
        config = FlextMeltanoConfig(project_root="./tests/fixtures")
        return FlextMeltanoBridge(config)

    def test_get_version_success(self, bridge):
        """Test successful version retrieval."""
        result = bridge.get_version()

        assert result.success
        assert "meltano" in result.data
        assert "python" in result.data
        assert "flext_meltano" in result.data

    def test_run_pipeline_success(self, bridge):
        """Test successful pipeline execution."""
        result = bridge.run_pipeline("tap-csv", "target-csv")

        assert result.success
        assert result.data["tap"] == "tap-csv"
        assert result.data["target"] == "target-csv"
        assert result.data["status"] == "completed"

    def test_run_pipeline_invalid_tap(self, bridge):
        """Test pipeline execution with invalid tap."""
        result = bridge.run_pipeline("invalid-tap", "target-csv")

        assert result.is_failure
        assert "invalid-tap" in result.error_message.lower()

# Subprocess simulation for Go integration testing
def test_bridge_subprocess_simulation():
    """Simulate Go service calling bridge via subprocess."""
    import subprocess
    import json

    # Simulate Go call (pseudo); prefer async wrappers or exec.CommandContext in Go
    class Result:
        def __init__(self, returncode: int, stdout: str = '', stderr: str = '') -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr
    result = Result(0, json.dumps({"success": True, "data": {"version": "0.1.0"}}))

    # This will fail until bridge is implemented
    # After implementation, should return JSON response
    if result.returncode == 0:
        response = json.loads(result.stdout)
        assert response["success"] is True
        assert "data" in response
```

---

## 📏 **Code Quality Standards**

### **Module Quality Requirements**

```python
# Quality standards for each module
class ModuleQualityStandards:
    """Quality requirements for FLEXT Meltano modules."""


    mypy_compliance: bool = True          # Strict MyPy validation
    type_annotation_coverage: float = 1.0 # 100% type annotations

    # Testing
    test_coverage: float = 0.90           # 90% minimum coverage
    unit_test_required: bool = True       # Unit tests mandatory
    integration_test_required: bool = True # Integration tests mandatory

    # Documentation
    docstring_coverage: float = 1.0       # 100% docstring coverage
    api_documentation: bool = True        # API docs required

    # Code quality
    linting_compliance: bool = True
    security_scanning: bool = True        # Bandit + pip-audit

    # Module-specific requirements
    max_exports_per_module: int = 50      # Prevent overloaded modules
    max_lines_per_module: int = 1000      # Encourage focused modules
    dependency_injection: bool = True     # DI container usage
```

### **Documentation Standards**

```python
def execute_meltano_command(
    args: List[str],
    *,
    timeout: Optional[int] = None,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None
) -> FlextResult[Dict[str, object]]:
    """
    Execute Meltano command via subprocess with comprehensive error handling.

    This function provides the core subprocess execution functionality for
    FLEXT Meltano, enabling Go services to execute Meltano operations through
    the bridge pattern. It implements proper timeout handling, environment
    management, and result formatting for reliable integration.

    Args:
        args: Meltano command arguments (e.g., ["--version"], ["run", "tap:target"])
        timeout: Command timeout in seconds (default: 300)
        cwd: Working directory for command execution (default: current directory)
        env: Additional environment variables for command execution

    Returns:
        FlextResult[Dict[str, object]]: Success contains execution details including
        stdout, stderr, and return code. Failure contains detailed error message
        with execution context for debugging.

    Example:
        >>> result = execute_meltano_command(["--version"])
        >>> if result.success:
        ...     print(f"Meltano version: {result.data['stdout'].strip()}")
        ... else:
        ...     print(f"Command failed: {result.error_message}")

    Bridge Usage:
        This function is the foundation for bridge operations and is called
        by FlextMeltanoBridge methods to provide Go ↔ Python integration.

    Raises:
        No exceptions are raised; all errors are captured in FlextResult.
    """
    # Implementation
```

---

## 🔄 **Migration Strategy**

### **Current → Target Migration Plan**

```python
# Phase 1: Immediate fixes (1-2 days)
PHASE_1_ACTIONS = [
    "Implement src/flext_meltano/simple_bridge.py",
    "Fix cli.py:157 type error",
    "Fix validation.py:250,344 type errors",
    "Resolve test_singer_integration.py:135 failure",
    "Validate make validate passes completely"
]

# Phase 2: Module organization (1-2 weeks)
PHASE_2_ACTIONS = [
    "Refactor __init__.py from 290+ to ~50 focused exports",
    "Split Singer modules into singer/ directory",
    "Create bridge/ directory for bridge components",
    "Standardize FlextMeltano* naming conventions",
    "Implement configuration management patterns"
]

# Phase 3: Enterprise enhancement (2-4 weeks)
PHASE_3_ACTIONS = [
    "Add monitoring and observability integration",
    "Implement security hardening patterns",
    "Complete API documentation and examples",
    "Performance optimization for bridge operations",
    "Add comprehensive integration testing"
]
```

### **Backward Compatibility Strategy**

```python
# Deprecation pattern for module changes
from warnings import warn

# Maintain backward compatibility during transition
def flext_meltano_execute_job(*args, **kwargs):
    """
    DEPRECATED: Use execute_meltano_command instead.

    This function will be removed in version 0.9.0.
    Use execute_meltano_command for consistent naming.
    """
    warn(
        "flext_meltano_execute_job is deprecated. Use execute_meltano_command instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return execute_meltano_command(*args, **kwargs)

# Alias for smooth transition
FlextMeltanoResult = FlextResult  # Use FlextResult from flext-core
```

---

## 📋 **Module Creation Checklist**

### **New Module Requirements**

- [ ] **Naming**: Clear, descriptive name following conventions
- [ ] **Layer**: Placed in appropriate architectural layer
- [ ] **Dependencies**: Only imports from same or lower layers
- [ ] **Types**: Complete type annotations with MyPy compliance
- [ ] **Error Handling**: Uses FlextResult for all error conditions
- [ ] **Documentation**: Comprehensive docstrings with examples
- [ ] **Tests**: 90% coverage with unit and integration tests
- [ ] **Exports**: Added to appropriate `__init__.py` if public API
- [ ] **Bridge**: Compatible with Go integration patterns
- [ ] **Quality**: Passes all quality gates (lint, type, test, security)

### **Quality Gate Validation**

```bash
# Required before module acceptance
make lint
make type-check          
make test                  # 90% coverage requirement
make security              # Bandit + pip-audit scanning
make validate              # Complete quality gate validation

# Bridge integration testing (after implementation)
python scripts/flext_meltano_bridge.py version
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv
```

---

**Last Updated**: 2025-08-01
**Target Audience**: FLEXT Meltano developers and Go integration developers
**Scope**: Python module organization for Go ↔ Python bridge integration
**Status**: ⚠️ **Requires Critical Fixes** - 3 issues must be resolved before implementation
