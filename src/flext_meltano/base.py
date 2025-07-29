"""FLEXT Meltano Base - Unified foundation using flext-core patterns.

This module consolidates all base classes for Singer, DBT, and Meltano integration
into a single module using composition and FlextDomainService patterns to reduce
code duplication and module count.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from flext_core import FlextResult

if TYPE_CHECKING:
    from pathlib import Path

# Type variable for generic results
T = TypeVar("T")

# External dependencies availability flags
try:
    from singer_sdk import Tap, Target
    from singer_sdk.typing import PropertiesList
    SINGER_AVAILABLE = True
except ImportError:
    Tap = Target = PropertiesList = None  # type: ignore[assignment,misc]
    SINGER_AVAILABLE = False

try:
    import dbt.version
    from dbt.cli.main import dbtRunner
    DBT_AVAILABLE = True
except ImportError:
    dbtRunner = None  # type: ignore[assignment,misc]
    DBT_AVAILABLE = False


class FlextMeltanoConfig:
    """Unified typed configuration for all FLEXT Meltano components."""

    def __init__(self, **config: Any) -> None:
        """Initialize configuration with validation."""
        self.config = config
        self._validated = False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
        self._validated = False  # Require re-validation

    def validate(self, required_keys: list[str] | None = None) -> FlextResult[bool]:
        """Validate configuration with optional required keys."""
        if not self.config:
            return FlextResult(error="Empty configuration")

        if required_keys:
            missing_keys = [key for key in required_keys if key not in self.config]
            if missing_keys:
                return FlextResult(error=f"Missing required config keys: {missing_keys}")

        self._validated = True
        return FlextResult(data=True)

    @property
    def is_validated(self) -> bool:
        """Check if configuration is validated."""
        return self._validated


class FlextMeltanoOperationProtocol(Protocol):
    """Protocol for all FLEXT Meltano operations."""

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute the operation."""
        ...

    def validate_config(self) -> FlextResult[bool]:
        """Validate configuration."""
        ...


class FlextMeltanoBaseService:
    """Unified base service for all FLEXT Meltano components.

    This replaces the separate base classes for Tap, Target, DBT with a single
    composable service that reduces method count and provides consistent patterns.
    """

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig, service_type: str) -> None:
        """Initialize base service with configuration and type."""
        if isinstance(config, FlextMeltanoConfig):
            self.config = config
        else:
            self.config = FlextMeltanoConfig(**config)

        self.service_type = service_type
        self._statistics = {"operations_count": 0, "last_execution": None}

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute service operations with unified patterns."""
        self._statistics["operations_count"] += 1
        self._statistics["last_execution"] = self._get_current_timestamp()

        return FlextResult(data={
            "service_type": self.service_type,
            "config_validated": self.config.is_validated,
            "statistics": self._statistics.copy(),
        })

    def validate_config(self, required_keys: list[str] | None = None) -> FlextResult[bool]:
        """Validate configuration using FlextValueObject patterns."""
        return self.config.validate(required_keys)

    def get_statistics(self) -> FlextResult[dict[str, Any]]:
        """Get service statistics."""
        return FlextResult(data=self._statistics.copy())

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for statistics."""
        import datetime
        return datetime.datetime.now().isoformat()


class FlextMeltanoTap(FlextMeltanoBaseService):
    """Singer SDK tap implementation using unified base service."""

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig) -> None:
        """Initialize tap with configuration."""
        super().__init__(config, "tap")
        self._streams_discovered = False
        self._catalog_cache: dict[str, Any] = {}

    def discover_streams(self) -> FlextResult[list[dict[str, Any]]]:
        """Discover available streams - base implementation."""
        if not SINGER_AVAILABLE:
            return FlextResult(error="Singer SDK not available")

        # Validate configuration first
        validation_result = self.validate_config()
        if not validation_result.is_success:
            return FlextResult(error=validation_result.error)

        try:
            # Base discovery - should be overridden by specific implementations
            self._streams_discovered = True
            streams = [{"name": "default_stream", "schema": {}}]
            return FlextResult(data=streams)
        except Exception as e:
            return FlextResult(error=f"Stream discovery failed: {e}")

    def extract_records(self, stream_name: str) -> FlextResult[list[dict[str, Any]]]:
        """Extract records from stream - base implementation."""
        try:
            # Base extraction - should be overridden by specific implementations
            records = [{"id": 1, "stream": stream_name, "data": "sample"}]
            return FlextResult(data=records)
        except Exception as e:
            return FlextResult(error=f"Record extraction failed: {e}")


class FlextMeltanoTarget(FlextMeltanoBaseService):
    """Singer SDK target implementation using unified base service."""

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig) -> None:
        """Initialize target with configuration."""
        super().__init__(config, "target")
        self._records_processed = 0

    def process_record(self, record: dict[str, Any]) -> FlextResult[bool]:
        """Process a single record - base implementation."""
        try:
            # Base processing - should be overridden by specific implementations
            self._records_processed += 1
            return FlextResult(data=True)
        except Exception as e:
            return FlextResult(error=f"Record processing failed: {e}")

    def batch_process(self, records: list[dict[str, Any]]) -> FlextResult[int]:
        """Process batch of records using composition."""
        try:
            processed_count = 0
            for record in records:
                result = self.process_record(record)
                if result.is_success:
                    processed_count += 1
            return FlextResult(data=processed_count)
        except Exception as e:
            return FlextResult(error=f"Batch processing failed: {e}")

    def get_processed_count(self) -> int:
        """Get number of processed records."""
        return self._records_processed


class FlextMeltanoDbt(FlextMeltanoBaseService):
    """DBT implementation using unified base service."""

    def __init__(self, project_dir: Path, config: dict[str, Any] | None = None) -> None:
        """Initialize DBT service with project directory."""
        config = config or {}
        super().__init__(config, "dbt")
        self.project_dir = project_dir
        self._models_compiled = False
        self._tests_passed = False

        # DBT runner initialization
        if DBT_AVAILABLE:
            self._dbt_runner = dbtRunner()
        else:
            self._dbt_runner = None

    def run_models(self, models: list[str] | None = None) -> FlextResult[dict[str, Any]]:
        """Run DBT models using dbt-core."""
        if not self._dbt_runner:
            return FlextResult(error="DBT runner not available")

        try:
            # Validate project first
            validation_result = self.validate_project()
            if not validation_result.is_success:
                return FlextResult(error=validation_result.error)

            # Build dbt command
            cmd = ["run", "--project-dir", str(self.project_dir)]
            if models:
                cmd.extend(["--models", *models])

            # Execute using dbt-core
            result = self._dbt_runner.invoke(cmd)

            if result.is_success:
                run_results = []
                if hasattr(result, "result") and result.result and hasattr(result.result, "results"):
                    run_results = result.result.results or []

                self._models_compiled = True
                return FlextResult(data={
                    "results": run_results,
                    "models_run": len(run_results),
                })

            error_msg = "Unknown error"
            if hasattr(result, "exception") and result.exception:
                error_msg = str(result.exception)

            return FlextResult(error=f"DBT run failed: {error_msg}")

        except Exception as e:
            return FlextResult(error=f"DBT execution error: {e}")

    def test_models(self, models: list[str] | None = None) -> FlextResult[dict[str, Any]]:
        """Test DBT models using dbt-core."""
        if not self._dbt_runner:
            return FlextResult(error="DBT runner not available")

        try:
            # Validate project first
            validation_result = self.validate_project()
            if not validation_result.is_success:
                return FlextResult(error=validation_result.error)

            # Build dbt command
            cmd = ["test", "--project-dir", str(self.project_dir)]
            if models:
                cmd.extend(["--models", *models])

            # Execute using dbt-core
            result = self._dbt_runner.invoke(cmd)

            if result.is_success:
                test_results = []
                if hasattr(result, "result") and result.result and hasattr(result.result, "results"):
                    test_results = result.result.results or []

                self._tests_passed = True
                return FlextResult(data={
                    "results": test_results,
                    "tests_run": len(test_results),
                })

            error_msg = "Unknown error"
            if hasattr(result, "exception") and result.exception:
                error_msg = str(result.exception)

            return FlextResult(error=f"DBT test failed: {error_msg}")

        except Exception as e:
            return FlextResult(error=f"DBT test error: {e}")

    def validate_project(self) -> FlextResult[bool]:
        """Validate DBT project configuration."""
        dbt_project_file = self.project_dir / "dbt_project.yml"
        if not dbt_project_file.exists():
            return FlextResult(error=f"DBT project not found at {self.project_dir}")

        return FlextResult(data=True)

    def get_version(self) -> FlextResult[str]:
        """Get DBT version."""
        if not DBT_AVAILABLE:
            return FlextResult(error="DBT not available")

        try:
            version_info = dbt.version.get_version_information()
            if isinstance(version_info, dict):
                version = version_info.get("version", "unknown")
            else:
                version = str(version_info)
            return FlextResult(data=version)
        except Exception as e:
            return FlextResult(error=f"Version check failed: {e}")


# Specific implementations for common use cases
class FlextMeltanoTapOracle(FlextMeltanoTap):
    """Oracle tap implementation."""

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig) -> None:
        """Initialize Oracle tap with configuration."""
        if isinstance(config, dict):
            config = FlextMeltanoConfig(**config)
        super().__init__(config)

    def validate_config(self, required_keys: list[str] | None = None) -> FlextResult[bool]:
        """Validate Oracle-specific configuration."""
        oracle_required = ["host", "port", "service_name", "user", "password"]
        return super().validate_config(oracle_required)


class FlextMeltanoTapLdap(FlextMeltanoTap):
    """LDAP tap implementation."""

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig) -> None:
        """Initialize LDAP tap with configuration."""
        if isinstance(config, dict):
            config = FlextMeltanoConfig(**config)
        super().__init__(config)

    def validate_config(self, required_keys: list[str] | None = None) -> FlextResult[bool]:
        """Validate LDAP-specific configuration."""
        ldap_required = ["host", "port", "bind_dn", "bind_password", "base_dn"]
        return super().validate_config(ldap_required)


class FlextMeltanoTargetOracle(FlextMeltanoTarget):
    """Oracle target implementation."""

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig) -> None:
        """Initialize Oracle target with configuration."""
        if isinstance(config, dict):
            config = FlextMeltanoConfig(**config)
        super().__init__(config)

    def validate_config(self, required_keys: list[str] | None = None) -> FlextResult[bool]:
        """Validate Oracle-specific configuration."""
        oracle_required = ["host", "port", "service_name", "user", "password", "default_target_schema"]
        return super().validate_config(oracle_required)


class FlextMeltanoTargetLdap(FlextMeltanoTarget):
    """LDAP target implementation."""

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig) -> None:
        """Initialize LDAP target with configuration."""
        if isinstance(config, dict):
            config = FlextMeltanoConfig(**config)
        super().__init__(config)

    def validate_config(self, required_keys: list[str] | None = None) -> FlextResult[bool]:
        """Validate LDAP-specific configuration."""
        ldap_required = ["host", "port", "bind_dn", "bind_password", "base_dn"]
        return super().validate_config(ldap_required)


class FlextMeltanoTargetCsv(FlextMeltanoTarget):
    """CSV target implementation."""

    def __init__(self, config: dict[str, Any] | FlextMeltanoConfig) -> None:
        """Initialize CSV target with configuration."""
        if isinstance(config, dict):
            config = FlextMeltanoConfig(**config)
        super().__init__(config)

    def validate_config(self, required_keys: list[str] | None = None) -> FlextResult[bool]:
        """Validate CSV-specific configuration."""
        csv_required = ["destination_path"]
        return super().validate_config(csv_required)


# Factory functions for creating components
def create_tap(tap_type: str, config: dict[str, Any]) -> FlextResult[FlextMeltanoTap]:
    """Factory function to create taps by type."""
    tap_classes = {
        "oracle": FlextMeltanoTapOracle,
        "ldap": FlextMeltanoTapLdap,
        "base": FlextMeltanoTap,
    }

    tap_class = tap_classes.get(tap_type, FlextMeltanoTap)
    try:
        tap = tap_class(config)
        return FlextResult(data=tap)
    except Exception as e:
        return FlextResult(error=f"Tap creation failed: {e}")


def create_target(target_type: str, config: dict[str, Any]) -> FlextResult[FlextMeltanoTarget]:
    """Factory function to create targets by type."""
    target_classes = {
        "oracle": FlextMeltanoTargetOracle,
        "ldap": FlextMeltanoTargetLdap,
        "csv": FlextMeltanoTargetCsv,
        "base": FlextMeltanoTarget,
    }

    target_class = target_classes.get(target_type, FlextMeltanoTarget)
    try:
        target = target_class(config)
        return FlextResult(data=target)
    except Exception as e:
        return FlextResult(error=f"Target creation failed: {e}")


def create_dbt_service(project_dir: Path, config: dict[str, Any] | None = None) -> FlextResult[FlextMeltanoDbt]:
    """Factory function to create DBT service."""
    try:
        dbt_service = FlextMeltanoDbt(project_dir, config)
        return FlextResult(data=dbt_service)
    except Exception as e:
        return FlextResult(error=f"DBT service creation failed: {e}")


__all__ = [
    "DBT_AVAILABLE",
    # Constants
    "SINGER_AVAILABLE",
    "FlextMeltanoBaseService",
    # Base classes
    "FlextMeltanoConfig",
    "FlextMeltanoDbt",
    # Protocols
    "FlextMeltanoOperationProtocol",
    "FlextMeltanoTap",
    "FlextMeltanoTapLdap",
    # Specific implementations
    "FlextMeltanoTapOracle",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetCsv",
    "FlextMeltanoTargetLdap",
    "FlextMeltanoTargetOracle",
    "create_dbt_service",
    # Factory functions
    "create_tap",
    "create_target",
]
