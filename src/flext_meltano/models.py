"""FLEXT Meltano Models - All Pydantic models and settings for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from flext_core import FlextConstants, FlextModels, FlextResult, FlextTypes
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.validators import FlextMeltanoValidators


class FlextMeltanoModels(FlextModels):
    """UNIFIED Meltano Models - SINGLE RESPONSIBILITY PATTERN.

    Contains ALL Pydantic models and settings for the Meltano domain.
    Follows flext-core standards with proper model organization.
    """

    # ========================================================================
    # TAP MODELS - Singer tap configurations and instances
    # ========================================================================

    class TapConfig(BaseModel):
        """Pydantic model for tap configuration with validation."""

        model_config = ConfigDict(extra=allow, validate_assignment=True)

        tap_type: str = Field(description="Type of the tap (e.g., tap-postgres)")
        connection_config: FlextTypes.Core.Dict = Field(
            description="Connection configuration",
        )
        stream_config: FlextTypes.Core.Dict = Field(
            default_factory=dict,
            description="Stream-specific configuration",
        )
        version: str = Field(default=latest, description="Tap version")

        @field_validator("tap_type")
        @classmethod
        def validate_tap_type(cls, v: str) -> str:
            """Validate tap_type is not empty."""
            if not v or not v.strip():
                msg = "tap_type cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("connection_config")
        @classmethod
        def validate_connection_config(
            cls,
            v: FlextTypes.Core.Dict,
        ) -> FlextTypes.Core.Dict:
            """Validate connection_config using centralized validator."""
            result: FlextResult[object] = (
                FlextMeltanoValidators.validate_connection_config(v)
            )
            if result.is_failure:
                raise ValueError(result.error or "Connection config validation failed")
            return v

    class StreamDefinition(BaseModel):
        """Pydantic model for stream definition."""

        model_config = ConfigDict(extra=allow, validate_assignment=True)

        stream_name: str = Field(description="Name of the stream")
        stream_schema: FlextTypes.Core.Dict = Field(
            description="JSON schema for the stream",
        )
        tap_type: str = Field(description="Type of tap this stream belongs to")
        status: str = Field(
            default=discovered,
            description="Current status of the stream",
        )
        records_extracted: int = Field(
            default=0,
            description="Number of records extracted",
        )

    class TapInstance(BaseModel):
        """Pydantic model for tap instance."""

        model_config = ConfigDict(extra=allow, validate_assignment=True)

        tap_type: str = Field(description="Type of the tap")
        config: FlextMeltanoModels.TapConfig = Field(description="Tap configuration")
        adapter: object | None = Field(
            default=None,
            description="FlextMeltanoAdapter instance",
        )
        status: str = Field(default=initialized, description="Current status")
        streams: dict[str, FlextMeltanoModels.StreamDefinition] = Field(
            default_factory=dict,
            description="Discovered streams",
        )
        discovered: bool = Field(
            default=False,
            description="Whether streams have been discovered",
        )
        metadata: FlextTypes.Core.Dict = Field(
            default_factory=dict,
            description="Additional metadata",
        )
        tap_id: str = Field(description="Unique tap identifier")

    # ========================================================================
    # TARGET MODELS - Singer target configurations and instances
    # ========================================================================

    class TargetConfig(BaseModel):
        """Pydantic model for target configuration with field validation."""

        model_config = ConfigDict(frozen=True, extra="allow")

        target_type: str = Field(description="Target type identifier")
        connection_config: FlextTypes.Core.Dict = Field(
            description="Connection configuration dictionary",
        )
        batch_size: int = Field(
            default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,
            description="Batch size for record processing",
        )
        max_batches: int = Field(
            default=100,
            description="Maximum number of batches to process",
        )

        @field_validator("target_type")
        @classmethod
        def validate_target_type(cls, v: str) -> str:
            """Validate target type is non-empty string."""
            if not v or not isinstance(v, str):
                msg = "Target type must be non-empty string"
                raise ValueError(msg)
            return v

        @field_validator("connection_config")
        @classmethod
        def validate_connection_config(
            cls,
            v: FlextTypes.Core.Dict,
        ) -> FlextTypes.Core.Dict:
            """Validate connection config using centralized validator."""
            result: FlextResult[object] = (
                FlextMeltanoValidators.validate_connection_config(v)
            )
            if result.is_failure:
                raise ValueError(result.error or "Connection config validation failed")
            return v

        @field_validator("batch_size")
        @classmethod
        def validate_batch_size(cls, v: int) -> int:
            """Validate batch size is positive integer."""
            if not isinstance(v, int) or v <= 0:
                msg = "Batch size must be positive integer"
                raise ValueError(msg)
            return v

        @field_validator("max_batches")
        @classmethod
        def validate_max_batches(cls, v: int) -> int:
            """Validate max batches is positive integer."""
            if not isinstance(v, int) or v <= 0:
                msg = "Max batches must be positive integer"
                raise ValueError(msg)
            return v

    class StreamInfo(BaseModel):
        """Pydantic model for stream information with validation."""

        model_config = ConfigDict(frozen=False, extra="allow")

        stream_name: str = Field(description="Stream name identifier")
        stream_schema: FlextTypes.Core.Dict = Field(
            description="Stream schema definition",
            alias="schema",
        )
        status: str = Field(
            default=initialized,
            description="Stream processing status",
        )
        records_loaded: int = Field(default=0, description="Number of records loaded")
        batches_processed: int = Field(
            default=0,
            description="Number of batches processed",
        )
        created_at: str = Field(description="Creation timestamp")

        @field_validator("stream_name")
        @classmethod
        def validate_stream_name(cls, v: str) -> str:
            """Validate stream name is non-empty string."""
            if not v or not isinstance(v, str):
                msg = "Stream name must be non-empty string"
                raise ValueError(msg)
            return v

        @field_validator("stream_schema")
        @classmethod
        def validate_stream_schema(
            cls,
            v: FlextTypes.Core.Dict,
        ) -> FlextTypes.Core.Dict:
            """Validate stream schema contains properties."""
            if "properties" not in v:
                msg = "Schema must contain properties"
                raise ValueError(msg)
            return v

    # ========================================================================
    # MELTANO PROJECT MODELS - Project configuration and validation
    # ========================================================================

    class MeltanoProjectModel(BaseModel):
        """Pydantic model for Meltano project configuration."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        version: int = Field(
            ge=1,
            le=1,
            description="Meltano project version (only version 1 supported)",
        )
        project_id: str = Field(min_length=1, description="Project ID required")
        default_environment: str = Field(
            default=dev,
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

        @field_validator("project_id")
        @classmethod
        def validate_project_id_business_rules(cls, v: str) -> str:
            """Validate Meltano-specific project ID business rules."""
            if not v.strip():
                msg = "Project ID cannot be empty or whitespace"
                raise ValueError(msg)
            if " " in v:
                msg = "Project ID cannot contain spaces"
                raise ValueError(msg)
            if not v.replace("-", "").replace("_", "").isalnum():
                msg = "Project ID can only contain letters, numbers, hyphens, and underscores"
                raise ValueError(msg)
            return v

    class PluginModel(BaseModel):
        """Pydantic model for Meltano plugin configuration."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        name: str = Field(min_length=1, description="Plugin name")
        namespace: str = Field(description="Plugin namespace")
        pip_url: str | None = Field(default=None, description="Plugin pip URL")
        executable: str | None = Field(default=None, description="Plugin executable")
        variant: str = Field(
            default=FlextMeltanoConstants.PLUGIN_DEFAULT_VARIANT,
            description="Plugin variant",
        )
        settings: FlextTypes.Core.Dict = Field(
            default_factory=dict,
            description="Plugin settings",
        )

        @field_validator("name")
        @classmethod
        def validate_plugin_name(cls, v: str) -> str:
            """Validate plugin name using centralized business rules."""
            result = FlextMeltanoValidators.validate_meltano_plugin_business_rules({
                "name": "v"
            })
            if result.is_failure:
                raise ValueError(result.error or "Plugin name validation failed")
            return v

    # ========================================================================
    # DBT MODELS - DBT project and execution models
    # ========================================================================

    class DbtProjectModel(BaseModel):
        """Pydantic model for DBT project configuration."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        name: str = Field(min_length=1, description="DBT project name")
        version: str = Field(description="DBT project version")
        profile: str = Field(description="DBT profile name")
        model_paths: list[str] = Field(
            default=["models"],
            description="DBT model paths",
        )
        analysis_paths: list[str] = Field(
            default=["analysis"],
            description="DBT analysis paths",
        )
        test_paths: list[str] = Field(
            default=["tests"],
            description="DBT test paths",
        )
        seed_paths: list[str] = Field(
            default=["seeds"],
            description="DBT seed paths",
        )
        macro_paths: list[str] = Field(
            default=["macros"],
            description="DBT macro paths",
        )

        @field_validator("name")
        @classmethod
        def validate_dbt_project_name(cls, v: str) -> str:
            """Validate DBT project name format."""
            if not v.strip():
                msg = "DBT project name cannot be empty"
                raise ValueError(msg)
            if " " in v:
                msg = "DBT project name cannot contain spaces"
                raise ValueError(msg)
            return v

    class DbtExecutionModel(BaseModel):
        """Pydantic model for DBT execution configuration."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        command: str = Field(description="DBT command to execute")
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

        @field_validator("command")
        @classmethod
        def validate_dbt_command(cls, v: str) -> str:
            """Validate DBT command is valid."""
            valid_commands = ["run", "test", "build", "compile", "docs", "seed"]
            if v not in valid_commands:
                msg = f"DBT command must be one of: {', '.join(valid_commands)}"
                raise ValueError(msg)
            return v

    # ========================================================================
    # EXECUTION RESULT MODELS - Pipeline execution and monitoring
    # ========================================================================

    class ExecutionResult(BaseModel):
        """Pydantic model for execution result tracking."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

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
        metadata: FlextTypes.Core.Dict = Field(
            default_factory=dict,
            description="Additional execution metadata",
        )

        @field_validator("status")
        @classmethod
        def validate_status(cls, v: str) -> str:
            """Validate execution status."""
            valid_statuses = ["pending", "running", "success", "error", "timeout"]
            if v not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)
            return v

    class PipelineResult(BaseModel):
        """Pydantic model for pipeline execution result."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        pipeline_id: str = Field(description="Pipeline identifier")
        tap_result: FlextMeltanoModels.ExecutionResult | None = Field(
            default=None,
            description="Tap execution result",
        )
        target_result: FlextMeltanoModels.ExecutionResult | None = Field(
            default=None,
            description="Target execution result",
        )
        dbt_result: FlextMeltanoModels.ExecutionResult | None = Field(
            default=None,
            description="DBT execution result",
        )
        overall_status: str = Field(
            default=pending,
            description="Overall pipeline status",
        )
        total_records: int = Field(
            default=0,
            description="Total records processed",
        )
        pipeline_metadata: FlextTypes.Core.Dict = Field(
            default_factory=dict,
            description="Pipeline execution metadata",
        )

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
