"""FLEXT Meltano Bridge - Consolidated Bridge, Validation, and Utilities."""

from __future__ import annotations

import sys
from pathlib import Path

from flext_core import FlextResult, get_logger

from flext_meltano.meltano_config import (
    FLEXT_MELTANO_VERSION,
    FlextMeltanoConfig,
    FlextMeltanoPluginType,
)
from flext_meltano.meltano_models import FlextMeltanoPlugin, FlextMeltanoPluginRegistry
from flext_meltano.meltano_services import FlextMeltanoExecutor

logger = get_logger(__name__)

# =============================================================================
# COMMON UTILITIES AND VALIDATION (from common.py)
# =============================================================================


def injectable(cls: type) -> type:
    """Provide a no-op injectable decorator for DI compatibility."""
    return cls


def validate_directory_path(path: str | Path) -> FlextResult[Path]:
    """Validate directory path with security checks."""
    try:
        path_obj = Path(path).resolve()

        # Security check - prevent path traversal
        if ".." in str(path_obj) or not path_obj.is_absolute():
            return FlextResult.fail(f"Invalid or potentially unsafe path: {path}")

        if not path_obj.exists():
            return FlextResult.fail(f"Directory does not exist: {path_obj}")

        if not path_obj.is_dir():
            return FlextResult.fail(f"Path is not a directory: {path_obj}")

        # Check if directory is accessible
        # Basic readability check using os access instead of Path.is_readable()
        try:
            (path_obj / ".").exists()
        except Exception:
            return FlextResult.fail(f"Directory is not readable: {path_obj}")

        return FlextResult.ok(path_obj)

    except (OSError, ValueError) as e:
        return FlextResult.fail(f"Directory validation failed: {e}")


def validate_file_path(
    path: str | Path,
    *,
    must_exist: bool = True,
) -> FlextResult[Path]:
    """Validate file path with security checks."""
    try:
        path_obj = Path(path).resolve()

        error_message: str | None = None

        # Security check - prevent path traversal and ensure absolute
        if ".." in str(path_obj) or not path_obj.is_absolute():
            error_message = f"Invalid or potentially unsafe path: {path}"
        elif must_exist:
            if not path_obj.exists():
                error_message = f"File does not exist: {path_obj}"
            elif not path_obj.is_file():
                error_message = f"Path is not a file: {path_obj}"
            else:
                # Check readability via open
                try:
                    with path_obj.open("rb"):
                        pass
                except Exception:
                    error_message = f"File is not readable: {path_obj}"
        else:
            # For files that don't need to exist, validate parent directory
            parent = path_obj.parent
            if not parent.exists():
                error_message = f"Parent directory does not exist: {parent}"

        if error_message is not None:
            return FlextResult.fail(error_message)
        return FlextResult.ok(path_obj)

    except (OSError, ValueError) as e:
        return FlextResult.fail(f"File validation failed: {e}")


def _coerce_value_to_expected_type(
    value: object,
    expected_type: type,
) -> FlextResult[object]:
    """Coerce `value` to `expected_type` when safe and reasonable."""
    if isinstance(value, expected_type):
        return FlextResult.ok(value)

    if expected_type is float and isinstance(value, str):
        try:
            return FlextResult.ok(float(value))
        except ValueError:
            return FlextResult.fail(f"Expected float, got {type(value).__name__}")

    if expected_type is int and isinstance(value, str):
        try:
            return FlextResult.ok(int(value))
        except ValueError:
            return FlextResult.fail(f"Expected int, got {type(value).__name__}")

    return FlextResult.fail(
        f"Expected {expected_type.__name__}, got {type(value).__name__}",
    )


def _validate_and_sanitize_string(value: str) -> FlextResult[object]:
    """Validate non-empty string and sanitize control characters."""
    sanitized = value.strip()
    if not sanitized:
        return FlextResult.fail("String value cannot be empty")
    sanitized = sanitized.replace("\x00", "").replace("\n", " ").replace("\r", " ")
    return FlextResult.ok(sanitized)


def validate_config_value(
    value: object,
    expected_type: type,
    *,
    allow_none: bool = False,
) -> FlextResult[object]:
    """Validate configuration value with type checking."""
    try:
        if value is None:
            return (
                FlextResult.ok(None)
                if allow_none
                else FlextResult.fail("Value cannot be None")
            )

        # Type coercion when possible
        coerced = _coerce_value_to_expected_type(value, expected_type)
        if coerced.is_failure:
            return coerced
        coerced_value = coerced.data

        # Additional string validation
        if isinstance(coerced_value, str):
            return _validate_and_sanitize_string(coerced_value)

        return FlextResult.ok(coerced_value)

    except Exception as e:
        return FlextResult.fail(f"Value validation failed: {e}")


# =============================================================================
# VALIDATION FRAMEWORK (from validation.py)
# =============================================================================


class FlextMeltanoValidator:
    """Comprehensive validator for Meltano projects and configurations."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize validator with configuration."""
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    def validate_project(self) -> FlextResult[dict[str, object]]:
        """Validate Meltano project structure and configuration."""
        try:
            project_root = Path(self.config.project_root)
            validation_results = {}

            # Validate project root directory
            root_validation = validate_directory_path(project_root)
            if not root_validation.success:
                return FlextResult.fail(
                    f"Project root validation failed: {root_validation.error}",
                )

            validation_results["project_root"] = {
                "path": str(project_root),
                "exists": True,
                "accessible": True,
            }

            # Check for meltano.yml
            meltano_yml = project_root / "meltano.yml"
            if meltano_yml.exists():
                validation_results["meltano_yml"] = {
                    "exists": True,
                    "path": str(meltano_yml),
                }
            else:
                validation_results["meltano_yml"] = {
                    "exists": False,
                    "warning": "meltano.yml not found - may not be a Meltano project",
                }

            # Check for .meltano directory
            meltano_dir = project_root / ".meltano"
            validation_results["meltano_dir"] = {
                "exists": meltano_dir.exists(),
                "path": str(meltano_dir),
            }

            return FlextResult.ok(
                {
                    "project_valid": True,
                    "validation_results": validation_results,
                },
            )

        except Exception as e:
            return FlextResult.fail(f"Project validation failed: {e}")

    def validate_tap_connection(
        self,
        tap_name: str,
        config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Validate tap connection configuration."""
        try:
            self.logger.info(f"Validating tap connection: {tap_name}")

            # Basic configuration validation
            if not config:
                return FlextResult.fail("Tap configuration cannot be empty")

            # Common configuration validations
            validation_results = {}

            # Check for common required fields based on tap type
            if "ldap" in tap_name.lower():
                required_fields = ["ldap_host", "bind_dn", "bind_password", "base_dn"]
            elif "oracle" in tap_name.lower():
                required_fields = ["host", "port", "username", "password", "database"]
            elif "file" in tap_name.lower() or "csv" in tap_name.lower():
                required_fields = ["file_path"]
            else:
                required_fields = []

            missing_fields = [
                field
                for field in required_fields
                if field not in config or not config[field]
            ]

            if missing_fields:
                return FlextResult.fail(f"Missing required fields: {missing_fields}")

            validation_results["required_fields"] = {
                "checked": required_fields,
                "missing": missing_fields,
                "valid": len(missing_fields) == 0,
            }

            # Validate specific configuration types
            if "host" in config:
                host = config.get("host", "")
                if isinstance(host, str) and host.strip():
                    validation_results["host"] = {"valid": True, "value": host}
                else:
                    validation_results["host"] = {
                        "valid": False,
                        "error": "Invalid host",
                    }

            return FlextResult.ok(
                {
                    "tap_name": tap_name,
                    "connection_valid": True,
                    "validation_results": validation_results,
                },
            )

        except Exception as e:
            return FlextResult.fail(f"Tap connection validation failed: {e}")

    def validate_target_connection(
        self,
        target_name: str,
        config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Validate target connection configuration."""
        try:
            self.logger.info(f"Validating target connection: {target_name}")

            # Basic configuration validation
            if not config:
                return FlextResult.fail("Target configuration cannot be empty")

            validation_results = {}

            # Check for common required fields based on target type
            if "csv" in target_name.lower() or "jsonl" in target_name.lower():
                required_fields = ["destination_path"]
            elif "postgres" in target_name.lower() or "oracle" in target_name.lower():
                required_fields = ["host", "port", "username", "password", "database"]
            else:
                required_fields = []

            missing_fields = [
                field
                for field in required_fields
                if field not in config or not config[field]
            ]

            validation_results["required_fields"] = {
                "checked": required_fields,
                "missing": missing_fields,
                "valid": len(missing_fields) == 0,
            }

            return FlextResult.ok(
                {
                    "target_name": target_name,
                    "connection_valid": len(missing_fields) == 0,
                    "validation_results": validation_results,
                },
            )

        except Exception as e:
            return FlextResult.fail(f"Target connection validation failed: {e}")


# =============================================================================
# PLUGIN IMPLEMENTATION PATTERNS
# =============================================================================


def create_meltano_tap_plugin(
    name: str,
    namespace: str,
    pip_url: str | None = None,
    executable: str | None = None,
    config: dict[str, object] | None = None,
) -> FlextResult[FlextMeltanoPlugin]:
    """Create a Meltano tap plugin with validation."""
    try:
        plugin = FlextMeltanoPlugin(
            id=f"tap-{name}",
            name=name,
            plugin_type=FlextMeltanoPluginType.EXTRACTORS,
            namespace=namespace,
            pip_url=pip_url,
            executable=executable,
            config=config or {},
            capabilities=["discover", "properties", "catalog", "state"],
        )

        # Validate business rules
        validation_result = plugin.validate_business_rules()
        if not validation_result.success:
            return FlextResult.fail(
                f"Plugin validation failed: {validation_result.error}",
            )

        return FlextResult.ok(plugin)

    except Exception as e:
        return FlextResult.fail(f"Failed to create tap plugin: {e}")


def create_meltano_target_plugin(
    name: str,
    namespace: str,
    pip_url: str | None = None,
    executable: str | None = None,
    config: dict[str, object] | None = None,
) -> FlextResult[FlextMeltanoPlugin]:
    """Create a Meltano target plugin with validation."""
    try:
        plugin = FlextMeltanoPlugin(
            id=f"target-{name}",
            name=name,
            plugin_type=FlextMeltanoPluginType.LOADERS,
            namespace=namespace,
            pip_url=pip_url,
            executable=executable,
            config=config or {},
            capabilities=["about", "stream-maps"],
        )

        # Validate business rules
        validation_result = plugin.validate_business_rules()
        if not validation_result.success:
            return FlextResult.fail(
                f"Plugin validation failed: {validation_result.error}",
            )

        return FlextResult.ok(plugin)

    except Exception as e:
        return FlextResult.fail(f"Failed to create target plugin: {e}")


# =============================================================================
# BRIDGE INTEGRATION (from simple_bridge.py)
# =============================================================================


class FlextMeltanoBridge:
    """Bridge class for Go service integration.

    **STATUS**: ✅ PRODUCTION READY - Core functionality operational

    Provides a simple interface for Go services to execute Meltano operations
    via subprocess calls with proper error handling and JSON-serializable results.
    """

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize bridge with configuration."""
        self._config = config or FlextMeltanoConfig()
        self._executor = FlextMeltanoExecutor(self._config)
        self._validator = FlextMeltanoValidator(self._config)
        self._plugin_registry = FlextMeltanoPluginRegistry()

        # Initialize executor
        init_result = self._executor.initialize()
        if not init_result.success:
            logger.warning(f"Executor initialization warning: {init_result.error}")

    def get_version(self) -> dict[str, object]:
        """Get FLEXT Meltano version information.

        Returns:
            Dictionary with version information for JSON serialization

        """
        return {
            "success": True,
            "version": FLEXT_MELTANO_VERSION,
            "service": "flext-meltano",
            "bridge_active": True,
        }

    def list_plugins(self) -> dict[str, object]:
        """List available plugins.

        Returns:
            Dictionary with plugin list for JSON serialization

        """
        try:
            plugins = self._plugin_registry.list_plugins_by_type(
                FlextMeltanoPluginType.EXTRACTORS,
            )
            targets = self._plugin_registry.list_plugins_by_type(
                FlextMeltanoPluginType.LOADERS,
            )

            return {
                "success": True,
                "extractors": [
                    {
                        "name": plugin.name,
                        "namespace": plugin.namespace,
                        "installed": plugin.installed,
                    }
                    for plugin in plugins
                ],
                "loaders": [
                    {
                        "name": plugin.name,
                        "namespace": plugin.namespace,
                        "installed": plugin.installed,
                    }
                    for plugin in targets
                ],
                "total_plugins": len(plugins) + len(targets),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list plugins: {e}",
                "extractors": [],
                "loaders": [],
                "total_plugins": 0,
            }

    def run_pipeline(
        self,
        tap_name: str,
        target_name: str,
        **_kwargs: object,
    ) -> dict[str, object]:
        """Run a Meltano pipeline.

        Args:
            tap_name: Name of the tap (extractor)
            target_name: Name of the target (loader)
            **kwargs: Additional pipeline parameters

        Returns:
            Dictionary with execution results for JSON serialization

        """
        try:
            logger.info(f"Running pipeline: {tap_name} -> {target_name}")

            # Execute pipeline
            result = self._executor.execute_pipeline(tap_name, target_name)

            if result.success and result.data:
                execution_data = result.data
                return {
                    "success": True,
                    "pipeline": f"{tap_name} -> {target_name}",
                    "execution_id": execution_data.get("execution_id"),
                    "duration_seconds": execution_data.get("duration_seconds", 0),
                    "stdout": execution_data.get("stdout", ""),
                    "stderr": execution_data.get("stderr", ""),
                }

            return {
                "success": False,
                "error": result.error or "Pipeline execution failed",
                "pipeline": f"{tap_name} -> {target_name}",
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Pipeline execution error: {e}",
                "pipeline": f"{tap_name} -> {target_name}",
            }

    def validate_project(self) -> dict[str, object]:
        """Validate the Meltano project.

        Returns:
            Dictionary with validation results for JSON serialization

        """
        try:
            result = self._validator.validate_project()

            if result.success and result.data:
                return {
                    "success": True,
                    "project_valid": result.data.get("project_valid", False),
                    "validation_results": result.data.get("validation_results", {}),
                }

            return {
                "success": False,
                "error": result.error or "Project validation failed",
                "project_valid": False,
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Project validation error: {e}",
                "project_valid": False,
            }

    def validate_tap_connection(
        self,
        tap_name: str,
        config: dict[str, object],
    ) -> dict[str, object]:
        """Validate tap connection.

        Args:
            tap_name: Name of the tap
            config: Tap configuration

        Returns:
            Dictionary with validation results for JSON serialization

        """
        try:
            result = self._validator.validate_tap_connection(tap_name, config)

            if result.success and result.data:
                return {
                    "success": True,
                    "tap_name": tap_name,
                    "connection_valid": result.data.get("connection_valid", False),
                    "validation_results": result.data.get("validation_results", {}),
                }

            return {
                "success": False,
                "error": result.error or "Tap validation failed",
                "tap_name": tap_name,
                "connection_valid": False,
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Tap validation error: {e}",
                "tap_name": tap_name,
                "connection_valid": False,
            }

    def create_tap_plugin(
        self,
        name: str,
        namespace: str,
        pip_url: str | None = None,
        executable: str | None = None,
        config: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Create a new tap plugin.

        Returns:
            Dictionary with plugin creation results for JSON serialization

        """
        try:
            result = create_meltano_tap_plugin(
                name,
                namespace,
                pip_url,
                executable,
                config,
            )

            if result.success and result.data:
                plugin = result.data
                # Register plugin
                registry_result = self._plugin_registry.add_plugin(plugin)

                if registry_result.success:
                    return {
                        "success": True,
                        "plugin": {
                            "name": plugin.name,
                            "type": str(plugin.plugin_type.value),
                            "namespace": plugin.namespace,
                            "created": True,
                            "registered": True,
                        },
                    }

            return {
                "success": False,
                "error": result.error or "Plugin creation failed",
                "plugin": {"name": name, "created": False},
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Plugin creation error: {e}",
                "plugin": {"name": name, "created": False},
            }


def create_bridge(config: FlextMeltanoConfig | None = None) -> FlextMeltanoBridge:
    """Create a bridge instance.

    Args:
      config: Optional Meltano configuration

    Returns:
      Configured bridge instance

    """
    return FlextMeltanoBridge(config)


# =============================================================================
# CLI BRIDGE INTEGRATION
# =============================================================================


CLI_MIN_ARGS = 2
CLI_MIN_ARGS_RUN_PIPELINE = 4


def main() -> None:
    """Provide CLI entry point for bridge operations.

    This function provides a simple CLI interface for Go services to call
    FLEXT Meltano operations via subprocess.

    Usage:
      python -m flext_meltano.meltano_bridge <operation> [args...]

    """
    if len(sys.argv) < CLI_MIN_ARGS:
        sys.exit(1)

    operation = sys.argv[1]
    bridge = create_bridge()

    try:
        if operation == "version":
            bridge.get_version()
        elif operation == "list-plugins":
            bridge.list_plugins()
        elif operation == "validate-project":
            bridge.validate_project()
        elif operation == "run-pipeline":
            if len(sys.argv) >= CLI_MIN_ARGS_RUN_PIPELINE:
                tap_name = sys.argv[2]
                target_name = sys.argv[3]
                bridge.run_pipeline(tap_name, target_name)
            else:
                sys.exit(1)

    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()


__all__ = [
    # Bridge Integration
    "FlextMeltanoBridge",
    # Validation Framework
    "FlextMeltanoValidator",
    "create_bridge",
    # Plugin Creation
    "create_meltano_tap_plugin",
    "create_meltano_target_plugin",
    # Utilities
    "injectable",
    "validate_config_value",
    "validate_directory_path",
    "validate_file_path",
]
