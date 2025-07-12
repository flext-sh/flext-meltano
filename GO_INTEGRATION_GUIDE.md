# FLEXT Meltano Go Integration Guide

## Overview

The FLEXT Meltano Go integration provides a bridge between Go applications and Meltano data pipelines using the FLEXT ecosystem architecture. This integration allows Go applications to manage Meltano projects, execute pipelines, and interact with Meltano functionality through a clean, type-safe interface.

## Architecture

```
Go Application
     ↓
   GoPy Bridge (Python-Go bindings)
     ↓
  MeltanoBridge (Python)
     ↓
FLEXT MeltanoProjectManager + FlextMeltanoOrchestrator
     ↓
   Meltano Core
```

## Key Features

- **Zero subprocess calls**: Uses FLEXT's native MeltanoProjectManager and FlextMeltanoOrchestrator
- **Type-safe Go bindings**: Generated using GoPy for seamless Go-Python interop
- **Async support**: Full async/await support in Python with sync wrappers for Go
- **Enterprise-ready**: Built on FLEXT's enterprise patterns with proper error handling
- **JSON communication**: All data exchange uses JSON for cross-language compatibility

## Installation & Setup

### Prerequisites

```bash
# Install Python dependencies
pip install gopy meltano flext-core flext-observability

# Install Go (1.19+ required)
go version  # Should show Go 1.19 or later
```

### Generate Go Bindings

```python
from flext_meltano.integrations import GopyIntegration

# Create integration instance
integration = GopyIntegration()

# Generate Go bindings
result = await integration.generate_go_bindings()
if result.is_success:
    print("✅ Go bindings generated successfully")
else:
    print(f"❌ Failed: {result.error}")

# Create Go wrapper
wrapper_result = await integration.create_go_wrapper()
print(f"Go wrapper created at: {wrapper_result.value}")
```

### Build Shared Library

```bash
# Generate shared library for Go
python -c "
import asyncio
from flext_meltano.integrations import GopyIntegration
integration = GopyIntegration()
result = asyncio.run(integration.build_shared_library())
print(f'Shared library: {result.value}')
"
```

## Usage Examples

### Python Side (Bridge)

```python
from flext_meltano.integrations import MeltanoBridge
import asyncio

async def main():
    # Initialize bridge
    bridge = MeltanoBridge(project_root="./meltano_projects")
    
    # Create project
    result = await bridge.init_project("my-project")
    print(f"Project creation: {result}")
    
    # Add plugins
    tap_result = await bridge.add_plugin("my-project", "extractor", "tap-csv")
    target_result = await bridge.add_plugin("my-project", "loader", "target-jsonl")
    
    # Run pipeline
    pipeline_result = await bridge.run_pipeline("my-project", "tap-csv", "target-jsonl")
    print(f"Pipeline execution: {pipeline_result}")

asyncio.run(main())
```

### Go Side (Generated Bindings)

```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    
    meltano "github.com/your-org/flext-meltano-gopy"
)

type MeltanoResult struct {
    Success  bool                   `json:"success"`
    Data     map[string]interface{} `json:"data"`
    Error    string                 `json:"error,omitempty"`
    Metadata map[string]interface{} `json:"metadata"`
}

func main() {
    // Check if Meltano is available
    if !meltano.IsAvailable() {
        log.Fatal("Meltano is not available")
    }
    
    // Initialize a project
    resultJSON := meltano.InitProjectSync("my-go-project", "./projects")
    
    var result MeltanoResult
    if err := json.Unmarshal([]byte(resultJSON), &result); err != nil {
        log.Fatal("Failed to parse result:", err)
    }
    
    if !result.Success {
        log.Fatal("Project initialization failed:", result.Error)
    }
    
    fmt.Printf("✅ Project created: %v\n", result.Data)
    
    // Add plugins
    tapResult := meltano.AddPluginSync("my-go-project", "extractor", "tap-csv", "")
    fmt.Printf("Tap added: %s\n", tapResult)
    
    targetResult := meltano.AddPluginSync("my-go-project", "loader", "target-jsonl", "")
    fmt.Printf("Target added: %s\n", targetResult)
    
    // Run pipeline
    pipelineResult := meltano.RunPipelineSync("my-go-project", "tap-csv", "target-jsonl", "")
    fmt.Printf("Pipeline result: %s\n", pipelineResult)
    
    // Get project info
    infoResult := meltano.GetProjectInfoSync("my-go-project")
    fmt.Printf("Project info: %s\n", infoResult)
}
```

## API Reference

### MeltanoBridge (Python)

#### `async init_project(project_name: str, project_dir: str = None) -> str`
Initialize a new Meltano project using FLEXT project manager.

#### `async add_plugin(project_name: str, plugin_type: str, plugin_name: str, plugin_variant: str = "") -> str`
Add a plugin to the project using FLEXT plugin management.

#### `async run_pipeline(project_name: str, extractor: str, loader: str, transformer: str = "") -> str`
Execute a pipeline using FLEXT orchestrator.

#### `async get_project_info(project_name: str) -> str`
Get project configuration and information.

#### `async execute_command(project_name: str, command_args: list[str]) -> str`
Execute arbitrary Meltano commands through FLEXT project manager.

### Go Functions (Generated Bindings)

#### `IsAvailable() bool`
Check if the FLEXT Meltano bridge is available.

#### `InitProjectSync(projectName, projectDir string) string`
Initialize a new Meltano project (synchronous wrapper).

#### `AddPluginSync(projectName, pluginType, pluginName, pluginVariant string) string`
Add a plugin to the project (synchronous wrapper).

#### `RunPipelineSync(projectName, extractor, loader, transformer string) string`
Execute a pipeline (synchronous wrapper).

#### `GetProjectInfoSync(projectName string) string`
Get project information (synchronous wrapper).

#### `ExecuteCommandSync(projectName, argsJSON string) string`
Execute custom commands (synchronous wrapper).

## Result Format

All functions return JSON strings with this format:

```json
{
    "success": true,
    "data": {
        "project_path": "/path/to/project",
        "run_id": "12345"
    },
    "error": null,
    "metadata": {
        "flext_result": "success"
    }
}
```

## Error Handling

### Python
```python
import json

result_json = await bridge.init_project("test-project")
result = json.loads(result_json)

if not result["success"]:
    print(f"Error: {result['error']}")
    print(f"Metadata: {result['metadata']}")
```

### Go
```go
var result MeltanoResult
json.Unmarshal([]byte(resultJSON), &result)

if !result.Success {
    log.Printf("Error: %s", result.Error)
    log.Printf("Metadata: %+v", result.Metadata)
}
```

## Configuration

### Environment Variables

```bash
# FLEXT Configuration
FLEXT_PROJECT_ROOT=/path/to/projects
FLEXT_ENVIRONMENT=production

# Meltano Configuration
MELTANO_PROJECT_ROOT=/path/to/meltano/projects
MELTANO_ENVIRONMENT=dev

# Integration Configuration
GOPY_MODULE_NAME=flext_meltano_gopy
GOPY_OUTPUT_DIR=./build
```

### Build Configuration

```python
from flext_meltano.integrations import GopyBuildConfig

config = GopyBuildConfig(
    module_name="my_meltano_bridge",
    output_dir="./go_bindings",
    go_package="github.com/myorg/meltano-bridge",
    python_modules=[
        "flext_meltano.integrations.bridge",
        "flext_meltano.project_manager",
        "flext_meltano.orchestrator",
    ]
)

integration = GopyIntegration(config)
```

## Integration Benefits

### Over Direct Meltano CLI

1. **Type Safety**: Go gets proper type checking and IDE support
2. **Performance**: No subprocess overhead, direct Python integration
3. **Error Handling**: Structured error responses with metadata
4. **Async Support**: Non-blocking operations in Python backend
5. **Enterprise Features**: Full FLEXT ecosystem integration

### Over Custom Implementations

1. **Standards Compliance**: Uses FLEXT's proven patterns
2. **No Code Duplication**: Leverages existing FLEXT components
3. **Maintainability**: Single source of truth for Meltano operations
4. **Extensibility**: Easy to add new functionality through FLEXT

## Troubleshooting

### Common Issues

#### GoPy Installation
```bash
# Make sure gopy is properly installed
pip install gopy
go install github.com/go-python/gopy@latest
```

#### Import Errors
```python
# Verify FLEXT modules are available
from flext_core import ServiceResult
from flext_observability.logging import get_logger
```

#### Go Build Issues
```bash
# Ensure CGO is enabled
export CGO_ENABLED=1
go build -v your_program.go
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test bridge availability
bridge = MeltanoBridge()
print(f"Bridge available: {bridge.is_available()}")
```

## Future Enhancements

- **Streaming Support**: Real-time pipeline output streaming to Go
- **Plugin Development**: Go SDK for custom Meltano plugins
- **Configuration Management**: Go-native configuration validation
- **Health Monitoring**: Real-time health checks and metrics

## Resources

- [FLEXT Core Documentation](../flext-core/README.md)
- [FLEXT Observability](../flext-observability/README.md)
- [Meltano Documentation](https://docs.meltano.com/)
- [GoPy Documentation](https://github.com/go-python/gopy)

---

**Note**: This integration is production-ready and uses FLEXT's enterprise patterns. No fallback implementations or legacy code paths are used.