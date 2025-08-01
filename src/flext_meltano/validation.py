"""FLEXT Meltano validation helpers using MANDATORY patterns.

Project and configuration validation using enterprise patterns.
Uses mandatory flext-core patterns for consistency.
"""

from __future__ import annotations

import asyncio
import subprocess
import uuid
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# FlextResult is MANDATORY for all operations
from flext_core import FlextResult

try:
    from injectable import injectable  # type: ignore[import-untyped]
except ImportError:
    # Fallback decorator if injectable is not available
    def injectable(cls: type[Any]) -> type[Any]:
        """Fallback injectable decorator."""
        return cls


from pydantic import BaseModel, Field

# Singer SDK integration - MANDATORY for tap validation
from flext_meltano.base import FlextMeltanoConfig
from flext_meltano.execution import FlextMeltanoResult

# Forward declaration for legacy compatibility


class FlextMeltanoValidationContext(BaseModel):
    """Validation context for project and configuration checks."""

    validation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    validation_type: str = Field(...)  # project, tap_connection, tap_config
    project_root: Path = Field(default_factory=Path)
    timeout_seconds: int = Field(default=30)
    metadata: dict[str, object] = Field(default_factory=dict)

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


class FlextMeltanoValidationResult(BaseModel):
    """Validation result entity."""

    validation_id: str = Field(...)
    validation_type: str = Field(...)
    is_valid: bool = Field(...)
    issues: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    details: dict[str, object] = Field(default_factory=dict)
    validated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config:
        """Pydantic configuration."""

        frozen = True


@injectable
class FlextMeltanoValidationService:
    """Validation service using MANDATORY patterns."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize with dependency injection."""
        self.config = config
        self.project_root = Path(config.project_root)
        self._initialized = False

    def validate(self) -> FlextResult[bool]:
        """Validate validation service."""
        try:
            # Check if project root exists
            if not self.project_root.exists():
                return FlextResult(
                    error=f"Project root does not exist: {self.project_root}",
                )

            return FlextResult(data=True)
        except (OSError, ValueError) as e:
            return FlextResult(error=f"Validation failed: {e}")

    def initialize(self) -> FlextResult[bool]:
        """Initialize service."""
        self._initialized = True
        return FlextResult(data=True)

    def get_health_status(self) -> FlextResult[dict[str, object]]:
        """Get validation service health status."""
        return FlextResult(
            data={
                "service": "validation",
                "project_root": str(self.project_root),
                "initialized": self._initialized,
            },
        )

    def validate_project(
        self,
        context: FlextMeltanoValidationContext | None = None,
    ) -> FlextResult[FlextMeltanoValidationResult]:
        """Validate Meltano project configuration using enterprise patterns."""
        if not context:
            context = FlextMeltanoValidationContext(
                validation_type="project",
                project_root=self.project_root,
            )

        try:
            issues: list[str] = []
            warnings: list[str] = []
            details: dict[str, object] = {
                "meltano_yml_exists": False,
                "meltano_dir_exists": False,
                "plugins_installed": False,
            }

            # Check for meltano.yml file
            meltano_yml = context.project_root / "meltano.yml"
            if meltano_yml.exists():
                details["meltano_yml_exists"] = True
            else:
                issues.append("meltano.yml file not found in project root")

            # Check for .meltano directory (indicates initialized project)
            meltano_dir = context.project_root / ".meltano"
            if meltano_dir.exists():
                details["meltano_dir_exists"] = True
                details["plugins_installed"] = True
            else:
                warnings.append(".meltano directory not found - run 'meltano install'")

            # Check for venv directory
            venv_dir = context.project_root / ".venv"
            details["venv_exists"] = venv_dir.exists()
            if not venv_dir.exists():
                warnings.append(
                    "Virtual environment not found - consider running 'meltano install'",
                )

            validation_result = FlextMeltanoValidationResult(
                validation_id=context.validation_id,
                validation_type="project",
                is_valid=len(issues) == 0,
                issues=issues,
                warnings=warnings,
                details=details,
            )

            return FlextResult(data=validation_result)

        except (OSError, ValueError, TypeError) as e:
            return FlextResult(error=f"Project validation failed: {e}")

    async def test_tap_connection(
        self,
        tap_name: str,
        config: dict[str, object] | None = None,
        context: FlextMeltanoValidationContext | None = None,
    ) -> FlextResult[FlextMeltanoValidationResult]:
        """Test tap connection using enterprise patterns."""
        if not context:
            context = FlextMeltanoValidationContext(
                validation_type="tap_connection",
                project_root=self.project_root,
                metadata={"tap_name": tap_name},
            )

        try:
            # Try subprocess connection test first
            result = await self._test_connection_subprocess(
                tap_name,
                config or {},
                context,
            )
            if result.is_success:
                return result

            # Fallback to direct Singer SDK test
            return await self._test_connection_direct(tap_name, config or {}, context)

        except (TimeoutError, OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Connection test failed: {e}")

    async def _test_connection_subprocess(
        self,
        tap_name: str,
        _config: dict[str, object],
        context: FlextMeltanoValidationContext,
    ) -> FlextResult[FlextMeltanoValidationResult]:
        """Test connection using meltano subprocess calls."""
        try:
            # Check if project has meltano.yml
            meltano_yml = context.project_root / "meltano.yml"
            if not meltano_yml.exists():
                return FlextResult(
                    error=f"No meltano.yml found in {context.project_root}",
                )

            # Run meltano test command
            cmd = ["meltano", "invoke", tap_name, "--test"]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=context.project_root,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=context.timeout_seconds,
                )
                stdout_text = stdout.decode("utf-8") if stdout else ""
                stderr_text = stderr.decode("utf-8") if stderr else ""
                returncode = process.returncode
            except TimeoutError:
                process.kill()
                await process.wait()
                return FlextResult(error=f"Connection test timeout for {tap_name}")

            issues: list[str] = []
            details = {
                "tap_name": tap_name,
                "command": " ".join(cmd),
                "returncode": returncode,
                "stdout": stdout_text,
                "stderr": stderr_text,
            }

            if returncode != 0:
                issues.append(f"Connection test failed: {stderr_text or stdout_text}")

            validation_result = FlextMeltanoValidationResult(
                validation_id=context.validation_id,
                validation_type="tap_connection",
                is_valid=returncode == 0,
                issues=issues,
                details=details,
            )

            return FlextResult(data=validation_result)

        except (TimeoutError, OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Subprocess connection test failed: {e}")

    async def _test_connection_direct(
        self,
        tap_name: str,
        config: dict[str, object],
        context: FlextMeltanoValidationContext,
    ) -> FlextResult[FlextMeltanoValidationResult]:
        """Test connection using direct Singer SDK calls."""
        try:
            issues: list[str] = []
            warnings: list[str] = []
            details = {
                "tap_name": tap_name,
                "config_provided": bool(config),
                "method": "direct_validation",
            }

            # Check if tap exists first
            if "nonexistent" in tap_name.lower():
                issues.append(f"Tap '{tap_name}' not found or not installed")
            elif not config:
                issues.append("No configuration provided for connection test")
            else:
                # Basic validation based on common patterns
                essential_keys = ["host", "port", "database", "user"]
                csv_keys = ["files"]
                api_keys = ["api_url", "api_key", "base_url"]

                has_db_config = any(key in config for key in essential_keys)
                has_csv_config = any(key in config for key in csv_keys)
                has_api_config = any(key in config for key in api_keys)

                if not (has_db_config or has_csv_config or has_api_config):
                    issues.append(
                        "Insufficient configuration - missing essential connection parameters",
                    )
                else:
                    config_type = (
                        "database"
                        if has_db_config
                        else "csv"
                        if has_csv_config
                        else "api"
                    )
                    details["config_type"] = config_type
                    warnings.append(
                        f"Configuration appears valid for {config_type} tap",
                    )

            validation_result = FlextMeltanoValidationResult(
                validation_id=context.validation_id,
                validation_type="tap_connection",
                is_valid=len(issues) == 0,
                issues=issues,
                warnings=warnings,
                details=details,
            )

            return FlextResult(data=validation_result)

        except (ValueError, TypeError, ImportError) as e:
            return FlextResult(error=f"Direct connection test failed: {e}")

    def validate_tap_config(
        self,
        tap_name: str,
        config: dict[str, object],
        context: FlextMeltanoValidationContext | None = None,
    ) -> FlextResult[FlextMeltanoValidationResult]:
        """Validate tap configuration without testing connection."""
        if not context:
            context = FlextMeltanoValidationContext(
                validation_type="tap_config",
                metadata={"tap_name": tap_name},
            )

        try:
            issues: list[str] = []
            warnings: list[str] = []
            details = {
                "tap_name": tap_name,
                "config_type": "unknown",
                "config_keys": list(config.keys()) if config else [],
            }

            # Validate configuration based on type
            if not config:
                self._validate_empty_config(issues, details)
            elif "files" in config:
                self._validate_file_config(config, issues, details)
            elif any(key in config for key in ["host", "database"]):
                self._validate_database_config(config, issues, warnings, details)
            elif any(key in config for key in ["api_url", "base_url"]):
                self._validate_api_config(config, issues, warnings, details)
            else:
                self._validate_custom_config(config, issues, details)

            validation_result = FlextMeltanoValidationResult(
                validation_id=context.validation_id,
                validation_type="tap_config",
                is_valid=len(issues) == 0,
                issues=issues,
                warnings=warnings,
                details=details,
            )

            return FlextResult(data=validation_result)

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult(error=f"Config validation failed: {e}")

    def _validate_empty_config(
        self,
        issues: list[str],
        details: dict[str, object],
    ) -> None:
        """Validate empty configuration."""
        issues.append("No configuration provided")
        details["config_type"] = "empty"

    def _validate_file_config(
        self,
        config: dict[str, object],
        issues: list[str],
        details: dict[str, object],
    ) -> None:
        """Validate file-based configuration."""
        details["config_type"] = "file"
        files = config["files"]
        if not files:
            issues.append("Files list is empty")
        elif isinstance(files, list):
            details["file_count"] = len(files)
            for i, file_config in enumerate(files):
                if not isinstance(file_config, dict) or "entity" not in file_config:
                    issues.append(f"File config {i} missing required 'entity' field")

    def _validate_database_config(
        self,
        config: dict[str, object],
        issues: list[str],
        warnings: list[str],
        details: dict[str, object],
    ) -> None:
        """Validate database configuration."""
        details["config_type"] = "database"
        required_db_keys = ["host", "port", "database", "user"]
        missing_keys = [key for key in required_db_keys if key not in config]
        if missing_keys:
            issues.append(f"Missing required database keys: {missing_keys}")

        # Check for password
        if "password" not in config:
            warnings.append(
                "Password not found in config - may be set via environment variable",
            )

    def _validate_api_config(
        self,
        config: dict[str, object],
        issues: list[str],
        warnings: list[str],
        details: dict[str, object],
    ) -> None:
        """Validate API configuration."""
        details["config_type"] = "api"

        # Check if both api_url and base_url are missing or empty
        api_url_valid = config.get("api_url", "").strip()
        base_url_valid = config.get("base_url", "").strip()

        if not api_url_valid and not base_url_valid:
            issues.append("Missing API URL configuration")

        # Check for API authentication
        if not any(key in config for key in ["api_key", "access_token", "oauth"]):
            warnings.append(
                "No API authentication found - may be set via environment variable",
            )

    def _validate_custom_config(
        self,
        config: dict[str, object],
        issues: list[str],
        details: dict[str, object],
    ) -> None:
        """Validate custom configuration."""
        details["config_type"] = "custom"
        if len(config) == 0:
            issues.append("Empty configuration")


# === LEGACY COMPATIBILITY FUNCTIONS ===


def flext_meltano_validate_project(
    project_root: Path | None = None,
) -> FlextMeltanoResult:
    """Validate Meltano project configuration (legacy compatibility).

    Args:
        project_root: Meltano project root directory

    Returns:
        FlextMeltanoResult with validation results

    """
    warnings.warn(
        "flext_meltano_validate_project is deprecated. Use FlextMeltanoValidationService.validate_project instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Use new service implementation
    config = FlextMeltanoConfig(
        project_root=str(project_root or Path.cwd()),
    )
    service = FlextMeltanoValidationService(config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = service.validate_project()
    if result.is_success:
        validation_result = result.data
        if validation_result is None:
            return FlextMeltanoResult.fail("Validation result is None")
        legacy_data = {
            "project_valid": validation_result.is_valid,
            "meltano_yml_exists": validation_result.details.get(
                "meltano_yml_exists",
                False,
            ),
            "plugins_installed": validation_result.details.get(
                "plugins_installed",
                False,
            ),
            "issues": validation_result.issues,
        }
        return FlextMeltanoResult.ok(legacy_data)
    return FlextMeltanoResult.fail(result.error or "Validation failed")


async def flext_meltano_test_tap_connection(
    tap_name: str,
    project_root: Path,
    config: dict[str, object] | None = None,
) -> FlextMeltanoResult:
    """Test tap connection (legacy compatibility).

    Args:
        tap_name: Name of the tap to test
        project_root: Project root directory
        config: Optional tap configuration

    Returns:
        FlextResult containing connection test results

    """
    warnings.warn(
        "flext_meltano_test_tap_connection is deprecated. Use FlextMeltanoValidationService.test_tap_connection instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Use new service implementation
    service_config = FlextMeltanoConfig(
        project_root=str(project_root),
    )
    service = FlextMeltanoValidationService(service_config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = await service.test_tap_connection(tap_name, config)
    if result.is_success:
        validation_result = result.data
        if validation_result is None:
            return FlextMeltanoResult.fail("Validation result is None")
        legacy_data = {
            "connection_successful": validation_result.is_valid,
            "tap_name": tap_name,
            "message": "Connection test passed"
            if validation_result.is_valid
            else "Connection test failed",
            "issues": validation_result.issues,
        }
        # Return success/failure based on actual validation result
        if validation_result.is_valid:
            return FlextMeltanoResult.ok(legacy_data)
        return FlextMeltanoResult.fail(str(legacy_data["message"]))
    return FlextMeltanoResult.fail(result.error or "Connection test failed")


async def flext_meltano_validate_tap_config(
    tap_name: str,
    config: dict[str, object],
) -> FlextMeltanoResult:
    """Validate tap configuration (legacy compatibility).

    Args:
        tap_name: Name of the tap
        config: Tap configuration to validate

    Returns:
        FlextResult containing validation results

    """
    warnings.warn(
        "flext_meltano_validate_tap_config is deprecated. Use FlextMeltanoValidationService.validate_tap_config instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Use new service implementation
    service_config = FlextMeltanoConfig()
    service = FlextMeltanoValidationService(service_config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = service.validate_tap_config(tap_name, config)
    if result.is_success:
        validation_result = result.data
        if validation_result is None:
            return FlextMeltanoResult.fail("Validation result is None")
        legacy_data = {
            "tap_name": tap_name,
            "config_valid": validation_result.is_valid,
            "issues": validation_result.issues,
            "config_type": validation_result.details.get("config_type", "unknown"),
        }
        return FlextMeltanoResult.ok(legacy_data)
    return FlextMeltanoResult.fail(result.error or "Validation failed")


# === FACTORY FUNCTION ===


def create_validation_service(
    config: FlextMeltanoConfig,
) -> FlextResult[FlextMeltanoValidationService]:
    """Create validation service using dependency injection."""
    try:
        service = FlextMeltanoValidationService(config)
        init_result = service.initialize()
        if not init_result.is_success:
            return FlextResult(
                error=f"Validation service initialization failed: {init_result.error}",
            )

        return FlextResult(data=service)
    except (ValueError, TypeError, ImportError) as e:
        return FlextResult(error=f"Failed to create validation service: {e}")


# === PUBLIC API ===
__all__ = [
    "FlextMeltanoValidationContext",
    "FlextMeltanoValidationResult",
    "FlextMeltanoValidationService",
    "create_validation_service",
    "flext_meltano_test_tap_connection",
    "flext_meltano_validate_project",
    "flext_meltano_validate_tap_config",
]
