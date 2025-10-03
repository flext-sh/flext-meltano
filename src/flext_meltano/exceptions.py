"""FLEXT Meltano Exceptions - Complete Meltano/Singer/DBT Error Handling.

This module implements comprehensive exception handling for the FLEXT Meltano data integration,
ELT pipeline orchestration, Singer protocol operations, and DBT transformations. Extends
flext-core exception foundation with domain-specific error types for production ELT needs.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import FlextExceptions


class FlextMeltanoExceptions(FlextExceptions):
    """Single CONSOLIDATED class containing ALL Meltano/Singer/DBT exceptions."""

    class MeltanoErrorCodes(Enum):
        """Error codes for Meltano domain operations."""

        MELTANO_ERROR = "MELTANO_ERROR"
        MELTANO_PROJECT_ERROR = "MELTANO_PROJECT_ERROR"
        PLUGIN_ERROR = "PLUGIN_ERROR"
        PLUGIN_INSTALLATION_ERROR = "PLUGIN_INSTALLATION_ERROR"
        PLUGIN_EXECUTION_ERROR = "PLUGIN_EXECUTION_ERROR"
        SINGER_PROTOCOL_ERROR = "SINGER_PROTOCOL_ERROR"
        SINGER_CATALOG_ERROR = "SINGER_CATALOG_ERROR"
        SINGER_STREAM_ERROR = "SINGER_STREAM_ERROR"
        DBT_EXECUTION_ERROR = "DBT_EXECUTION_ERROR"
        DBT_COMPILATION_ERROR = "DBT_COMPILATION_ERROR"
        DBT_MODEL_ERROR = "DBT_MODEL_ERROR"
        PIPELINE_ERROR = "PIPELINE_ERROR"
        PIPELINE_EXECUTION_ERROR = "PIPELINE_EXECUTION_ERROR"
        CATALOG_DISCOVERY_ERROR = "CATALOG_DISCOVERY_ERROR"
        STREAM_VALIDATION_ERROR = "STREAM_VALIDATION_ERROR"
        CONFIG_BUILDER_ERROR = "CONFIG_BUILDER_ERROR"

    # Base Meltano exception classes as nested classes
    class MeltanoBaseError(FlextExceptions.BaseError):
        """Base exception for all Meltano domain errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            meltano_component: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Meltano error with context using helpers.

            Args:
                message: Error message
                meltano_component: Meltano component that caused the error
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store component before extracting common kwargs
            self.meltano_component = meltano_component

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with Meltano-specific fields
            context = self._build_context(
                base_context,
                meltano_component=meltano_component,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "MELTANO_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MeltanoProjectError(MeltanoBaseError):
        """Meltano project configuration or initialization errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            project_path: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Meltano project error using helpers.

            Args:
                message: Error message
                project_path: Path to the Meltano project
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store project attributes before extracting common kwargs
            self.project_path = project_path

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with project-specific fields
            context = self._build_context(
                base_context,
                project_path=project_path,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="project",
                code=error_code or "MELTANO_PROJECT_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PluginError(MeltanoBaseError):
        """Meltano plugin installation or execution errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_name: str | None = None,
            plugin_type: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize plugin error using helpers.

            Args:
                message: Error message
                plugin_name: Name of the plugin
                plugin_type: Type of the plugin (tap, target, utility, etc.)
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store plugin attributes before extracting common kwargs
            self.plugin_name = plugin_name
            self.plugin_type = plugin_type

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with plugin fields
            context = self._build_context(
                base_context,
                plugin_name=plugin_name,
                plugin_type=plugin_type,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="plugin",
                code=error_code or "PLUGIN_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PluginInstallationError(PluginError):
        """Plugin installation specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize plugin installation error using helpers.

            Args:
                message: Error message
                plugin_name: Name of the plugin being installed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with installation fields
            context = self._build_context(
                base_context,
                plugin_name=plugin_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_name=plugin_name,
                code=error_code or "PLUGIN_INSTALLATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PluginExecutionError(PluginError):
        """Plugin execution specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_name: str | None = None,
            exit_code: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize plugin execution error using helpers.

            Args:
                message: Error message
                plugin_name: Name of the plugin being executed
                exit_code: Exit code from plugin execution
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store execution attributes before extracting common kwargs
            self.exit_code = exit_code

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with execution fields
            context = self._build_context(
                base_context,
                plugin_name=plugin_name,
                exit_code=exit_code,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_name=plugin_name,
                code=error_code or "PLUGIN_EXECUTION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class SingerProtocolError(MeltanoBaseError):
        """Singer tap/target protocol compliance errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            singer_component: str | None = None,
            protocol_version: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Singer protocol error using helpers.

            Args:
                message: Error message
                singer_component: Singer component (tap, target)
                protocol_version: Singer protocol version
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store Singer attributes before extracting common kwargs
            self.singer_component = singer_component
            self.protocol_version = protocol_version

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with Singer protocol fields
            context = self._build_context(
                base_context,
                singer_component=singer_component,
                protocol_version=protocol_version,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="singer",
                code=error_code or "SINGER_PROTOCOL_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class SingerCatalogError(SingerProtocolError):
        """Singer catalog discovery errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            tap_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Singer catalog error using helpers.

            Args:
                message: Error message
                tap_name: Name of the tap for catalog discovery
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store tap attributes before extracting common kwargs
            self.tap_name = tap_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with catalog fields
            context = self._build_context(
                base_context,
                tap_name=tap_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                singer_component="catalog",
                code=error_code or "SINGER_CATALOG_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class SingerStreamError(SingerProtocolError):
        """Singer stream validation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            stream_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Singer stream error using helpers.

            Args:
                message: Error message
                stream_name: Name of the Singer stream
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store stream attributes before extracting common kwargs
            self.stream_name = stream_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with stream fields
            context = self._build_context(
                base_context,
                stream_name=stream_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                singer_component="stream",
                code=error_code or "SINGER_STREAM_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class DbtExecutionError(MeltanoBaseError):
        """DBT model execution or compilation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            dbt_command: str | None = None,
            model_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize DBT execution error using helpers.

            Args:
                message: Error message
                dbt_command: DBT command being executed
                model_name: Name of the DBT model
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store DBT attributes before extracting common kwargs
            self.dbt_command = dbt_command
            self.model_name = model_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with DBT fields
            context = self._build_context(
                base_context,
                dbt_command=dbt_command,
                model_name=model_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="dbt",
                code=error_code or "DBT_EXECUTION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class DbtCompilationError(DbtExecutionError):
        """DBT model compilation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            model_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize DBT compilation error using helpers.

            Args:
                message: Error message
                model_name: Name of the model being compiled
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with compilation fields
            context = self._build_context(
                base_context,
                model_name=model_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                dbt_command="compile",
                model_name=model_name,
                code=error_code or "DBT_COMPILATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class DbtModelError(DbtExecutionError):
        """DBT model specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            model_name: str | None = None,
            test_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize DBT model error using helpers.

            Args:
                message: Error message
                model_name: Name of the DBT model
                test_name: Name of the test that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store test attributes before extracting common kwargs
            self.test_name = test_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with model fields
            context = self._build_context(
                base_context,
                model_name=model_name,
                test_name=test_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                dbt_command="test",
                model_name=model_name,
                code=error_code or "DBT_MODEL_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PipelineError(MeltanoBaseError):
        """ELT pipeline execution errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            pipeline_name: str | None = None,
            pipeline_stage: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize pipeline error using helpers.

            Args:
                message: Error message
                pipeline_name: Name of the pipeline
                pipeline_stage: Stage of the pipeline (extract, load, transform)
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store pipeline attributes before extracting common kwargs
            self.pipeline_name = pipeline_name
            self.pipeline_stage = pipeline_stage

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with pipeline fields
            context = self._build_context(
                base_context,
                pipeline_name=pipeline_name,
                pipeline_stage=pipeline_stage,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="pipeline",
                code=error_code or "PIPELINE_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PipelineExecutionError(PipelineError):
        """Pipeline execution specific errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            pipeline_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize pipeline execution error using helpers.

            Args:
                message: Error message
                pipeline_name: Name of the pipeline being executed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with execution fields
            context = self._build_context(
                base_context,
                pipeline_name=pipeline_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                pipeline_name=pipeline_name,
                code=error_code or "PIPELINE_EXECUTION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class CatalogDiscoveryError(MeltanoBaseError):
        """Singer catalog discovery errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            tap_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize catalog discovery error using helpers.

            Args:
                message: Error message
                tap_name: Name of the tap for catalog discovery
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store tap attributes before extracting common kwargs
            self.tap_name = tap_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with catalog discovery fields
            context = self._build_context(
                base_context,
                tap_name=tap_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="catalog",
                code=error_code or "CATALOG_DISCOVERY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class StreamValidationError(MeltanoBaseError):
        """Singer stream validation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            stream_name: str | None = None,
            validation_rule: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize stream validation error using helpers.

            Args:
                message: Error message
                stream_name: Name of the stream being validated
                validation_rule: Validation rule that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store stream validation attributes before extracting common kwargs
            self.stream_name = stream_name
            self.validation_rule = validation_rule

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with stream validation fields
            context = self._build_context(
                base_context,
                stream_name=stream_name,
                validation_rule=validation_rule,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="stream_validation",
                code=error_code or "STREAM_VALIDATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ConfigBuilderError(MeltanoBaseError):
        """Meltano configuration builder errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            config_type: str | None = None,
            config_key: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize config builder error using helpers.

            Args:
                message: Error message
                config_type: Type of configuration being built
                config_key: Configuration key that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store config builder attributes before extracting common kwargs
            self.config_type = config_type
            self.config_key = config_key

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with config builder fields
            context = self._build_context(
                base_context,
                config_type=config_type,
                config_key=config_key,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                meltano_component="config_builder",
                code=error_code or "CONFIG_BUILDER_ERROR",
                context=context,
                correlation_id=correlation_id,
            )


# Backward compatibility aliases - property-based exports
FlextMeltanoError = FlextMeltanoExceptions.MeltanoBaseError
FlextMeltanoErrorCodes = FlextMeltanoExceptions.MeltanoErrorCodes
FlextMeltanoProjectError = FlextMeltanoExceptions.MeltanoProjectError
FlextPluginError = FlextMeltanoExceptions.PluginError
FlextPluginInstallationError = FlextMeltanoExceptions.PluginInstallationError
FlextPluginExecutionError = FlextMeltanoExceptions.PluginExecutionError
FlextSingerProtocolError = FlextMeltanoExceptions.SingerProtocolError
FlextSingerCatalogError = FlextMeltanoExceptions.SingerCatalogError
FlextSingerStreamError = FlextMeltanoExceptions.SingerStreamError
FlextDbtExecutionError = FlextMeltanoExceptions.DbtExecutionError
FlextDbtCompilationError = FlextMeltanoExceptions.DbtCompilationError
FlextDbtModelError = FlextMeltanoExceptions.DbtModelError
FlextPipelineError = FlextMeltanoExceptions.PipelineError
FlextPipelineExecutionError = FlextMeltanoExceptions.PipelineExecutionError
FlextCatalogDiscoveryError = FlextMeltanoExceptions.CatalogDiscoveryError
FlextStreamValidationError = FlextMeltanoExceptions.StreamValidationError
FlextConfigBuilderError = FlextMeltanoExceptions.ConfigBuilderError

__all__ = [
    "FlextCatalogDiscoveryError",
    "FlextConfigBuilderError",
    "FlextDbtCompilationError",
    "FlextDbtExecutionError",
    "FlextDbtModelError",
    "FlextMeltanoError",
    "FlextMeltanoErrorCodes",
    "FlextMeltanoExceptions",
    "FlextMeltanoProjectError",
    "FlextPipelineError",
    "FlextPipelineExecutionError",
    "FlextPluginError",
    "FlextPluginExecutionError",
    "FlextPluginInstallationError",
    "FlextSingerCatalogError",
    "FlextSingerProtocolError",
    "FlextSingerStreamError",
    "FlextStreamValidationError",
]
