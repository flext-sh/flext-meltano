"""FLEXT Meltano Type Adapters - Modern Flext* abstractions for Meltano/dBT/Singer types.

This module provides comprehensive Flext* abstractions that transform native Meltano, dBT, and Singer SDK
types to use modern flext-core patterns with FlextResult railway-oriented programming, type safety,
and enterprise-grade error handling.

Architecture:
    Foundation Layer: Base adapter protocols using flext-core patterns
    Service Layer: Meltano/Singer/dBT type wrappers with FlextResult integration
    Integration Layer: Native type conversion and validation

Core Components:
    FlextMeltanoTypeAdapters: Main type adapter class following flext-core single-class pattern
    FlextTap/FlextTarget/FlextDbt: Modern wrapper types with FlextResult error handling
    FlextSingerStream/FlextSingerMessage: Type-safe message and stream handling
    FlextMeltanoProject: Project wrapper with enterprise validation

Features:
    - Railway-oriented programming via FlextResult for all operations
    - Type-safe transformations from native types to Flext* types
    - Enterprise error handling with detailed context
    - Python 3.13+ generic syntax and type annotations
    - Zero-duplication following flext-core architectural patterns

Examples:
    Basic tap wrapping:
        >>> from flext_meltano import FlextMeltanoTypeAdapters
        >>> adapters = FlextMeltanoTypeAdapters()
        >>> flext_tap = adapters.wrap_singer_tap(native_tap)
        >>> result = flext_tap.discover_streams()
        >>> if result.success:
        ...     streams = result.value

    Project wrapping with validation:
        >>> project_result = adapters.wrap_meltano_project(meltano_project)
        >>> if project_result.success:
        ...     flext_project = project_result.value
        ...     plugins_result = flext_project.list_plugins()

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import Protocol, TypeVar, runtime_checkable

# DBT imports - use proper imports without try/except
from dbt.cli.main import dbtRunner
from flext_core import (
    FlextLogger,
    FlextProtocols,
    FlextResult,
)
from meltano.core.project import Project as MeltanoProject
from singer_sdk import Stream as SingerStream, Tap as SingerTap, Target as SingerTarget

# Type variables for generic patterns
T = TypeVar("T")
TData = TypeVar("TData")

# Initialize logger
logger = FlextLogger(__name__)

# =============================================================================
# FLEXT TYPE ADAPTER PROTOCOLS - Following flext-core protocol patterns
# =============================================================================


@runtime_checkable
class FlextTypeAdapter(FlextProtocols.Foundation.Factory[T], Protocol):
    """Base protocol for Flext* type adapters with FlextResult integration."""

    @abstractmethod
    def validate_native_type(self, native_obj: object) -> FlextResult[bool]:
        """Validate that native object is compatible with this adapter."""
        ...

    @abstractmethod
    def wrap_native_type(self, native_obj: object) -> FlextResult[T]:
        """Wrap native type into Flext* equivalent with error handling."""
        ...

    @abstractmethod
    def unwrap_to_native(self, flext_obj: T) -> FlextResult[object]:
        """Convert Flext* type back to native type."""
        ...


@runtime_checkable
class FlextStreamAdapter(Protocol):
    """Protocol for Singer stream adapters with FlextResult integration."""

    def get_schema(self) -> FlextResult[dict[str, object]]:
        """Get stream schema with type safety."""
        ...

    def get_records(self) -> FlextResult[list[dict[str, object]]]:
        """Get stream records with error handling."""
        ...


# =============================================================================
# FLEXT ABSTRACT BASE CLASSES - Complete abstractions for TAP/TARGET/DBT
# =============================================================================


@runtime_checkable
class FlextStream(Protocol):
    """Protocol for FlextStream implementations."""

    def get_name(self) -> str:
        """Get stream name."""
        ...

    def get_schema(self) -> FlextResult[dict[str, object]]:
        """Get stream schema."""
        ...

    def get_records(
        self, config: dict[str, object] | None = None
    ) -> FlextResult[list[dict[str, object]]]:
        """Get stream records."""
        ...


@runtime_checkable
class FlextTapBase(Protocol):
    """Protocol for FlextTap implementations."""

    def discover_streams(self) -> FlextResult[list[FlextStream]]:
        """Discover available streams."""
        ...

    def get_stream_by_name(self, name: str) -> FlextResult[FlextStream]:
        """Get specific stream by name."""
        ...

    def sync_stream(
        self, stream_name: str, config: dict[str, object] | None = None
    ) -> FlextResult[dict[str, object]]:
        """Sync specific stream data."""
        ...


# =============================================================================
# FLEXT WRAPPED TYPES - Modern abstractions with FlextResult integration
# =============================================================================


class FlextTap:
    """Modern Flext* wrapper for Singer SDK Tap with FlextResult error handling.

    Provides enterprise-grade tap functionality with:
    - FlextResult railway-oriented programming for all operations
    - Type-safe stream discovery and extraction
    - Comprehensive error handling and logging
    - Integration with flext-core patterns
    """

    def __init__(
        self, native_tap: SingerTap, adapter: FlextMeltanoTypeAdapters
    ) -> None:
        """Initialize FlextTap wrapper.

        Args:
            native_tap: Native Singer SDK tap instance
            adapter: Parent type adapter for context

        """
        self._native_tap = native_tap
        self._adapter = adapter
        self._logger = FlextLogger(f"{__name__}.FlextTap")

    def discover_streams(self) -> FlextResult[list[FlextSingerStream]]:
        """Discover available streams with type safety and error handling.

        Returns:
            FlextResult containing list of FlextSingerStream objects or error

        """
        try:
            tap_name = getattr(self._native_tap, "tap_type", "unknown-tap")
            self._logger.debug("Discovering streams from tap", tap_name=tap_name)

            # Use native tap discovery
            native_streams = self._native_tap.discover_streams()

            # Wrap each stream in FlextSingerStream
            flext_streams: list[FlextSingerStream] = []
            for native_stream in native_streams:
                stream_result = self._adapter.wrap_singer_stream(native_stream)
                if stream_result.failure:
                    return FlextResult[list[FlextSingerStream]].fail(
                        f"Failed to wrap stream {native_stream.name}: {stream_result.error}"
                    )
                flext_streams.append(stream_result.value)

            self._logger.info(
                "Successfully discovered streams",
                tap_name=tap_name,
                stream_count=len(flext_streams),
            )

            return FlextResult[list[FlextSingerStream]].ok(flext_streams)

        except Exception as e:
            tap_name = getattr(self._native_tap, "tap_type", "unknown-tap")
            error_msg = f"Stream discovery failed for tap {tap_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[list[FlextSingerStream]].fail(error_msg)

    def get_native_tap(self) -> SingerTap:
        """Get underlying native Singer tap."""
        return self._native_tap

    def validate_config(self) -> FlextResult[dict[str, object]]:
        """Validate tap configuration with enterprise error handling.

        Returns:
            FlextResult containing validated config dict or error

        """
        try:
            # Use tap's built-in config validation if available
            config = self._native_tap.config

            if not config:
                tap_name = getattr(self._native_tap, "tap_type", "unknown-tap")
                return FlextResult[dict[str, object]].fail(
                    f"No configuration found for tap {tap_name}"
                )

            tap_name = getattr(self._native_tap, "tap_type", "unknown-tap")
            self._logger.debug("Tap configuration validated", tap_name=tap_name)
            return FlextResult[dict[str, object]].ok(dict(config))

        except Exception as e:
            tap_name = getattr(self._native_tap, "tap_type", "unknown-tap")
            error_msg = f"Configuration validation failed for tap {tap_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)


class FlextTarget:
    """Modern Flext* wrapper for Singer SDK Target with FlextResult error handling."""

    def __init__(
        self, native_target: SingerTarget, adapter: FlextMeltanoTypeAdapters
    ) -> None:
        """Initialize FlextTarget wrapper."""
        self._native_target = native_target
        self._adapter = adapter
        self._logger = FlextLogger(f"{__name__}.FlextTarget")

    def get_native_target(self) -> SingerTarget:
        """Get underlying native Singer target."""
        return self._native_target

    def validate_config(self) -> FlextResult[dict[str, object]]:
        """Validate target configuration with enterprise error handling."""
        try:
            config = self._native_target.config

            if not config:
                return FlextResult[dict[str, object]].fail(
                    f"No configuration found for target {self._native_target.name}"
                )

            return FlextResult[dict[str, object]].ok(dict(config))

        except Exception as e:
            error_msg = f"Configuration validation failed for target {self._native_target.name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)


class FlextSingerStream:
    """Modern Flext* wrapper for Singer SDK Stream with FlextResult error handling."""

    def __init__(
        self, native_stream: SingerStream, adapter: FlextMeltanoTypeAdapters
    ) -> None:
        """Initialize FlextSingerStream wrapper."""
        self._native_stream = native_stream
        self._adapter = adapter
        self._logger = FlextLogger(f"{__name__}.FlextSingerStream")

    def get_schema(self) -> FlextResult[dict[str, object]]:
        """Get stream schema with type safety."""
        try:
            schema = self._native_stream.schema

            if not schema:
                return FlextResult[dict[str, object]].fail(
                    f"No schema found for stream {self._native_stream.name}"
                )

            # Convert schema to dict if it's not already
            if hasattr(schema, "to_dict") and callable(getattr(schema, "to_dict")):
                schema_dict = schema.to_dict()
            else:
                schema_dict = dict(schema) if schema else {}

            return FlextResult[dict[str, object]].ok(schema_dict)

        except Exception as e:
            error_msg = (
                f"Failed to get schema for stream {self._native_stream.name}: {e}"
            )
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)

    def get_native_stream(self) -> SingerStream:
        """Get underlying native Singer stream."""
        return self._native_stream

    @property
    def name(self) -> str:
        """Get stream name."""
        return self._native_stream.name


class FlextMeltanoProject:
    """Modern Flext* wrapper for Meltano Project with FlextResult error handling."""

    def __init__(
        self, native_project: MeltanoProject, adapter: FlextMeltanoTypeAdapters
    ) -> None:
        """Initialize FlextMeltanoProject wrapper."""
        self._native_project = native_project
        self._adapter = adapter
        self._logger = FlextLogger(f"{__name__}.FlextMeltanoProject")

    def list_plugins(self) -> FlextResult[list[dict[str, object]]]:
        """List project plugins with error handling."""
        try:
            plugins: list[dict[str, object]] = []
            # Use the plugins() method which returns a generator
            for plugin in self._native_project.plugins.plugins():
                plugin_info: dict[str, object] = {
                    "name": plugin.name,
                    "type": plugin.type.value
                    if hasattr(plugin.type, "value")
                    else str(plugin.type),
                    "namespace": plugin.namespace,
                }
                plugins.append(plugin_info)

            return FlextResult[list[dict[str, object]]].ok(plugins)

        except Exception as e:
            error_msg = (
                f"Failed to list plugins for project {self._native_project.root}: {e}"
            )
            self._logger.exception(error_msg)
            return FlextResult[list[dict[str, object]]].fail(error_msg)

    def get_native_project(self) -> MeltanoProject:
        """Get underlying native Meltano project."""
        return self._native_project

    @property
    def root_path(self) -> Path:
        """Get project root path."""
        return self._native_project.root


class FlextDbt:
    """Modern Flext* wrapper for dBT Core with FlextResult error handling.

    Provides enterprise-grade dBT functionality with:
    - FlextResult railway-oriented programming for all operations
    - Type-safe model execution and testing
    - Comprehensive error handling and logging
    - Integration with flext-core patterns
    """

    def __init__(
        self, project_path: Path | str, adapter: FlextMeltanoTypeAdapters
    ) -> None:
        """Initialize FlextDbt wrapper.

        Args:
            project_path: Path to dBT project directory
            adapter: Parent type adapter for context

        """
        self._project_path = (
            Path(project_path) if isinstance(project_path, str) else project_path
        )
        self._adapter = adapter
        self._logger = FlextLogger(f"{__name__}.FlextDbt")

    def run_models(
        self, model_names: list[str] | None = None
    ) -> FlextResult[dict[str, object]]:
        """Run dBT models with error handling.

        Args:
            model_names: Optional list of specific models to run

        Returns:
            FlextResult containing execution results or error

        """
        try:
            self._logger.info(
                "Starting dBT model execution", project_path=str(self._project_path)
            )

            # Prepare dBT command arguments
            args = ["run"]
            if model_names:
                args.extend(["--models", " ".join(model_names)])

            # Execute using dBT runner with correct instantiation
            dbt = dbtRunner()
            result = dbt.invoke(args)

            if result.success:
                execution_result: dict[str, object] = {
                    "status": "success",
                    "models_executed": model_names or "all",
                    "project_path": str(self._project_path),
                }
                return FlextResult[dict[str, object]].ok(execution_result)
            return FlextResult[dict[str, object]].fail(
                f"dBT execution failed: {result.exception if hasattr(result, 'exception') else 'Unknown error'}"
            )

        except Exception as e:
            error_msg = f"Failed to run dBT models: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)

    def test_models(self) -> FlextResult[dict[str, object]]:
        """Run dBT tests with error handling."""
        try:
            self._logger.info(
                "Starting dBT test execution", project_path=str(self._project_path)
            )

            # Execute dBT test with correct instantiation
            dbt = dbtRunner()
            result = dbt.invoke(["test"])

            if result.success:
                test_result: dict[str, object] = {
                    "status": "success",
                    "project_path": str(self._project_path),
                }
                return FlextResult[dict[str, object]].ok(test_result)
            return FlextResult[dict[str, object]].fail(
                f"dBT tests failed: {result.exception if hasattr(result, 'exception') else 'Unknown error'}"
            )

        except Exception as e:
            error_msg = f"Failed to run dBT tests: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)

    @property
    def project_path(self) -> Path:
        """Get dBT project path."""
        return self._project_path

    def validate_project(self) -> FlextResult[dict[str, object]]:
        """Validate dBT project configuration."""
        try:
            # Check if dbt_project.yml exists
            dbt_project_file = self._project_path / "dbt_project.yml"

            if not dbt_project_file.exists():
                return FlextResult[dict[str, object]].fail(
                    f"dbt_project.yml not found in {self._project_path}"
                )

            validation_result: dict[str, object] = {
                "status": "valid",
                "project_file": str(dbt_project_file),
                "project_path": str(self._project_path),
            }

            return FlextResult[dict[str, object]].ok(validation_result)

        except Exception as e:
            error_msg = f"Failed to validate dBT project: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)


# =============================================================================
# MAIN TYPE ADAPTERS CLASS - Following flext-core single class pattern
# =============================================================================


class FlextMeltanoTypeAdapters:
    """Main type adapters class for Meltano/Singer/dBT type transformations.

    Following flext-core single class architecture, this class provides all type
    adaptation functionality for converting native Meltano, Singer SDK, and dBT
    types to modern Flext* equivalents with FlextResult error handling.

    Features:
        - Comprehensive type validation and conversion
        - FlextResult railway-oriented programming throughout
        - Enterprise error handling and logging
        - Type-safe transformations with generic patterns
        - Zero duplication following flext-core patterns
    """

    def __init__(self) -> None:
        """Initialize FlextMeltanoTypeAdapters with flext-core patterns."""
        self._logger = FlextLogger(f"{__name__}.FlextMeltanoTypeAdapters")
        self._logger.info("FlextMeltanoTypeAdapters initialized")

    def wrap_singer_tap(self, native_tap: SingerTap) -> FlextResult[FlextTap]:
        """Wrap native Singer tap in FlextTap with validation.

        Args:
            native_tap: Native Singer SDK tap instance

        Returns:
            FlextResult containing FlextTap or error

        """
        try:
            # Type annotations guarantee SingerTap type - no runtime check needed in strict mode
            flext_tap = FlextTap(native_tap, self)
            self._logger.debug(
                "Successfully wrapped Singer tap", tap_name=native_tap.name
            )

            return FlextResult[FlextTap].ok(flext_tap)

        except Exception as e:
            error_msg = f"Failed to wrap Singer tap: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTap].fail(error_msg)

    def wrap_singer_target(
        self, native_target: SingerTarget
    ) -> FlextResult[FlextTarget]:
        """Wrap native Singer target in FlextTarget with validation.

        Args:
            native_target: Native Singer SDK target instance

        Returns:
            FlextResult containing FlextTarget or error

        """
        try:
            # Type annotations guarantee SingerTarget type - no runtime check needed in strict mode
            flext_target = FlextTarget(native_target, self)
            self._logger.debug(
                "Successfully wrapped Singer target", target_name=native_target.name
            )

            return FlextResult[FlextTarget].ok(flext_target)

        except Exception as e:
            error_msg = f"Failed to wrap Singer target: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTarget].fail(error_msg)

    def wrap_singer_stream(
        self, native_stream: SingerStream
    ) -> FlextResult[FlextSingerStream]:
        """Wrap native Singer stream in FlextSingerStream with validation.

        Args:
            native_stream: Native Singer SDK stream instance

        Returns:
            FlextResult containing FlextSingerStream or error

        """
        try:
            # Type annotations guarantee SingerStream type - no runtime check needed in strict mode
            flext_stream = FlextSingerStream(native_stream, self)
            self._logger.debug(
                "Successfully wrapped Singer stream", stream_name=native_stream.name
            )

            return FlextResult[FlextSingerStream].ok(flext_stream)

        except Exception as e:
            error_msg = f"Failed to wrap Singer stream: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextSingerStream].fail(error_msg)

    def wrap_meltano_project(
        self, native_project: MeltanoProject
    ) -> FlextResult[FlextMeltanoProject]:
        """Wrap native Meltano project in FlextMeltanoProject with validation.

        Args:
            native_project: Native Meltano project instance

        Returns:
            FlextResult containing FlextMeltanoProject or error

        """
        try:
            # Type annotations guarantee MeltanoProject type - no runtime check needed in strict mode
            flext_project = FlextMeltanoProject(native_project, self)
            self._logger.debug(
                "Successfully wrapped Meltano project",
                project_root=str(native_project.root),
            )

            return FlextResult[FlextMeltanoProject].ok(flext_project)

        except Exception as e:
            error_msg = f"Failed to wrap Meltano project: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextMeltanoProject].fail(error_msg)

    def create_flext_dbt(self, project_path: Path | str) -> FlextResult[FlextDbt]:
        """Create FlextDbt wrapper from project path with validation.

        Args:
            project_path: Path to dBT project directory

        Returns:
            FlextResult containing FlextDbt or error

        """
        try:
            path_obj = (
                Path(project_path) if isinstance(project_path, str) else project_path
            )

            if not path_obj.exists():
                return FlextResult[FlextDbt].fail(
                    f"dBT project path does not exist: {project_path}"
                )

            if not path_obj.is_dir():
                return FlextResult[FlextDbt].fail(
                    f"dBT project path is not a directory: {project_path}"
                )

            flext_dbt = FlextDbt(path_obj, self)

            # Validate the project
            validation_result = flext_dbt.validate_project()
            if validation_result.failure:
                return FlextResult[FlextDbt].fail(
                    f"Invalid dBT project: {validation_result.error}"
                )

            self._logger.debug(
                "Successfully created FlextDbt", project_path=str(path_obj)
            )
            return FlextResult[FlextDbt].ok(flext_dbt)

        except Exception as e:
            error_msg = f"Failed to create FlextDbt: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextDbt].fail(error_msg)

    def create_flext_tap_from_config(
        self, _tap_config: dict[str, object]
    ) -> FlextResult[FlextTap]:
        """Create FlextTap from configuration dict with validation.

        Args:
            _tap_config: Configuration dictionary for tap creation (unused in placeholder)

        Returns:
            FlextResult containing FlextTap or error

        """
        try:
            # Type annotations guarantee dict type - no runtime check needed in strict mode
            # This would need to be implemented based on specific tap requirements
            # For now, return an error indicating this needs implementation
            return FlextResult[FlextTap].fail(
                "create_flext_tap_from_config not yet implemented - requires tap factory"
            )

        except Exception as e:
            error_msg = f"Failed to create FlextTap from config: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTap].fail(error_msg)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "FlextDbt",
    "FlextMeltanoProject",
    # Main adapter class
    "FlextMeltanoTypeAdapters",
    "FlextSingerStream",
    "FlextStreamAdapter",
    # Flext* wrapped types
    "FlextTap",
    "FlextTarget",
    # Protocols
    "FlextTypeAdapter",
]
