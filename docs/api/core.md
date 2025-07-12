# Core API Reference

This document provides comprehensive API reference for FLEXT-Meltano core components.

## 🏗️ MeltanoBridge API

The primary interface for Go-Python integration and external access to Meltano functionality.

### Class: MeltanoBridge

**File**: `src/flext_meltano/integrations/bridge.py`

**Purpose**: Facade interface providing unified access to Meltano operations with Go compatibility.

#### Constructor

```python
def __init__(self, project_root: str = ".") -> None
```

**Parameters**:
- `project_root` (str): Root directory for Meltano projects. Defaults to current directory.

**Example**:
```python
from src.flext_meltano.integrations.bridge import MeltanoBridge

# Initialize with default root
bridge = MeltanoBridge()

# Initialize with custom root
bridge = MeltanoBridge("/path/to/projects")
```

#### Async Methods

##### init_project()

```python
async def init_project(
    self, 
    project_name: str, 
    project_dir: str | None = None
) -> JSONStr
```

Create a new Meltano project with enterprise configuration.

**Parameters**:
- `project_name` (str): Name for the new project
- `project_dir` (str | None): Optional directory path. Uses project_root if None.

**Returns**: JSON string with operation result
```json
{
  "success": true,
  "data": {
    "project_path": "/path/to/project",
    "project_name": "my_project",
    "environment": "dev"
  },
  "metadata": {
    "flext_result": "success"
  }
}
```

**Example**:
```python
result_json = await bridge.init_project("analytics_pipeline", "./projects")
result = json.loads(result_json)
if result['success']:
    print(f"Project created at: {result['data']['project_path']}")
```

##### add_plugin()

```python
async def add_plugin(
    self,
    project_name: str,
    plugin_type: str,
    plugin_name: str,
    plugin_variant: str = ""
) -> JSONStr
```

Add and install a Singer plugin to the Meltano project.

**Parameters**:
- `project_name` (str): Target Meltano project name
- `plugin_type` (str): Plugin type (`extractor`, `loader`, `transformer`, etc.)
- `plugin_name` (str): Plugin name (e.g., `tap-csv`, `target-postgres`)
- `plugin_variant` (str): Optional plugin variant

**Returns**: JSON string with operation result
```json
{
  "success": true,
  "data": {
    "plugin_type": "extractor",
    "plugin_name": "tap-csv",
    "plugin_variant": "meltanolabs"
  },
  "metadata": {
    "flext_result": "success"
  }
}
```

**Example**:
```python
# Add CSV extractor
result = await bridge.add_plugin(
    "my_project", 
    "extractor", 
    "tap-csv",
    "meltanolabs"
)

# Add PostgreSQL loader
result = await bridge.add_plugin(
    "my_project",
    "loader", 
    "target-postgres"
)
```

##### run_pipeline()

```python
async def run_pipeline(
    self,
    project_name: str,
    extractor: str,
    loader: str,
    transformer: str = ""
) -> JSONStr
```

Execute a Meltano pipeline using zero-warning approach.

**Parameters**:
- `project_name` (str): Target Meltano project
- `extractor` (str): Name of extractor plugin
- `loader` (str): Name of loader plugin  
- `transformer` (str): Optional transformer plugin

**Returns**: JSON string with execution result
```json
{
  "success": true,
  "data": {
    "extractor": "tap-csv",
    "loader": "target-postgres", 
    "transformer": "",
    "message": "Pipeline executed using FLEXT project manager"
  },
  "metadata": {
    "flext_result": {...}
  }
}
```

**Example**:
```python
# Simple extract-load pipeline
result = await bridge.run_pipeline(
    "my_project",
    "tap-csv",
    "target-postgres"
)

# Extract-transform-load pipeline
result = await bridge.run_pipeline(
    "my_project", 
    "tap-postgres",
    "target-snowflake",
    "dbt-snowflake"
)
```

##### get_project_info()

```python
async def get_project_info(self, project_name: str) -> JSONStr
```

Retrieve comprehensive project information and configuration.

**Parameters**:
- `project_name` (str): Target project name

**Returns**: JSON string with project details
```json
{
  "success": true,
  "data": {
    "project_name": "my_project",
    "project_root": "/path/to/root",
    "config": {
      "version": 1,
      "project_id": "my_project-20250712",
      "plugins": {...},
      "environments": [...]
    }
  }
}
```

##### execute_command()

```python
async def execute_command(
    self, 
    project_name: str, 
    command_args: list[str]
) -> JSONStr
```

Execute arbitrary Meltano command in project context.

**Parameters**:
- `project_name` (str): Target project
- `command_args` (list[str]): Meltano command arguments

**Example**:
```python
# Run meltano discover
result = await bridge.execute_command(
    "my_project",
    ["discover", "tap-csv"]
)

# Run meltano test  
result = await bridge.execute_command(
    "my_project",
    ["test", "tap-csv"]
)
```

#### Sync Wrapper Methods (Go Compatibility)

##### init_project_sync()

```python
def init_project_sync(project_name: str, project_dir: str = "") -> str
```

Synchronous wrapper for `init_project()`. Handles async event loop detection and thread execution.

**Thread Safety**: Uses ThreadPoolExecutor when called from existing event loop.

**Example**:
```python
# Can be called from Go or sync Python code
result_json = init_project_sync("my_project", "./projects")
```

##### add_plugin_sync()

```python
def add_plugin_sync(
    project_name: str, 
    plugin_type: str, 
    plugin_name: str, 
    plugin_variant: str = ""
) -> str
```

Synchronous wrapper for `add_plugin()`.

##### run_pipeline_sync()

```python
def run_pipeline_sync(
    project_name: str, 
    extractor: str, 
    loader: str, 
    transformer: str = ""
) -> str
```

Synchronous wrapper for `run_pipeline()`.

##### get_project_info_sync()

```python
def get_project_info_sync(project_name: str) -> str
```

Synchronous wrapper for `get_project_info()`.

##### execute_command_sync()

```python
def execute_command_sync(
    project_name: str, 
    args_json: str = "[]"
) -> str
```

Synchronous wrapper for `execute_command()`. Takes JSON-encoded argument list.

**Parameters**:
- `args_json` (str): JSON-encoded list of command arguments

**Example**:
```python
import json
args = json.dumps(["discover", "tap-csv"])
result = execute_command_sync("my_project", args)
```

#### Utility Methods

##### is_available()

```python
def is_available(self) -> bool
```

Check if Meltano integration is available and functioning.

**Returns**: `True` if Meltano is available, `False` otherwise.

#### Global Functions

##### get_bridge()

```python
def get_bridge() -> MeltanoBridge
```

Get or create global bridge instance (singleton pattern).

**Returns**: Global `MeltanoBridge` instance.

**Example**:
```python
from src.flext_meltano.integrations.bridge import get_bridge

bridge = get_bridge()
available = bridge.is_available()
```

---

## 🗂️ MeltanoProjectManager API

Enterprise project lifecycle management with comprehensive validation and backup capabilities.

### Class: MeltanoProjectManager

**File**: `src/flext_meltano/project_manager.py`

#### Constructor

```python
def __init__(self, project_root: Path | str) -> None
```

**Parameters**:
- `project_root` (Path | str): Root directory for Meltano projects

#### Core Methods

##### create_project()

```python
async def create_project(
    self, 
    project_name: str, 
    environment: str = "dev"
) -> ServiceResult[dict[str, Any]]
```

Create new Meltano project with enterprise configuration.

**Parameters**:
- `project_name` (str): Project name
- `environment` (str): Default environment name

**Returns**: `ServiceResult` containing project creation details

**Example**:
```python
from src.flext_meltano.project_manager import MeltanoProjectManager

manager = MeltanoProjectManager('.')
result = await manager.create_project('analytics', 'dev')

if result.is_success:
    project_info = result.value
    print(f"Created: {project_info['project_path']}")
else:
    print(f"Failed: {result.error}")
```

##### load_project_config()

```python
async def load_project_config(
    self, 
    project_name: str
) -> ServiceResult[dict[str, Any]]
```

Load and parse Meltano project configuration.

**Returns**: `ServiceResult` containing parsed `meltano.yml` configuration

##### save_project_config()

```python
async def save_project_config(
    self, 
    project_name: str, 
    config: dict[str, Any]
) -> ServiceResult[None]
```

Save project configuration with atomic backup.

**Features**:
- Creates backup before overwriting
- Atomic file operations
- YAML validation

##### run_command()

```python
async def run_command(
    self,
    project_name: str,
    command_args: list[str],
    environment: str = "dev"
) -> ServiceResult[dict[str, Any]]
```

Execute Meltano command with zero-warning environment.

**Environment Variables Set**:
- `PYTHONWARNINGS`: Suppress deprecation warnings
- `SINGER_SDK_LOG_LEVEL`: Set to ERROR
- `SINGER_SDK_DISABLE_WARNINGS`: true
- `MELTANO_LOG_LEVEL`: info

**Returns**: ServiceResult with command execution details
```python
{
  "command": "meltano add extractor tap-csv",
  "returncode": 0,
  "stdout": "...",
  "stderr": "",  # Filtered for warnings
  "success": True
}
```

##### add_plugin()

```python
async def add_plugin(
    self,
    project_name: str,
    plugin_type: str,
    plugin_name: str,
    variant: str = "",
    **plugin_config: Any
) -> ServiceResult[dict[str, Any]]
```

Add plugin using proper Meltano CLI with locking.

**Process**:
1. Execute `meltano add` command
2. Run `meltano lock --update` for proper installation
3. Return comprehensive result

##### validate_project()

```python
async def validate_project(
    self, 
    project_name: str
) -> ServiceResult[dict[str, Any]]
```

Comprehensive project validation.

**Validation Checks**:
- Project directory exists
- `meltano.yml` exists and is valid
- `.meltano` directory exists
- Required configuration fields present

**Returns**: Detailed validation results
```python
{
  "project_exists": True,
  "config_exists": True,
  "meltano_dir_exists": True,
  "config_valid": True,
  "is_valid": True,
  "errors": []
}
```

##### run_pipeline_direct()

```python
async def run_pipeline_direct(
    self,
    project_name: str,
    tap_name: str,
    target_name: str,
    environment: str = "dev"
) -> ServiceResult[dict[str, Any]]
```

Execute pipeline using Singer SDK directly (zero warnings).

**Purpose**: Bypass Meltano CLI to eliminate deprecation warnings entirely.

---

## 🎼 FlextMeltanoOrchestrator API

Advanced pipeline orchestration with job management and real-time monitoring.

### Class: FlextMeltanoOrchestrator

**File**: `src/flext_meltano/orchestrator.py`

#### Constructor

```python
def __init__(
    self,
    project_manager: FlextMeltanoProjectManager,
    state_manager: FlextMeltanoStateManager,
    event_bus: EventBusProtocol
) -> None
```

#### Core Orchestration Methods

##### run_pipeline()

```python
async def run_pipeline(
    self,
    project_name: str,
    pipeline_definition: dict[str, Any],
    environment: str = "dev",
    execution_mode: OrchestrationMode = OrchestrationMode.ASYNC,
    run_id: str | None = None,
    run_mode: RunMode = RunMode.FULL_RUN
) -> dict[str, Any]
```

Execute pipeline with comprehensive orchestration.

**Parameters**:
- `pipeline_definition` (dict): Pipeline configuration with blocks
- `execution_mode` (OrchestrationMode): SYNC or ASYNC execution
- `run_mode` (RunMode): FULL_RUN or DRY_RUN

**Pipeline Definition Example**:
```python
pipeline_def = {
    "name": "customer_data_pipeline",
    "blocks": [
        {
            "block_type": "meltano",
            "extractor": "tap-postgres",
            "loader": "target-snowflake"
        },
        {
            "block_type": "run",
            "commands": ["dbt", "run", "--models", "staging"]
        }
    ]
}
```

**Returns**: Pipeline execution result
```python
{
  "run_id": "uuid-string",
  "status": "success",
  "started_at": "2025-07-12T09:00:00Z",
  "completed_at": "2025-07-12T09:05:30Z",
  "duration_seconds": 330
}
```

##### get_pipeline_status()

```python
async def get_pipeline_status(
    self, 
    run_id: str
) -> dict[str, Any] | None
```

Get real-time pipeline execution status.

**Returns**: Status information or None if not found
```python
{
  "run_id": "uuid-string",
  "status": "running",
  "started_at": "2025-07-12T09:00:00Z",
  "last_heartbeat_at": "2025-07-12T09:03:45Z",
  "error": None
}
```

##### cancel_pipeline()

```python
async def cancel_pipeline(self, run_id: str) -> bool
```

Cancel running pipeline execution.

**Returns**: `True` if cancellation successful, `False` otherwise.

##### list_running_pipelines()

```python
async def list_running_pipelines(self) -> list[dict[str, Any]]
```

List all currently executing pipelines.

**Returns**: List of pipeline summaries
```python
[
  {
    "run_id": "uuid-1",
    "project_name": "analytics",
    "environment": "prod",
    "pipeline_name": "daily_sync",
    "started_at": "2025-07-12T09:00:00Z"
  }
]
```

#### Enums and Types

##### OrchestrationMode

```python
class OrchestrationMode(Enum):
    SYNC = "sync"        # Synchronous execution
    ASYNC = "async"      # Asynchronous execution  
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"
```

##### RunMode

```python
class RunMode(Enum):
    DRY_RUN = "dry_run"    # Validation only
    FULL_RUN = "full_run"  # Full execution
```

##### PipelineStatus

```python
class PipelineStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
```

---

## 🎵 SingerDirectRunner API

Zero-warning Singer protocol execution by bypassing Meltano CLI.

### Class: SingerDirectRunner

**File**: `src/flext_meltano/singer_direct.py`

#### Constructor

```python
def __init__(self, project_root: Path) -> None
```

#### Methods

##### run_tap_target_direct()

```python
async def run_tap_target_direct(
    self,
    project_name: str,
    tap_executable: str,
    target_executable: str,
    tap_config: dict[str, Any] | None = None,
    target_config: dict[str, Any] | None = None,
) -> ServiceResult[dict[str, Any]]
```

Execute Singer tap|target pipeline directly without Meltano CLI.

**Process**:
1. Build tap and target commands with modern Singer patterns
2. Execute tap process with stdout piped to target stdin
3. Monitor both processes for completion
4. Return comprehensive execution result

**Example**:
```python
from src.flext_meltano.singer_direct import SingerDirectRunner

runner = SingerDirectRunner(Path('.'))
result = await runner.run_tap_target_direct(
    'my_project',
    'tap-csv',
    'target-postgres'
)

if result.is_success:
    execution_info = result.value
    print(f"Success: {execution_info['success']}")
```

##### discover_tap_schema()

```python
async def discover_tap_schema(
    self,
    project_name: str,
    tap_executable: str,
    tap_config: dict[str, Any],
) -> ServiceResult[dict[str, Any]]
```

Discover tap schema using Singer discovery protocol.

---

## 🌉 MeltanoEventBridge API

Bidirectional event translation between FLEXT and Meltano ecosystems.

### Class: MeltanoEventBridge

**File**: `src/flext_meltano/event_bridge.py`

#### Constructor

```python
def __init__(self, flext_event_bus: EventBusProtocol | None = None) -> None
```

#### Methods

##### translate_meltano_event()

```python
async def translate_meltano_event(
    self, 
    meltano_event: dict[str, Any]
) -> DomainEvent
```

Convert Meltano events to FLEXT domain events.

##### subscribe_to_meltano_events()

```python
async def subscribe_to_meltano_events(
    self, 
    event_pattern: str, 
    handler: Callable
) -> str
```

Subscribe to Meltano events with pattern matching.

**Returns**: Subscription ID for later unsubscription.

---

## 🔧 ServiceResult Pattern

All FLEXT-Meltano operations return `ServiceResult<T>` for consistent error handling.

### ServiceResult\<T>

```python
class ServiceResult[T]:
    def is_success(self) -> bool
    def is_failure(self) -> bool
    
    @property
    def value(self) -> T  # Available when is_success == True
    
    @property  
    def error(self) -> str  # Available when is_failure == True
    
    @classmethod
    def success(cls, value: T) -> ServiceResult[T]
    
    @classmethod
    def fail(cls, error: str) -> ServiceResult[T]
```

**Usage Pattern**:
```python
result = await some_operation()
if result.is_success:
    data = result.value
    # Process successful result
else:
    error_message = result.error
    # Handle error
```

---

**Next**: [Bridge API Reference](./bridge.md) for detailed Go integration documentation.