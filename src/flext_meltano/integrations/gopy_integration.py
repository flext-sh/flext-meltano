"""GoPy Integration for FLEXT Meltano.

This module provides Python-Go bridge functionality using gopy,
enabling Go applications to call Meltano operations through Python.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from flext_core import ServiceResult
from flext_observability.logging import get_logger

logger = get_logger(__name__)


@dataclass
class GopyBuildConfig:
    """Configuration for GoPy build process."""
    
    module_name: str = "flext_meltano_gopy"
    output_dir: str = "build"
    go_package: str = "github.com/flext-sh/flext-meltano-gopy"
    python_modules: list[str] = None
    
    def __post_init__(self):
        if self.python_modules is None:
            self.python_modules = [
                "flext_meltano.integrations.bridge",
                "flext_meltano.project_manager",
                "flext_meltano.orchestrator",
            ]


class GopyIntegration:
    """GoPy integration for exposing Python Meltano functionality to Go."""
    
    def __init__(self, config: GopyBuildConfig | None = None) -> None:
        """Initialize GoPy integration."""
        self.config = config or GopyBuildConfig()
        self.logger = logger
        self.project_root = Path.cwd()
        
    def check_gopy_available(self) -> bool:
        """Check if gopy is available in the system."""
        try:
            result = subprocess.run(
                ["gopy", "version"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                self.logger.info(f"GoPy available: {result.stdout.strip()}")
                return True
            else:
                self.logger.warning("GoPy not available or not working")
                return False
        except FileNotFoundError:
            self.logger.warning("GoPy not found in PATH")
            return False
    
    def generate_go_bindings(self) -> ServiceResult[dict[str, Any]]:
        """Generate Go bindings for Python Meltano modules."""
        if not self.check_gopy_available():
            return ServiceResult.failure("GoPy not available")
        
        try:
            output_dir = Path(self.config.output_dir)
            output_dir.mkdir(exist_ok=True)
            
            # Generate bindings for each Python module
            results = {}
            for module in self.config.python_modules:
                self.logger.info(f"Generating Go bindings for {module}")
                
                cmd = [
                    "gopy", "build",
                    "-output", str(output_dir),
                    "-name", f"{self.config.module_name}_{module.split('.')[-1]}",
                    module,
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                
                if result.returncode == 0:
                    results[module] = {
                        "success": True,
                        "output": result.stdout,
                        "bindings_path": str(output_dir),
                    }
                    self.logger.info(f"Successfully generated bindings for {module}")
                else:
                    results[module] = {
                        "success": False,
                        "error": result.stderr,
                        "output": result.stdout,
                    }
                    self.logger.error(f"Failed to generate bindings for {module}: {result.stderr}")
            
            return ServiceResult.success(results)
            
        except Exception as e:
            self.logger.error(f"Error generating Go bindings: {e}")
            return ServiceResult.failure(f"Error generating Go bindings: {e}")
    
    def create_go_wrapper(self) -> ServiceResult[str]:
        """Create a Go wrapper for the Python bindings."""
        wrapper_content = self._generate_go_wrapper_code()
        
        try:
            wrapper_path = Path(self.config.output_dir) / "wrapper.go"
            wrapper_path.write_text(wrapper_content)
            
            self.logger.info(f"Go wrapper created at {wrapper_path}")
            return ServiceResult.success(str(wrapper_path))
            
        except Exception as e:
            self.logger.error(f"Error creating Go wrapper: {e}")
            return ServiceResult.failure(f"Error creating Go wrapper: {e}")
    
    def _generate_go_wrapper_code(self) -> str:
        """Generate Go wrapper code for the Python bindings."""
        return '''package main

import (
    "encoding/json"
    "fmt"
    "log"
    
    bridge "github.com/flext-sh/flext-meltano-gopy/bridge"
    orchestrator "github.com/flext-sh/flext-meltano-gopy/orchestrator"
    project "github.com/flext-sh/flext-meltano-gopy/project_manager"
)

// MeltanoWrapper provides a unified Go interface to Python Meltano operations
type MeltanoWrapper struct {
    bridge      *bridge.MeltanoBridge
    orchestrator *orchestrator.FlextMeltanoOrchestrator
    project     *project.MeltanoProjectManager
}

// NewMeltanoWrapper creates a new Meltano wrapper instance
func NewMeltanoWrapper() *MeltanoWrapper {
    return &MeltanoWrapper{
        bridge:      bridge.GetBridge(),
        orchestrator: orchestrator.New(),
        project:     project.New(),
    }
}

// InitProject initializes a new Meltano project
func (w *MeltanoWrapper) InitProject(name, dir string) (map[string]interface{}, error) {
    result := w.bridge.InitProject(name, dir)
    
    var data map[string]interface{}
    if err := json.Unmarshal([]byte(result), &data); err != nil {
        return nil, fmt.Errorf("failed to parse result: %v", err)
    }
    
    return data, nil
}

// RunPipeline executes a Meltano pipeline
func (w *MeltanoWrapper) RunPipeline(extractor, loader, transformer string) (map[string]interface{}, error) {
    result := w.bridge.RunPipeline(extractor, loader, transformer)
    
    var data map[string]interface{}
    if err := json.Unmarshal([]byte(result), &data); err != nil {
        return nil, fmt.Errorf("failed to parse result: %v", err)
    }
    
    return data, nil
}

// GetPlugins returns list of available plugins
func (w *MeltanoWrapper) GetPlugins() ([]string, error) {
    result := w.bridge.GetPlugins()
    
    var data map[string]interface{}
    if err := json.Unmarshal([]byte(result), &data); err != nil {
        return nil, fmt.Errorf("failed to parse result: %v", err)
    }
    
    if !data["success"].(bool) {
        return nil, fmt.Errorf("operation failed: %v", data["error"])
    }
    
    pluginsData := data["data"].(map[string]interface{})
    plugins := pluginsData["plugins"].([]interface{})
    
    result_plugins := make([]string, len(plugins))
    for i, p := range plugins {
        result_plugins[i] = p.(string)
    }
    
    return result_plugins, nil
}

// IsAvailable checks if Meltano is available
func (w *MeltanoWrapper) IsAvailable() bool {
    return w.bridge.IsAvailable()
}

func main() {
    wrapper := NewMeltanoWrapper()
    
    if !wrapper.IsAvailable() {
        log.Fatal("Meltano is not available")
    }
    
    fmt.Println("Meltano Go wrapper is ready")
    
    // Example usage
    plugins, err := wrapper.GetPlugins()
    if err != nil {
        log.Printf("Error getting plugins: %v", err)
    } else {
        fmt.Printf("Available plugins: %v\\n", plugins)
    }
}
'''
    
    def build_shared_library(self) -> ServiceResult[str]:
        """Build shared library for use with Go."""
        if not self.check_gopy_available():
            return ServiceResult.failure("GoPy not available")
        
        try:
            output_dir = Path(self.config.output_dir)
            output_dir.mkdir(exist_ok=True)
            
            # Build shared library
            cmd = [
                "gopy", "build",
                "-output", str(output_dir),
                "-name", self.config.module_name,
                "-vm", "python3",
                "flext_meltano.integrations.bridge",
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )
            
            if result.returncode == 0:
                shared_lib_path = output_dir / f"{self.config.module_name}.so"
                self.logger.info(f"Shared library built at {shared_lib_path}")
                return ServiceResult.success(str(shared_lib_path))
            else:
                error_msg = f"Failed to build shared library: {result.stderr}"
                self.logger.error(error_msg)
                return ServiceResult.failure(error_msg)
                
        except Exception as e:
            error_msg = f"Error building shared library: {e}"
            self.logger.error(error_msg)
            return ServiceResult.failure(error_msg)
    
    def generate_documentation(self) -> ServiceResult[str]:
        """Generate documentation for the Go bindings."""
        doc_content = self._generate_documentation_content()
        
        try:
            doc_path = Path(self.config.output_dir) / "README.md"
            doc_path.write_text(doc_content)
            
            self.logger.info(f"Documentation generated at {doc_path}")
            return ServiceResult.success(str(doc_path))
            
        except Exception as e:
            error_msg = f"Error generating documentation: {e}"
            self.logger.error(error_msg)
            return ServiceResult.failure(error_msg)
    
    def _generate_documentation_content(self) -> str:
        """Generate documentation content for Go bindings."""
        return f'''# FLEXT Meltano GoPy Integration

This package provides Go bindings for FLEXT Meltano functionality.

## Generated Bindings

The following Python modules have been bound to Go:

{chr(10).join(f"- {module}" for module in self.config.python_modules)}

## Usage

```go
package main

import (
    "fmt"
    "log"
    
    meltano "{self.config.go_package}"
)

func main() {{
    wrapper := meltano.NewMeltanoWrapper()
    
    if !wrapper.IsAvailable() {{
        log.Fatal("Meltano is not available")
    }}
    
    // Initialize a project
    result, err := wrapper.InitProject("my-project", ".")
    if err != nil {{
        log.Fatal(err)
    }}
    
    fmt.Printf("Project initialized: %v\\n", result)
    
    // Run a pipeline
    pipelineResult, err := wrapper.RunPipeline("tap-csv", "target-jsonl", "")
    if err != nil {{
        log.Fatal(err)
    }}
    
    fmt.Printf("Pipeline result: %v\\n", pipelineResult)
}}
```

## Building

1. Ensure GoPy is installed: `pip install gopy`
2. Generate bindings: `python -m flext_meltano.integrations.gopy_integration`
3. Build your Go application with the generated bindings

## Configuration

The bindings are configured with:
- Module name: {self.config.module_name}
- Output directory: {self.config.output_dir}
- Go package: {self.config.go_package}

## Features

- Project initialization and management
- Pipeline execution
- Plugin management
- Error handling with proper Go error types
- JSON serialization for complex data structures

## Requirements

- Python 3.13+
- GoPy
- Meltano
- FLEXT Core libraries
'''


def main():
    """Main function for CLI usage."""
    integration = GopyIntegration()
    
    print("Generating Go bindings for FLEXT Meltano...")
    
    # Generate bindings
    result = integration.generate_go_bindings()
    if result.is_success:
        print("✅ Go bindings generated successfully")
        print(json.dumps(result.value, indent=2))
    else:
        print(f"❌ Failed to generate Go bindings: {result.error}")
        return
    
    # Create wrapper
    wrapper_result = integration.create_go_wrapper()
    if wrapper_result.is_success:
        print(f"✅ Go wrapper created: {wrapper_result.value}")
    else:
        print(f"❌ Failed to create Go wrapper: {wrapper_result.error}")
    
    # Generate documentation
    doc_result = integration.generate_documentation()
    if doc_result.is_success:
        print(f"✅ Documentation generated: {doc_result.value}")
    else:
        print(f"❌ Failed to generate documentation: {doc_result.error}")


if __name__ == "__main__":
    main()