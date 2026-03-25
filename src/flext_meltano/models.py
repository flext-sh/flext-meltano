"""FLEXT pipeline models.

Provides Pydantic models for data pipeline operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, ClassVar, Literal, Self

import yaml
from flext_cli import FlextCliModels, u
from flext_core import FlextModels, r
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from flext_meltano import c, t

type _ValidatorInput = (
    t.ContainerMapping
    | Mapping[str, t.ContainerMapping | None]
    | Sequence[t.ContainerMapping | None]
    | tuple[t.ContainerMapping | None, ...]
    | set[t.ContainerMapping | None]
    | None
)


class FlextMeltanoModels(FlextCliModels):
    """Generic pipeline models.

    Provides reusable Pydantic models for pipeline operations.
    """

    class Meltano:
        """Meltano domain namespace."""

        @staticmethod
        def _protect_sensitive_config(
            value: t.ConfigurationMapping,
        ) -> t.ConfigurationMapping:
            """Protect sensitive keys in configuration dict."""
            sensitive_keys = {"password", "token", "api_key", "secret", "credentials"}

            def is_sensitive(k: str) -> bool:
                normalized = u.normalize(k, case="lower")
                # Convert set to list of str for processing
                sensitive_keys_list: t.StrSequence = list(sensitive_keys)
                checks_result = u.process(
                    sensitive_keys_list,
                    lambda s: r[bool].ok(s in normalized),
                )
                checks = FlextMeltanoModels.Meltano.BooleanListValue.model_validate({
                    "items": checks_result.unwrap_or([]),
                }).items
                if checks:
                    return u.any_(*checks)
                return False

            # Transform dict values with protection for sensitive fields
            protected: t.MutableConfigurationMapping = {}
            for key, item in value.items():
                protected[key] = "[PROTECTED]" if is_sensitive(key) else item

            return protected

        @staticmethod
        def _validated_string_list(value: _ValidatorInput) -> t.StrSequence:
            """Normalize arbitrary values into a validated list of strings."""
            return FlextMeltanoModels.Meltano.StringListValue.model_validate({
                "items": value,
            }).items

        class StringListValue(FlextCliModels.ArbitraryTypesModel):
            """Validated string list wrapper for result normalization."""

            items: Annotated[
                t.StrSequence,
                Field(
                    description="Normalized list of string values",
                ),
            ] = Field(default_factory=list)

            @field_validator("items", mode="before")
            @classmethod
            def normalize_items(cls, value: _ValidatorInput) -> t.StrSequence:
                """Convert sequence-like values into string lists."""
                if isinstance(value, (list, tuple, set)):
                    return [str(item) for item in value if item is not None]
                return []

        class BooleanListValue(FlextCliModels.ArbitraryTypesModel):
            """Validated boolean list wrapper for process output."""

            items: Annotated[
                Sequence[bool],
                Field(
                    description="Normalized list of boolean values",
                ),
            ] = Field(default_factory=list)

            @field_validator("items", mode="before")
            @classmethod
            def normalize_items(cls, value: _ValidatorInput) -> Sequence[bool]:
                """Convert sequence-like values into booleans."""
                if isinstance(value, (list, tuple, set)):
                    return [bool(item) for item in value]
                return []

        class LoggingConfig(BaseModel):
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
            pipeline_execution: Annotated[
                bool,
                Field(default=True, description="Log pipeline execution details"),
            ]
            pipeline_stages: Annotated[
                bool,
                Field(default=True, description="Log pipeline stage transitions"),
            ]
            pipeline_progress: Annotated[
                bool,
                Field(default=True, description="Log pipeline progress updates"),
            ]
            pipeline_errors: Annotated[
                bool,
                Field(default=True, description="Log pipeline errors and failures"),
            ]
            pipeline_warnings: Annotated[
                bool,
                Field(default=True, description="Log pipeline warnings"),
            ]
            pipeline_performance: Annotated[
                bool,
                Field(default=True, description="Log pipeline performance metrics"),
            ]
            pipeline_timing: Annotated[
                bool,
                Field(default=True, description="Log pipeline timing information"),
            ]
            pipeline_memory: Annotated[
                bool,
                Field(default=True, description="Log pipeline memory usage"),
            ]
            pipeline_throughput: Annotated[
                bool,
                Field(default=True, description="Log pipeline throughput metrics"),
            ]

            # Extract/Source Operations Logging (8 fields)
            extract_operations: Annotated[
                bool,
                Field(default=True, description="Log extract operations"),
            ]
            extract_queries: Annotated[
                bool,
                Field(default=True, description="Log extract queries"),
            ]
            extract_results: Annotated[
                bool,
                Field(default=True, description="Log extract results"),
            ]
            extract_errors: Annotated[
                bool,
                Field(default=True, description="Log extract errors"),
            ]
            extract_performance: Annotated[
                bool,
                Field(default=True, description="Log extract performance metrics"),
            ]
            extract_timing: Annotated[
                bool,
                Field(default=True, description="Log extract timing information"),
            ]
            extract_memory: Annotated[
                bool,
                Field(default=True, description="Log extract memory usage"),
            ]
            extract_throughput: Annotated[
                bool,
                Field(default=True, description="Log extract throughput metrics"),
            ]

            # Load/Sink Operations Logging (8 fields)
            load_operations: Annotated[
                bool,
                Field(default=True, description="Log load operations"),
            ]
            load_batches: Annotated[
                bool,
                Field(default=True, description="Log load batches"),
            ]
            load_results: Annotated[
                bool,
                Field(default=True, description="Log load results"),
            ]
            load_errors: Annotated[
                bool,
                Field(default=True, description="Log load errors"),
            ]
            load_performance: Annotated[
                bool,
                Field(default=True, description="Log load performance metrics"),
            ]
            load_timing: Annotated[
                bool,
                Field(default=True, description="Log load timing information"),
            ]
            load_memory: Annotated[
                bool,
                Field(default=True, description="Log load memory usage"),
            ]
            load_throughput: Annotated[
                bool,
                Field(default=True, description="Log load throughput metrics"),
            ]

            # Transform/DBT Operations Logging (8 fields)
            transform_operations: Annotated[
                bool,
                Field(default=True, description="Log transform operations"),
            ]
            transform_sql: Annotated[
                bool,
                Field(default=True, description="Log transform SQL queries"),
            ]
            transform_results: Annotated[
                bool,
                Field(default=True, description="Log transform results"),
            ]
            transform_errors: Annotated[
                bool,
                Field(default=True, description="Log transform errors"),
            ]
            transform_performance: Annotated[
                bool,
                Field(default=True, description="Log transform performance metrics"),
            ]
            transform_timing: Annotated[
                bool,
                Field(default=True, description="Log transform timing information"),
            ]
            transform_memory: Annotated[
                bool,
                Field(default=True, description="Log transform memory usage"),
            ]
            transform_lineage: Annotated[
                bool,
                Field(default=True, description="Log transform lineage tracking"),
            ]

            # DBT Specific Logging (6 fields)
            dbt_parse: Annotated[
                bool,
                Field(default=True, description="Log DBT parsing operations"),
            ]
            dbt_compile: Annotated[
                bool,
                Field(default=True, description="Log DBT compilation"),
            ]
            dbt_execute: Annotated[
                bool,
                Field(default=True, description="Log DBT execution"),
            ]
            dbt_test: Annotated[
                bool,
                Field(default=True, description="Log DBT test operations"),
            ]
            dbt_snapshot: Annotated[
                bool,
                Field(default=True, description="Log DBT snapshot operations"),
            ]
            dbt_docs: Annotated[
                bool,
                Field(default=True, description="Log DBT documentation generation"),
            ]

            # Data Quality Logging (8 fields)
            data_quality: Annotated[
                bool,
                Field(default=True, description="Log data quality checks"),
            ]
            data_quality_checks: Annotated[
                bool,
                Field(default=True, description="Log data quality check results"),
            ]
            data_quality_errors: Annotated[
                bool,
                Field(default=True, description="Log data quality errors"),
            ]
            data_quality_warnings: Annotated[
                bool,
                Field(default=True, description="Log data quality warnings"),
            ]
            data_quality_metrics: Annotated[
                bool,
                Field(default=True, description="Log data quality metrics"),
            ]
            data_quality_timing: Annotated[
                bool,
                Field(default=True, description="Log data quality timing information"),
            ]
            data_quality_memory: Annotated[
                bool,
                Field(default=True, description="Log data quality memory usage"),
            ]
            data_quality_throughput: Annotated[
                bool,
                Field(default=True, description="Log data quality throughput metrics"),
            ]

            # Plugin Logging (6 fields)
            plugin_operations: Annotated[
                bool,
                Field(default=True, description="Log plugin operations"),
            ]
            plugin_errors: Annotated[
                bool,
                Field(default=True, description="Log plugin errors"),
            ]
            plugin_performance: Annotated[
                bool,
                Field(default=True, description="Log plugin performance metrics"),
            ]
            plugin_timing: Annotated[
                bool,
                Field(default=True, description="Log plugin timing information"),
            ]
            plugin_memory: Annotated[
                bool,
                Field(default=True, description="Log plugin memory usage"),
            ]
            plugin_throughput: Annotated[
                bool,
                Field(default=True, description="Log plugin throughput metrics"),
            ]

            # Source and Target Logging (14 fields)
            source_info: Annotated[
                bool,
                Field(default=True, description="Log source information"),
            ]
            target_info: Annotated[
                bool,
                Field(default=True, description="Log target information"),
            ]
            source_errors: Annotated[
                bool,
                Field(default=True, description="Log source errors"),
            ]
            target_errors: Annotated[
                bool,
                Field(default=True, description="Log target errors"),
            ]
            source_performance: Annotated[
                bool,
                Field(default=True, description="Log source performance metrics"),
            ]
            target_performance: Annotated[
                bool,
                Field(default=True, description="Log target performance metrics"),
            ]
            source_timing: Annotated[
                bool,
                Field(default=True, description="Log source timing information"),
            ]
            target_timing: Annotated[
                bool,
                Field(default=True, description="Log target timing information"),
            ]
            source_memory: Annotated[
                bool,
                Field(default=True, description="Log source memory usage"),
            ]
            target_memory: Annotated[
                bool,
                Field(default=True, description="Log target memory usage"),
            ]
            source_throughput: Annotated[
                bool,
                Field(default=True, description="Log source throughput metrics"),
            ]
            target_throughput: Annotated[
                bool,
                Field(default=True, description="Log target throughput metrics"),
            ]

            # Meltano Performance Tracking (1 field)
            track_meltano_performance: Annotated[
                bool,
                Field(default=True, description="Track Meltano performance metrics"),
            ]

            # Orchestration Logging (5 fields)
            orchestration_scheduling: Annotated[
                bool,
                Field(default=True, description="Log orchestration scheduling events"),
            ]
            orchestration_execution: Annotated[
                bool,
                Field(default=True, description="Log orchestration execution"),
            ]
            orchestration_state: Annotated[
                bool,
                Field(default=True, description="Log orchestration state changes"),
            ]
            orchestration_hooks: Annotated[
                bool,
                Field(default=True, description="Log orchestration hook execution"),
            ]
            orchestration_dependencies: Annotated[
                bool,
                Field(default=True, description="Log dependency resolution"),
            ]

            # Monitoring and Observability Logging (5 fields)
            monitoring_metrics: Annotated[
                bool,
                Field(default=True, description="Log collected metrics"),
            ]
            monitoring_alerts: Annotated[
                bool,
                Field(default=True, description="Log alert generation"),
            ]
            monitoring_health: Annotated[
                bool,
                Field(default=True, description="Log health checks"),
            ]
            monitoring_traces: Annotated[
                bool,
                Field(default=True, description="Log distributed traces"),
            ]
            monitoring_events: Annotated[
                bool,
                Field(default=True, description="Log observability events"),
            ]

            # Debugging and Diagnostics Logging (5 fields)
            debug_verbose: Annotated[
                bool,
                Field(default=False, description="Enable verbose debug logging"),
            ]
            debug_trace_calls: Annotated[
                bool,
                Field(default=False, description="Log function call traces"),
            ]
            debug_variable_state: Annotated[
                bool,
                Field(default=False, description="Log variable state changes"),
            ]
            debug_configuration: Annotated[
                bool,
                Field(default=False, description="Log configuration details"),
            ]
            debug_performance_profile: Annotated[
                bool,
                Field(default=False, description="Log performance profiling data"),
            ]

            @computed_field
            def extract_dict(self) -> Mapping[str, bool]:
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
            def load_dict(self) -> Mapping[str, bool]:
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
            def pipeline_dict(self) -> Mapping[str, bool]:
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
            def transform_dict(self) -> Mapping[str, bool]:
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

            class DataSourceParams(FlextCliModels.Entity):
                """Generic parameters for data source operations."""

                source_name: Annotated[
                    str,
                    Field(description="Name of the data source"),
                ]
                config_file: Annotated[
                    str | None,
                    Field(
                        default=None,
                        description="Path to source configuration file",
                    ),
                ]
                catalog_file: Annotated[
                    str | None,
                    Field(
                        default=None,
                        description="Path to catalog file for schema discovery",
                    ),
                ]
                state_file: Annotated[
                    str | None,
                    Field(
                        default=None,
                        description="Path to state file for incremental sync",
                    ),
                ]
                discover: Annotated[
                    bool,
                    Field(
                        default=False,
                        description="Run in discovery mode to output schema",
                    ),
                ]

            class DataSinkParams(FlextCliModels.Entity):
                """Generic parameters for data sink operations."""

                sink_name: Annotated[str, Field(description="Name of the data sink")]
                config_file: Annotated[
                    str | None,
                    Field(default=None, description="Path to sink configuration file"),
                ]
                input_file: Annotated[
                    str | None,
                    Field(
                        default=None,
                        description="Path to input data file (default: stdin)",
                    ),
                ]

            class PipelineParams(FlextCliModels.Entity):
                """Generic parameters for pipeline operations."""

                source_name: Annotated[
                    str,
                    Field(description="Name of the data source"),
                ]
                sink_name: Annotated[str, Field(description="Name of the data sink")]
                source_config: Annotated[
                    str | None,
                    Field(
                        default=None,
                        description="Path to source configuration file",
                    ),
                ]
                sink_config: Annotated[
                    str | None,
                    Field(default=None, description="Path to sink configuration file"),
                ]
                catalog_file: Annotated[
                    str | None,
                    Field(default=None, description="Path to catalog file"),
                ]
                state_file: Annotated[
                    str | None,
                    Field(default=None, description="Path to state file"),
                ]
                state_output_file: Annotated[
                    str | None,
                    Field(default=None, description="Path to write final state"),
                ]

            class TransformationParams(FlextCliModels.Entity):
                """Generic parameters for transformation operations."""

                project_dir: Annotated[
                    str,
                    Field(description="Transformation project directory"),
                ]
                models: Annotated[
                    str | None,
                    Field(
                        default=None,
                        description="Specific models to run (space-separated)",
                    ),
                ]
                select: Annotated[
                    str | None,
                    Field(default=None, description="Selection syntax for models"),
                ]
                exclude: Annotated[
                    str | None,
                    Field(default=None, description="Exclusion syntax for models"),
                ]
                full_refresh: Annotated[
                    bool,
                    Field(default=False, description="Run with full refresh"),
                ]

            class PluginInstallParams(FlextCliModels.Entity):
                """Generic parameters for plugin installation."""

                plugin_type: Annotated[
                    str,
                    Field(description="Type of plugin (source, sink, transformer)"),
                ]
                plugin_name: Annotated[
                    str,
                    Field(description="Name of the plugin to install"),
                ]
                variant: Annotated[
                    str | None,
                    Field(default=None, description="Specific plugin variant"),
                ]

        class PipelineRunParams(FlextCliModels.Entity):
            """Parameters for pipeline run operations."""

            tap_name: Annotated[str, Field(description="Name of the tap to run")]
            target_name: Annotated[str, Field(description="Name of the target to run")]
            catalog_file: Annotated[
                str | None,
                Field(default=None, description="Path to catalog file"),
            ]
            state_file: Annotated[
                str | None,
                Field(default=None, description="Path to state file"),
            ]
            state_output_file: Annotated[
                str | None,
                Field(default=None, description="Path to write final state"),
            ]
            tap_config: Annotated[
                str | None,
                Field(default=None, description="Path to tap configuration file"),
            ]
            target_config: Annotated[
                str | None,
                Field(default=None, description="Path to target configuration file"),
            ]
            full_refresh: Annotated[
                bool,
                Field(default=False, description="Run with full refresh"),
            ]

        class ServiceConstructorConfig(FlextCliModels.ArbitraryTypesModel):
            """Configuration model for FlextMeltanoService constructor."""

            config: Annotated[
                Mapping[str, t.ContainerMapping | None] | None,
                Field(
                    default=None,
                    description="Optional Meltano settings payload",
                ),
            ]
            service_name: Annotated[
                t.NonEmptyStr,
                Field(
                    default="flext_meltano_service",
                    description="Name of the Meltano service instance",
                ),
            ]
            service_version: Annotated[
                t.NonEmptyStr,
                Field(
                    default="0.9.9",
                    description="Version identifier for the service",
                ),
            ]
            source_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Optional source name for specialization",
                ),
            ]
            sink_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Optional sink name for specialization",
                ),
            ]
            transformation_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Optional transformation name for specialization",
                ),
            ]
            service_type: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Optional service type (tap, target, dbt)",
                ),
            ]
            tap_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Optional Singer tap name alias for source_name",
                ),
            ]
            target_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Optional Singer target name alias for sink_name",
                ),
            ]
            project_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Optional DBT project alias for transformation_name",
                ),
            ]

        # ========================================================================
        # DATA SOURCE MODELS - Generic data source configurations and instances
        # ========================================================================

        class DbtRunParams(FlextCliModels.Entity):
            """Generic parameters for dbt run operations."""

            project_dir: Annotated[str, Field(description="dbt project directory")]
            models: Annotated[
                str | None,
                Field(default=None, description="Models to run"),
            ]
            select: Annotated[
                str | None,
                Field(default=None, description="Selection syntax"),
            ]
            exclude: Annotated[
                str | None,
                Field(default=None, description="Exclusion syntax"),
            ]
            full_refresh: Annotated[
                bool,
                Field(default=False, description="Full refresh flag"),
            ]
            vars: Annotated[
                t.ConfigurationMapping | None,
                Field(default=None, description="dbt variables"),
            ]

        class TapRunParams(FlextCliModels.Entity):
            """Generic parameters for tap run operations."""

            tap_name: Annotated[str, Field(description="Name of the tap to run")]
            discover: Annotated[
                bool,
                Field(default=False, description="Run tap in discover mode"),
            ]
            config_file: Annotated[
                str | None,
                Field(default=None, description="Path to tap configuration file"),
            ]
            catalog_file: Annotated[
                str | None,
                Field(default=None, description="Path to Singer catalog file"),
            ]
            state_file: Annotated[
                str | None,
                Field(default=None, description="Path to Singer state file"),
            ]
            properties_file: Annotated[
                str | None,
                Field(default=None, description="Path to Singer properties file"),
            ]

        class TargetRunParams(FlextCliModels.Entity):
            """Generic parameters for target run operations."""

            target_name: Annotated[str, Field(description="Name of the target to run")]
            config_file: Annotated[
                str | None,
                Field(default=None, description="Path to target configuration file"),
            ]
            input_file: Annotated[
                str | None,
                Field(default=None, description="Input file path for target loading"),
            ]
            batch_size: Annotated[
                t.BatchSize | None,
                Field(default=None, description="Batch size for target operations"),
            ]

        class TapConfig(FlextCliModels.Entity):
            """Generic tap configuration for data extraction."""

            tap_type: Annotated[str, Field(description="Type of the tap")]
            connection_config: Annotated[
                t.ConfigurationMapping,
                Field(description="Connection configuration"),
            ]
            stream_config: Annotated[
                t.ConfigurationMapping,
                Field(
                    description="Stream-specific configuration",
                ),
            ] = Field(default_factory=dict)
            tap_version: Annotated[
                str,
                Field(default="latest", description="Tap version"),
            ]

            @computed_field
            def config_size(self) -> int:
                """Total number of configuration parameters."""
                conn_keys = list(self.connection_config.keys())
                stream_keys = list(self.stream_config.keys())
                return u.count(conn_keys) + u.count(stream_keys)

            @computed_field
            def has_stream_config(self) -> bool:
                """Check if stream configuration is present."""
                return bool(self.stream_config)

            @computed_field
            def tap_identifier(self) -> str:
                """Unique tap identifier."""
                return f"{self.tap_type}:{self.tap_version}"

            @field_serializer("connection_config")
            def serialize_connection_config(
                self,
                value: t.ConfigurationMapping,
            ) -> t.ConfigurationMapping:
                """Serialize connection config with sensitive data protection."""
                return FlextMeltanoModels._protect_sensitive_config(value)

            @model_validator(mode="after")
            def validate_tap_config(self) -> Self:
                """Validate tap configuration consistency."""
                if not self.tap_type or not self.tap_type.strip():
                    msg = "tap_type cannot be empty"
                    raise ValueError(msg)

                if not self.connection_config:
                    msg = "Connection configuration cannot be empty"
                    raise ValueError(msg)

                return self

        class TargetConfig(FlextCliModels.Entity):
            """Generic target configuration for data loading."""

            target_type: Annotated[str, Field(description="Type of the target")]
            connection_config: Annotated[
                t.ContainerMapping,
                Field(description="Connection configuration"),
            ] = Field(default_factory=dict)
            batch_size: Annotated[
                int | None,
                Field(default=None, description="Batch size for data loading"),
            ]
            batch_wait_limit: Annotated[
                float | None,
                Field(default=None, description="Batch wait limit in seconds"),
            ]
            target_version: Annotated[
                str,
                Field(default="latest", description="Target version"),
            ]

            @computed_field
            def config_size(self) -> int:
                """Total number of configuration parameters."""
                return len(self.connection_config)

            @computed_field
            def has_connection_config(self) -> bool:
                """Check if connection configuration is present."""
                return bool(self.connection_config)

            @computed_field
            def target_identifier(self) -> str:
                """Unique target identifier."""
                return f"{self.target_type}:{self.target_version}"

            @field_serializer("connection_config")
            def serialize_connection_config(
                self,
                value: t.ConfigurationMapping,
            ) -> t.ConfigurationMapping:
                """Serialize connection config with sensitive data protection."""
                return FlextMeltanoModels._protect_sensitive_config(value)

            @model_validator(mode="after")
            def validate_target_config(self) -> Self:
                """Validate target configuration consistency."""
                if not self.target_type or not self.target_type.strip():
                    msg = "target_type cannot be empty"
                    raise ValueError(msg)

                return self

        class DataSourceConfig(FlextCliModels.Entity):
            """Generic data source configuration with validation."""

            source_type: Annotated[str, Field(description="Type of the data source")]
            connection_config: Annotated[
                t.ConfigurationMapping,
                Field(description="Connection configuration"),
            ]
            stream_config: Annotated[
                t.ConfigurationMapping,
                Field(
                    description="Stream-specific configuration",
                ),
            ] = Field(default_factory=dict)
            source_version: Annotated[
                str,
                Field(default="latest", description="Source version"),
            ]

            @computed_field
            def config_size(self) -> int:
                """Total number of configuration parameters."""
                conn_keys = list(self.connection_config.keys())
                stream_keys = list(self.stream_config.keys())
                return u.count(conn_keys) + u.count(stream_keys)

            @computed_field
            def has_stream_config(self) -> bool:
                """Check if stream configuration is present."""
                return bool(self.stream_config)

            @computed_field
            def source_identifier(self) -> str:
                """Unique source identifier."""
                return f"{self.source_type}:{self.source_version}"

            @field_serializer("connection_config")
            def serialize_connection_config(
                self,
                value: t.ConfigurationMapping,
            ) -> t.ConfigurationMapping:
                """Serialize connection config with sensitive data protection."""
                return FlextMeltanoModels._protect_sensitive_config(value)

            @model_validator(mode="after")
            def validate_source_config(self) -> Self:
                """Validate source configuration consistency."""
                if not self.source_type or not self.source_type.strip():
                    msg = "Source type cannot be empty"
                    raise ValueError(msg)

                if not self.connection_config:
                    msg = "Connection configuration cannot be empty"
                    raise ValueError(msg)

                return self

        class StreamDefinition(FlextCliModels.Entity):
            """Generic stream definition for data pipeline operations."""

            stream_name: Annotated[str, Field(description="Name of the stream")]
            stream_schema: Annotated[
                t.ContainerMapping,
                Field(description="JSON schema for the stream"),
            ]
            source_type: Annotated[
                str,
                Field(description="Type of source this stream belongs to"),
            ]
            status: Annotated[
                str,
                Field(
                    default=c.Meltano.Enums.StreamStatus.DISCOVERED,
                    description="Current status of the stream",
                ),
            ]
            records_extracted: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of records extracted"),
            ]

            @computed_field
            def has_data(self) -> bool:
                """Check if stream has extracted data."""
                return self.records_extracted > 0

            @computed_field
            def is_active(self) -> bool:
                """Check if stream is active."""
                return self.status in c.Meltano.Enums.ACTIVE_STATUSES

            @computed_field
            def schema_properties_count(self) -> int:
                """Number of schema properties."""
                properties = self.stream_schema.get("properties", {})
                match properties:
                    case dict():
                        return len(properties)
                    case _:
                        return 0

            @field_serializer("stream_schema")
            def serialize_stream_schema(
                self,
                value: t.ContainerMapping,
            ) -> t.ContainerMapping:
                """Normalize stream schema structure."""
                result: t.MutableContainerMapping = dict(value)
                if "properties" not in result:
                    empty: t.MutableContainerMapping = {}
                    result["properties"] = empty
                if "type" not in result:
                    result["type"] = "t.NormalizedValue"
                return result

            @model_validator(mode="after")
            def validate_stream_definition(self) -> Self:
                """Validate stream definition consistency."""
                if "properties" not in self.stream_schema:
                    msg = "Stream schema must contain properties"
                    raise ValueError(msg)

                valid_statuses = c.Meltano.Enums.ACTIVE_STATUSES | {
                    c.Meltano.Enums.StreamStatus.COMPLETED,
                    c.Meltano.Enums.StreamStatus.ERROR,
                }
                if self.status not in valid_statuses:
                    msg = f"Status must be one of: {', '.join(valid_statuses)}"
                    raise ValueError(msg)

                return self

        class DataSinkDefinition(FlextCliModels.Entity):
            """Generic data sink definition for pipeline operations."""

            sink_name: Annotated[str, Field(description="Name of the sink")]
            sink_type: Annotated[str, Field(description="Type of the sink")]
            config: Annotated[
                t.ConfigurationMapping,
                Field(description="Sink configuration"),
            ] = Field(default_factory=dict)
            sink_schema: Annotated[
                t.FlatContainerMapping,
                Field(description="Sink schema"),
            ] = Field(default_factory=dict)
            status: Annotated[
                str,
                Field(
                    default=c.Meltano.Enums.StreamStatus.INITIALIZED,
                    description="Current status",
                ),
            ] = c.Meltano.Enums.StreamStatus.INITIALIZED

            @computed_field
            def config_keys_count(self) -> int:
                """Number of config keys."""
                keys = list(self.config.keys())
                return u.count(keys)

            @model_validator(mode="after")
            def validate_sink_definition(self) -> Self:
                """Validate sink definition consistency."""
                valid_statuses = {
                    c.Meltano.Enums.StreamStatus.INITIALIZED,
                    "configured",
                    "running",
                    c.Meltano.Enums.StreamStatus.COMPLETED,
                    c.Meltano.Enums.StreamStatus.ERROR,
                }
                if self.status not in valid_statuses:
                    msg = f"Status must be one of: {', '.join(valid_statuses)}"
                    raise ValueError(msg)

                return self

        class TapInstance(FlextCliModels.Entity):
            """Generic tap instance for data extraction."""

            tap_id: Annotated[
                str | None,
                Field(default=None, description="Unique tap identifier"),
            ] = None
            tap_type: Annotated[str, Field(description="Type of the tap")]
            config: Annotated[
                FlextMeltanoModels.Meltano.TapConfig,
                Field(description="Tap configuration"),
            ]
            adapter: Annotated[
                t.ContainerValue | None,
                Field(default=None, description="Tap adapter instance"),
            ] = None
            streams: Annotated[
                Sequence[FlextMeltanoModels.Meltano.StreamInfo],
                Field(
                    description="Available streams",
                ),
            ] = Field(default_factory=list)
            status: Annotated[
                str,
                Field(
                    default=c.Meltano.Enums.StreamStatus.INITIALIZED,
                    description="Tap status",
                ),
            ] = c.Meltano.Enums.StreamStatus.INITIALIZED

            @computed_field
            def active_streams(self) -> Sequence[FlextMeltanoModels.Meltano.StreamInfo]:
                """Active streams for extraction."""
                return [
                    s
                    for s in self.streams
                    if s.status in c.Meltano.Enums.ACTIVE_STATUSES
                ]

            @computed_field
            def stream_count(self) -> int:
                """Number of available streams."""
                return len(self.streams)

        class DataSourceInstance(FlextCliModels.Entity):
            """Generic data source instance for pipeline operations."""

            source_type: Annotated[str, Field(description="Type of the data source")]
            config: Annotated[
                FlextMeltanoModels.Meltano.DataSourceConfig,
                Field(description="Source configuration"),
            ]
            adapter: Annotated[
                t.ContainerValue | None,
                Field(default=None, description="Adapter instance"),
            ] = None
            status: Annotated[
                str,
                Field(
                    default=c.Meltano.Enums.StreamStatus.INITIALIZED,
                    description="Current status",
                ),
            ] = c.Meltano.Enums.StreamStatus.INITIALIZED
            streams: Annotated[
                Mapping[str, FlextMeltanoModels.Meltano.StreamDefinition],
                Field(description="Discovered streams"),
            ] = Field(default_factory=dict)
            discovered: Annotated[
                bool,
                Field(
                    default=False,
                    description="Whether streams have been discovered",
                ),
            ] = False
            metadata: Annotated[
                t.ConfigurationMapping,
                Field(description="Additional metadata"),
            ] = Field(default_factory=dict)
            source_id: Annotated[str, Field(description="Unique source identifier")]

            @computed_field
            def active_stream_count(self) -> int:
                """Number of active streams."""
                active_statuses = c.Meltano.Enums.ACTIVE_STATUSES
                return sum(
                    1
                    for stream in self.streams.values()
                    if stream.status in active_statuses
                )

            @computed_field
            def is_ready_for_extraction(self) -> bool:
                """Check if source is ready for data extraction."""
                streams_list: Sequence[FlextMeltanoModels.Meltano.StreamDefinition] = (
                    list(self.streams.values())
                )
                return (
                    self.discovered
                    and u.count(streams_list) > 0
                    and self.status == "configured"
                )

            @computed_field
            def stream_count(self) -> int:
                """Number of discovered streams."""
                return len(self.streams)

            @computed_field
            def total_records_extracted(self) -> int:
                """Total records extracted across all streams."""
                streams_list: Sequence[FlextMeltanoModels.Meltano.StreamDefinition] = (
                    list(self.streams.values())
                )
                result = u.agg(streams_list, "records_extracted", fn=sum)
                match result:
                    case int():
                        return result
                    case _:
                        return 0

            @model_validator(mode="after")
            def validate_source_instance(self) -> Self:
                """Validate source instance consistency."""
                if self.config.source_type != self.source_type:
                    msg = "Source type must match between instance and config"
                    raise ValueError(msg)

                if self.discovered and not self.streams:
                    msg = "Discovered source must have at least one stream"
                    raise ValueError(msg)

                return self

        class DataSinkInstance(FlextCliModels.Entity):
            """Generic data sink instance for pipeline operations."""

            sink_id: Annotated[
                str | None,
                Field(default=None, description="Unique sink identifier"),
            ] = None
            sink_type: Annotated[str, Field(description="Type of the data sink")]
            config: Annotated[
                FlextMeltanoModels.Meltano.DataSinkConfig,
                Field(description="Sink configuration"),
            ]
            adapter: Annotated[
                t.ContainerValue | None,
                Field(default=None, description="Adapter instance"),
            ] = None
            status: Annotated[
                str,
                Field(
                    default=c.Meltano.Enums.StreamStatus.INITIALIZED,
                    description="Current status",
                ),
            ] = c.Meltano.Enums.StreamStatus.INITIALIZED
            batch_size: Annotated[
                t.BatchSize,
                Field(default=1000, description="Batch processing size"),
            ] = 1000
            sink_count: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of configured sinks"),
            ] = 0

            @computed_field
            def is_ready(self) -> bool:
                """Check if sink is ready for processing."""
                return self.status == "configured" and self.adapter is not None

        # ========================================================================
        # DATA SINK CONFIGURATION - Generic sink configuration models
        # ========================================================================

        class DataSinkConfig(FlextCliModels.Entity):
            """Generic data sink configuration with validation."""

            sink_type: Annotated[str, Field(description="Sink type identifier")]
            connection_config: Annotated[
                t.ConfigurationMapping,
                Field(description="Connection configuration dictionary"),
            ]
            batch_size: Annotated[
                t.BatchSize,
                Field(
                    default=c.DEFAULT_SIZE,
                    description="Batch size for record processing",
                ),
            ]
            max_batches: Annotated[
                t.PositiveInt,
                Field(
                    default=c.DEFAULT_SIZE,
                    description="Maximum number of batches to process",
                ),
            ]

            @computed_field
            def max_records_capacity(self) -> int:
                """Maximum records capacity."""
                return self.batch_size * self.max_batches

            @computed_field
            def processing_efficiency(self) -> str:
                """Processing efficiency assessment."""
                if (
                    self.batch_size
                    >= c.Meltano.ModelValidation.EXECUTION_HIGH_PERFORMANCE_THRESHOLD
                ):
                    return "high"
                if (
                    self.batch_size
                    >= c.Meltano.ModelValidation.EXECUTION_GOOD_PERFORMANCE_THRESHOLD
                ):
                    return "medium"
                return "low"

            @computed_field
            def sink_identifier(self) -> str:
                """Unique sink identifier."""
                return f"{self.sink_type}:batch_{self.batch_size}"

            @field_serializer("connection_config")
            def serialize_connection_config(
                self,
                value: t.ConfigurationMapping,
            ) -> t.ConfigurationMapping:
                """Serialize connection config with sensitive data protection."""
                return FlextMeltanoModels._protect_sensitive_config(value)

            @model_validator(mode="after")
            def validate_sink_config(self) -> Self:
                """Validate sink configuration consistency."""
                if not self.sink_type or not self.sink_type.strip():
                    msg = "Sink type must be non-empty string"
                    raise ValueError(msg)

                max_reasonable_batch_size = (
                    c.Meltano.Logging.MELTANO_PERFORMANCE_THRESHOLD_CRITICAL
                )
                if self.batch_size > max_reasonable_batch_size:
                    msg = f"Batch size too large (max {max_reasonable_batch_size})"
                    raise ValueError(msg)

                return self

        class StreamInfo(FlextCliModels.Entity):
            """Generic stream information for data pipeline operations."""

            stream_name: Annotated[
                t.NonEmptyStr,
                Field(description="Stream name identifier"),
            ]
            stream_schema: Annotated[
                Mapping[str, t.Scalar | t.ScalarMapping],
                Field(description="Stream schema definition"),
            ]
            key_properties: Annotated[
                t.StrSequence,
                Field(
                    description="Primary key properties for the stream",
                ),
            ] = Field(default_factory=list)
            replication_method: Annotated[
                str,
                Field(
                    default="FULL_TABLE",
                    description="Replication method (FULL_TABLE, INCREMENTAL, LOG_BASED)",
                ),
            ]
            replication_key: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Field used for incremental replication",
                ),
            ]
            status: Annotated[
                str,
                Field(
                    default=c.Meltano.Enums.StreamStatus.INITIALIZED,
                    description="Stream processing status",
                ),
            ]
            records_loaded: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of records loaded"),
            ]
            batches_processed: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of batches processed"),
            ]
            stream_created_at: Annotated[str, Field(description="Creation timestamp")]

            @computed_field
            def average_records_per_batch(self) -> float:
                """Average records per batch."""
                if self.batches_processed == 0:
                    return 0.0
                return self.records_loaded / self.batches_processed

            @computed_field
            def has_processed_data(self) -> bool:
                """Check if stream has processed data."""
                return self.records_loaded > 0 or self.batches_processed > 0

            @computed_field
            def processing_status(self) -> str:
                """Processing status assessment."""
                if (
                    self.status == c.Meltano.Enums.StreamStatus.COMPLETED
                    and self.records_loaded > 0
                ):
                    return c.Meltano.Enums.StreamStatus.SUCCESS
                if self.status == c.Meltano.Enums.StreamStatus.ERROR:
                    return c.Meltano.Enums.StreamStatus.FAILED
                if self.records_loaded > 0:
                    return c.Meltano.Enums.StreamStatus.IN_PROGRESS
                return c.Meltano.Enums.StreamStatus.PENDING

            @model_validator(mode="after")
            def validate_stream_info(self) -> Self:
                """Validate stream information consistency."""
                if self.records_loaded > 0 and self.batches_processed == 0:
                    msg = "Records loaded but no batches processed"
                    raise ValueError(msg)

                valid_statuses = c.Meltano.Enums.VALID_STATUSES
                if self.status not in valid_statuses:
                    msg = f"Status must be one of: {', '.join(valid_statuses)}"
                    raise ValueError(msg)

                return self

        class SingerSchemaMessage(FlextCliModels.ArbitraryTypesModel):
            """Canonical Singer SCHEMA message model."""

            type: Annotated[
                Literal["SCHEMA"],
                Field(default="SCHEMA", description="Singer message discriminator"),
            ]
            stream: Annotated[
                t.NonEmptyStr,
                Field(description="Singer stream name"),
            ]
            schema_definition: Annotated[
                t.FlatContainerMapping,
                Field(
                    alias="schema",
                    serialization_alias="schema",
                    validation_alias="schema",
                    description="Singer JSON schema payload",
                ),
            ]
            key_properties: Annotated[
                t.StrSequence,
                Field(description="Singer stream key properties"),
            ] = Field(default_factory=list)
            bookmark_properties: Annotated[
                t.StrSequence,
                Field(
                    description="Singer bookmark columns for incremental replication",
                ),
            ] = Field(default_factory=list)

        class SingerRecordMessage(FlextCliModels.ArbitraryTypesModel):
            """Canonical Singer RECORD message model."""

            type: Annotated[
                Literal["RECORD"],
                Field(default="RECORD", description="Singer message discriminator"),
            ]
            stream: Annotated[
                str,
                Field(description="Singer stream name"),
            ]
            record: Annotated[
                t.FlatContainerMapping,
                Field(description="Singer record payload"),
            ]
            time_extracted: Annotated[
                str | None,
                Field(
                    default=None,
                    description="ISO 8601 timestamp when the record was extracted",
                ),
            ]
            version: Annotated[
                int | None,
                Field(
                    default=None,
                    description="Stream version number for activate_version protocol",
                ),
            ]

        class SingerStateMessage(FlextCliModels.ArbitraryTypesModel):
            """Canonical Singer STATE message model."""

            type: Annotated[
                Literal["STATE"],
                Field(default="STATE", description="Singer message discriminator"),
            ] = "STATE"
            value: Annotated[
                t.MutableContainerMapping,
                Field(
                    description="Singer state bookmark payload",
                ),
            ] = Field(default_factory=dict)

        class SingerActivateVersionMessage(FlextCliModels.ArbitraryTypesModel):
            """Canonical Singer ACTIVATE_VERSION message model.

            Sent by a tap to signal that all records for a stream version
            have been emitted. The target should remove any records not
            matching this version.
            """

            type: Annotated[
                Literal["ACTIVATE_VERSION"],
                Field(
                    default="ACTIVATE_VERSION",
                    description="Singer message discriminator",
                ),
            ]
            stream: Annotated[
                str,
                Field(description="Singer stream name"),
            ]
            version: Annotated[
                t.PositiveInt,
                Field(description="Stream version to activate"),
            ]

        class SingerStateEntry(FlextCliModels.Entity):
            """Singer state entry for a stream bookmark.

            Tracks per-stream incremental sync bookmarks with validation
            ensuring bookmark_key and bookmark_value are both set or both None.
            """

            stream_name: Annotated[str, Field(description="Name of the stream")]
            bookmark_key: Annotated[
                str | None,
                Field(default=None, description="Bookmark field for incremental"),
            ]
            bookmark_value: Annotated[
                str | None,
                Field(default=None, description="Current bookmark value"),
            ]

            @model_validator(mode="after")
            def validate_bookmark(self) -> Self:
                """Ensure bookmark_key and bookmark_value are both set or both None."""
                if (self.bookmark_key is None) != (self.bookmark_value is None):
                    msg = "bookmark_key and bookmark_value must both be set or both be None"
                    raise ValueError(msg)
                return self

        class SingerCatalogMetadata(FlextCliModels.ArbitraryTypesModel):
            """Singer catalog metadata block model."""

            breadcrumb: Annotated[
                t.StrSequence,
                Field(
                    description="Singer metadata breadcrumb path",
                ),
            ] = Field(default_factory=list)
            metadata: Annotated[
                t.ContainerMapping,
                Field(description="Singer metadata properties"),
            ] = Field(default_factory=dict)

        class SingerCatalogEntry(FlextCliModels.ArbitraryTypesModel):
            """Singer catalog stream entry model."""

            tap_stream_id: Annotated[
                str,
                Field(description="Tap stream identifier"),
            ]
            stream: Annotated[
                str,
                Field(description="Singer stream name"),
            ]
            schema_definition: Annotated[
                t.FlatContainerMapping,
                Field(
                    alias="schema",
                    serialization_alias="schema",
                    validation_alias="schema",
                    description="Singer stream schema payload",
                ),
            ]
            metadata: Annotated[
                Sequence[FlextMeltanoModels.Meltano.SingerCatalogMetadata],
                Field(
                    description="Singer stream metadata blocks",
                ),
            ] = Field(default_factory=list)
            key_properties: Annotated[
                t.StrSequence,
                Field(
                    description="Primary key columns for this stream",
                ),
            ] = Field(default_factory=list)
            replication_key: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Column used for incremental replication",
                ),
            ]
            replication_method: Annotated[
                (Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"] | None),
                Field(default=None, description="Replication method for this stream"),
            ]
            is_view: Annotated[
                bool | None,
                Field(
                    default=None,
                    description="Whether this stream is a database view",
                ),
            ]
            table_name: Annotated[
                str | None,
                Field(default=None, description="Source table name"),
            ]
            database_name: Annotated[
                str | None,
                Field(default=None, description="Source database name"),
            ]
            row_count: Annotated[
                int | None,
                Field(default=None, description="Estimated row count from source"),
            ]

        class SingerCatalog(FlextCliModels.ArbitraryTypesModel):
            """Singer catalog response model."""

            type: Annotated[
                Literal["CATALOG"],
                Field(
                    default="CATALOG",
                    description="Singer catalog message discriminator",
                ),
            ] = "CATALOG"
            streams: Annotated[
                Sequence[FlextMeltanoModels.Meltano.SingerCatalogEntry],
                Field(
                    description="Singer catalog stream entries",
                ),
            ] = Field(default_factory=list)

        class SingerPipelineConfig(FlextCliModels.Entity):
            """Configuration for a Singer ELT pipeline."""

            tap_config_path: Annotated[
                Path | None,
                Field(default=None, description="Path to tap configuration"),
            ]
            target_config_path: Annotated[
                Path | None,
                Field(default=None, description="Path to target configuration"),
            ]
            catalog_path: Annotated[
                Path | None,
                Field(default=None, description="Path to catalog file"),
            ]
            state_path: Annotated[
                Path | None,
                Field(default=None, description="Path to state file"),
            ]
            selected_streams: Annotated[
                t.StrSequence | None,
                Field(default=None, description="Specific streams to sync"),
            ]

        class SingerSyncResult(FlextCliModels.Entity):
            """Result of a Singer sync operation."""

            records_processed: Annotated[
                t.NonNegativeInt,
                Field(description="Number of records processed"),
            ]
            records_written: Annotated[
                t.NonNegativeInt,
                Field(description="Number of records written"),
            ]
            errors: Annotated[t.NonNegativeInt, Field(description="Number of errors")]
            state: Annotated[
                t.ContainerMapping,
                Field(description="Final state payload"),
            ] = Field(default_factory=dict)
            duration_seconds: Annotated[
                t.NonNegativeFloat,
                Field(description="Execution duration"),
            ]

        # ========================================================================
        # API PAYLOAD MODELS - Typed payloads for API operations
        # ========================================================================

        class CreatePipelinePayload(FlextCliModels.ArbitraryTypesModel):
            """Payload for create_pipeline operation."""

            tap_name: Annotated[t.NonEmptyStr, Field(description="Singer tap name")]
            target_name: Annotated[
                str,
                Field(description="Singer target name"),
            ]
            config: Annotated[
                t.ContainerMapping,
                Field(description="Pipeline config"),
            ] = Field(default_factory=dict)

        class ExecutePipelinePayload(FlextCliModels.ArbitraryTypesModel):
            """Payload for execute_pipeline operation."""

            pipeline_id: Annotated[
                str,
                Field(description="Pipeline identifier"),
            ]
            config: Annotated[
                t.ContainerMapping,
                Field(description="Execution config"),
            ] = Field(default_factory=dict)

        class InstallPluginPayload(FlextCliModels.ArbitraryTypesModel):
            """Payload for install_plugin operation."""

            plugin_type: Annotated[t.NonEmptyStr, Field(description="Plugin type")]
            plugin_name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
            config: Annotated[
                t.ContainerMapping,
                Field(description="Plugin config"),
            ] = Field(default_factory=dict)

        class ListPluginsPayload(FlextCliModels.ArbitraryTypesModel):
            """Payload for list_plugins operation."""

            plugin_type: Annotated[
                str | None,
                Field(default=None, description="Filter by plugin type"),
            ]

        class ConfigureEnvironmentPayload(FlextCliModels.ArbitraryTypesModel):
            """Payload for configure_environment operation."""

            environment_name: Annotated[
                str,
                Field(description="Environment name"),
            ]
            config: Annotated[
                t.ContainerMapping,
                Field(description="Environment config"),
            ] = Field(default_factory=dict)

        class RunDbtModelsPayload(FlextCliModels.ArbitraryTypesModel):
            """Payload for run/test dbt models operation."""

            models: Annotated[
                t.StrSequence | None,
                Field(default=None, description="Models to run"),
            ]
            config: Annotated[
                t.ContainerMapping | None,
                Field(default=None, description="Execution config"),
            ]

        class RunEltPipelinePayload(FlextCliModels.ArbitraryTypesModel):
            """Payload for run_elt_pipeline operation."""

            tap_name: Annotated[t.NonEmptyStr, Field(description="Singer tap name")]
            target_name: Annotated[
                str,
                Field(description="Singer target name"),
            ]
            dbt_models: Annotated[
                t.StrSequence | None,
                Field(default=None, description="DBT models to run"),
            ]
            config: Annotated[
                t.ContainerMapping | None,
                Field(default=None, description="Pipeline config"),
            ]

        class JsonSchemaPayload(FlextCliModels.ArbitraryTypesModel):
            """Typed schema payload used by API extract flow."""

            schema_definition: Annotated[
                t.FlatContainerMapping,
                Field(
                    alias="schema",
                    serialization_alias="schema",
                    validation_alias="schema",
                    description="Schema-like JSON payload",
                ),
            ] = Field(default_factory=dict)

            @field_validator("schema_definition", mode="before")
            @classmethod
            def normalize_schema(cls, value: _ValidatorInput) -> t.ContainerMapping:
                """Normalize mapping input before JSON validation."""
                match value:
                    case Mapping():
                        return {str(key): item for key, item in value.items()}
                    case _:
                        empty_schema: t.ContainerMapping = {}
                        return empty_schema

        class JsonRecordBatchPayload(FlextCliModels.ArbitraryTypesModel):
            """Typed record batch payload used by API load flow."""

            records: Annotated[
                Sequence[t.FlatContainerMapping],
                Field(description="Normalized record payloads"),
            ] = Field(default_factory=list)

            @field_validator("records", mode="before")
            @classmethod
            def normalize_records(
                cls,
                value: _ValidatorInput,
            ) -> Sequence[t.FlatContainerMapping] | t.StrSequence:
                """Normalize mixed record input into dict records."""
                match value:
                    case list() | tuple():
                        records: MutableSequence[t.FlatContainerMapping] = []
                        for record in value:
                            match record:
                                case Mapping():
                                    # Type narrowing: convert mapping items to t.NormalizedValue
                                    record_dict: t.MutableFlatContainerMapping = {}
                                    for key, item in record.items():
                                        # Only include JSON-serializable values (exclude None, BaseModel, Path)
                                        if u.is_primitive(item):
                                            record_dict[str(key)] = item
                                    records.append(record_dict)
                                case _:
                                    continue
                        return records
                    case _:
                        return []

        class ConfigMappingPayload(FlextCliModels.ArbitraryTypesModel):
            """Normalized mapping payload with string keys."""

            values: Annotated[
                Mapping[
                    str,
                    t.Scalar
                    | Sequence[t.Scalar | None]
                    | Mapping[str, t.Scalar | None]
                    | None,
                ],
                Field(description="Normalized mapping values"),
            ] = Field(default_factory=dict)

            @field_validator("values", mode="before")
            @classmethod
            def normalize_values(
                cls,
                value: _ValidatorInput,
            ) -> Mapping[
                str,
                t.Scalar
                | Sequence[t.Scalar | None]
                | Mapping[str, t.Scalar | None]
                | None,
            ]:
                """Normalize mapping-like payloads to Mapping[str, value]."""
                if not isinstance(value, Mapping):
                    return {}
                result: MutableMapping[
                    str,
                    t.Scalar
                    | Sequence[t.Scalar | None]
                    | Mapping[str, t.Scalar | None]
                    | None,
                ] = {}
                for key, item in value.items():
                    if u.is_scalar(item) or item is None:
                        result[str(key)] = item
                    elif isinstance(item, list):
                        result[str(key)] = [
                            v if u.is_scalar(v) or v is None else str(v) for v in item
                        ]
                    elif isinstance(item, Mapping):
                        result[str(key)] = {
                            str(k): v if u.is_scalar(v) or v is None else str(v)
                            for k, v in item.items()
                        }
                    else:
                        result[str(key)] = str(item)
                return result

        class PathPayload(FlextCliModels.ArbitraryTypesModel):
            """Path normalization payload for runtime path conversions."""

            value: Annotated[
                Path,
                Field(description="Normalized path"),
            ] = Field(default_factory=Path)

            @field_validator("value", mode="before")
            @classmethod
            def normalize_path(cls, value: _ValidatorInput) -> Path:
                """Normalize mixed path input into Path objects."""
                if value is None:
                    return Path()
                return Path(str(value))

        class FileContentPayload(FlextCliModels.ArbitraryTypesModel):
            """Normalize str|dict content to writable string for file operations."""

            content: Annotated[
                str,
                Field(default="", description="Normalized writable string content"),
            ]

            @field_validator("content", mode="before")
            @classmethod
            def normalize_content(cls, value: _ValidatorInput) -> str:
                """Normalize dict content via yaml.dump, pass str through."""
                match value:
                    case Mapping():
                        return yaml.dump(
                            dict(value),
                            default_flow_style=False,
                            indent=2,
                            allow_unicode=True,
                        )
                    case None:
                        return ""
                    case _:
                        return str(value)

        class VariantPayload(FlextCliModels.ArbitraryTypesModel):
            """Normalize plugin variant from external extraction (str|list|dict)."""

            value: Annotated[
                str | t.StrSequence | t.ScalarMapping | None,
                Field(default=None, description="Normalized variant value"),
            ]

            @field_validator("value", mode="before")
            @classmethod
            def normalize_variant(
                cls,
                value: _ValidatorInput,
            ) -> str | t.StrSequence | t.ScalarMapping | None:
                """Normalize variant_raw into typed union."""
                match value:
                    case None:
                        return None
                    case str():
                        return value
                    case list() | tuple():
                        return [str(item) for item in value]
                    case Mapping():
                        result: t.MutableConfigurationMapping = {}
                        for k, v in value.items():
                            # Type narrowing for JSON-serializable primitives
                            if u.is_primitive(v):
                                result[str(k)] = v
                            elif v is None:
                                result[str(k)] = ""
                            elif isinstance(v, (list, dict)):
                                result[str(k)] = str(v)
                        return result
                    case _:
                        return str(value)

        class PluginDiscoverySource(FlextCliModels.ArbitraryTypesModel):
            """Normalized raw plugin discovery payload from external sources."""

            default_variant: Annotated[
                str,
                Field(default="", description="Plugin default variant"),
            ]
            variants: Annotated[
                t.ContainerMapping,
                Field(description="Available plugin variants"),
            ] = Field(default_factory=dict)
            logo_url: Annotated[str, Field(default="", description="Plugin logo URL")]
            description: Annotated[
                str,
                Field(default="", description="Plugin description"),
            ]

            @field_validator(
                "default_variant",
                "logo_url",
                "description",
                mode="before",
            )
            @classmethod
            def normalize_string_fields(cls, value: _ValidatorInput) -> str:
                """Normalize optional string fields from external payloads."""
                return "" if value is None else str(value)

            @field_validator("variants", mode="before")
            @classmethod
            def normalize_variants(cls, value: _ValidatorInput) -> t.ContainerMapping:
                """Normalize variant maps from external payloads."""
                match value:
                    case Mapping():
                        return {str(key): item for key, item in value.items()}
                    case _:
                        empty: t.ContainerMapping = {}
                        return empty

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

        class PluginDiscoveryItem(FlextCliModels.ArbitraryTypesModel):
            """Typed plugin discovery response item."""

            name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
            type: Annotated[t.NonEmptyStr, Field(description="Plugin type")]
            default_variant: Annotated[
                str,
                Field(default="", description="Default plugin variant"),
            ]
            variants: Annotated[
                str,
                Field(default="", description="Comma-separated variants"),
            ]
            logo_url: Annotated[str, Field(default="", description="Plugin logo URL")]
            description: Annotated[
                str,
                Field(default="", description="Plugin description"),
            ]

        class PluginDiscoveryCatalog(FlextCliModels.ArbitraryTypesModel):
            """Typed plugin discovery catalog keyed by plugin name."""

            plugins: Mapping[str, FlextMeltanoModels.Meltano.PluginDiscoverySource] = (
                Field(default_factory=dict, description="Discovered plugins catalog")
            )

            @field_validator("plugins", mode="before")
            @classmethod
            def normalize_plugins(cls, value: _ValidatorInput) -> t.ContainerMapping:
                """Normalize plugin catalog mapping."""
                match value:
                    case Mapping():
                        return {str(key): item for key, item in value.items()}
                    case _:
                        empty: t.ContainerMapping = {}
                        return empty

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

        class PipelineExecutionContext(FlextCliModels.ArbitraryTypesModel):
            """Typed context envelope for ELT pipeline execution."""

            project_root: Annotated[str, Field(description="Project root path")]
            elt_context: Annotated[
                t.ContainerMapping,
                Field(description="ELT execution context"),
            ] = Field(default_factory=dict)
            extractor_name: Annotated[
                str,
                Field(description="Extractor name"),
            ]
            loader_name: Annotated[t.NonEmptyStr, Field(description="Loader name")]
            execution_completed: Annotated[
                bool,
                Field(default=False, description="Execution completion flag"),
            ]
            execution_result: Annotated[
                t.ContainerMapping,
                Field(description="Execution result payload"),
            ] = Field(default_factory=dict)

            @field_validator("elt_context", "execution_result", mode="before")
            @classmethod
            def normalize_mapping_payloads(
                cls,
                value: _ValidatorInput,
            ) -> t.ContainerMapping:
                """Normalize mapping-like payloads into dictionaries."""
                match value:
                    case Mapping():
                        return {str(key): item for key, item in value.items()}
                    case _:
                        empty: t.ContainerMapping = {}
                        return empty

            @field_validator(
                "project_root",
                "extractor_name",
                "loader_name",
                mode="before",
            )
            @classmethod
            def normalize_required_strings(cls, value: _ValidatorInput) -> str:
                """Normalize required string fields from context payloads."""
                normalized = "" if value is None else str(value)
                return normalized.strip()

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

        class PipelineResultContext(FlextCliModels.ArbitraryTypesModel):
            """Typed subset for extracting final pipeline result fields."""

            project_root: Annotated[
                str,
                Field(default="unknown", description="Project root path"),
            ]
            execution_result: Annotated[
                t.ContainerMapping,
                Field(description="Execution result payload"),
            ] = Field(default_factory=dict)

            @field_validator("execution_result", mode="before")
            @classmethod
            def normalize_execution_result(
                cls,
                value: _ValidatorInput,
            ) -> t.ContainerMapping:
                """Normalize execution result map payload."""
                match value:
                    case Mapping():
                        return {str(key): item for key, item in value.items()}
                    case _:
                        empty: t.ContainerMapping = {}
                        return empty

            @field_validator("project_root", mode="before")
            @classmethod
            def normalize_project_root(cls, value: _ValidatorInput) -> str:
                """Normalize project root from mixed payload values."""
                normalized = "unknown" if value is None else str(value)
                return normalized.strip() or "unknown"

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

        class PipelineExecutionScalarMap(FlextCliModels.ArbitraryTypesModel):
            """Scalar-only pipeline execution values normalized to strings."""

            values: Annotated[
                t.StrMapping,
                Field(
                    description="Execution values filtered to scalar strings",
                ),
            ] = Field(default_factory=dict)

            @field_validator("values", mode="before")
            @classmethod
            def normalize_values(cls, value: _ValidatorInput) -> t.StrMapping:
                """Keep scalar execution values and stringify them."""
                match value:
                    case Mapping():
                        return {
                            str(key): str(item)
                            for key, item in value.items()
                            if u.is_type(item, (str, int, bool, float))
                        }
                    case _:
                        return {}

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

        class PluginComponentConfig(FlextCliModels.Entity):
            """Validated plugin component configuration for pipeline validators."""

            name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
            namespace: Annotated[
                str,
                Field(description="Plugin namespace"),
            ]
            pip_url: Annotated[t.NonEmptyStr, Field(description="Plugin pip URL")]
            executable: Annotated[
                str,
                Field(description="Plugin executable"),
            ]
            type: Annotated[str, Field(default="extractor", description="Plugin type")]

            @field_validator("name")
            @classmethod
            def validate_name_business_rules(cls, v: str) -> str:
                """Validate plugin name business rules."""
                v = v.strip()
                if not v:
                    msg = "Plugin name cannot be empty"
                    raise ValueError(msg)
                if (
                    v.startswith("target-")
                    and len(v) < c.Meltano.Plugin.MIN_TARGET_PLUGIN_NAME_LENGTH
                ):
                    msg = "Target plugin names must be at least 8 characters"
                    raise ValueError(msg)
                if (
                    v.startswith("tap-")
                    and len(v) < c.Meltano.Plugin.MIN_TAP_PLUGIN_NAME_LENGTH
                ):
                    msg = "Source component names must be at least 5 characters"
                    raise ValueError(msg)
                return v

        class DbtManifestNode(FlextCliModels.ArbitraryTypesModel):
            """Parsed dbt manifest node with typed fields."""

            name: Annotated[str | None, Field(default=None, description="Node name")]
            path: Annotated[str | None, Field(default=None, description="Node path")]
            description: Annotated[
                str | None,
                Field(default=None, description="Node description"),
            ]
            fqn: Annotated[
                t.StrSequence,
                Field(description="Fully qualified name parts"),
            ] = Field(default_factory=list)
            resource_type: Annotated[
                str,
                Field(default="", description="Node resource type (model, test, etc.)"),
            ]

            @computed_field
            def fqn_string(self) -> str:
                """Fully qualified name as dot-separated string."""
                return ".".join(self.fqn) if self.fqn else ""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

        class DbtManifest(FlextCliModels.ArbitraryTypesModel):
            """Parsed dbt manifest with typed nodes."""

            nodes: Annotated[
                Mapping[str, FlextMeltanoModels.Meltano.DbtManifestNode],
                Field(
                    description="Manifest nodes keyed by node_id",
                ),
            ] = Field(default_factory=dict)

            def get_nodes_by_type(
                self,
                resource_type: str,
            ) -> Sequence[FlextMeltanoModels.Meltano.DbtManifestNode]:
                """Get all nodes of a specific resource type."""
                return [
                    node
                    for node in self.nodes.values()
                    if node.resource_type == resource_type
                ]

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")

        # ========================================================================
        # PROJECT MODELS - Generic project configuration and validation
        # ========================================================================

        class MeltanoProjectModel(FlextCliModels.Entity):
            """Generic Meltano project configuration with validation."""

            project_id: Annotated[str, Field(description="Unique project identifier")]
            project_version: Annotated[
                str,
                Field(default="1", description="Project version"),
            ]
            default_environment: Annotated[
                str,
                Field(default="dev", description="Default environment name"),
            ]
            plugins: Annotated[
                t.ContainerMapping,
                Field(description="Plugin configurations"),
            ] = Field(default_factory=dict)
            environments: Annotated[
                t.ContainerMapping,
                Field(description="Environment configurations"),
            ] = Field(default_factory=dict)

            @model_validator(mode="after")
            def validate_meltano_project(self) -> Self:
                """Validate Meltano project configuration consistency."""
                if not self.project_id or not self.project_id.strip():
                    msg = "project_id cannot be empty"
                    raise ValueError(msg)

                return self

        class PipelineProjectModel(FlextCliModels.Entity):
            """Generic pipeline project configuration with validation."""

            version: Annotated[
                int,
                Field(
                    default=1,
                    ge=1,
                    le=1,
                    description="Project version (only version 1 supported)",
                ),
            ] = 1
            project_id: Annotated[
                str,
                Field(description="Project ID required"),
            ]
            default_environment: Annotated[
                str,
                Field(default="dev", description="Default environment"),
            ]
            project_root: Annotated[
                Path,
                Field(description="Project root directory"),
            ] = Field(default_factory=Path.cwd)
            environments: Annotated[
                t.StrSequence,
                Field(
                    description="Available environments",
                ),
            ] = Field(default_factory=lambda: ["dev", "staging", "prod"])

            @computed_field
            def environment_count(self) -> int:
                """Number of environments."""
                return u.count(self.environments)

            @computed_field
            def has_production_environment(self) -> bool:
                """Check if production environment exists."""
                prod_environments = {"prod", "production", "live"}
                normalized_envs = [
                    u.normalize(env, case="lower") for env in self.environments
                ]
                # Convert prod_environments set to list for u.in_
                prod_envs_list: t.StrSequence = list(prod_environments)
                return u.any_(*[u.in_(env, prod_envs_list) for env in normalized_envs])

            @computed_field
            def project_maturity(self) -> str:
                """Project maturity assessment."""
                prod_envs = {"prod", "production", "live"}
                normalized_envs = [
                    u.normalize(env, case="lower") for env in self.environments
                ]
                # Convert prod_envs set to list for u.in_
                prod_envs_list: t.StrSequence = list(prod_envs)
                has_prod = u.any_(*[
                    u.in_(env, prod_envs_list) for env in normalized_envs
                ])
                env_count = u.count(self.environments)

                if (
                    has_prod
                    and env_count >= c.Meltano.ModelValidation.MATURITY_MATURE_ENV_COUNT
                ):
                    return "mature"
                if env_count >= c.Meltano.ModelValidation.MATURITY_DEVELOPING_ENV_COUNT:
                    return "developing"
                return "basic"

            @model_validator(mode="after")
            def validate_project_consistency(self) -> Self:
                """Validate project consistency."""
                if self.default_environment not in self.environments:
                    msg = (
                        f"Default environment '{self.default_environment}' "
                        f"not in environments list"
                    )
                    raise ValueError(msg)

                if not self.project_root.exists():
                    msg = f"Project root directory does not exist: {self.project_root}"
                    raise ValueError(msg)

                return self

        class PluginModel(FlextCliModels.TimestampedModel):
            """Generic plugin configuration for pipeline operations."""

            name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
            namespace: Annotated[str, Field(description="Plugin namespace")]
            pip_url: Annotated[
                str | None,
                Field(default=None, description="Plugin pip URL"),
            ]
            executable: Annotated[
                str | None,
                Field(default=None, description="Plugin executable"),
            ]
            variant: Annotated[
                str,
                Field(default="standard", description="Plugin variant"),
            ]
            settings: Annotated[
                t.ContainerMapping,
                Field(description="Plugin settings"),
            ] = Field(default_factory=dict)
            capabilities: Annotated[
                t.StrSequence,
                Field(description="Plugin capabilities"),
            ] = Field(default_factory=list)
            config_files: Annotated[
                t.StrSequence,
                Field(description="Plugin configuration files"),
            ] = Field(default_factory=list)

            @computed_field
            def full_plugin_name(self) -> str:
                """Full plugin name with namespace."""
                return f"{self.namespace}.{self.name}"

            @computed_field
            def has_custom_executable(self) -> bool:
                """Check if plugin has custom executable."""
                return self.executable is not None

            @computed_field
            def plugin_complexity(self) -> str:
                """Plugin complexity assessment."""
                settings_keys = list(self.settings.keys())
                settings_count = u.count(settings_keys)
                if settings_count == 0:
                    return "minimal"
                if (
                    settings_count
                    <= c.Meltano.ModelValidation.COMPLEXITY_SIMPLE_MAX_SETTINGS
                ):
                    return "simple"
                if (
                    settings_count
                    <= c.Meltano.ModelValidation.COMPLEXITY_MODERATE_MAX_SETTINGS
                ):
                    return "moderate"
                return "complex"

            @computed_field
            def settings_count(self) -> int:
                """Number of plugin settings."""
                keys: t.StrSequence = list(self.settings.keys())
                return u.count(keys)

            @model_validator(mode="after")
            def validate_plugin_consistency(self) -> Self:
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

        class DbtProjectModel(FlextCliModels.Entity):
            """Generic DBT project configuration with validation."""

            name: Annotated[str, Field(description="DBT project name")]
            profile: Annotated[str, Field(description="DBT profile name")]
            dbt_version: Annotated[
                str,
                Field(default="1.0.0", description="DBT project version"),
            ]
            config: Annotated[
                t.ContainerMapping,
                Field(description="DBT project configuration"),
            ] = Field(default_factory=dict)
            models: Annotated[
                t.ContainerMapping,
                Field(description="DBT models configuration"),
            ] = Field(default_factory=dict)
            sources: Annotated[
                t.ContainerMapping,
                Field(description="DBT sources configuration"),
            ] = Field(default_factory=dict)
            tests: Annotated[
                t.ContainerMapping,
                Field(description="DBT tests configuration"),
            ] = Field(default_factory=dict)

            @model_validator(mode="after")
            def validate_dbt_project(self) -> Self:
                """Validate DBT project configuration consistency."""
                if not self.name or not self.name.strip():
                    msg = "name cannot be empty"
                    raise ValueError(msg)

                if not self.profile or not self.profile.strip():
                    msg = "profile cannot be empty"
                    raise ValueError(msg)

                return self

        class TransformationProjectModel(FlextCliModels.Entity):
            """Generic transformation project configuration with validation."""

            name: Annotated[t.NonEmptyStr, Field(description="Project name")]
            transformation_version: Annotated[str, Field(description="Project version")]
            profile: Annotated[str, Field(description="Profile name")]
            model_paths: Annotated[
                t.StrSequence,
                Field(default=["models"], description="Model paths"),
            ]
            analysis_paths: Annotated[
                t.StrSequence,
                Field(default=["analysis"], description="Analysis paths"),
            ]
            test_paths: Annotated[
                t.StrSequence,
                Field(default=["tests"], description="Test paths"),
            ]
            seed_paths: Annotated[
                t.StrSequence,
                Field(default=["seeds"], description="Seed paths"),
            ]
            macro_paths: Annotated[
                t.StrSequence,
                Field(default=["macros"], description="Macro paths"),
            ]

            @computed_field
            def has_custom_paths(self) -> bool:
                """Check if project has custom paths."""
                default_paths = {"models", "analysis", "tests", "seeds", "macros"}
                all_paths = {
                    *self.model_paths,
                    *self.analysis_paths,
                    *self.test_paths,
                    *self.seed_paths,
                    *self.macro_paths,
                }
                return bool(all_paths - default_paths)

            @computed_field
            def project_structure_complexity(self) -> str:
                """Project structure complexity."""
                # Use u.count() for unified counting (DSL pattern)
                total_path_count = (
                    u.count(self.model_paths)
                    + u.count(self.analysis_paths)
                    + u.count(self.test_paths)
                    + u.count(self.seed_paths)
                    + u.count(self.macro_paths)
                )
                if (
                    total_path_count
                    <= c.Meltano.ModelValidation.STRUCTURE_SIMPLE_MAX_PATHS
                ):
                    return "simple"
                if (
                    total_path_count
                    <= c.Meltano.ModelValidation.STRUCTURE_MODERATE_MAX_PATHS
                ):
                    return "moderate"
                return "complex"

            @computed_field
            def total_path_count(self) -> int:
                """Total number of configured paths."""
                # Use u.count() for unified counting (DSL pattern)
                return (
                    u.count(self.model_paths)
                    + u.count(self.analysis_paths)
                    + u.count(self.test_paths)
                    + u.count(self.seed_paths)
                    + u.count(self.macro_paths)
                )

            @model_validator(mode="after")
            def validate_project_consistency(self) -> Self:
                """Validate project consistency."""
                if not self.model_paths:
                    msg = "Project must have at least one model path"
                    raise ValueError(msg)

                return self

        class TransformationExecutionModel(FlextCliModels.Entity):
            """Generic transformation execution configuration with validation."""

            command: Annotated[str, Field(description="Command to execute")]
            models: Annotated[
                t.StrSequence,
                Field(description="Models to execute"),
            ] = Field(default_factory=list)
            exclude: Annotated[
                t.StrSequence,
                Field(description="Models to exclude"),
            ] = Field(default_factory=list)
            full_refresh: Annotated[
                bool,
                Field(default=False, description="Full refresh execution"),
            ]
            fail_fast: Annotated[
                bool,
                Field(default=True, description="Fail fast on first error"),
            ]
            threads: Annotated[
                t.WorkerCount,
                Field(default=1, description="Number of threads to use"),
            ]

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
                if (
                    total_scope
                    <= c.Meltano.ModelValidation.DBT_SIMPLE_EXECUTION_THRESHOLD
                ):
                    return "simple"
                if total_scope <= c.Meltano.ModelValidation.MAX_WORKERS_THRESHOLD:
                    return "moderate"
                return "complex"

            @computed_field
            def is_parallel_execution(self) -> bool:
                """Check if execution uses multiple threads."""
                return self.threads > 1

            @computed_field
            def model_count(self) -> int:
                """Number of models to execute."""
                return len(self.models)

            @model_validator(mode="after")
            def validate_execution_consistency(self) -> Self:
                """Validate execution consistency."""
                max_threads = (
                    c.Meltano.ModelValidation.MAX_WORKERS_THRESHOLD // 3
                )  # ~33, reasonable thread limit
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

        class ExecutionResult(FlextCliModels.TimestampedModel):
            """Generic execution result tracking with validation."""

            operation: Annotated[str, Field(description="Operation performed")]
            status: Annotated[str, Field(description="Execution status")]
            start_time: Annotated[
                datetime,
                Field(
                    description="Execution start time",
                ),
            ] = Field(default_factory=lambda: datetime.now(tz=UTC))
            end_time: Annotated[
                datetime | None,
                Field(default=None, description="Execution end time"),
            ]
            duration_seconds: Annotated[
                float | None,
                Field(default=None, description="Execution duration in seconds"),
            ]
            records_processed: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of records processed"),
            ]
            error_message: Annotated[
                str | None,
                Field(default=None, description="Error message if failed"),
            ]
            metadata: Annotated[
                t.ConfigurationMapping,
                Field(
                    description="Additional execution metadata",
                ),
            ] = Field(default_factory=dict)

            @computed_field
            def execution_rate_per_second(self) -> float:
                """Execution rate (records/second)."""
                if not self.duration_seconds or self.duration_seconds <= 0:
                    return 0.0
                return self.records_processed / self.duration_seconds

            @computed_field
            def is_completed(self) -> bool:
                """Check if execution is completed."""
                return self.end_time is not None

            @computed_field
            def is_successful(self) -> bool:
                """Check if execution was successful."""
                return (
                    self.status == c.Meltano.Enums.OperationStatus.SUCCESS
                    and self.error_message is None
                )

            @computed_field
            def performance_category(self) -> str:
                """Performance categorization."""
                if not self.duration_seconds or self.duration_seconds <= 0:
                    rate = 0.0
                else:
                    rate = self.records_processed / self.duration_seconds

                if (
                    rate
                    >= c.Meltano.ModelValidation.EXECUTION_HIGH_PERFORMANCE_THRESHOLD
                ):
                    return "high_performance"
                if (
                    rate
                    >= c.Meltano.ModelValidation.EXECUTION_GOOD_PERFORMANCE_THRESHOLD
                ):
                    return "good_performance"
                if (
                    rate
                    >= c.Meltano.ModelValidation.EXECUTION_MODERATE_PERFORMANCE_THRESHOLD
                ):
                    return "moderate_performance"
                return "low_performance"

            @field_validator("status", mode="before")
            @classmethod
            def validate_status(cls, v: str) -> str:
                """Validate execution status."""
                valid_statuses = [
                    c.Meltano.Enums.OperationStatus.PENDING,
                    c.Meltano.Enums.OperationStatus.RUNNING,
                    c.Meltano.Enums.OperationStatus.SUCCESS,
                    c.Meltano.Enums.OperationStatus.ERROR,
                    c.Meltano.Enums.OperationStatus.TIMEOUT,
                ]
                if v not in valid_statuses:
                    msg = f"Status must be one of: {', '.join(valid_statuses)}"
                    raise ValueError(msg)
                return v

            @model_validator(mode="after")
            def validate_execution_result(self) -> Self:
                """Validate execution result consistency."""
                if self.start_time and self.end_time:
                    calculated_duration = (
                        self.end_time - self.start_time
                    ).total_seconds()
                    if self.duration_seconds is None:
                        self.duration_seconds = calculated_duration
                    elif abs(self.duration_seconds - calculated_duration) > 1.0:
                        msg = "Duration inconsistent with start/end times"
                        raise ValueError(msg)

                if (
                    self.status == c.Meltano.Enums.OperationStatus.ERROR
                    and not self.error_message
                ):
                    msg = "Error status requires error message"
                    raise ValueError(msg)

                return self

        class PipelineResult(FlextCliModels.TimestampedModel):
            """Generic pipeline execution result with complete validation."""

            pipeline_id: Annotated[str, Field(description="Pipeline identifier")]
            source_result: Annotated[
                FlextMeltanoModels.Meltano.ExecutionResult | None,
                Field(default=None, description="Source execution result"),
            ]
            sink_result: Annotated[
                FlextMeltanoModels.Meltano.ExecutionResult | None,
                Field(default=None, description="Sink execution result"),
            ]
            transformation_result: FlextMeltanoModels.Meltano.ExecutionResult | None = (
                Field(default=None, description="Transformation execution result")
            )
            overall_status: Annotated[
                str,
                Field(
                    default=c.Meltano.Enums.OperationStatus.PENDING,
                    description="Overall pipeline status",
                ),
            ]
            total_records: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Total records processed"),
            ]
            pipeline_metadata: Annotated[
                t.ConfigurationMapping,
                Field(description="Pipeline execution metadata"),
            ] = Field(default_factory=dict)

            @computed_field
            def completed_stages(self) -> t.StrSequence:
                """Completed pipeline stages."""
                return [
                    stage
                    for stage, result in (
                        ("extraction", self.source_result),
                        ("loading", self.sink_result),
                        ("transformation", self.transformation_result),
                    )
                    if result is not None and result.end_time is not None
                ]

            @computed_field
            def completion_percentage(self) -> float:
                """Pipeline completion percentage."""
                total_stages = 3
                completed = 0
                src = self.source_result
                if src is not None and src.end_time is not None:
                    completed += 1
                snk = self.sink_result
                if snk is not None and snk.end_time is not None:
                    completed += 1
                trn = self.transformation_result
                if trn is not None and trn.end_time is not None:
                    completed += 1
                return (completed / total_stages) * 100

            @computed_field
            def is_fully_successful(self) -> bool:
                """Check if all stages completed successfully."""
                return bool(
                    self.source_result
                    and self.source_result.status
                    == c.Meltano.Enums.OperationStatus.SUCCESS
                    and self.source_result.error_message is None
                    and self.sink_result
                    and self.sink_result.status
                    == c.Meltano.Enums.OperationStatus.SUCCESS
                    and self.sink_result.error_message is None
                    and self.transformation_result
                    and self.transformation_result.status
                    == c.Meltano.Enums.OperationStatus.SUCCESS
                    and self.transformation_result.error_message is None,
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

            @field_validator("overall_status", mode="before")
            @classmethod
            def validate_overall_status(cls, v: str) -> str:
                """Validate overall pipeline status."""
                valid_statuses = [
                    c.Meltano.Enums.OperationStatus.PENDING,
                    c.Meltano.Enums.OperationStatus.RUNNING,
                    c.Meltano.Enums.OperationStatus.SUCCESS,
                    "partial",
                    c.Meltano.Enums.OperationStatus.ERROR,
                ]
                if v not in valid_statuses:
                    msg = f"Overall status must be one of: {', '.join(valid_statuses)}"
                    raise ValueError(msg)
                return v

            @model_validator(mode="after")
            def validate_pipeline_result(self) -> Self:
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
                    and self.source_result.status
                    == c.Meltano.Enums.OperationStatus.SUCCESS
                    and self.source_result.error_message is None
                    and self.sink_result
                    and self.sink_result.status
                    == c.Meltano.Enums.OperationStatus.SUCCESS
                    and self.sink_result.error_message is None
                    and self.transformation_result
                    and self.transformation_result.status
                    == c.Meltano.Enums.OperationStatus.SUCCESS
                    and self.transformation_result.error_message is None,
                )
                if (
                    all_successful
                    and self.overall_status != c.Meltano.Enums.OperationStatus.SUCCESS
                ):
                    self.overall_status = c.Meltano.Enums.OperationStatus.SUCCESS

                return self

        class DbtProjectInfo(FlextCliModels.ArbitraryTypesModel):
            """Information about a DBT project."""

            root: Annotated[Path, Field(description="Project root directory")]
            name: Annotated[str, Field(description="Project name")]
            dbt_version: Annotated[
                str | None,
                Field(default=None, description="DBT version"),
            ]
            models_count: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of models"),
            ]
            tests_count: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of tests"),
            ]

        class DbtRunResult(FlextCliModels.ArbitraryTypesModel):
            """Result of a DBT model run operation."""

            success: Annotated[
                bool,
                Field(default=True, description="Whether the run was successful"),
            ] = True
            models_run: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of models executed"),
            ] = 0
            status: Annotated[
                str,
                Field(
                    default="completed",
                    description="Run status (completed, failed, etc.)",
                ),
            ] = "completed"
            error_message: Annotated[
                str | None,
                Field(default=None, description="Error message if run failed"),
            ] = None
            execution_time_seconds: Annotated[
                float | None,
                Field(default=None, description="Total execution time in seconds"),
            ] = None

        class DbtTestResult(FlextCliModels.ArbitraryTypesModel):
            """Result of a DBT test operation."""

            success: Annotated[
                bool,
                Field(default=True, description="Whether tests passed"),
            ] = True
            tests_run: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of tests executed"),
            ] = 0
            tests_passed: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of tests passed"),
            ] = 0
            tests_failed: Annotated[
                t.NonNegativeInt,
                Field(default=0, description="Number of tests failed"),
            ] = 0
            status: Annotated[
                str,
                Field(
                    default="completed",
                    description="Test status (completed, failed, etc.)",
                ),
            ] = "completed"
            error_message: Annotated[
                str | None,
                Field(default=None, description="Error message if tests failed"),
            ] = None
            execution_time_seconds: Annotated[
                float | None,
                Field(default=None, description="Total execution time in seconds"),
            ] = None

        class CommandExecutionResult(FlextCliModels.ArbitraryTypesModel):
            """Execution result model for Meltano command operations following flext-core patterns."""

            command: Annotated[
                t.StrSequence,
                Field(description="Command that was executed"),
            ]
            success: Annotated[bool, Field(description="Whether the command succeeded")]
            exit_code: Annotated[int, Field(description="Process exit code")]
            output: Annotated[str, Field(description="Standard output")]
            error: Annotated[str, Field(description="Standard error")]
            execution_time: Annotated[
                t.NonNegativeFloat,
                Field(description="Execution time in seconds"),
            ]

            @computed_field
            def timestamp(self) -> str:
                """ISO timestamp of when the result was generated."""
                return u.generate_iso_timestamp()

            def to_dict(self) -> Mapping[str, t.Scalar | t.StrSequence]:
                """Convert to dictionary representation.

                Returns:
                Mapping[str, t.Primitives | t.StrSequence]: Dictionary representation of execution result.

                """
                dumped: MutableMapping[str, t.Scalar | t.StrSequence] = {}
                dumped["command"] = self.command
                dumped["success"] = self.success
                dumped["exit_code"] = self.exit_code
                dumped["output"] = self.output
                dumped["error"] = self.error
                dumped["execution_time"] = self.execution_time
                dumped["timestamp"] = u.generate_iso_timestamp()
                return dumped


# ==========================================================================
# Model rebuild calls removed to avoid forward reference resolution issues
# These were causing NameError during import due to complex inheritance chains
# ==========================================================================


m = FlextMeltanoModels

__all__ = [
    "FlextMeltanoModels",
    "m",
]
