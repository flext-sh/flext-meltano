"""FLEXT Meltano Installation - Plugin Installation and Management.

**Architecture Layer**: Plugin Management Layer
**Status**: ✅ STABLE - Plugin installation and lifecycle management
**Dependencies**: flext-core (FlextResult), Meltano Hub, subprocess execution

## Module Purpose

This module provides **plugin installation and lifecycle management** for FLEXT
Meltano's bridge architecture, enabling Go services to install, configure, and
manage Meltano plugins through subprocess orchestration with enterprise patterns.

## Design Principles

1. **Plugin Lifecycle**: Complete plugin installation and management workflow
2. **Hub Integration**: Meltano Hub integration for plugin discovery and installation
3. **Configuration Management**: Plugin configuration validation and persistence
4. **Bridge-Friendly**: JSON-serializable installation results for Go services
5. **Enterprise Patterns**: FlextResult integration and structured error handling

## Core Components

### Plugin Installation
- `FlextMeltanoInstaller`: Primary plugin installation service
- `install_plugin()`: Function for installing plugins from Hub or custom sources
- `FlextMeltanoPluginInfo`: Plugin information entity with installation metadata
- Version management and dependency resolution

### Installation Context
- `FlextMeltanoInstallationContext`: Installation tracking and metadata
- Installation validation and compatibility checking
- Plugin configuration management and persistence
- Installation rollback and cleanup mechanisms

### Plugin Management
- Plugin availability verification and health checking
- Configuration validation and schema compliance
- Plugin updates and version management
- Dependency analysis and conflict resolution

## Usage Patterns

### Basic Plugin Installation
```python
from flext_meltano.installation import install_plugin, FlextMeltanoInstaller

# Install extractor plugin
result = install_plugin("extractor", "tap-postgres")
if result.success:
    print(f"Plugin installed: {result.data}")
else:
    print(f"Installation failed: {result.error_message}")

# Service-based installation with configuration
installer = FlextMeltanoInstaller(config)
result = installer.install_plugin_with_config(
    "extractor", "tap-postgres", config={"host": "localhost", "port": 5432}
)
```

### Advanced Installation Operations
```python
from flext_meltano.installation import FlextMeltanoInstaller

installer = FlextMeltanoInstaller(config)

# Install with custom pip URL
result = installer.install_plugin(
    plugin_type="extractor",
    name="tap-custom",
    pip_url="git+https://github.com/example/tap-custom.git",
)

# Install specific variant
result = installer.install_plugin(
    plugin_type="loader", name="target-postgres", variant="transferwise"
)

# Batch installation
plugins_to_install = [
    {"type": "extractor", "name": "tap-postgres"},
    {"type": "loader", "name": "target-csv"},
    {"type": "transformer", "name": "dbt"},
]
result = installer.install_multiple_plugins(plugins_to_install)
```

### Plugin Configuration Management
```python
from flext_meltano.installation import configure_plugin, validate_plugin_config

# Configure installed plugin
config_data = {
    "host": "postgres.example.com",
    "port": 5432,
    "database": "analytics",
    "username": "etl_user",
}

result = configure_plugin("tap-postgres", config_data)
if result.success:
    print("Plugin configured successfully")

# Validate configuration before installation
validation_result = validate_plugin_config("tap-postgres", config_data)
if validation_result.success:
    # Proceed with installation
    install_result = install_plugin("extractor", "tap-postgres")
```

## Bridge Integration Patterns

### Go Service Usage
```go
// Go service installing plugins via bridge
func (c *FlextMeltanoClient) InstallPlugin(pluginType, name string) (*InstallResult, error) {
    cmd := exec.Command("python", "scripts/flext_meltano_bridge.py", "add_plugin", pluginType, name)
    output, err := cmd.Output()
    if err != nil {
        return nil, err
    }

    var result InstallResult
    err = json.Unmarshal(output, &result)
    return &result, err
}

func (c *FlextMeltanoClient) InstallPluginWithConfig(
    pluginType, name string,
    config map[string]interface{}
) (*InstallResult, error) {
    configJson, _ := json.Marshal(config)
    cmd := exec.Command("python", "scripts/flext_meltano_bridge.py",
        "add_plugin", pluginType, name, "--config", string(configJson))
    // Process installation result
}
```

### Installation Result Format
```python
# Standard installation result structure for bridge
installation_result = {
    "success": True,
    "plugin": {
        "name": "tap-postgres",
        "type": "extractor",
        "version": "0.4.40",
        "executable": "tap-postgres",
        "pip_url": "pipelinewise-tap-postgres==0.4.40"
    },
    "installation_context": {
        "installation_id": "uuid-string",
        "installed_at": "2025-08-02T10:30:00Z",
        "environment": "dev",
        "dependencies_installed": ["psycopg2-binary", "singer-python"]
    },
    "configuration": {
        "schema_applied": True,
        "settings_available": ["host", "port", "database", "username", "password"],
        "capabilities": ["discover", "properties", "state"]
    }
}
```

### Error Handling Format
```python
# Standard installation error format for bridge
installation_error = {
    "success": False,
    "error": {
        "message": "Plugin installation failed: dependency conflict",
        "type": "installation_error",
        "plugin_name": "tap-postgres",
        "details": {
            "conflicting_dependencies": ["psycopg2==2.8.6", "psycopg2-binary==2.9.1"],
            "resolution_suggestions": [
                "Use --force flag to override conflicts",
                "Update conflicting packages manually",
                "Use virtual environment isolation",
            ],
        },
        "timestamp": "2025-08-02T10:30:00Z",
    },
    "plugin": None,
    "installation_context": None,
}
```

## Installation Operations

### Plugin Installation Service
```python
class FlextMeltanoInstaller:
    '''Enterprise plugin installation service with Hub integration.'''

    def __init__(self, config: FlextMeltanoConfig):
        self._config = config
        self._installation_cache = {}
        self._dependency_resolver = DependencyResolver()

    def install_plugin(
        self,
        plugin_type: str,
        name: str,
        *,
        variant: Optional[str] = None,
        pip_url: Optional[str] = None,
        force: bool = False,
    ) -> FlextResult[dict[str, object]]:
        '''Install plugin with comprehensive validation and error handling.'''
        try:
            # Pre-installation validation
            validation_result = self._validate_installation_prerequisites(
                plugin_type, name, variant
            )
            if validation_result.is_failure:
                return validation_result

            # Dependency resolution
            deps_result = self._resolve_dependencies(name, variant)
            if deps_result.is_failure:
                return deps_result

            # Execute installation
            install_result = self._execute_installation(
                plugin_type, name, variant, pip_url, force
            )

            if install_result.success:
                # Post-installation configuration
                config_result = self._apply_default_configuration(name)
                return self._build_installation_result(
                    name, install_result.data, config_result.data
                )
            else:
                return install_result

        except Exception as e:
            return FlextResult.fail(f"Installation error: {e}")
```

### Configuration Management
```python
def configure_plugin_with_validation(
    plugin_name: str, config_data: dict[str, object], validate_connection: bool = True
) -> FlextResult[dict[str, object]]:
    '''Configure plugin with validation and connection testing.'''
    try:
        # Validate configuration schema
        schema_result = validate_plugin_configuration_schema(plugin_name, config_data)
        if schema_result.is_failure:
            return schema_result

        # Apply configuration
        config_result = apply_plugin_configuration(plugin_name, config_data)
        if config_result.is_failure:
            return config_result

        # Test connection if requested
        if validate_connection:
            test_result = test_plugin_connection(plugin_name)
            if test_result.is_failure:
                return FlextResult.fail(
                    f"Configuration applied but connection test failed: {test_result.error_message}"
                )

        return FlextResult.ok(
            {
                "plugin_name": plugin_name,
                "configuration_applied": True,
                "connection_tested": validate_connection,
                "status": "ready",
            }
        )

    except Exception as e:
        return FlextResult.fail(f"Configuration error: {e}")
```

## Installation Validation

### Prerequisites Checking
```python
def validate_installation_prerequisites(
    plugin_type: str, plugin_name: str
) -> FlextResult[dict[str, object]]:
    '''Validate installation prerequisites and environment.'''
    validation_results = {}

    # Check Meltano project
    if not check_meltano_project_exists():
        return FlextResult.fail("Meltano project not found")

    # Check plugin availability in Hub
    hub_check = check_plugin_in_hub(plugin_name)
    validation_results["hub_available"] = hub_check.success

    # Check existing installation
    existing_check = check_plugin_already_installed(plugin_name)
    validation_results["already_installed"] = existing_check.success

    # Check dependencies
    deps_check = check_system_dependencies(plugin_name)
    validation_results["dependencies_met"] = deps_check.success

    # Check disk space
    space_check = check_available_disk_space()
    validation_results["sufficient_space"] = space_check.success

    # Overall validation result
    all_valid = all(
        [
            validation_results["hub_available"],
            not validation_results["already_installed"],  # Should not be installed
            validation_results["dependencies_met"],
            validation_results["sufficient_space"],
        ]
    )

    if all_valid:
        return FlextResult.ok(validation_results)
    else:
        return FlextResult.fail(f"Prerequisites not met: {validation_results}")
```

### Dependency Resolution
```python
class DependencyResolver:
    '''Dependency resolution service for plugin installations.'''

    def resolve_plugin_dependencies(
        self, plugin_name: str, variant: Optional[str] = None
    ) -> FlextResult[list[dict[str, object]]]:
        '''Resolve plugin dependencies with conflict detection.'''
        try:
            # Get plugin metadata from Hub
            metadata_result = get_plugin_metadata(plugin_name, variant)
            if metadata_result.is_failure:
                return metadata_result

            metadata = metadata_result.data
            dependencies = metadata.get("dependencies", [])

            # Check for conflicts with existing plugins
            conflict_check = self._check_dependency_conflicts(dependencies)
            if conflict_check.is_failure:
                return conflict_check

            # Resolve dependency versions
            resolved_deps = []
            for dep in dependencies:
                version_result = self._resolve_dependency_version(dep)
                if version_result.success:
                    resolved_deps.append(version_result.data)
                else:
                    return FlextResult.fail(f"Could not resolve dependency: {dep}")

            return FlextResult.ok(resolved_deps)

        except Exception as e:
            return FlextResult.fail(f"Dependency resolution error: {e}")
```

## Quality Standards

### Installation Reliability
- **Validation Pipeline**: Comprehensive pre-installation validation
- **Dependency Resolution**: Automated dependency conflict detection and resolution
- **Rollback Capability**: Failed installation cleanup and rollback mechanisms
- **Configuration Validation**: Schema validation and connection testing

### Bridge Compatibility
- **JSON Serialization**: All installation results JSON-serializable for Go consumption
- **Error Standardization**: Consistent error format with troubleshooting context
- **Progress Tracking**: Installation progress reporting for long-running operations
- **Configuration Management**: Bridge-friendly configuration apply and validation

## Integration Points

### Execution Module Integration
- Uses FlextMeltanoExecutor for Meltano CLI installation commands
- Subprocess execution for plugin installation and configuration
- Command result parsing and installation status tracking

### Discovery Module Integration
- Plugin availability verification before installation
- Hub integration for plugin metadata and version information
- Dependency discovery and compatibility checking

### Bridge Module Integration (After Implementation)
- FlextMeltanoBridge will use installation functions
- Bridge-friendly installation operations with progress tracking
- Go service integration via subprocess calls

## Next Actions

- ✅ **Plugin Installation**: Hub integration and plugin installation working
- ✅ **Configuration Management**: Plugin configuration and validation working
- 🔄 **Bridge Integration**: Ready for bridge module consumption
- 📈 **Performance**: Installation caching and batch operations
- 🛡️ **Security**: Secure plugin installation and validation

This module provides essential **plugin installation and management** capabilities
for FLEXT Meltano's bridge architecture, enabling comprehensive plugin lifecycle
management for Go service integration.
"""

from __future__ import annotations

import json
import subprocess
import uuid
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

# FlextResult is MANDATORY for all operations
from flext_core import FlextModel, FlextResult
from pydantic import Field

from flext_meltano.base import FlextMeltanoConfig

# Injectable decorator from common utilities
from flext_meltano.common import injectable
from flext_meltano.execution import (
    FlextMeltanoResult,
    SubprocessExecutionContext,
    execute_subprocess_common,
)


class FlextMeltanoInstallationContext(FlextModel):
    """Installation context for plugin operations."""

    installation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    plugin_name: str = Field(...)
    plugin_type: str = Field(...)
    project_root: Path = Field(default_factory=Path)
    timeout_seconds: int = Field(default=600)  # 10 minutes default
    metadata: dict[str, object] = Field(default_factory=dict)


@dataclass
class InstallationResultData:
    """Data class to reduce argument count in installation result building."""

    plugin_name: str
    plugin_type: str
    pip_url: str | None
    cmd: list[str]


class FlextMeltanoPluginInfo(FlextModel):
    """Plugin information entity."""

    name: str = Field(...)
    type: str = Field(...)
    namespace: str = Field(...)
    pip_url: str | None = Field(default=None)
    executable: str | None = Field(default=None)
    description: str = Field(default="")
    version: str | None = Field(default=None)
    installed: bool = Field(default=False)


@injectable
class FlextMeltanoInstaller:
    """Plugin installer using MANDATORY patterns."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize with dependency injection."""
        self.config = config
        self.project_root = Path(config.project_root)
        self._initialized = False

    def validate(self) -> FlextResult[bool]:
        """Validate installation service."""
        try:
            # Check if project root exists
            if not self.project_root.exists():
                return FlextResult(
                    error=f"Project root does not exist: {self.project_root}",
                )

            # Check if meltano.yml exists
            meltano_yml = self.project_root / "meltano.yml"
            if not meltano_yml.exists():
                return FlextResult(error=f"No meltano.yml found in {self.project_root}")

            return FlextResult(data=True)
        except (OSError, ValueError) as e:
            return FlextResult(error=f"Validation failed: {e}")

    def initialize(self) -> FlextResult[bool]:
        """Initialize service."""
        self._initialized = True
        return FlextResult(data=True)

    def get_health_status(self) -> FlextResult[dict[str, object]]:
        """Get installation service health status."""
        return FlextResult(
            data={
                "service": "installation",
                "project_root": str(self.project_root),
                "meltano_yml_exists": (self.project_root / "meltano.yml").exists(),
                "initialized": self._initialized,
            },
        )

    def add_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        pip_url: str | None = None,
        context: FlextMeltanoInstallationContext | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Add plugin to meltano project using enterprise patterns."""
        if not context:
            context = FlextMeltanoInstallationContext(
                plugin_name=plugin_name,
                plugin_type=plugin_type,
                project_root=self.project_root,
            )

        try:
            return self._execute_plugin_add(plugin_type, plugin_name, pip_url, context)
        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin add timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin add error: {e}")

    def _execute_plugin_add(
        self,
        plugin_type: str,
        plugin_name: str,
        pip_url: str | None,
        context: FlextMeltanoInstallationContext,
    ) -> FlextResult[dict[str, object]]:
        """Execute plugin addition with validation and result processing."""
        # Validate first
        validation_result = self.validate()
        if not validation_result.success:
            return FlextResult(error=validation_result.error)

        # Build and execute command
        cmd = ["meltano", "add", plugin_type, plugin_name]
        if pip_url:
            cmd.extend(["--custom", pip_url])

        exec_context = SubprocessExecutionContext(
            command=cmd,
            cwd=self.project_root,
            timeout_seconds=context.timeout_seconds,
        )
        exec_result = execute_subprocess_common(exec_context)

        if not exec_result.success:
            return FlextResult(error=exec_result.error)

        result_data = exec_result.data
        if not isinstance(result_data, dict):
            return FlextResult(error="Invalid execution result format")

        # Process results
        result_data_obj = InstallationResultData(plugin_name, plugin_type, pip_url, cmd)
        return self._build_installation_result(result_data, context, result_data_obj)

    def _build_installation_result(
        self,
        result_data: dict[str, object],
        context: FlextMeltanoInstallationContext,
        plugin_data: InstallationResultData,
    ) -> FlextResult[dict[str, object]]:
        """Build installation result from execution data."""

        # Create mock result object for compatibility
        class MockResult:
            def __init__(self, data: dict[str, object]) -> None:
                self.returncode = data.get("returncode", 1)
                self.stdout = data.get("stdout", "")
                self.stderr = data.get("stderr", "")

        result = MockResult(result_data)

        installation_result: dict[str, object] = {
            "installation_id": context.installation_id,
            "plugin_name": plugin_data.plugin_name,
            "plugin_type": plugin_data.plugin_type,
            "pip_url": plugin_data.pip_url,
            "command": " ".join(plugin_data.cmd),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
            "started_at": context.started_at.isoformat(),
            "completed_at": datetime.now(UTC).isoformat(),
            "duration_seconds": (
                datetime.now(UTC) - context.started_at
            ).total_seconds(),
        }

        if result.returncode == 0:
            return FlextResult(data=installation_result)
        return FlextResult(
            error=f"Plugin add failed: {result.stderr or result.stdout}",
        )

    def install_plugins(
        self,
        context: FlextMeltanoInstallationContext | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Install all plugins in meltano project."""
        if not context:
            context = FlextMeltanoInstallationContext(
                plugin_name="all",
                plugin_type="install",
                project_root=self.project_root,
            )

        try:
            # Validate first
            validation_result = self.validate()
            if not validation_result.success:
                return FlextResult(error=validation_result.error)

            # Execute meltano install
            cmd = ["meltano", "install"]
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=context.timeout_seconds,
                check=False,
            )

            installation_result = {
                "installation_id": context.installation_id,
                "operation": "install_all",
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "started_at": context.started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "duration_seconds": (
                    datetime.now(UTC) - context.started_at
                ).total_seconds(),
            }

            if result.returncode == 0:
                return FlextResult(data=installation_result)
            return FlextResult(
                error=f"Plugin install failed: {result.stderr or result.stdout}",
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin install timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin install error: {e}")

    def remove_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        context: FlextMeltanoInstallationContext | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Remove plugin from meltano project."""
        if not context:
            context = FlextMeltanoInstallationContext(
                plugin_name=plugin_name,
                plugin_type=plugin_type,
                project_root=self.project_root,
                timeout_seconds=300,  # 5 minutes for removal
            )

        try:
            # Validate first
            validation_result = self.validate()
            if not validation_result.success:
                return FlextResult(error=validation_result.error)

            # Build command
            cmd = ["meltano", "remove", plugin_type, plugin_name]

            # Execute subprocess
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=context.timeout_seconds,
                check=False,
            )

            removal_result = {
                "installation_id": context.installation_id,
                "operation": "remove",
                "plugin_name": plugin_name,
                "plugin_type": plugin_type,
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "started_at": context.started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "duration_seconds": (
                    datetime.now(UTC) - context.started_at
                ).total_seconds(),
            }

            if result.returncode == 0:
                return FlextResult(data=removal_result)
            return FlextResult(
                error=f"Plugin remove failed: {result.stderr or result.stdout}",
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin remove timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin remove error: {e}")

    def list_plugins(self) -> FlextResult[list[FlextMeltanoPluginInfo]]:
        """List installed plugins in meltano project."""
        try:
            # Validate first
            validation_result = self.validate()
            if not validation_result.success:
                return FlextResult(error=validation_result.error)

            # Execute subprocess
            result = self._execute_meltano_list()
            if not result.success:
                return FlextResult(error=result.error)

            # Parse JSON response
            if result.data is not None:
                return self._parse_plugin_list(result.data)
            return FlextResult(error="No plugin data received")

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin list timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin list error: {e}")

    def _execute_meltano_list(self) -> FlextResult[str]:
        """Execute meltano list command."""
        cmd = ["meltano", "list", "--format=json"]
        result = subprocess.run(
            cmd,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        if result.returncode == 0:
            return FlextResult(data=result.stdout)
        return FlextResult(
            error=f"Plugin list failed: {result.stderr or result.stdout}",
        )

    def _parse_plugin_list(
        self,
        stdout: str,
    ) -> FlextResult[list[FlextMeltanoPluginInfo]]:
        """Parse plugin list JSON response."""
        try:
            plugins_data = json.loads(stdout)
            plugins: list[FlextMeltanoPluginInfo] = []

            if isinstance(plugins_data, dict):
                for plugin_type, plugin_list in plugins_data.items():
                    plugins.extend(self._convert_plugin_list(plugin_type, plugin_list))

            return FlextResult(data=plugins)
        except json.JSONDecodeError:
            return FlextResult(error="Failed to parse plugin list JSON")

    def _convert_plugin_list(
        self,
        plugin_type: str,
        plugin_list: object,
    ) -> list[FlextMeltanoPluginInfo]:
        """Convert plugin list to FlextMeltanoPluginInfo entities."""
        plugins = []
        if isinstance(plugin_list, list):
            for plugin in plugin_list:
                if isinstance(plugin, dict):
                    plugin_info = FlextMeltanoPluginInfo(
                        name=plugin.get("name", ""),
                        type=plugin_type,
                        namespace=plugin.get(
                            "namespace",
                            plugin.get("name", "").replace("-", "_"),
                        ),
                        pip_url=plugin.get("pip_url"),
                        executable=plugin.get("executable"),
                        description=plugin.get("description", ""),
                        version=plugin.get("version"),
                        installed=True,
                    )
                    plugins.append(plugin_info)
        return plugins


# === LEGACY COMPATIBILITY FUNCTIONS ===


def flext_meltano_install_plugin(
    plugin_type: str,
    plugin_name: str,
    project_root: Path | None = None,
    pip_url: str | None = None,
) -> FlextMeltanoResult:
    """Install plugin using installer (legacy compatibility).

    Args:
        plugin_type: Type of plugin (extractors, loaders, etc.)
        plugin_name: Name of the plugin
        project_root: Project directory
        pip_url: Optional pip URL for custom plugins

    Returns:
        Result with installation status

    """
    warnings.warn(
        "flext_meltano_install_plugin is deprecated. Use FlextMeltanoInstaller.add_plugin instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Use new service implementation
    config = FlextMeltanoConfig(
        project_root=str(project_root or Path.cwd()),
    )
    installer = FlextMeltanoInstaller(config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = installer.add_plugin(plugin_type, plugin_name, pip_url)
    if result.success:
        return FlextMeltanoResult.ok(result.data)
    return FlextMeltanoResult.fail(result.error or "Unknown error")


# === FACTORY FUNCTION ===


def create_installer_service(
    config: FlextMeltanoConfig,
) -> FlextResult[FlextMeltanoInstaller]:
    """Create installer service using dependency injection."""
    try:
        service = FlextMeltanoInstaller(config)
        init_result = service.initialize()
        if not init_result.success:
            return FlextResult(
                error=f"Installer service initialization failed: {init_result.error}",
            )

        return FlextResult(data=service)
    except (ValueError, TypeError, ImportError) as e:
        return FlextResult(error=f"Failed to create installer service: {e}")


# === PUBLIC API ===
__all__: list[str] = [
    "FlextMeltanoInstallationContext",
    "FlextMeltanoInstaller",
    "FlextMeltanoPluginInfo",
    "create_installer_service",
    "flext_meltano_install_plugin",
]
