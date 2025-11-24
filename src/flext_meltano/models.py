"""FLEXT Generic Pipeline Models - Generic Pydantic models for data pipeline operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

This module provides generic, reusable models for data pipeline operations.
All models are designed to be domain-agnostic and follow SOLID principles.

Each class has a single responsibility and follows the Open/Closed Principle.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from flext_core import FlextConstants, FlextModels
from pydantic import (
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)


class FlextMeltanoModels(FlextModels):
    """Generic pipeline models following SOLID principles.

    Each inner class has a single responsibility and can be used independently.
    All models are domain-agnostic and reusable across different pipeline types.
    """

    # Constants for magic values used throughout the models
    PROJECT_MATURITY_MATURE_ENV_COUNT: int = 3
    PROJECT_MATURITY_DEVELOPING_ENV_COUNT: int = 2
    PLUGIN_COMPLEXITY_SIMPLE_MAX_SETTINGS: int = 5
    PLUGIN_COMPLEXITY_MODERATE_MAX_SETTINGS: int = 15
    TRANSFORMATION_SIMPLE_MAX_PATHS: int = 5
    TRANSFORMATION_MODERATE_MAX_PATHS: int = 10
    EXECUTION_SIMPLE_THRESHOLD: int = 10
    EXECUTION_MODERATE_THRESHOLD: int = 50
    PERFORMANCE_HIGH_THRESHOLD: int = 1000
    PERFORMANCE_GOOD_THRESHOLD: int = 500
    PERFORMANCE_MODERATE_THRESHOLD: int = 100

    # ========================================================================
    # LOGGING CONFIGURATION - Consolidated logging settings
    # ========================================================================

    class LoggingConfig(FlextModels):
        """Consolidated logging configuration for all pipeline operations.

        Organizes 62+ logging boolean fields into coherent categories:
        - Pipeline operations logging
        - Extract/source operations logging
        - Load/sink operations logging
        - Transform/DBT operations logging
        - Orchestration and monitoring logging
        - Debugging and performance logging

        Single responsibility: manage logging configuration across all domains.
        """

        # Pipeline Operations Logging (9 fields)
        pipeline_execution: bool = Field(
            default=True, description="Log pipeline execution details"
        )
        pipeline_stages: bool = Field(
            default=True, description="Log pipeline stage transitions"
        )
        pipeline_progress: bool = Field(
            default=True, description="Log pipeline progress updates"
        )
        pipeline_errors: bool = Field(
            default=True, description="Log pipeline errors and failures"
        )
        pipeline_warnings: bool = Field(
            default=True, description="Log pipeline warnings"
        )
        pipeline_performance: bool = Field(
            default=True, description="Log pipeline performance metrics"
        )
        pipeline_timing: bool = Field(
            default=True, description="Log pipeline timing information"
        )
        pipeline_memory: bool = Field(
            default=True, description="Log pipeline memory usage"
        )
        pipeline_throughput: bool = Field(
            default=True, description="Log pipeline throughput metrics"
        )

        # Extract/Source Operations Logging (8 fields)
        extract_operations: bool = Field(
            default=True, description="Log extract operations"
        )
        extract_queries: bool = Field(default=True, description="Log extract queries")
        extract_results: bool = Field(default=True, description="Log extract results")
        extract_errors: bool = Field(default=True, description="Log extract errors")
        extract_performance: bool = Field(
            default=True, description="Log extract performance metrics"
        )
        extract_timing: bool = Field(
            default=True, description="Log extract timing information"
        )
        extract_memory: bool = Field(
            default=True, description="Log extract memory usage"
        )
        extract_throughput: bool = Field(
            default=True, description="Log extract throughput metrics"
        )

        # Load/Sink Operations Logging (8 fields)
        load_operations: bool = Field(default=True, description="Log load operations")
        load_batches: bool = Field(default=True, description="Log load batches")
        load_results: bool = Field(default=True, description="Log load results")
        load_errors: bool = Field(default=True, description="Log load errors")
        load_performance: bool = Field(
            default=True, description="Log load performance metrics"
        )
        load_timing: bool = Field(
            default=True, description="Log load timing information"
        )
        load_memory: bool = Field(default=True, description="Log load memory usage")
        load_throughput: bool = Field(
            default=True, description="Log load throughput metrics"
        )

        # Transform/DBT Operations Logging (8 fields)
        transform_operations: bool = Field(
            default=True, description="Log transform operations"
        )
        transform_sql: bool = Field(
            default=True, description="Log transform SQL queries"
        )
        transform_results: bool = Field(
            default=True, description="Log transform results"
        )
        transform_errors: bool = Field(default=True, description="Log transform errors")
        transform_performance: bool = Field(
            default=True, description="Log transform performance metrics"
        )
        transform_timing: bool = Field(
            default=True, description="Log transform timing information"
        )
        transform_memory: bool = Field(
            default=True, description="Log transform memory usage"
        )
        transform_lineage: bool = Field(
            default=True, description="Log transform lineage tracking"
        )

        # DBT Specific Logging (6 fields)
        dbt_parse: bool = Field(default=True, description="Log DBT parsing operations")
        dbt_compile: bool = Field(default=True, description="Log DBT compilation")
        dbt_execute: bool = Field(default=True, description="Log DBT execution")
        dbt_test: bool = Field(default=True, description="Log DBT test operations")
        dbt_snapshot: bool = Field(
            default=True, description="Log DBT snapshot operations"
        )
        dbt_docs: bool = Field(
            default=True, description="Log DBT documentation generation"
        )

        # Data Quality Logging (8 fields)
        data_quality: bool = Field(default=True, description="Log data quality checks")
        data_quality_checks: bool = Field(
            default=True, description="Log data quality check results"
        )
        data_quality_errors: bool = Field(
            default=True, description="Log data quality errors"
        )
        data_quality_warnings: bool = Field(
            default=True, description="Log data quality warnings"
        )
        data_quality_metrics: bool = Field(
            default=True, description="Log data quality metrics"
        )
        data_quality_timing: bool = Field(
            default=True, description="Log data quality timing information"
        )
        data_quality_memory: bool = Field(
            default=True, description="Log data quality memory usage"
        )
        data_quality_throughput: bool = Field(
            default=True, description="Log data quality throughput metrics"
        )

        # Plugin Logging (6 fields)
        plugin_operations: bool = Field(
            default=True, description="Log plugin operations"
        )
        plugin_errors: bool = Field(default=True, description="Log plugin errors")
        plugin_performance: bool = Field(
            default=True, description="Log plugin performance metrics"
        )
        plugin_timing: bool = Field(
            default=True, description="Log plugin timing information"
        )
        plugin_memory: bool = Field(default=True, description="Log plugin memory usage")
        plugin_throughput: bool = Field(
            default=True, description="Log plugin throughput metrics"
        )

        # Source and Target Logging (14 fields)
        source_info: bool = Field(default=True, description="Log source information")
        target_info: bool = Field(default=True, description="Log target information")
        source_errors: bool = Field(default=True, description="Log source errors")
        target_errors: bool = Field(default=True, description="Log target errors")
        source_performance: bool = Field(
            default=True, description="Log source performance metrics"
        )
        target_performance: bool = Field(
            default=True, description="Log target performance metrics"
        )
        source_timing: bool = Field(
            default=True, description="Log source timing information"
        )
        target_timing: bool = Field(
            default=True, description="Log target timing information"
        )
        source_memory: bool = Field(default=True, description="Log source memory usage")
        target_memory: bool = Field(default=True, description="Log target memory usage")
        source_throughput: bool = Field(
            default=True, description="Log source throughput metrics"
        )
        target_throughput: bool = Field(
            default=True, description="Log target throughput metrics"
        )

        # Meltano Performance Tracking (1 field)
        track_meltano_performance: bool = Field(
            default=True, description="Track Meltano performance metrics"
        )

        # Orchestration Logging (5 fields)
        orchestration_scheduling: bool = Field(
            default=True, description="Log orchestration scheduling events"
        )
        orchestration_execution: bool = Field(
            default=True, description="Log orchestration execution"
        )
        orchestration_state: bool = Field(
            default=True, description="Log orchestration state changes"
        )
        orchestration_hooks: bool = Field(
            default=True, description="Log orchestration hook execution"
        )
        orchestration_dependencies: bool = Field(
            default=True, description="Log dependency resolution"
        )

        # Monitoring and Observability Logging (5 fields)
        monitoring_metrics: bool = Field(
            default=True, description="Log collected metrics"
        )
        monitoring_alerts: bool = Field(
            default=True, description="Log alert generation"
        )
        monitoring_health: bool = Field(default=True, description="Log health checks")
        monitoring_traces: bool = Field(
            default=True, description="Log distributed traces"
        )
        monitoring_events: bool = Field(
            default=True, description="Log observability events"
        )

        # Debugging and Diagnostics Logging (5 fields)
        debug_verbose: bool = Field(
            default=False, description="Enable verbose debug logging"
        )
        debug_trace_calls: bool = Field(
            default=False, description="Log function call traces"
        )
        debug_variable_state: bool = Field(
            default=False, description="Log variable state changes"
        )
        debug_configuration: bool = Field(
            default=False, description="Log configuration details"
        )
        debug_performance_profile: bool = Field(
            default=False, description="Log performance profiling data"
        )

        @computed_field
        def pipeline_dict(self) -> dict[str, bool]:
            """Pipeline logging as dictionary."""
            return {
                "execution": self.pipeline_execution,
                "stages": self.pipeline_stages,
                "progress": self.pipeline_progress,
                "errors": self.pipeline_errors,
                "warnings": self.pipeline_warnings,
                "performance": self.pipeline_performance,
                "timing": self.pipeline_timing,
                "memory": self.pipeline_memory,
                "throughput": self.pipeline_throughput,
            }

        @computed_field
        def extract_dict(self) -> dict[str, bool]:
            """Extract logging as dictionary."""
            return {
                "operations": self.extract_operations,
                "queries": self.extract_queries,
                "results": self.extract_results,
                "errors": self.extract_errors,
                "performance": self.extract_performance,
                "timing": self.extract_timing,
                "memory": self.extract_memory,
                "throughput": self.extract_throughput,
            }

        @computed_field
        def load_dict(self) -> dict[str, bool]:
            """Load logging as dictionary."""
            return {
                "operations": self.load_operations,
                "batches": self.load_batches,
                "results": self.load_results,
                "errors": self.load_errors,
                "performance": self.load_performance,
                "timing": self.load_timing,
                "memory": self.load_memory,
                "throughput": self.load_throughput,
            }

        @computed_field
        def transform_dict(self) -> dict[str, bool]:
            """Transform logging as dictionary."""
            return {
                "operations": self.transform_operations,
                "sql": self.transform_sql,
                "results": self.transform_results,
                "errors": self.transform_errors,
                "performance": self.transform_performance,
                "timing": self.transform_timing,
                "memory": self.transform_memory,
                "lineage": self.transform_lineage,
            }

    # ========================================================================
    # CLI PARAMETER MODELS - Generic CLI parameters following SOLID principles
    # ========================================================================

    class CliParameters(FlextModels):
        """Base class for all CLI parameter models."""

        class DataSourceParams(FlextModels.ArbitraryTypesModel):
            """Generic parameters for data source operations."""

            source_name: str = Field(description="Name of the data source")
            config_file: str | None = Field(
                default=None, description="Path to source configuration file"
            )
            catalog_file: str | None = Field(
                default=None, description="Path to catalog file for schema discovery"
            )
            state_file: str | None = Field(
                default=None, description="Path to state file for incremental sync"
            )
            discover: bool = Field(
                default=False, description="Run in discovery mode to output schema"
            )

        class DataSinkParams(FlextModels.ArbitraryTypesModel):
            """Generic parameters for data sink operations."""

            sink_name: str = Field(description="Name of the data sink")
            config_file: str | None = Field(
                default=None, description="Path to sink configuration file"
            )
            input_file: str | None = Field(
                default=None,
                description="Path to input data file (default: stdin)",
            )

        class PipelineParams(FlextModels.ArbitraryTypesModel):
            """Generic parameters for pipeline operations."""

            source_name: str = Field(description="Name of the data source")
            sink_name: str = Field(description="Name of the data sink")
            source_config: str | None = Field(
                default=None, description="Path to source configuration file"
            )
            sink_config: str | None = Field(
                default=None, description="Path to sink configuration file"
            )
            catalog_file: str | None = Field(
                default=None, description="Path to catalog file"
            )
            state_file: str | None = Field(
                default=None, description="Path to state file"
            )
            state_output_file: str | None = Field(
                default=None, description="Path to write final state"
            )

    class PipelineRunParams(FlextModels.ArbitraryTypesModel):
        """Parameters for pipeline run operations."""

        tap_name: str = Field(description="Name of the tap to run")
        target_name: str = Field(description="Name of the target to run")
        catalog_file: str | None = Field(
            default=None, description="Path to catalog file"
        )
        state_file: str | None = Field(default=None, description="Path to state file")
        state_output_file: str | None = Field(
            default=None, description="Path to write final state"
        )
        tap_config: str | None = Field(
            default=None, description="Path to tap configuration file"
        )
        target_config: str | None = Field(
            default=None, description="Path to target configuration file"
        )
        full_refresh: bool = Field(default=False, description="Run with full refresh")

        class TransformationParams(FlextModels.ArbitraryTypesModel):
            """Generic parameters for transformation operations."""

            project_dir: str = Field(description="Transformation project directory")
            models: str | None = Field(
                default=None, description="Specific models to run (space-separated)"
            )
            select: str | None = Field(
                default=None, description="Selection syntax for models"
            )
            exclude: str | None = Field(
                default=None, description="Exclusion syntax for models"
            )
            full_refresh: bool = Field(
                default=False, description="Run with full refresh"
            )

        class PluginInstallParams(FlextModels.ArbitraryTypesModel):
            """Generic parameters for plugin installation."""

            plugin_type: str = Field(
                description="Type of plugin (source, sink, transformer)"
            )
            plugin_name: str = Field(description="Name of the plugin to install")
            variant: str | None = Field(
                default=None, description="Specific plugin variant"
            )

    # ========================================================================
    # DATA SOURCE MODELS - Generic data source configurations and instances
    # ========================================================================

    class TapRunParams(FlextModels.ArbitraryTypesModel):
        """Generic parameters for tap run operations."""

        tap_name: str = Field(description="Name of the tap to run")
        discover: bool = Field(default=False, description="Run tap in discover mode")
        config_file: str | None = Field(
            default=None, description="Path to tap configuration file"
        )
        catalog_file: str | None = Field(
            default=None, description="Path to Singer catalog file"
        )
        state_file: str | None = Field(
            default=None, description="Path to Singer state file"
        )
        properties_file: str | None = Field(
            default=None, description="Path to Singer properties file"
        )

    class TargetRunParams(FlextModels.ArbitraryTypesModel):
        """Generic parameters for target run operations."""

        target_name: str = Field(description="Name of the target to run")
        config_file: str | None = Field(
            default=None, description="Path to target configuration file"
        )
        input_file: str | None = Field(
            default=None, description="Input file path for target loading"
        )
        batch_size: int | None = Field(
            default=None, description="Batch size for target operations"
        )

    class TapConfig(FlextModels.ArbitraryTypesModel):
        """Generic tap configuration for data extraction."""

        tap_type: str = Field(description="Type of the tap")
        connection_config: dict[str, object] = Field(
            description="Connection configuration",
        )
        stream_config: dict[str, object] = Field(
            default_factory=dict,
            description="Stream-specific configuration",
        )
        version: str = Field(default="latest", description="Tap version")

        @computed_field
        def tap_identifier(self) -> str:
            """Unique tap identifier."""
            return f"{self.tap_type}:{self.version}"

        @computed_field
        def has_stream_config(self) -> bool:
            """Check if stream configuration is present."""
            return bool(self.stream_config)

        @computed_field
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return len(self.connection_config) + len(self.stream_config)

        @model_validator(mode="after")
        def validate_tap_config(self) -> FlextMeltanoModels.TapConfig:
            """Validate tap configuration consistency."""
            if not self.tap_type or not self.tap_type.strip():
                msg = "tap_type cannot be empty"
                raise ValueError(msg)

            if not self.connection_config:
                msg = "Connection configuration cannot be empty"
                raise ValueError(msg)

            return self

        @field_serializer("connection_config")
        def serialize_connection_config(
            self, value: dict[str, object]
        ) -> dict[str, object]:
            """Serialize connection config with sensitive data protection."""
            sensitive_keys = {"password", "token", "api_key", "secret"}
            serialized: dict[str, object] = {}
            for key, val in value.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    serialized[key] = "[PROTECTED]"
                else:
                    serialized[key] = val
            return serialized

    class TargetConfig(FlextModels.ArbitraryTypesModel):
        """Generic target configuration for data loading."""

        target_type: str = Field(description="Type of the target")
        connection_config: dict[str, object] = Field(
            default_factory=dict,
            description="Connection configuration",
        )
        batch_size: int | None = Field(
            default=None, description="Batch size for data loading"
        )
        batch_wait_limit: float | None = Field(
            default=None, description="Batch wait limit in seconds"
        )
        version: str = Field(default="latest", description="Target version")

        @computed_field
        def target_identifier(self) -> str:
            """Unique target identifier."""
            return f"{self.target_type}:{self.version}"

        @computed_field
        def has_connection_config(self) -> bool:
            """Check if connection configuration is present."""
            return bool(self.connection_config)

        @computed_field
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return len(self.connection_config)

        @model_validator(mode="after")
        def validate_target_config(self) -> FlextMeltanoModels.TargetConfig:
            """Validate target configuration consistency."""
            if not self.target_type or not self.target_type.strip():
                msg = "target_type cannot be empty"
                raise ValueError(msg)

            return self

        @field_serializer("connection_config")
        def serialize_connection_config(
            self, value: dict[str, object]
        ) -> dict[str, object]:
            """Serialize connection config with sensitive data protection."""
            sensitive_keys = {"password", "token", "api_key", "secret"}
            serialized: dict[str, object] = {}
            for key, val in value.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    serialized[key] = "[PROTECTED]"
                else:
                    serialized[key] = val
            return serialized

    class DataSourceConfig(FlextModels.ArbitraryTypesModel):
        """Generic data source configuration with validation."""

        source_type: str = Field(description="Type of the data source")
        connection_config: dict[str, object] = Field(
            description="Connection configuration",
        )
        stream_config: dict[str, object] = Field(
            default_factory=dict,
            description="Stream-specific configuration",
        )
        version: str = Field(default="latest", description="Source version")

        @computed_field
        def source_identifier(self) -> str:
            """Unique source identifier."""
            return f"{self.source_type}:{self.version}"

        @computed_field
        def has_stream_config(self) -> bool:
            """Check if stream configuration is present."""
            return bool(self.stream_config)

        @computed_field
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return len(self.connection_config) + len(self.stream_config)

        @model_validator(mode="after")
        def validate_source_config(self) -> FlextMeltanoModels.DataSourceConfig:
            """Validate source configuration consistency."""
            if not self.source_type or not self.source_type.strip():
                msg = "Source type cannot be empty"
                raise ValueError(msg)

            if not self.connection_config:
                msg = "Connection configuration cannot be empty"
                raise ValueError(msg)

            return self

        @field_serializer("connection_config")
        def serialize_connection_config(
            self, value: dict[str, object]
        ) -> dict[str, object]:
            """Serialize connection config with sensitive data protection."""
            sensitive_keys = {"password", "token", "api_key", "secret"}
            serialized: dict[str, object] = {}
            for key, val in value.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    serialized[key] = "[PROTECTED]"
                else:
                    serialized[key] = val
            return serialized

    class StreamDefinition(FlextModels.Entity):
        """Generic stream definition for data pipeline operations."""

        stream_name: str = Field(description="Name of the stream")
        stream_schema: dict[str, object] = Field(
            description="JSON schema for the stream",
        )
        source_type: str = Field(description="Type of source this stream belongs to")
        status: str = Field(
            default="discovered",
            description="Current status of the stream",
        )
        records_extracted: int = Field(
            default=0,
            description="Number of records extracted",
        )

        @computed_field
        def is_active(self) -> bool:
            """Check if stream is active."""
            return self.status in {"discovered", "selected", "extracting"}

        @computed_field
        def has_data(self) -> bool:
            """Check if stream has extracted data."""
            return self.records_extracted > 0

        @computed_field
        def schema_properties_count(self) -> int:
            """Number of schema properties."""
            return len(
                cast("dict[str, object]", self.stream_schema.get("properties", {}))
            )

        @model_validator(mode="after")
        def validate_stream_definition(self) -> FlextMeltanoModels.StreamDefinition:
            """Validate stream definition consistency."""
            if "properties" not in self.stream_schema:
                msg = "Stream schema must contain properties"
                raise ValueError(msg)

            valid_statuses = {
                "discovered",
                "selected",
                "extracting",
                "completed",
                "error",
            }
            if self.status not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)

            return self

        @field_serializer("stream_schema")
        def serialize_stream_schema(
            self, value: dict[str, object]
        ) -> dict[str, object]:
            """Normalize stream schema structure."""
            if "properties" not in value:
                value["properties"] = {}
            if "type" not in value:
                value["type"] = "object"
            return value

    class DataSinkDefinition(FlextModels.Entity):
        """Generic data sink definition for pipeline operations."""

        sink_name: str = Field(description="Name of the sink")
        sink_type: str = Field(description="Type of the sink")
        config: dict[str, object] = Field(
            default_factory=dict, description="Sink configuration"
        )
        sink_schema: dict[str, object] = Field(
            default_factory=dict, description="Sink schema"
        )
        status: str = Field(default="initialized", description="Current status")

        @computed_field
        def config_keys_count(self) -> int:
            """Number of config keys."""
            return len(self.config)

        @model_validator(mode="after")
        def validate_sink_definition(self) -> FlextMeltanoModels.DataSinkDefinition:
            """Validate sink definition consistency."""
            valid_statuses = {
                "initialized",
                "configured",
                "running",
                "completed",
                "error",
            }
            if self.status not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)

            return self

    class TapInstance(FlextModels.Entity):
        """Generic tap instance for data extraction."""

        tap_id: str | None = Field(default=None, description="Unique tap identifier")
        tap_type: str = Field(description="Type of the tap")
        config: FlextMeltanoModels.TapConfig = Field(description="Tap configuration")
        adapter: object | None = Field(default=None, description="Tap adapter instance")
        streams: list[FlextMeltanoModels.StreamInfo] = Field(
            default_factory=list, description="Available streams"
        )
        status: str = Field(default="initialized", description="Tap status")

        @computed_field
        def stream_count(self) -> int:
            """Number of available streams."""
            return len(self.streams)

        @computed_field
        def active_streams(self) -> list[FlextMeltanoModels.StreamInfo]:
            """Active streams for extraction."""
            return [s for s in self.streams if s.status in {"discovered", "selected"}]

    class DataSourceInstance(FlextModels.Entity):
        """Generic data source instance for pipeline operations."""

        source_type: str = Field(description="Type of the data source")
        config: FlextMeltanoModels.DataSourceConfig = Field(
            description="Source configuration"
        )
        adapter: object | None = Field(
            default=None,
            description="Adapter instance",
        )
        status: str = Field(default="initialized", description="Current status")
        streams: dict[str, FlextMeltanoModels.StreamDefinition] = Field(
            default_factory=dict,
            description="Discovered streams",
        )
        discovered: bool = Field(
            default=False,
            description="Whether streams have been discovered",
        )
        metadata: dict[str, object] = Field(
            default_factory=dict,
            description="Additional metadata",
        )
        source_id: str = Field(description="Unique source identifier")

        @computed_field
        def stream_count(self) -> int:
            """Number of discovered streams."""
            return len(self.streams)

        @computed_field
        def active_stream_count(self) -> int:
            """Number of active streams."""
            active_statuses = {"discovered", "selected", "extracting"}
            return sum(
                1
                for stream in self.streams.values()
                if stream.status in active_statuses
            )

        @computed_field
        def total_records_extracted(self) -> int:
            """Total records extracted across all streams."""
            return sum(stream.records_extracted for stream in self.streams.values())

        @computed_field
        def is_ready_for_extraction(self) -> bool:
            """Check if source is ready for data extraction."""
            return (
                self.discovered
                and len(self.streams) > 0
                and self.status == "configured"
            )

        @model_validator(mode="after")
        def validate_source_instance(self) -> FlextMeltanoModels.DataSourceInstance:
            """Validate source instance consistency."""
            if self.config.source_type != self.source_type:
                msg = "Source type must match between instance and config"
                raise ValueError(msg)

            if self.discovered and not self.streams:
                msg = "Discovered source must have at least one stream"
                raise ValueError(msg)

            return self

    class DataSinkInstance(FlextModels.Entity):
        """Generic data sink instance for pipeline operations."""

        sink_id: str | None = Field(default=None, description="Unique sink identifier")
        sink_type: str = Field(description="Type of the data sink")
        config: FlextMeltanoModels.DataSinkConfig = Field(
            description="Sink configuration"
        )
        adapter: object | None = Field(
            default=None,
            description="Adapter instance",
        )
        status: str = Field(default="initialized", description="Current status")
        batch_size: int = Field(default=1000, description="Batch processing size")
        sink_count: int = Field(default=0, description="Number of configured sinks")

        @computed_field
        def is_ready(self) -> bool:
            """Check if sink is ready for processing."""
            return self.status == "configured" and self.adapter is not None

    # ========================================================================
    # DATA SINK CONFIGURATION - Generic sink configuration models
    # ========================================================================

    class DataSinkConfig(FlextModels.Entity):
        """Generic data sink configuration with validation."""

        sink_type: str = Field(description="Sink type identifier")
        connection_config: dict[str, object] = Field(
            description="Connection configuration dictionary",
        )
        batch_size: int = Field(
            default=FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
            description="Batch size for record processing",
        )
        max_batches: int = Field(
            default=FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
            description="Maximum number of batches to process",
        )

        @computed_field
        def sink_identifier(self) -> str:
            """Unique sink identifier."""
            return f"{self.sink_type}:batch_{self.batch_size}"

        @computed_field
        def max_records_capacity(self) -> int:
            """Maximum records capacity."""
            return self.batch_size * self.max_batches

        @computed_field
        def processing_efficiency(self) -> str:
            """Processing efficiency assessment."""
            if self.batch_size >= FlextMeltanoModels.PERFORMANCE_HIGH_THRESHOLD:
                return "high"
            if self.batch_size >= FlextMeltanoModels.PERFORMANCE_GOOD_THRESHOLD:
                return "medium"
            return "low"

        @model_validator(mode="after")
        def validate_sink_config(self) -> FlextMeltanoModels.DataSinkConfig:
            """Validate sink configuration consistency."""
            if not self.sink_type or not self.sink_type.strip():
                msg = "Sink type must be non-empty string"
                raise ValueError(msg)

            max_reasonable_batch_size = 10000
            if self.batch_size > max_reasonable_batch_size:
                msg = f"Batch size too large (max {max_reasonable_batch_size})"
                raise ValueError(msg)

            return self

        @field_serializer("connection_config")
        def serialize_connection_config(
            self, value: dict[str, object]
        ) -> dict[str, object]:
            """Serialize connection config with sensitive data protection."""
            sensitive_keys = {"password", "token", "api_key", "secret", "credentials"}
            serialized: dict[str, object] = {}
            for key, val in value.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    serialized[key] = "[PROTECTED]"
                else:
                    serialized[key] = val
            return serialized

    class StreamInfo(FlextModels.ArbitraryTypesModel):
        """Generic stream information for data pipeline operations."""

        stream_name: str = Field(min_length=1, description="Stream name identifier")
        stream_schema: dict[str, object] = Field(
            description="Stream schema definition",
        )
        key_properties: list[str] = Field(
            default_factory=list,
            description="Primary key properties for the stream",
        )
        replication_method: str = Field(
            default="FULL_TABLE",
            description="Replication method (FULL_TABLE, INCREMENTAL, LOG_BASED)",
        )
        replication_key: str | None = Field(
            default=None,
            description="Field used for incremental replication",
        )
        status: str = Field(
            default="initialized",
            description="Stream processing status",
        )
        records_loaded: int = Field(default=0, description="Number of records loaded")
        batches_processed: int = Field(
            default=0,
            description="Number of batches processed",
        )
        created_at: str = Field(description="Creation timestamp")

        @computed_field
        def has_processed_data(self) -> bool:
            """Check if stream has processed data."""
            return self.records_loaded > 0 or self.batches_processed > 0

        @computed_field
        def average_records_per_batch(self) -> float:
            """Average records per batch."""
            if self.batches_processed == 0:
                return 0.0
            return self.records_loaded / self.batches_processed

        @computed_field
        def processing_status(self) -> str:
            """Processing status assessment."""
            if self.status == "completed" and self.records_loaded > 0:
                return "success"
            if self.status == "error":
                return "failed"
            if self.records_loaded > 0:
                return "in_progress"
            return "pending"

        @model_validator(mode="after")
        def validate_stream_info(self) -> FlextMeltanoModels.StreamInfo:
            """Validate stream information consistency."""
            if self.records_loaded > 0 and self.batches_processed == 0:
                msg = "Records loaded but no batches processed"
                raise ValueError(msg)

            valid_statuses = {"initialized", "processing", "completed", "error"}
            if self.status not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)

            return self

    # ========================================================================
    # PROJECT MODELS - Generic project configuration and validation
    # ========================================================================

    class MeltanoProjectModel(FlextModels.ArbitraryTypesModel):
        """Generic Meltano project configuration with validation."""

        project_id: str = Field(description="Unique project identifier")
        version: str = Field(default="1", description="Project version")
        default_environment: str = Field(
            default="dev", description="Default environment name"
        )
        plugins: dict[str, object] = Field(
            default_factory=dict, description="Plugin configurations"
        )
        environments: dict[str, object] = Field(
            default_factory=dict, description="Environment configurations"
        )

        @model_validator(mode="after")
        def validate_meltano_project(self) -> FlextMeltanoModels.MeltanoProjectModel:
            """Validate Meltano project configuration consistency."""
            if not self.project_id or not self.project_id.strip():
                msg = "project_id cannot be empty"
                raise ValueError(msg)

            return self

    class PipelineProjectModel(FlextModels.Entity):
        """Generic pipeline project configuration with validation."""

        version: int = Field(
            default=1,
            ge=1,
            le=1,
            description="Project version (only version 1 supported)",
        )
        project_id: str = Field(min_length=1, description="Project ID required")
        default_environment: str = Field(
            default="dev",
            description="Default environment",
        )
        project_root: Path = Field(
            default_factory=Path.cwd,
            description="Project root directory",
        )
        environments: list[str] = Field(
            default_factory=lambda: ["dev", "staging", "prod"],
            description="Available environments",
        )

        @computed_field
        def environment_count(self) -> int:
            """Number of environments."""
            return len(self.environments)

        @computed_field
        def has_production_environment(self) -> bool:
            """Check if production environment exists."""
            prod_environments = {"prod", "production", "live"}
            return any(env.lower() in prod_environments for env in self.environments)

        @computed_field
        def project_maturity(self) -> str:
            """Project maturity assessment."""
            has_prod = any(
                env.lower() in {"prod", "production", "live"}
                for env in self.environments
            )
            env_count = len(self.environments)

            if (
                has_prod
                and env_count >= FlextMeltanoModels.PROJECT_MATURITY_MATURE_ENV_COUNT
            ):
                return "mature"
            if env_count >= FlextMeltanoModels.PROJECT_MATURITY_DEVELOPING_ENV_COUNT:
                return "developing"
            return "basic"

        @model_validator(mode="after")
        def validate_project_consistency(
            self,
        ) -> FlextMeltanoModels.PipelineProjectModel:
            """Validate project consistency."""
            if self.default_environment not in self.environments:
                msg = f"Default environment '{self.default_environment}' not in environments list"
                raise ValueError(msg)

            if not self.project_root.exists():
                msg = f"Project root directory does not exist: {self.project_root}"
                raise ValueError(msg)

            return self

    class PluginModel(FlextModels.Entity):
        """Generic plugin configuration for pipeline operations."""

        name: str = Field(min_length=1, description="Plugin name")
        namespace: str = Field(description="Plugin namespace")
        pip_url: str | None = Field(default=None, description="Plugin pip URL")
        executable: str | None = Field(default=None, description="Plugin executable")
        variant: str = Field(
            default="standard",
            description="Plugin variant",
        )
        settings: dict[str, object] = Field(
            default_factory=dict,
            description="Plugin settings",
        )
        capabilities: list[str] = Field(
            default_factory=list,
            description="Plugin capabilities",
        )
        config_files: list[str] = Field(
            default_factory=list,
            description="Plugin configuration files",
        )

        @computed_field
        def full_plugin_name(self) -> str:
            """Full plugin name with namespace."""
            return f"{self.namespace}.{self.name}"

        @computed_field
        def has_custom_executable(self) -> bool:
            """Check if plugin has custom executable."""
            return self.executable is not None

        @computed_field
        def settings_count(self) -> int:
            """Number of plugin settings."""
            return len(self.settings)

        @computed_field
        def plugin_complexity(self) -> str:
            """Plugin complexity assessment."""
            settings_count = len(self.settings)
            if settings_count == 0:
                return "minimal"
            if (
                settings_count
                <= FlextMeltanoModels.PLUGIN_COMPLEXITY_SIMPLE_MAX_SETTINGS
            ):
                return "simple"
            if (
                settings_count
                <= FlextMeltanoModels.PLUGIN_COMPLEXITY_MODERATE_MAX_SETTINGS
            ):
                return "moderate"
            return "complex"

        @model_validator(mode="after")
        def validate_plugin_consistency(self) -> FlextMeltanoModels.PluginModel:
            """Validate plugin consistency."""
            if "." in self.namespace:
                msg = "Plugin namespace cannot contain dots"
                raise ValueError(msg)

            if not self.pip_url and not self.executable:
                msg = "Plugin must have either pip_url or executable"
                raise ValueError(msg)

            return self

    # ========================================================================
    # TRANSFORMATION MODELS - Generic transformation project and execution models
    # ========================================================================

    class DbtProjectModel(FlextModels.ArbitraryTypesModel):
        """Generic DBT project configuration with validation."""

        name: str = Field(description="DBT project name")
        profile: str = Field(description="DBT profile name")
        version: str = Field(default="1.0.0", description="DBT project version")
        config: dict[str, object] = Field(
            default_factory=dict, description="DBT project configuration"
        )
        models: dict[str, object] = Field(
            default_factory=dict, description="DBT models configuration"
        )
        sources: dict[str, object] = Field(
            default_factory=dict, description="DBT sources configuration"
        )
        tests: dict[str, object] = Field(
            default_factory=dict, description="DBT tests configuration"
        )

        @model_validator(mode="after")
        def validate_dbt_project(self) -> FlextMeltanoModels.DbtProjectModel:
            """Validate DBT project configuration consistency."""
            if not self.name or not self.name.strip():
                msg = "name cannot be empty"
                raise ValueError(msg)

            if not self.profile or not self.profile.strip():
                msg = "profile cannot be empty"
                raise ValueError(msg)

            return self

    class TransformationProjectModel(FlextModels.ArbitraryTypesModel):
        """Generic transformation project configuration with validation."""

        name: str = Field(min_length=1, description="Project name")
        version: str = Field(description="Project version")
        profile: str = Field(description="Profile name")
        model_paths: list[str] = Field(
            default=["models"],
            description="Model paths",
        )
        analysis_paths: list[str] = Field(
            default=["analysis"],
            description="Analysis paths",
        )
        test_paths: list[str] = Field(
            default=["tests"],
            description="Test paths",
        )
        seed_paths: list[str] = Field(
            default=["seeds"],
            description="Seed paths",
        )
        macro_paths: list[str] = Field(
            default=["macros"],
            description="Macro paths",
        )

        @computed_field
        def total_path_count(self) -> int:
            """Total number of configured paths."""
            return (
                len(self.model_paths)
                + len(self.analysis_paths)
                + len(self.test_paths)
                + len(self.seed_paths)
                + len(self.macro_paths)
            )

        @computed_field
        def has_custom_paths(self) -> bool:
            """Check if project has custom paths."""
            default_paths = {"models", "analysis", "tests", "seeds", "macros"}
            all_paths = set(
                self.model_paths
                + self.analysis_paths
                + self.test_paths
                + self.seed_paths
                + self.macro_paths
            )
            return bool(all_paths - default_paths)

        @computed_field
        def project_structure_complexity(self) -> str:
            """Project structure complexity."""
            total_path_count = (
                len(self.model_paths)
                + len(self.analysis_paths)
                + len(self.test_paths)
                + len(self.seed_paths)
                + len(self.macro_paths)
            )
            if total_path_count <= FlextMeltanoModels.TRANSFORMATION_SIMPLE_MAX_PATHS:
                return "simple"
            if total_path_count <= FlextMeltanoModels.TRANSFORMATION_MODERATE_MAX_PATHS:
                return "moderate"
            return "complex"

        @model_validator(mode="after")
        def validate_project_consistency(
            self,
        ) -> FlextMeltanoModels.TransformationProjectModel:
            """Validate project consistency."""
            if not self.model_paths:
                msg = "Project must have at least one model path"
                raise ValueError(msg)

            return self

    class TransformationExecutionModel(FlextModels.Entity):
        """Generic transformation execution configuration with validation."""

        command: str = Field(description="Command to execute")
        models: list[str] = Field(
            default_factory=list,
            description="Models to execute",
        )
        exclude: list[str] = Field(
            default_factory=list,
            description="Models to exclude",
        )
        full_refresh: bool = Field(
            default=False,
            description="Full refresh execution",
        )
        fail_fast: bool = Field(
            default=True,
            description="Fail fast on first error",
        )
        threads: int = Field(
            default=1,
            description="Number of threads to use",
        )

        @computed_field
        def model_count(self) -> int:
            """Number of models to execute."""
            return len(self.models)

        @computed_field
        def exclude_count(self) -> int:
            """Number of models to exclude."""
            return len(self.exclude)

        @computed_field
        def execution_complexity(self) -> str:
            """Execution complexity assessment."""
            total_scope = len(self.models) + len(self.exclude)
            if total_scope == 0:
                return "full_project"
            if total_scope <= FlextMeltanoModels.EXECUTION_SIMPLE_THRESHOLD:
                return "simple"
            if total_scope <= FlextMeltanoModels.EXECUTION_MODERATE_THRESHOLD:
                return "moderate"
            return "complex"

        @computed_field
        def is_parallel_execution(self) -> bool:
            """Check if execution uses multiple threads."""
            return self.threads > 1

        @model_validator(mode="after")
        def validate_execution_consistency(
            self,
        ) -> FlextMeltanoModels.TransformationExecutionModel:
            """Validate execution consistency."""
            max_threads = 32
            if self.threads > max_threads:
                msg = f"Thread count cannot exceed {max_threads}"
                raise ValueError(msg)

            model_set = set(self.models)
            exclude_set = set(self.exclude)
            overlap = model_set & exclude_set
            if overlap:
                msg = f"Models cannot be both included and excluded: {overlap}"
                raise ValueError(msg)

            return self

    # ========================================================================
    # EXECUTION RESULT MODELS - Pipeline execution and monitoring
    # ========================================================================

    class ExecutionResult(FlextModels.TimestampedModel):
        """Generic execution result tracking with validation."""

        operation: str = Field(description="Operation performed")
        status: str = Field(description="Execution status")
        start_time: datetime = Field(
            default_factory=lambda: datetime.now(tz=UTC),
            description="Execution start time",
        )
        end_time: datetime | None = Field(
            default=None,
            description="Execution end time",
        )
        duration_seconds: float | None = Field(
            default=None,
            description="Execution duration in seconds",
        )
        records_processed: int = Field(
            default=0,
            description="Number of records processed",
        )
        error_message: str | None = Field(
            default=None,
            description="Error message if failed",
        )
        metadata: dict[str, object] = Field(
            default_factory=dict,
            description="Additional execution metadata",
        )

        @computed_field
        def is_completed(self) -> bool:
            """Check if execution is completed."""
            return self.end_time is not None

        @computed_field
        def is_successful(self) -> bool:
            """Check if execution was successful."""
            return self.status == "success" and self.error_message is None

        @computed_field
        def execution_rate_per_second(self) -> float:
            """Execution rate (records/second)."""
            if not self.duration_seconds or self.duration_seconds <= 0:
                return 0.0
            return self.records_processed / self.duration_seconds

        @computed_field
        def performance_category(self) -> str:
            """Performance categorization."""
            if not self.duration_seconds or self.duration_seconds <= 0:
                rate = 0.0
            else:
                rate = self.records_processed / self.duration_seconds

            if rate >= FlextMeltanoModels.PERFORMANCE_HIGH_THRESHOLD:
                return "high_performance"
            if rate >= FlextMeltanoModels.PERFORMANCE_GOOD_THRESHOLD:
                return "good_performance"
            if rate >= FlextMeltanoModels.PERFORMANCE_MODERATE_THRESHOLD:
                return "moderate_performance"
            return "low_performance"

        @model_validator(mode="after")
        def validate_execution_result(self) -> FlextMeltanoModels.ExecutionResult:
            """Validate execution result consistency."""
            if self.start_time and self.end_time:
                calculated_duration = (self.end_time - self.start_time).total_seconds()
                if self.duration_seconds is None:
                    self.duration_seconds = calculated_duration
                elif abs(self.duration_seconds - calculated_duration) > 1.0:
                    msg = "Duration inconsistent with start/end times"
                    raise ValueError(msg)

            if self.status == "error" and not self.error_message:
                msg = "Error status requires error message"
                raise ValueError(msg)

            return self

        @field_validator("status")
        @classmethod
        def validate_status(cls, v: str) -> str:
            """Validate execution status."""
            valid_statuses = ["pending", "running", "success", "error", "timeout"]
            if v not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)
            return v

    class PipelineResult(FlextModels.TimestampedModel):
        """Generic pipeline execution result with complete validation."""

        pipeline_id: str = Field(description="Pipeline identifier")
        source_result: FlextMeltanoModels.ExecutionResult | None = Field(
            default=None,
            description="Source execution result",
        )
        sink_result: FlextMeltanoModels.ExecutionResult | None = Field(
            default=None,
            description="Sink execution result",
        )
        transformation_result: FlextMeltanoModels.ExecutionResult | None = Field(
            default=None,
            description="Transformation execution result",
        )
        overall_status: str = Field(
            default="pending",
            description="Overall pipeline status",
        )
        total_records: int = Field(
            default=0,
            description="Total records processed",
        )
        pipeline_metadata: dict[str, object] = Field(
            default_factory=dict,
            description="Pipeline execution metadata",
        )

        @computed_field
        def completed_stages(self) -> list[str]:
            """Completed pipeline stages."""
            stages: list[str] = []
            if self.source_result and self.source_result.end_time is not None:
                stages.append("extraction")
            if self.sink_result and self.sink_result.end_time is not None:
                stages.append("loading")
            if (
                self.transformation_result
                and self.transformation_result.end_time is not None
            ):
                stages.append("transformation")
            return stages

        @computed_field
        def completion_percentage(self) -> float:
            """Pipeline completion percentage."""
            total_stages = 3
            completed = 0
            if self.source_result and self.source_result.end_time is not None:
                completed += 1
            if self.sink_result and self.sink_result.end_time is not None:
                completed += 1
            if (
                self.transformation_result
                and self.transformation_result.end_time is not None
            ):
                completed += 1
            return (completed / total_stages) * 100

        @computed_field
        def is_fully_successful(self) -> bool:
            """Check if all stages completed successfully."""
            return bool(
                self.source_result
                and self.source_result.status == "success"
                and self.source_result.error_message is None
                and self.sink_result
                and self.sink_result.status == "success"
                and self.sink_result.error_message is None
                and self.transformation_result
                and self.transformation_result.status == "success"
                and self.transformation_result.error_message is None
            )

        @computed_field
        def total_duration_seconds(self) -> float:
            """Total pipeline duration."""
            total = 0.0
            if self.source_result and self.source_result.duration_seconds:
                total += self.source_result.duration_seconds
            if self.sink_result and self.sink_result.duration_seconds:
                total += self.sink_result.duration_seconds
            if (
                self.transformation_result
                and self.transformation_result.duration_seconds
            ):
                total += self.transformation_result.duration_seconds
            return total

        @model_validator(mode="after")
        def validate_pipeline_result(self) -> FlextMeltanoModels.PipelineResult:
            """Validate pipeline result consistency."""
            total_from_stages = 0
            if self.source_result:
                total_from_stages += self.source_result.records_processed

            if (
                self.total_records > 0
                and total_from_stages > 0
                and abs(self.total_records - total_from_stages)
                > (total_from_stages * 0.1)
            ):
                msg = "Total records inconsistent with stage results"
                raise ValueError(msg)

            all_successful = bool(
                self.source_result
                and self.source_result.status == "success"
                and self.source_result.error_message is None
                and self.sink_result
                and self.sink_result.status == "success"
                and self.sink_result.error_message is None
                and self.transformation_result
                and self.transformation_result.status == "success"
                and self.transformation_result.error_message is None
            )
            if all_successful and self.overall_status != "success":
                self.overall_status = "success"

            return self

        @field_validator("overall_status")
        @classmethod
        def validate_overall_status(cls, v: str) -> str:
            """Validate overall pipeline status."""
            valid_statuses = ["pending", "running", "success", "partial", "error"]
            if v not in valid_statuses:
                msg = f"Overall status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)
            return v


__all__ = [
    "FlextMeltanoModels",
]
