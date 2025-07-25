"""FLEXT Meltano boilerplate reduction patterns.

Helpers, mixins, decorators, and typedefs to drastically reduce application code.
Replaces 200+ lines of repetitive code with single-line patterns.
"""

from __future__ import annotations

import asyncio
import functools
from pathlib import Path
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar, Union

from flext_meltano.helpers.discovery import (
    flext_meltano_discover_catalog,
    flext_meltano_discover_plugins,
)
from flext_meltano.helpers.execution import (
    FlextMeltanoResult,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)
from flext_meltano.helpers.validation import (
    flext_meltano_test_tap_connection,
    flext_meltano_validate_project,
    flext_meltano_validate_tap_config,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

# Type definitions for reducing boilerplate
P = ParamSpec("P")
T = TypeVar("T")

MeltanoConfig = dict[str, Any]
TapConfig = dict[str, Any]
TargetConfig = dict[str, Any]
PluginConfig = dict[str, Any]
ProjectConfig = dict[str, Any]
PipelineConfig = dict[str, Any]
CatalogData = dict[str, Any]
StreamData = dict[str, Any]
ExecutionResult = FlextMeltanoResult

# Path type aliases
ProjectPath = Union[str, Path]
MeltanoProjectPath = Union[str, Path]

# Common configuration templates to eliminate config boilerplate
CSV_TAP_CONFIG_TEMPLATE: TapConfig = {
    "files": [
        {"entity": "data", "path": "data.csv", "keys": ["id"]},
    ],
}

POSTGRES_TAP_CONFIG_TEMPLATE: TapConfig = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "",
    "schema": "public",
}

ORACLE_TAP_CONFIG_TEMPLATE: TapConfig = {
    "host": "localhost",
    "port": 1521,
    "sid": "xe",
    "user": "system",
    "password": "",
    "service_name": "",
}

JSONL_TARGET_CONFIG_TEMPLATE: TargetConfig = {
    "destination_path": "output",
    "file_naming_scheme": "{stream_name}.jsonl",
}

CSV_TARGET_CONFIG_TEMPLATE: TargetConfig = {
    "destination_path": "output",
    "file_naming_scheme": "{stream_name}.csv",
    "delimiter": ",",
    "quotechar": '"',
}


def flext_meltano_config(
    tap_name: str,
    target_name: str = "target-jsonl",
    **overrides: object,
) -> PipelineConfig:
    """Create pipeline config with zero boilerplate.

    Replaces 15+ lines of manual config assembly.

    Args:
        tap_name: Tap plugin name
        target_name: Target plugin name
        **overrides: Config overrides

    Returns:
        Complete pipeline configuration

    """
    # Smart config selection based on tap name
    if "csv" in tap_name:
        tap_config = {**CSV_TAP_CONFIG_TEMPLATE, **overrides.get("tap_config", {})}
    elif "postgres" in tap_name:
        tap_config = {**POSTGRES_TAP_CONFIG_TEMPLATE, **overrides.get("tap_config", {})}
    elif "oracle" in tap_name:
        tap_config = {**ORACLE_TAP_CONFIG_TEMPLATE, **overrides.get("tap_config", {})}
    else:
        tap_config = overrides.get("tap_config", {})

    # Smart target config selection
    if "jsonl" in target_name:
        target_config = {**JSONL_TARGET_CONFIG_TEMPLATE, **overrides.get("target_config", {})}
    elif "csv" in target_name:
        target_config = {**CSV_TARGET_CONFIG_TEMPLATE, **overrides.get("target_config", {})}
    else:
        target_config = overrides.get("target_config", {})

    return {
        "tap_name": tap_name,
        "target_name": target_name,
        "tap_config": tap_config,
        "target_config": target_config,
        "project_root": overrides.get("project_root", "."),
        "environment": overrides.get("environment", "dev"),
    }


def flext_meltano_auto_retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic retry with exponential backoff.

    Eliminates 20+ lines of manual retry logic.

    Args:
        max_retries: Maximum number of retries
        delay: Initial delay between retries
        backoff: Backoff multiplier

    Returns:
        Decorated function with retry logic

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            current_delay = delay
            last_error = None

            for attempt in range(max_retries + 1):
                try:
                    result = await func(*args, **kwargs)
                    if result.success:
                        return result
                    last_error = result.error
                except Exception as e:
                    last_error = str(e)

                if attempt < max_retries:
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

            return FlextMeltanoResult.fail(f"Failed after {max_retries} retries: {last_error}")

        return wrapper
    return decorator


def flext_meltano_validate_config(
    config_validators: dict[str, Callable[[Any], bool]] | None = None,
) -> Callable[[Callable[P, Awaitable[FlextMeltanoResult]]], Callable[P, Awaitable[FlextMeltanoResult]]]:
    """Decorator for automatic config validation.

    Eliminates 10+ lines of manual validation per function.

    Args:
        config_validators: Dictionary of field -> validator function mappings

    Returns:
        Decorated function with config validation

    """
    def decorator(
        func: Callable[P, Awaitable[FlextMeltanoResult]],
    ) -> Callable[P, Awaitable[FlextMeltanoResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> FlextMeltanoResult:
            # Extract config from kwargs if present
            config = kwargs.get("config", {})
            if config and config_validators:
                for field, validator in config_validators.items():
                    if field in config and not validator(config[field]):
                        return FlextMeltanoResult.fail(f"Invalid config field '{field}': {config[field]}")

            return await func(*args, **kwargs)

        return wrapper
    return decorator


class FlextMeltanoMixin:
    """Mixin class providing zero-boilerplate Meltano operations.

    Reduces 50+ lines of repetitive class setup to single inheritance.
    """

    def __init__(self, project_root: ProjectPath = ".") -> None:
        """Initialize mixin with project root."""
        self.project_root = Path(project_root)
        self._config_cache: dict[str, Any] = {}

    async def discover_catalog(
        self,
        tap_name: str,
        config: TapConfig | None = None,
    ) -> ExecutionResult:
        """Discover catalog with zero boilerplate."""
        return await flext_meltano_discover_catalog(tap_name, self.project_root, config)

    def discover_plugins(self, plugin_type: str | None = None) -> ExecutionResult:
        """Discover plugins with zero boilerplate."""
        return flext_meltano_discover_plugins(plugin_type)

    async def test_connection(
        self,
        tap_name: str,
        config: TapConfig | None = None,
    ) -> ExecutionResult:
        """Test connection with zero boilerplate."""
        return await flext_meltano_test_tap_connection(tap_name, self.project_root, config)

    def validate_project(self) -> ExecutionResult:
        """Validate project with zero boilerplate."""
        return flext_meltano_validate_project(self.project_root)

    async def validate_config(
        self,
        tap_name: str,
        config: TapConfig,
    ) -> ExecutionResult:
        """Validate config with zero boilerplate."""
        return await flext_meltano_validate_tap_config(tap_name, config)

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
        environment: str = "dev",
    ) -> ExecutionResult:
        """Execute pipeline with zero boilerplate."""
        return flext_meltano_execute_job(tap_name, target_name, self.project_root, environment)

    def run_command(
        self,
        args: list[str],
        environment: str = "dev",
    ) -> ExecutionResult:
        """Run command with zero boilerplate."""
        return flext_meltano_run_command(args, self.project_root, environment)

    def cache_config(self, key: str, config: dict[str, Any]) -> None:
        """Cache config to eliminate repeated lookups."""
        self._config_cache[key] = config

    def get_cached_config(self, key: str) -> dict[str, Any] | None:
        """Get cached config."""
        return self._config_cache.get(key)


class FlextMeltanoPipeline(FlextMeltanoMixin):
    """Complete pipeline class eliminating 100+ lines of setup.

    Provides end-to-end pipeline operations with minimal configuration.
    """

    def __init__(
        self,
        tap_name: str,
        target_name: str = "target-jsonl",
        project_root: ProjectPath = ".",
        environment: str = "dev",
    ) -> None:
        """Initialize complete pipeline."""
        super().__init__(project_root)
        self.tap_name = tap_name
        self.target_name = target_name
        self.environment = environment
        self._pipeline_config: PipelineConfig | None = None

    def configure(self, **overrides: object) -> FlextMeltanoPipeline:
        """Configure pipeline with smart defaults."""
        self._pipeline_config = flext_meltano_config(
            self.tap_name,
            self.target_name,
            project_root=str(self.project_root),
            environment=self.environment,
            **overrides,
        )
        return self

    async def validate(self) -> ExecutionResult:
        """Validate complete pipeline setup."""
        # Validate project
        project_result = self.validate_project()
        if not project_result.success:
            return project_result

        # Validate tap config if available
        if self._pipeline_config and "tap_config" in self._pipeline_config:
            config_result = await self.validate_config(
                self.tap_name,
                self._pipeline_config["tap_config"],
            )
            if not config_result.success:
                return config_result

        return FlextMeltanoResult.ok({"pipeline_valid": True})

    async def test(self) -> ExecutionResult:
        """Test complete pipeline connectivity."""
        if self._pipeline_config and "tap_config" in self._pipeline_config:
            return await self.test_connection(self.tap_name, self._pipeline_config["tap_config"])
        return await self.test_connection(self.tap_name)

    async def discover(self) -> ExecutionResult:
        """Discover pipeline catalog."""
        config = None
        if self._pipeline_config and "tap_config" in self._pipeline_config:
            config = self._pipeline_config["tap_config"]
        return await self.discover_catalog(self.tap_name, config)

    def execute(self) -> ExecutionResult:
        """Execute complete pipeline."""
        return self.execute_pipeline(self.tap_name, self.target_name, self.environment)

    async def run_full_cycle(self) -> ExecutionResult:
        """Run complete validation -> test -> execute cycle."""
        # Step 1: Validate
        validation_result = await self.validate()
        if not validation_result.success:
            return FlextMeltanoResult.fail(f"Validation failed: {validation_result.error}")

        # Step 2: Test connection
        test_result = await self.test()
        if not test_result.success:
            return FlextMeltanoResult.fail(f"Connection test failed: {test_result.error}")

        # Step 3: Execute pipeline
        execution_result = self.execute()
        if not execution_result.success:
            return FlextMeltanoResult.fail(f"Pipeline execution failed: {execution_result.error}")

        return FlextMeltanoResult.ok({
            "full_cycle_completed": True,
            "validation": validation_result.data,
            "test": test_result.data,
            "execution": execution_result.data,
        })


# Convenience functions eliminating even more boilerplate

async def flext_meltano_quick_pipeline(
    tap_name: str,
    target_name: str = "target-jsonl",
    project_root: ProjectPath = ".",
    **config_overrides: object,
) -> ExecutionResult:
    """Create and execute pipeline in single call.

    Eliminates 50+ lines of manual pipeline setup and execution.

    Args:
        tap_name: Source tap name
        target_name: Target name
        project_root: Project directory
        **config_overrides: Configuration overrides

    Returns:
        Pipeline execution result

    """
    pipeline = FlextMeltanoPipeline(tap_name, target_name, project_root)
    pipeline.configure(**config_overrides)
    return await pipeline.run_full_cycle()


def flext_meltano_csv_to_jsonl(
    csv_path: str,
    output_dir: str = "output",
    project_root: ProjectPath = ".",
) -> ExecutionResult:
    """CSV to JSONL pipeline in single function call.

    Eliminates 30+ lines of CSV pipeline setup.

    Args:
        csv_path: Path to CSV file
        output_dir: Output directory
        project_root: Project directory

    Returns:
        Pipeline execution result

    """
    pipeline = FlextMeltanoPipeline("tap-csv", "target-jsonl", project_root)
    pipeline.configure(
        tap_config={"files": [{"entity": "data", "path": csv_path}]},
        target_config={"destination_path": output_dir},
    )
    return pipeline.execute()


async def flext_meltano_postgres_to_csv(
    db_config: dict[str, Any],
    output_dir: str = "output",
    project_root: ProjectPath = ".",
) -> ExecutionResult:
    """PostgreSQL to CSV pipeline in single function call.

    Eliminates 40+ lines of database pipeline setup.

    Args:
        db_config: Database connection config
        output_dir: Output directory
        project_root: Project directory

    Returns:
        Pipeline execution result

    """
    return await flext_meltano_quick_pipeline(
        "tap-postgres",
        "target-csv",
        project_root,
        tap_config=db_config,
        target_config={"destination_path": output_dir},
    )


def flext_meltano_config_builder() -> dict[str, Any]:
    """Start building config with fluent interface.

    Returns:
        Config builder dictionary

    """
    return {
        "tap_name": "",
        "target_name": "target-jsonl",
        "tap_config": {},
        "target_config": {},
        "project_root": ".",
        "environment": "dev",
    }


# Dict helpers for even more convenience

class FlextMeltanoConfigDict(dict[str, Any]):
    """Enhanced dict with fluent config building."""

    def tap(self, name: str) -> FlextMeltanoConfigDict:
        """Set tap name."""
        self["tap_name"] = name
        return self

    def target(self, name: str) -> FlextMeltanoConfigDict:
        """Set target name."""
        self["target_name"] = name
        return self

    def tap_config(self, **config: object) -> FlextMeltanoConfigDict:
        """Set tap configuration."""
        self["tap_config"] = config
        return self

    def target_config(self, **config: object) -> FlextMeltanoConfigDict:
        """Set target configuration."""
        self["target_config"] = config
        return self

    def project(self, path: ProjectPath) -> FlextMeltanoConfigDict:
        """Set project root."""
        self["project_root"] = str(path)
        return self

    def env(self, environment: str) -> FlextMeltanoConfigDict:
        """Set environment."""
        self["environment"] = environment
        return self


def config() -> FlextMeltanoConfigDict:
    """Create fluent config builder.

    Usage:
        cfg = config().tap("tap-csv").target("target-jsonl").tap_config(files=[...])

    """
    return FlextMeltanoConfigDict(flext_meltano_config_builder())
