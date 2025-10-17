"""FLEXT Meltano Models - All Pydantic models and settings for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from flext_core import FlextConstants, FlextModels, FlextTypes
from pydantic import (
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoModels(FlextModels):
    """UNIFIED Meltano Models - Advanced Pydantic 2.11 Features with FLEXT Ecosystem Integration.

    Contains ALL Pydantic models and settings for the Meltano domain.
    Follows flext-core standards with proper model organization and composition patterns.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=False,
        str_strip_whitespace=True,
        validate_return=True,
        ser_json_timedelta="iso8601",
        ser_json_bytes="base64",
    )

    # ========================================================================
    # CLI PARAMETER MODELS - For Singer SDK CLI Translation
    # ========================================================================

    class TapRunParams(FlextModels.ArbitraryTypesModel):
        """CLI parameters for running Singer taps with automatic Singer SDK translation."""

        model_config = ConfigDict(
            validate_assignment=True,
            validate_return=True,
            validate_default=True,
            strict=True,
            str_strip_whitespace=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            frozen=False,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            hide_input_in_errors=True,
            json_schema_extra={
                "title": "TapRunParams",
                "description": "CLI parameters for running Singer taps",
            },
        )

        tap_name: str = Field(description="Name of the tap to run (e.g., tap-postgres)")
        config_file: str | None = Field(
            default=None, description="Path to tap configuration file"
        )
        catalog_file: str | None = Field(
            default=None, description="Path to catalog file for stream selection"
        )
        state_file: str | None = Field(
            default=None, description="Path to state file for incremental sync"
        )
        properties_file: str | None = Field(
            default=None, description="Path to properties file (legacy format)"
        )
        discover: bool = Field(
            default=False, description="Run in discovery mode to output catalog"
        )

    class TargetRunParams(FlextModels.ArbitraryTypesModel):
        """CLI parameters for running Singer targets with automatic Singer SDK translation."""

        model_config = ConfigDict(
            validate_assignment=True,
            validate_return=True,
            validate_default=True,
            strict=True,
            str_strip_whitespace=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            frozen=False,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            hide_input_in_errors=True,
            json_schema_extra={
                "title": "TapRunParams",
                "description": "CLI parameters for running Singer taps",
            },
        )

        target_name: str = Field(
            description="Name of the target to run (e.g., target-postgres)"
        )
        config_file: str | None = Field(
            default=None, description="Path to target configuration file"
        )
        input_file: str | None = Field(
            default=None,
            description="Path to Singer messages input file (default: stdin)",
        )

    class PipelineRunParams(FlextModels.ArbitraryTypesModel):
        """CLI parameters for running complete Singer pipelines (tap → target)."""

        model_config = ConfigDict(
            validate_assignment=True,
            validate_return=True,
            validate_default=True,
            strict=True,
            str_strip_whitespace=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            frozen=False,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            hide_input_in_errors=True,
            json_schema_extra={
                "title": "TapRunParams",
                "description": "CLI parameters for running Singer taps",
            },
        )

        tap_name: str = Field(description="Name of the tap")
        target_name: str = Field(description="Name of the target")
        tap_config: str | None = Field(
            default=None, description="Path to tap configuration file"
        )
        target_config: str | None = Field(
            default=None, description="Path to target configuration file"
        )
        catalog_file: str | None = Field(
            default=None, description="Path to catalog file"
        )
        state_file: str | None = Field(default=None, description="Path to state file")
        state_output_file: str | None = Field(
            default=None, description="Path to write final state"
        )

    class DbtRunParams(FlextModels.ArbitraryTypesModel):
        """CLI parameters for DBT operations."""

        model_config = ConfigDict(
            validate_assignment=True,
            validate_return=True,
            validate_default=True,
            strict=True,
            str_strip_whitespace=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            frozen=False,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            hide_input_in_errors=True,
            json_schema_extra={
                "title": "TapRunParams",
                "description": "CLI parameters for running Singer taps",
            },
        )

        project_dir: str = Field(description="DBT project directory")
        models: str | None = Field(
            default=None, description="Specific models to run (space-separated)"
        )
        select: str | None = Field(
            default=None, description="DBT selection syntax for models"
        )
        exclude: str | None = Field(
            default=None, description="DBT exclusion syntax for models"
        )
        full_refresh: bool = Field(
            default=False, description="Run models with --full-refresh"
        )
        vars: str | None = Field(
            default=None, description="DBT variables as JSON string"
        )

    class PluginInstallParams(FlextModels.ArbitraryTypesModel):
        """CLI parameters for plugin installation."""

        model_config = ConfigDict(
            validate_assignment=True,
            validate_return=True,
            validate_default=True,
            strict=True,
            str_strip_whitespace=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            frozen=False,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            hide_input_in_errors=True,
            json_schema_extra={
                "title": "TapRunParams",
                "description": "CLI parameters for running Singer taps",
            },
        )

        plugin_type: str = Field(
            description="Type of plugin (tap, target, transformer)"
        )
        plugin_name: str = Field(description="Name of the plugin to install")
        variant: str | None = Field(default=None, description="Specific plugin variant")
        pip_url: str | None = Field(
            default=None, description="Custom pip URL for plugin"
        )

    # ========================================================================
    # TAP MODELS - Singer tap configurations and instances
    # ========================================================================

    class TapConfig(FlextModels.ArbitraryTypesModel):
        """Pydantic model for tap configuration with advanced validation and composition."""

        model_config = ConfigDict(extra="allow", validate_assignment=True)

        # Configuration complexity thresholds (from FlextMeltanoConstants)
        _SIMPLE_CONFIG_THRESHOLD = (
            FlextMeltanoConstants.Model.TAP_SIMPLE_CONFIG_THRESHOLD
        )
        _MODERATE_CONFIG_THRESHOLD = (
            FlextMeltanoConstants.Model.TAP_MODERATE_CONFIG_THRESHOLD
        )

        tap_type: str = Field(description="Type of the tap (e.g., tap-postgres)")
        connection_config: FlextTypes.Dict = Field(
            description="Connection configuration",
        )
        stream_config: FlextTypes.Dict = Field(
            default_factory=dict,
            description="Stream-specific configuration",
        )
        version: str = Field(default="latest", description="Tap version")

        @computed_field
        def tap_identifier(self) -> str:
            """Computed field for unique tap identifier."""
            return f"{self.tap_type}:{self.version}"

        @computed_field
        def has_stream_config(self) -> bool:
            """Computed field indicating if stream configuration is present."""
            return bool(self.stream_config)

        @computed_field
        def config_complexity(self) -> str:
            """Computed field for configuration complexity assessment."""
            total_configs = len(self.connection_config) + len(self.stream_config)
            if total_configs <= self._SIMPLE_CONFIG_THRESHOLD:
                return "simple"
            if total_configs <= self._MODERATE_CONFIG_THRESHOLD:
                return "moderate"
            return "complex"

        @model_validator(mode="after")
        def validate_tap_config_consistency(self) -> FlextMeltanoModels.TapConfig:
            """Model validator for tap configuration consistency."""
            # Validate tap_type format
            if not self.tap_type.startswith("tap-"):
                msg = "Tap type must start with 'tap-'"
                raise ValueError(msg)

            # Ensure connection config has minimum required fields
            if not self.connection_config:
                msg = "Connection configuration cannot be empty"
                raise ValueError(msg)

            return self

        @field_serializer("connection_config")
        def serialize_connection_config(
            self, value: FlextTypes.Dict
        ) -> FlextTypes.Dict:
            """Field serializer for connection config with sensitive data protection."""
            # Mask sensitive fields
            sensitive_keys = {"password", "token", "api_key", "secret"}
            serialized: FlextTypes.Dict = {}
            for key, val in value.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    serialized[key] = "[PROTECTED]"
                else:
                    serialized[key] = val
            return serialized

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
            v: FlextTypes.Dict,
        ) -> FlextTypes.Dict:
            """Validate connection_config with basic validation."""
            if not v:
                empty_config_msg = "Connection configuration cannot be empty"
                raise ValueError(empty_config_msg)
            if not isinstance(v, dict):
                invalid_type_msg = "Connection configuration must be a dictionary"
                raise TypeError(invalid_type_msg)
            return v

    class StreamDefinition(FlextModels.Entity):
        """Pydantic model for stream definition with advanced Pydantic 2.11 features."""

        model_config = ConfigDict(extra="allow", validate_assignment=True)

        stream_name: str = Field(description="Name of the stream")
        stream_schema: FlextTypes.Dict = Field(
            description="JSON schema for the stream",
        )
        tap_type: str = Field(description="Type of tap this stream belongs to")
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
            """Computed field indicating if stream is active."""
            return self.status in {"discovered", "selected", "extracting"}

        @computed_field
        def has_data(self) -> bool:
            """Computed field indicating if stream has extracted data."""
            return self.records_extracted > 0

        @computed_field
        def schema_properties_count(self) -> int:
            """Computed field for number of schema properties."""
            return len(
                cast("dict[str, object]", self.stream_schema.get("properties", {}))
            )

        @model_validator(mode="after")
        def validate_stream_definition_consistency(
            self,
        ) -> FlextMeltanoModels.StreamDefinition:
            """Model validator for stream definition consistency."""
            # Validate schema has required properties
            if "properties" not in self.stream_schema:
                msg = "Stream schema must contain properties"
                raise ValueError(msg)

            # Validate status values
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
        def serialize_stream_schema(self, value: FlextTypes.Dict) -> FlextTypes.Dict:
            """Field serializer for stream schema normalization."""
            # Ensure consistent schema structure
            if "properties" not in value:
                value["properties"] = {}
            if "type" not in value:
                value["type"] = "object"
            return value

    class SinkDefinition(FlextModels.Entity):
        """Pydantic model for sink definition with advanced Pydantic 2.11 features."""

        model_config = ConfigDict(extra="allow", validate_assignment=True)

        sink_name: str = Field(description="Name of the sink")
        target_name: str = Field(description="Name of the target")
        config: FlextTypes.Dict = Field(
            default_factory=dict, description="Sink configuration"
        )
        sink_schema: FlextTypes.Dict = Field(
            default_factory=dict, description="Sink schema"
        )
        status: str = Field(default="initialized", description="Current status")

        @computed_field
        def config_keys_count(self) -> int:
            """Computed field for number of config keys."""
            return len(self.config)

        @model_validator(mode="after")
        def validate_sink_definition_consistency(
            self,
        ) -> FlextMeltanoModels.SinkDefinition:
            """Model validator for sink definition consistency."""
            # Validate status values
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
        """Pydantic model for tap instance with comprehensive composition."""

        model_config = ConfigDict(extra="allow", validate_assignment=True)

        tap_type: str = Field(description="Type of the tap")
        config: FlextMeltanoModels.TapConfig = Field(description="Tap configuration")
        adapter: object | None = Field(
            default=None,
            description="FlextMeltanoAdapter instance",
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
        metadata: FlextTypes.Dict = Field(
            default_factory=dict,
            description="Additional metadata",
        )
        tap_id: str = Field(description="Unique tap identifier")

        @computed_field
        def stream_count(self) -> int:
            """Computed field for number of discovered streams."""
            return len(self.streams)

        @computed_field
        def active_streams_count(self) -> int:
            """Computed field for number of active streams."""
            active_statuses = {"discovered", "selected", "extracting"}
            return sum(1 for stream in self.streams.values() if stream.status in active_statuses)

        @computed_field
        def total_records_extracted(self) -> int:
            """Computed field for total records extracted across all streams."""
            return sum(stream.records_extracted for stream in self.streams.values())

        @computed_field
        def is_ready_for_extraction(self) -> bool:
            """Computed field indicating if tap is ready for data extraction."""
            return (
                self.discovered
                and len(self.streams) > 0
                and self.status == "configured"
            )

        @model_validator(mode="after")
        def validate_tap_instance_consistency(self) -> FlextMeltanoModels.TapInstance:
            """Model validator for tap instance consistency."""
            # Ensure tap types match
            if self.config.tap_type != self.tap_type:
                msg = "Tap type must match between instance and config"
                raise ValueError(msg)

            # Validate discovery state
            if self.discovered and not self.streams:
                msg = "Discovered tap must have at least one stream"
                raise ValueError(msg)

            return self

    class TargetInstance(FlextModels.Entity):
        """Pydantic model for target instance with comprehensive composition."""

        model_config = ConfigDict(extra="allow", validate_assignment=True)

        target_type: str = Field(description="Type of the target")
        config: FlextMeltanoModels.TargetConfig = Field(
            description="Target configuration"
        )
        adapter: object | None = Field(
            default=None,
            description="FlextMeltanoAdapter instance",
        )
        status: str = Field(default="initialized", description="Current status")
        batch_size: int = Field(default=1000, description="Batch processing size")
        sink_count: int = Field(default=0, description="Number of configured sinks")

        @computed_field
        def is_ready(self) -> bool:
            """Computed field indicating if target is ready for processing."""
            return (
                self.status == "configured"
                and self.config is not None
                and self.batch_size > 0
            )

        @model_validator(mode="after")
        def validate_target_instance_consistency(
            self,
        ) -> FlextMeltanoModels.TargetInstance:
            """Model validator for target instance consistency."""
            # Ensure target types match
            if self.config.target_type != self.target_type:
                msg = "Target type must match between instance and config"
                raise ValueError(msg)

            # Validate batch size
            if self.batch_size <= 0:
                msg = "Batch size must be positive"
                raise ValueError(msg)

            return self

    # ========================================================================
    # TARGET MODELS - Singer target configurations and instances
    # ========================================================================

    class TargetConfig(FlextModels.Entity):
        """Pydantic model for target configuration with advanced field validation and composition."""

        model_config = ConfigDict(frozen=True, extra="allow")

        # Processing efficiency thresholds (from FlextMeltanoConstants)
        _HIGH_EFFICIENCY_THRESHOLD = (
            FlextMeltanoConstants.Model.TARGET_HIGH_EFFICIENCY_THRESHOLD
        )
        _MEDIUM_EFFICIENCY_THRESHOLD = (
            FlextMeltanoConstants.Model.TARGET_MEDIUM_EFFICIENCY_THRESHOLD
        )

        target_type: str = Field(description="Target type identifier")
        connection_config: FlextTypes.Dict = Field(
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
        def target_identifier(self) -> str:
            """Computed field for unique target identifier."""
            return f"{self.target_type}:batch_{self.batch_size}"

        @computed_field
        def max_records_capacity(self) -> int:
            """Computed field for maximum records capacity."""
            return self.batch_size * self.max_batches

        @computed_field
        def processing_efficiency(self) -> str:
            """Computed field for processing efficiency assessment."""
            if self.batch_size >= self._HIGH_EFFICIENCY_THRESHOLD:
                return "high"
            if self.batch_size >= self._MEDIUM_EFFICIENCY_THRESHOLD:
                return "medium"
            return "low"

        @model_validator(mode="after")
        def validate_target_config_consistency(self) -> FlextMeltanoModels.TargetConfig:
            """Model validator for target configuration consistency."""
            # Validate target_type format
            if not self.target_type.startswith("target-"):
                msg = "Target type must start with 'target-'"
                raise ValueError(msg)

            # Validate batch configuration
            max_reasonable_batch_size = 10000
            if self.batch_size > max_reasonable_batch_size:
                msg = f"Batch size too large (max {max_reasonable_batch_size})"
                raise ValueError(msg)

            return self

        @field_serializer("connection_config")
        def serialize_connection_config(
            self, value: FlextTypes.Dict
        ) -> FlextTypes.Dict:
            """Field serializer for connection config with sensitive data protection."""
            # Mask sensitive fields
            sensitive_keys = {"password", "token", "api_key", "secret", "credentials"}
            serialized: FlextTypes.Dict = {}
            for key, val in value.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    serialized[key] = "[PROTECTED]"
                else:
                    serialized[key] = val
            return serialized

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
            v: FlextTypes.Dict,
        ) -> FlextTypes.Dict:
            """Validate connection config with basic validation."""
            if not v:
                empty_config_msg = "Connection configuration cannot be empty"
                raise ValueError(empty_config_msg)
            if not isinstance(v, dict):
                invalid_type_msg = "Connection configuration must be a dictionary"
                raise TypeError(invalid_type_msg)
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

    class StreamInfo(FlextModels.ArbitraryTypesModel):
        """Pydantic model for stream information with advanced validation and computed fields."""

        model_config = ConfigDict(frozen=False, extra="allow")

        stream_name: str = Field(description="Stream name identifier")
        stream_schema: FlextTypes.Dict = Field(
            description="Stream schema definition",
            alias="schema",
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
            """Computed field indicating if stream has processed data."""
            return self.records_loaded > 0 or self.batches_processed > 0

        @computed_field
        def average_records_per_batch(self) -> float:
            """Computed field for average records per batch."""
            if self.batches_processed == 0:
                return 0.0
            return self.records_loaded / self.batches_processed

        @computed_field
        def processing_status(self) -> str:
            """Computed field for processing status assessment."""
            if self.status == "completed" and self.records_loaded > 0:
                return "success"
            if self.status == "error":
                return "failed"
            if self.records_loaded > 0:
                return "in_progress"
            return "pending"

        @model_validator(mode="after")
        def validate_stream_info_consistency(self) -> FlextMeltanoModels.StreamInfo:
            """Model validator for stream information consistency."""
            # Validate records and batches consistency
            if self.records_loaded > 0 and self.batches_processed == 0:
                msg = "Records loaded but no batches processed"
                raise ValueError(msg)

            # Validate status values
            valid_statuses = {"initialized", "processing", "completed", "error"}
            if self.status not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)

            return self

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
            v: FlextTypes.Dict,
        ) -> FlextTypes.Dict:
            """Validate stream schema contains properties."""
            if "properties" not in v:
                msg = "Schema must contain properties"
                raise ValueError(msg)
            return v

    # ========================================================================
    # MELTANO PROJECT MODELS - Project configuration and validation
    # ========================================================================

    class MeltanoProjectModel(FlextModels.Entity):
        """Pydantic model for Meltano project configuration with advanced validation."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        # Project maturity thresholds (using FlextMeltanoConstants as source)
        _MATURE_PROJECT_ENVIRONMENTS = (
            FlextMeltanoConstants.Model.MATURITY_MATURE_ENV_COUNT
        )
        _DEVELOPING_PROJECT_ENVIRONMENTS = (
            FlextMeltanoConstants.Model.MATURITY_DEVELOPING_ENV_COUNT
        )

        version: int = Field(
            default=1,
            ge=1,
            le=1,
            description="Meltano project version (only version 1 supported)",
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
        environments: FlextMeltanoTypes.MeltanoCore.PluginNameList = Field(
            default_factory=lambda: ["dev", "staging", "prod"],
            description="Available environments",
        )

        @computed_field
        def environment_count(self) -> int:
            """Computed field for number of environments."""
            return len(self.environments)

        @computed_field
        def has_production_environment(self) -> bool:
            """Computed field indicating if production environment exists."""
            prod_environments = {"prod", "production", "live"}
            return any(env.lower() in prod_environments for env in self.environments)

        @computed_field
        def project_maturity(self) -> str:
            """Computed field for project maturity assessment."""
            prod_environments = {"prod", "production", "live"}
            has_prod = any(env.lower() in prod_environments for env in self.environments)
            env_count = len(self.environments)

            if (
                has_prod
                and env_count
                >= FlextMeltanoConstants.Model.PROJECT_MATURITY_MATURE_ENV_COUNT
            ):
                return "mature"
            if (
                env_count
                >= FlextMeltanoConstants.Model.PROJECT_MATURITY_DEVELOPING_ENV_COUNT
            ):
                return "developing"
            return "basic"

        @model_validator(mode="after")
        def validate_meltano_project_consistency(
            self,
        ) -> FlextMeltanoModels.MeltanoProjectModel:
            """Model validator for Meltano project consistency."""
            # Ensure default environment exists
            if self.default_environment not in self.environments:
                msg = f"Default environment '{self.default_environment}' not in environments list"
                raise ValueError(msg)

            # Validate project root exists
            if not self.project_root.exists():
                msg = f"Project root directory does not exist: {self.project_root}"
                raise ValueError(msg)

            return self

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

    class PluginModel(FlextModels.Entity):
        """Pydantic model for Meltano plugin configuration with advanced composition."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        name: str = Field(min_length=1, description="Plugin name")
        namespace: str = Field(description="Plugin namespace")
        pip_url: str | None = Field(default=None, description="Plugin pip URL")
        executable: str | None = Field(default=None, description="Plugin executable")
        variant: str = Field(
            default=FlextMeltanoConstants.Plugin.DEFAULT_VARIANT,
            description="Plugin variant",
        )
        settings: FlextTypes.Dict = Field(
            default_factory=dict,
            description="Plugin settings",
        )

        @computed_field
        def full_plugin_name(self) -> str:
            """Computed field for full plugin name with namespace."""
            return f"{self.namespace}.{self.name}"

        @computed_field
        def has_custom_executable(self) -> bool:
            """Computed field indicating if plugin has custom executable."""
            return self.executable is not None

        @computed_field
        def settings_count(self) -> int:
            """Computed field for number of plugin settings."""
            return len(self.settings)

        @computed_field
        def plugin_complexity(self) -> str:
            """Computed field for plugin complexity assessment."""
            settings_count = len(self.settings)
            if (
                settings_count
                == FlextMeltanoConstants.Model.COMPLEXITY_MINIMAL_SETTINGS
            ):
                return "minimal"
            if (
                settings_count
                <= FlextMeltanoConstants.Model.COMPLEXITY_SIMPLE_MAX_SETTINGS
            ):
                return "simple"
            if (
                settings_count
                <= FlextMeltanoConstants.Model.COMPLEXITY_MODERATE_MAX_SETTINGS
            ):
                return "moderate"
            return "complex"

        @model_validator(mode="after")
        def validate_plugin_consistency(self) -> FlextMeltanoModels.PluginModel:
            """Model validator for plugin consistency."""
            # Validate namespace format
            if "." in self.namespace:
                msg = "Plugin namespace cannot contain dots"
                raise ValueError(msg)

            # Ensure pip_url or executable is provided
            if not self.pip_url and not self.executable:
                msg = "Plugin must have either pip_url or executable"
                raise ValueError(msg)

            return self

        @field_validator("name")
        @classmethod
        def validate_plugin_name(cls, v: str) -> str:
            """Validate plugin name with basic business rules."""
            if not v or not v.strip():
                empty_name_msg = "Plugin name cannot be empty"
                raise ValueError(empty_name_msg)
            if " " in v:
                spaces_msg = "Plugin name cannot contain spaces"
                raise ValueError(spaces_msg)
            return v.strip()

    # ========================================================================
    # DBT MODELS - DBT project and execution models
    # ========================================================================

    class DbtProjectModel(FlextModels.ArbitraryTypesModel):
        """Pydantic model for DBT project configuration with advanced validation."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        name: str = Field(min_length=1, description="DBT project name")
        version: str = Field(description="DBT project version")
        profile: str = Field(description="DBT profile name")
        model_paths: FlextMeltanoTypes.MeltanoCore.DbtModelList = Field(
            default=["models"],
            description="DBT model paths",
        )
        analysis_paths: FlextMeltanoTypes.MeltanoCore.DbtModelList = Field(
            default=["analysis"],
            description="DBT analysis paths",
        )
        test_paths: FlextMeltanoTypes.MeltanoCore.DbtTestList = Field(
            default=["tests"],
            description="DBT test paths",
        )
        seed_paths: FlextMeltanoTypes.MeltanoCore.DbtModelList = Field(
            default=["seeds"],
            description="DBT seed paths",
        )
        macro_paths: FlextMeltanoTypes.MeltanoCore.DbtModelList = Field(
            default=["macros"],
            description="DBT macro paths",
        )

        @computed_field
        def total_path_count(self) -> int:
            """Computed field for total number of configured paths."""
            return (
                len(self.model_paths)
                + len(self.analysis_paths)
                + len(self.test_paths)
                + len(self.seed_paths)
                + len(self.macro_paths)
            )

        @computed_field
        def has_custom_paths(self) -> bool:
            """Computed field indicating if project has custom paths."""
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
            """Computed field for project structure complexity."""
            total_path_count = (
                len(self.model_paths)
                + len(self.analysis_paths)
                + len(self.test_paths)
                + len(self.seed_paths)
                + len(self.macro_paths)
            )
            if (
                total_path_count
                <= FlextMeltanoConstants.Model.STRUCTURE_SIMPLE_MAX_PATHS
            ):
                return "simple"
            if (
                total_path_count
                <= FlextMeltanoConstants.Model.STRUCTURE_MODERATE_MAX_PATHS
            ):
                return "moderate"
            return "complex"

        @model_validator(mode="after")
        def validate_dbt_project_consistency(
            self,
        ) -> FlextMeltanoModels.DbtProjectModel:
            """Model validator for DBT project consistency."""
            # Ensure model paths are not empty
            if not self.model_paths:
                msg = "DBT project must have at least one model path"
                raise ValueError(msg)

            # Validate version format
            version_parts = self.version.split(".")
            if len(version_parts) != FlextMeltanoConstants.Model.VERSION_PARTS_COUNT:
                msg = "DBT project version must be in format 'x.y.z'"
                raise ValueError(msg)

            return self

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

    class DbtExecutionModel(FlextModels.Entity):
        """Pydantic model for DBT execution configuration with advanced validation."""

        model_config = ConfigDict(validate_assignment=True, extra="allow")

        # Execution complexity thresholds (from FlextMeltanoConstants)
        _SIMPLE_EXECUTION_THRESHOLD = (
            FlextMeltanoConstants.Model.DBT_SIMPLE_EXECUTION_THRESHOLD
        )
        _MODERATE_EXECUTION_THRESHOLD = (
            FlextMeltanoConstants.Model.DBT_MODERATE_EXECUTION_THRESHOLD
        )

        command: str = Field(description="DBT command to execute")
        models: FlextMeltanoTypes.MeltanoCore.DbtModelList = Field(
            default_factory=list,
            description="Models to execute",
        )
        exclude: FlextMeltanoTypes.MeltanoCore.DbtModelList = Field(
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
            """Computed field for number of models to execute."""
            return len(self.models)

        @computed_field
        def exclude_count(self) -> int:
            """Computed field for number of models to exclude."""
            return len(self.exclude)

        @computed_field
        def execution_complexity(self) -> str:
            """Computed field for execution complexity assessment."""
            total_scope = len(self.models) + len(self.exclude)
            if total_scope == 0:
                return "full_project"
            if total_scope <= self._SIMPLE_EXECUTION_THRESHOLD:
                return "simple"
            if total_scope <= self._MODERATE_EXECUTION_THRESHOLD:
                return "moderate"
            return "complex"

        @computed_field
        def is_parallel_execution(self) -> bool:
            """Computed field indicating if execution uses multiple threads."""
            return self.threads > 1

        @model_validator(mode="after")
        def validate_dbt_execution_consistency(
            self,
        ) -> FlextMeltanoModels.DbtExecutionModel:
            """Model validator for DBT execution consistency."""
            # Validate thread count
            max_threads = 32
            if self.threads > max_threads:
                msg = f"Thread count cannot exceed {max_threads}"
                raise ValueError(msg)

            # Ensure models and exclude don't overlap
            model_set = set(self.models)
            exclude_set = set(self.exclude)
            overlap = model_set & exclude_set
            if overlap:
                msg = f"Models cannot be both included and excluded: {overlap}"
                raise ValueError(msg)

            return self

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

    class ExecutionResult(FlextModels.TimestampedModel):
        """Pydantic model for execution result tracking with advanced composition."""

        # Performance categorization thresholds (from FlextMeltanoConstants)
        _HIGH_PERFORMANCE_THRESHOLD = (
            FlextMeltanoConstants.Model.EXECUTION_HIGH_PERFORMANCE_THRESHOLD
        )
        _GOOD_PERFORMANCE_THRESHOLD = (
            FlextMeltanoConstants.Model.EXECUTION_GOOD_PERFORMANCE_THRESHOLD
        )
        _MODERATE_PERFORMANCE_THRESHOLD = (
            FlextMeltanoConstants.Model.EXECUTION_MODERATE_PERFORMANCE_THRESHOLD
        )

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
        metadata: FlextTypes.Dict = Field(
            default_factory=dict,
            description="Additional execution metadata",
        )

        @computed_field
        def is_completed(self) -> bool:
            """Computed field indicating if execution is completed."""
            return self.end_time is not None

        @computed_field
        def is_successful(self) -> bool:
            """Computed field indicating if execution was successful."""
            return self.status == "success" and self.error_message is None

        @computed_field
        def execution_rate_per_second(self) -> float:
            """Computed field for execution rate (records/second)."""
            if not self.duration_seconds or self.duration_seconds <= 0:
                return 0.0
            return self.records_processed / self.duration_seconds

        @computed_field
        def performance_category(self) -> str:
            """Computed field for performance categorization."""
            if not self.duration_seconds or self.duration_seconds <= 0:
                rate = 0.0
            else:
                rate = self.records_processed / self.duration_seconds

            if rate >= self._HIGH_PERFORMANCE_THRESHOLD:
                return "high_performance"
            if rate >= self._GOOD_PERFORMANCE_THRESHOLD:
                return "good_performance"
            if rate >= self._MODERATE_PERFORMANCE_THRESHOLD:
                return "moderate_performance"
            return "low_performance"

        @model_validator(mode="after")
        def validate_execution_result_consistency(
            self,
        ) -> FlextMeltanoModels.ExecutionResult:
            """Model validator for execution result consistency."""
            # Calculate duration if both times are available
            if self.start_time and self.end_time:
                calculated_duration = (self.end_time - self.start_time).total_seconds()
                if self.duration_seconds is None:
                    self.duration_seconds = calculated_duration
                elif abs(self.duration_seconds - calculated_duration) > 1.0:
                    msg = "Duration inconsistent with start/end times"
                    raise ValueError(msg)

            # Validate error status consistency
            if self.status == "error" and not self.error_message:
                msg = "Error status requires error message"
                raise ValueError(msg)

            return self

        @field_serializer("error_message")
        def serialize_error_message(self, value: str | None) -> str | None:
            """Field serializer for error message truncation."""
            if value is None:
                return None
            max_length = 1000
            if len(value) > max_length:
                return f"{value[:max_length]}... (truncated)"
            return value

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
        """Pydantic model for pipeline execution result with comprehensive composition."""

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
            default="pending",
            description="Overall pipeline status",
        )
        total_records: int = Field(
            default=0,
            description="Total records processed",
        )
        pipeline_metadata: FlextTypes.Dict = Field(
            default_factory=dict,
            description="Pipeline execution metadata",
        )

        @computed_field
        def completed_stages(self) -> FlextTypes.StringList:
            """Computed field for completed pipeline stages."""
            stages: FlextTypes.StringList = []
            if self.tap_result and self.tap_result.end_time is not None:
                stages.append("extraction")
            if self.target_result and self.target_result.end_time is not None:
                stages.append("loading")
            if self.dbt_result and self.dbt_result.end_time is not None:
                stages.append("transformation")
            return stages

        @computed_field
        def completion_percentage(self) -> float:
            """Computed field for pipeline completion percentage."""
            total_stages = 3  # tap, target, dbt
            # Count completed stages directly without accessing computed field
            completed = 0
            if self.tap_result and self.tap_result.end_time is not None:
                completed += 1
            if self.target_result and self.target_result.end_time is not None:
                completed += 1
            if self.dbt_result and self.dbt_result.end_time is not None:
                completed += 1
            return (completed / total_stages) * 100

        @computed_field
        def is_fully_successful(self) -> bool:
            """Computed field indicating if all stages completed successfully."""
            return bool(
                self.tap_result
                and self.tap_result.status == "success"
                and self.tap_result.error_message is None
                and self.target_result
                and self.target_result.status == "success"
                and self.target_result.error_message is None
                and self.dbt_result
                and self.dbt_result.status == "success"
                and self.dbt_result.error_message is None
            )

        @computed_field
        def total_duration_seconds(self) -> float:
            """Computed field for total pipeline duration."""
            total = 0.0
            if self.tap_result and self.tap_result.duration_seconds:
                total += self.tap_result.duration_seconds
            if self.target_result and self.target_result.duration_seconds:
                total += self.target_result.duration_seconds
            if self.dbt_result and self.dbt_result.duration_seconds:
                total += self.dbt_result.duration_seconds
            return total

        @model_validator(mode="after")
        def validate_pipeline_result_consistency(
            self,
        ) -> FlextMeltanoModels.PipelineResult:
            """Model validator for pipeline result consistency."""
            # Validate total records consistency
            total_from_stages = 0
            if self.tap_result:
                total_from_stages += self.tap_result.records_processed

            if (
                self.total_records > 0
                and total_from_stages > 0
                and abs(self.total_records - total_from_stages)
                > (total_from_stages * 0.1)
            ):
                msg = "Total records inconsistent with stage results"
                raise ValueError(msg)

            # Validate overall status - check if all stages were successful directly
            all_successful = bool(
                self.tap_result
                and self.tap_result.status == "success"
                and self.tap_result.error_message is None
                and self.target_result
                and self.target_result.status == "success"
                and self.target_result.error_message is None
                and self.dbt_result
                and self.dbt_result.status == "success"
                and self.dbt_result.error_message is None
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
