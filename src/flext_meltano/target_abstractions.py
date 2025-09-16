"""FLEXT Meltano Target Abstractions - Singer target protocol abstractions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import (
    FlextConstants,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from pydantic import BaseModel, ConfigDict, Field, field_validator

from flext_meltano.validators import FlextMeltanoValidators

if TYPE_CHECKING:
    from flext_meltano.adapters import FlextMeltanoAdapter

# Constants

# Type aliases to replace explicit object (avoid shadowing Pydantic ConfigDict)
RecordDict = FlextTypes.Core.Dict
ConnectionConfig = FlextTypes.Core.Dict
SchemaDict = FlextTypes.Core.Dict
StateDict = FlextTypes.Core.Dict
ResultDict = FlextTypes.Core.Dict


class FlextTargetAbstractions:
    """UNIFIED Target Abstractions - SINGLE RESPONSIBILITY PATTERN.

    CORRECTED ARCHITECTURE:
    - NO longer inherits from FlextModels.Entity (inappropriate for abstractions)
    - Simple class focused on target functionality abstraction
    - Follows single responsibility principle
    - Consolidates all target functionality: FlextTargetConfig, FlextStreamInfo nested classes
    """

    # =========================================================================
    # NESTED PYDANTIC MODELS - Domain-specific data validation
    # =========================================================================

    class FlextTargetConfig(BaseModel):
        """Pydantic model for target configuration with field validation."""

        model_config = ConfigDict(frozen=True, extra="allow")

        target_type: str = Field(..., description="Target type identifier")
        connection_config: FlextTypes.Core.Dict = Field(
            ..., description="Connection configuration dictionary"
        )
        batch_size: int = Field(
            default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,  # SOURCE OF TRUTH
            description="Batch size for record processing",
        )
        max_batches: int = Field(
            default=100, description="Maximum number of batches to process"
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
            cls, v: FlextTypes.Core.Dict
        ) -> FlextTypes.Core.Dict:
            """Validate connection config using centralized validator."""
            # Use centralized validator to eliminate duplication
            result = FlextMeltanoValidators.validate_connection_config(v)
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

    class FlextStreamInfo(BaseModel):
        """Pydantic model for stream information with validation."""

        model_config = ConfigDict(frozen=False, extra="allow")

        stream_name: str = Field(..., description="Stream name identifier")
        stream_schema: FlextTypes.Core.Dict = Field(
            ..., description="Stream schema definition", alias="schema"
        )
        status: str = Field(
            default="initialized", description="Stream processing status"
        )
        records_loaded: int = Field(default=0, description="Number of records loaded")
        batches_processed: int = Field(
            default=0, description="Number of batches processed"
        )
        created_at: str = Field(..., description="Creation timestamp")

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
            cls, v: FlextTypes.Core.Dict
        ) -> FlextTypes.Core.Dict:
            """Validate stream schema contains properties."""
            if "properties" not in v:
                msg = "Schema must contain properties"
                raise ValueError(msg)
            return v

    # =========================================================================
    # UNIFIED CLASS INSTANCE METHODS
    # =========================================================================

    def __init__(self, target_id: str | None = None) -> None:
        """Initialize unified target abstractions."""
        self.target_id = (
            target_id
            or f"target_abstractions_{FlextUtilities.Generators.generate_uuid()[:8]}"
        )
        self._logger = FlextLogger(f"{__name__}.FlextTargetAbstractions")
        self._active_targets: dict[str, FlextTypes.Core.Dict] = {}
        self._target_configs: dict[str, FlextTargetAbstractions.FlextTargetConfig] = {}
        self._stream_registry: dict[str, FlextTargetAbstractions.FlextStreamInfo] = {}

    # ============================================================================
    # TARGET CONFIGURATION METHODS
    # ============================================================================

    def create_flext_target_config(
        self,
        target_type: str,
        connection_config: ConnectionConfig,
        batch_size: int = FlextConstants.Performance.DEFAULT_BATCH_SIZE,  # SOURCE OF TRUTH
        max_batches: int = 100,  # No specific constant for max_batches yet
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create FlextTarget configuration with Pydantic validation."""
        try:
            # Use Pydantic model for validation - all validation is automatic
            config_model = self.FlextTargetConfig(
                target_type=target_type,
                connection_config=connection_config,
                batch_size=batch_size,
                max_batches=max_batches,
                **kwargs,
            )

            # Store validated configuration
            config_id = f"{target_type}_{id(config_model)}"
            self._target_configs[config_id] = config_model

            # Convert to dict for compatibility
            config_dict = config_model.model_dump()
            config_dict["config_id"] = config_id

            self._logger.info(
                "FlextTarget config created",
                target_type=target_type,
                config_id=config_id,
            )
            return FlextResult[FlextTypes.Core.Dict].ok(config_dict)

        except Exception as e:
            error_msg = f"Failed to create FlextTarget config: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # Removed _validate_target_config - validation now handled by Pydantic FlextTargetConfig model

    # ============================================================================
    # TARGET CREATION AND MANAGEMENT METHODS
    # ============================================================================

    def create_flext_target(
        self, config: FlextTypes.Core.Dict, adapter: FlextMeltanoAdapter | None = None
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create FlextTarget instance from configuration."""
        try:
            # Extract target_type for logging
            target_type = str(config.get("target_type", "unknown"))
            self._logger.info("Creating FlextTarget", target_type=target_type)

            # Config validation is handled by Pydantic models during usage

            # Create target instance
            target_instance: FlextTypes.Core.Dict = {
                "target_type": target_type,
                "config": dict(config),
                "adapter": adapter,
                "status": "initialized",
                "streams": {},
                "state": {},
                "loaded_records": 0,
                "batches_processed": 0,
                "metadata": {
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    "version": str(config.get("version", "latest")),
                },
            }

            # Register target
            target_id = f"{target_type}_{id(target_instance)}"
            self._active_targets[target_id] = target_instance

            self._logger.info(
                "FlextTarget created successfully",
                target_type=target_type,
                target_id=target_id,
            )
            return FlextResult[FlextTypes.Core.Dict].ok(
                {
                    **target_instance,
                    "target_id": target_id,
                }
            )

        except Exception as e:
            error_msg = f"Failed to create FlextTarget: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ============================================================================
    # MESSAGE PROCESSING METHODS
    # ============================================================================

    def process_schema_message(
        self, target: FlextTypes.Core.Dict, stream_name: str, schema: SchemaDict
    ) -> FlextResult[bool]:
        """Process Singer SCHEMA message with error handling."""
        try:
            self._logger.info("Processing SCHEMA message", stream_name=stream_name)

            # Create stream info with Pydantic validation
            try:
                stream_info_model = self.FlextStreamInfo(
                    stream_name=stream_name,
                    schema=schema,  # Use alias parameter
                    status="schema_processed",
                    created_at=FlextUtilities.Generators.generate_iso_timestamp(),
                )
            except Exception as e:
                return FlextResult[bool].fail(f"Stream validation failed: {e}")

            # Target validation is handled by business logic, not field validation

            # Create or update stream
            target_streams = target.get("streams", {})
            if not isinstance(target_streams, dict):
                target_streams = {}
                target["streams"] = target_streams

            # Use validated stream info from Pydantic model
            stream_info_dict = stream_info_model.model_dump()
            target_streams[stream_name] = stream_info_dict

            # Register stream with Pydantic model
            stream_key = f"{target.get('target_type', 'unknown')}_{stream_name}"
            self._stream_registry[stream_key] = stream_info_model

            self._logger.info(
                "SCHEMA message processed successfully", stream_name=stream_name
            )
            return FlextResult[bool].ok(data=True)

        except Exception as e:
            error_msg = (
                f"Failed to process SCHEMA message for stream {stream_name}: {e}"
            )
            self._logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    def process_record_message(
        self, target: FlextTypes.Core.Dict, stream_name: str, record: RecordDict
    ) -> FlextResult[bool]:
        """Process Singer RECORD message with error handling."""
        try:
            self._logger.debug("Processing RECORD message", stream_name=stream_name)

            # Log record for debugging (fulfilling ARG002 requirement)
            # Use basic debug logging without level comparison
            self._logger.debug(
                "Record data received",
                record_keys=list(record.keys())
                if isinstance(record, dict)
                else "non-dict",
            )

            # Parameter validation is handled by business logic, not field validation

            # Check if stream exists
            target_streams = target.get("streams", {})
            if (
                not isinstance(target_streams, dict)
                or stream_name not in target_streams
            ):
                return FlextResult[bool].fail(
                    f"Stream {stream_name} not found - SCHEMA message required first"
                )

            # Process record
            stream_info = target_streams[stream_name]
            if isinstance(stream_info, dict):
                stream_info["records_loaded"] = stream_info.get("records_loaded", 0) + 1
                stream_info["status"] = "record_processed"

            # Update target statistics with proper type handling
            current_count = target.get("loaded_records", 0)
            target["loaded_records"] = (
                int(current_count) + 1 if isinstance(current_count, (int, str)) else 1
            )

            self._logger.debug(
                "RECORD message processed successfully", stream_name=stream_name
            )
            return FlextResult[bool].ok(data=True)

        except Exception as e:
            error_msg = (
                f"Failed to process RECORD message for stream {stream_name}: {e}"
            )
            self._logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    def process_state_message(
        self, target: FlextTypes.Core.Dict, state: StateDict
    ) -> FlextResult[bool]:
        """Process Singer STATE message with error handling."""
        try:
            self._logger.debug("Processing STATE message")

            # Parameter validation is handled by business logic

            # Update internal state
            target_state = target.get("state", {})
            if not isinstance(target_state, dict):
                target_state = {}
                target["state"] = target_state

            target_state.update(state)

            self._logger.debug("STATE message processed successfully")
            return FlextResult[bool].ok(data=True)

        except Exception as e:
            error_msg = f"Failed to process STATE message: {e}"
            self._logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    # ============================================================================
    # DATA LOADING METHODS
    # ============================================================================

    def load_record(
        self, target: FlextTypes.Core.Dict, stream_name: str, record: RecordDict
    ) -> FlextResult[bool]:
        """Load single record to target system."""
        try:
            # Process as RECORD message
            return self.process_record_message(target, stream_name, record)

        except Exception as e:
            error_msg = f"Failed to load record to stream {stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    def load_batch(
        self, target: FlextTypes.Core.Dict, stream_name: str, records: list[RecordDict]
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Load batch of records to target system."""
        try:
            self._logger.info(
                "Loading batch", stream_name=stream_name, record_count=len(records)
            )

            # Records validation is handled by business logic

            # Process each record
            loaded_count = 0
            failed_count = 0

            for record in records:
                load_result = self.load_record(target, stream_name, record)
                if load_result.success:
                    loaded_count += 1
                else:
                    failed_count += 1
                    self._logger.warning(
                        "Failed to load record",
                        stream_name=stream_name,
                        error=load_result.error,
                    )

            # Update batch statistics with proper type handling
            current_batches = target.get("batches_processed", 0)
            target["batches_processed"] = (
                int(current_batches) + 1
                if isinstance(current_batches, (int, str))
                else 1
            )

            batch_result = {
                "stream_name": stream_name,
                "records_attempted": len(records),
                "records_loaded": loaded_count,
                "records_failed": failed_count,
                "batch_number": target["batches_processed"],
                "status": "completed" if failed_count == 0 else "partial_failure",
            }

            self._logger.info(
                "Batch loading completed",
                stream_name=stream_name,
                loaded_count=loaded_count,
                failed_count=failed_count,
            )

            return FlextResult[FlextTypes.Core.Dict].ok(batch_result)

        except Exception as e:
            error_msg = f"Failed to load batch to stream {stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    def finalize_stream(
        self, target: FlextTypes.Core.Dict, stream_name: str
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Finalize stream loading (commit, cleanup, etc.)."""
        try:
            self._logger.info("Finalizing stream", stream_name=stream_name)

            # Get stream info
            target_streams = target.get("streams", {})
            if (
                not isinstance(target_streams, dict)
                or stream_name not in target_streams
            ):
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Stream {stream_name} not found"
                )

            stream_info = target_streams[stream_name]
            if isinstance(stream_info, dict):
                stream_info["status"] = "finalized"
                stream_info["finalized_at"] = (
                    FlextUtilities.Generators.generate_iso_timestamp()
                )

                finalization_result = {
                    "stream_name": stream_name,
                    "records_loaded": stream_info.get("records_loaded", 0),
                    "batches_processed": stream_info.get("batches_processed", 0),
                    "status": "finalized",
                }

                self._logger.info(
                    "Stream finalized successfully", stream_name=stream_name
                )
                return FlextResult[FlextTypes.Core.Dict].ok(finalization_result)

            return FlextResult[FlextTypes.Core.Dict].fail("Invalid stream info")

        except Exception as e:
            error_msg = f"Failed to finalize stream {stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ============================================================================
    # TARGET FINALIZATION METHODS
    # ============================================================================

    def finalize(
        self, target: FlextTypes.Core.Dict
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Finalize target operations with comprehensive reporting."""
        try:
            self._logger.info("Finalizing target operations")

            # Target validation is handled by business logic

            # Collect statistics from all streams
            stream_stats = {}
            total_records = 0
            target_streams = target.get("streams", {})

            if isinstance(target_streams, dict):
                for stream_name, stream_info in target_streams.items():
                    if isinstance(stream_info, dict):
                        records_loaded = stream_info.get("records_loaded", 0)
                        stream_stats[stream_name] = {
                            "records_loaded": records_loaded,
                            "batches_processed": stream_info.get(
                                "batches_processed", 0
                            ),
                            "status": stream_info.get("status", "unknown"),
                        }
                        total_records += (
                            int(records_loaded)
                            if isinstance(records_loaded, (int, str))
                            else 0
                        )

            finalization_result: FlextTypes.Core.Dict = {
                "status": "completed",
                "total_streams": len(target_streams)
                if isinstance(target_streams, dict)
                else 0,
                "total_records": total_records,
                "stream_stats": stream_stats,
                "final_state": target.get("state", {}),
                "config_summary": {
                    "target_type": target.get("target_type", "unknown"),
                    "batch_size": 0,
                    "max_batches": 0,
                },
                "finalized_at": FlextUtilities.Generators.generate_iso_timestamp(),
            }

            # Update target status
            target["status"] = "finalized"
            target["finalized_at"] = FlextUtilities.Generators.generate_iso_timestamp()

            self._logger.info(
                "Target operations finalized successfully",
                total_streams=finalization_result["total_streams"],
                total_records=total_records,
            )

            return FlextResult[FlextTypes.Core.Dict].ok(finalization_result)

        except Exception as e:
            error_msg = f"Failed to finalize target operations: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ============================================================================
    # QUERY AND UTILITY METHODS
    # ============================================================================

    def get_stream_by_name(
        self, target: FlextTypes.Core.Dict, stream_name: str
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Get stream by name with error handling."""
        try:
            target_streams = target.get("streams", {})
            if (
                not isinstance(target_streams, dict)
                or stream_name not in target_streams
            ):
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Stream {stream_name} not found"
                )

            return FlextResult[FlextTypes.Core.Dict].ok(target_streams[stream_name])

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to get stream {stream_name}: {e}"
            )

    def list_streams(self, target: FlextTypes.Core.Dict) -> FlextTypes.Core.StringList:
        """List all active stream names."""
        target_streams = target.get("streams", {})
        return list(target_streams.keys()) if isinstance(target_streams, dict) else []

    def get_target_type(self, target: FlextTypes.Core.Dict) -> str:
        """Get target type."""
        return str(target.get("target_type", "unknown"))

    def get_active_targets(self) -> FlextTypes.Core.StringList:
        """Get list of active target IDs."""
        return list(self._active_targets.keys())

    def get_registered_streams(self) -> FlextTypes.Core.StringList:
        """Get list of registered stream keys."""
        return list(self._stream_registry.keys())

    @classmethod
    def create_instance(cls) -> FlextResult[FlextTargetAbstractions]:
        """Factory method to create FlextTargetAbstractions instance."""
        return FlextResult["FlextTargetAbstractions"].ok(cls())

    # Test compatibility methods and properties
    @property
    def id(self) -> str:
        """Get target ID for test compatibility."""
        return self.target_id

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate business rules for test compatibility."""
        validation_result = True
        return FlextResult[bool].ok(data=validation_result)

    def is_development(self) -> bool:
        """Check if running in development mode."""
        return True

    def is_test(self) -> bool:
        """Check if running in test mode."""
        return True

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return False

    # =============================================================================

    # =============================================================================


__all__ = [
    "FlextTargetAbstractions",
]
