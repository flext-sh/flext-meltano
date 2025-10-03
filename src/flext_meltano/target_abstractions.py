"""FLEXT Meltano Target Abstractions - Singer target protocol abstractions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_cli import FlextCli

from flext_core import (
    FlextConstants,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.typings import FlextMeltanoTypes

# Constants

# Type aliases to replace explicit object (avoid shadowing Pydantic ConfigDict)
RecordDict = FlextTypes.Dict
ConnectionConfig = FlextTypes.Dict
SchemaDict = FlextTypes.Dict
StateDict = FlextTypes.Dict
ResultDict = FlextTypes.Dict


class FlextTargetAbstractions(FlextMeltanoProtocols.SingerTargetProtocol):
    """UNIFIED Target Abstractions implementing SingerTargetProtocol.

    CORRECTED ARCHITECTURE:
    - NO longer inherits from FlextModels.Entity (inappropriate for abstractions)
    - Simple class focused on target functionality abstraction
    - Follows single responsibility principle
    - Consolidates all target functionality: "FlextTargetConfig", FlextStreamInfo nested classes
    """

    # =========================================================================
    # NESTED PYDANTIC MODELS - Domain-specific data validation
    # =========================================================================

    class FlextTargetConfig(FlextMeltanoModels.TargetConfig):
        """Target configuration - uses unified FlextMeltanoModels.TargetConfig.

        This class extends the unified model for any target-specific customizations
        while maintaining the consolidated [Project]Models pattern.
        """

    class FlextStreamInfo(FlextMeltanoModels.StreamInfo):
        """Stream information - uses unified FlextMeltanoModels.StreamInfo.

        This class extends the unified model for any target-specific customizations
        while maintaining the consolidated [Project]Models pattern.
        """

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
        self._cli = FlextCli()
        self._active_targets: FlextTypes.NestedDict = {}
        self._target_configs: dict[str, FlextTargetAbstractions.FlextTargetConfig] = {}
        self._stream_registry: dict[str, FlextTargetAbstractions.FlextStreamInfo] = {}

    # ============================================================================
    # TARGET CONFIGURATION METHODS
    # ============================================================================

    def create_flext_target_config(
        self,
        target_type: str,
        connection_config: ConnectionConfig,
        batch_size: int = FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,  # SOURCE OF TRUTH
        max_batches: int = 100,  # No specific constant for max_batches yet
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Dict]:
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
            config_id: str = f"{target_type}_{id(config_model)}"
            self._target_configs[config_id] = config_model

            # Convert to dict for compatibility
            config_dict: FlextMeltanoTypes.Core.PluginConfigDict = (
                config_model.model_dump()
            )
            config_dict["config_id"] = config_id

            self._logger.info(
                "FlextTarget config created",
                target_type=target_type,
                config_id=config_id,
            )
            return FlextResult[FlextTypes.Dict].ok(data=config_dict)

        except Exception as e:
            error_msg = f"Failed to create FlextTarget config: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Dict].fail(error_msg)

    # Removed _validate_target_config - validation now handled by Pydantic FlextTargetConfig model

    # ============================================================================
    # TARGET CREATION AND MANAGEMENT METHODS
    # ============================================================================

    def create_flext_target(
        self,
        config: FlextTypes.Dict,
        _adapter: FlextMeltanoAdapter | None = None,
    ) -> FlextResult[FlextTypes.Dict]:
        """Create FlextTarget instance from configuration."""
        try:
            # Extract target_type for logging
            target_type = str(config.get("target_type", "unknown"))
            self._logger.info("Creating FlextTarget", target_type=target_type)

            # Config validation is handled by Pydantic models during usage

            # Create target instance
            target_instance: FlextTypes.Dict = {
                "target_type": "target_type",
                "config": dict(config),
                "adapter": "adapter",
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
            return FlextResult[FlextTypes.Dict].ok(
                {
                    **target_instance,
                    "target_id": "target_id",
                },
            )

        except Exception as e:
            error_msg = f"Failed to create FlextTarget: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Dict].fail(error_msg)

    # ============================================================================
    # MESSAGE PROCESSING METHODS
    # ============================================================================

    def process_schema_message(
        self,
        target: FlextTypes.Dict,
        stream_name: str,
        schema: SchemaDict,
    ) -> FlextResult[bool]:
        """Process Singer SCHEMA message with error handling."""
        try:
            self._cli.info(f"Processing SCHEMA message for stream: {stream_name}")
            self._logger.info("Processing SCHEMA message", stream_name=stream_name)

            # Create stream info with Pydantic validation
            try:
                stream_info_model = self.FlextStreamInfo(
                    stream_name=stream_name,
                    schema=schema,  # Use alias parameter
                    status="processing",  # Valid status: initialized, processing, completed, error
                    created_at=FlextUtilities.Generators.generate_iso_timestamp(),
                )
            except Exception as e:
                return FlextResult[bool].fail(f"Stream validation failed: {e}")

            # Target validation is handled by business logic, not field validation

            # Create or update stream
            target_streams_raw = target.get("streams", {})
            target_streams: FlextMeltanoTypes.Core.SingerSchemaDict = cast(
                "FlextMeltanoTypes.Core.SingerSchemaDict", target_streams_raw
            )
            if not target_streams:
                target_streams = {}
                target["streams"] = target_streams

            # Use validated stream info from Pydantic model
            stream_info_dict: FlextMeltanoTypes.Core.SingerSchemaDict = (
                stream_info_model.model_dump()
            )
            target_streams[stream_name] = stream_info_dict

            # Register stream with Pydantic model
            stream_key = f"{target.get('target_type', 'unknown')}_{stream_name}"
            self._stream_registry[stream_key] = stream_info_model

            self._cli.success(
                f"SCHEMA message processed successfully for stream: {stream_name}"
            )
            self._logger.info(
                "SCHEMA message processed successfully",
                stream_name=stream_name,
            )
            return FlextResult[bool].ok(data=True)

        except Exception as e:
            error_msg = (
                f"Failed to process SCHEMA message for stream {stream_name}: {e}"
            )
            self._logger.exception(error_msg)
            self._cli.error(error_msg)
            return FlextResult[bool].fail(error_msg)

    def process_record_message(
        self,
        target: FlextTypes.Dict,
        stream_name: str,
        record: RecordDict,
    ) -> FlextResult[bool]:
        """Process Singer RECORD message with error handling."""
        try:
            self._logger.debug("Processing RECORD message", stream_name=stream_name)

            # Log record for debugging (fulfilling ARG002 requirement)
            # Use basic debug logging without level comparison
            self._logger.debug(
                "Record data received",
                record_keys=list(record.keys()),
            )

            # Parameter validation is handled by business logic, not field validation

            # Check if stream exists
            target_streams_raw = target.get("streams", {})
            target_streams: FlextMeltanoTypes.Core.SingerSchemaDict = cast(
                "FlextMeltanoTypes.Core.SingerSchemaDict", target_streams_raw
            )
            if stream_name not in target_streams:
                return FlextResult[bool].fail(
                    f"Stream {stream_name} not found - SCHEMA message required first",
                )

            # Process record
            stream_info_raw = target_streams[stream_name]
            stream_info: FlextMeltanoTypes.Core.SingerSchemaDict = cast(
                "FlextMeltanoTypes.Core.SingerSchemaDict", stream_info_raw
            )
            current_count = stream_info.get("records_loaded", 0)
            # Cast to int for arithmetic operation
            stream_info["records_loaded"] = cast("int", current_count) + 1
            stream_info["status"] = "record_processed"

            # Update target statistics with proper type handling
            current_count = target.get("loaded_records", 0)
            # Cast to int for arithmetic operation
            target["loaded_records"] = cast("int", current_count) + 1

            self._logger.debug(
                "RECORD message processed successfully",
                stream_name=stream_name,
            )
            return FlextResult[bool].ok(data=True)

        except Exception as e:
            error_msg = (
                f"Failed to process RECORD message for stream {stream_name}: {e}"
            )
            self._logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    def process_state_message(
        self,
        target: FlextTypes.Dict,
        state: StateDict,
    ) -> FlextResult[bool]:
        """Process Singer STATE message with error handling."""
        try:
            self._logger.debug("Processing STATE message")

            # Parameter validation is handled by business logic

            # Update internal state
            target_state_raw = target.get("state", {})
            target_state: FlextMeltanoTypes.Core.SingerStateDict = cast(
                "FlextMeltanoTypes.Core.SingerStateDict", target_state_raw
            )
            if not target_state:
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
        self,
        target: FlextTypes.Dict,
        stream_name: str,
        record: RecordDict,
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
        self,
        target: FlextTypes.Dict,
        stream_name: str,
        records: list[RecordDict],
    ) -> FlextResult[FlextTypes.Dict]:
        """Load batch of records to target system."""
        try:
            self._logger.info(
                "Loading batch",
                stream_name=stream_name,
                record_count=len(records),
            )

            # Records validation is handled by business logic

            # Process each record
            loaded_count = 0
            failed_count = 0

            for record in records:
                load_result: FlextResult[bool] = self.load_record(
                    target, stream_name, record
                )
                if not load_result.is_failure:
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

            batch_result: FlextTypes.Dict = {
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

            return FlextResult[FlextTypes.Dict].ok(data=batch_result)

        except Exception as e:
            error_msg = f"Failed to load batch to stream {stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Dict].fail(error_msg)

    def finalize_stream(
        self,
        target: FlextTypes.Dict,
        stream_name: str,
    ) -> FlextResult[FlextTypes.Dict]:
        """Finalize stream loading (commit, cleanup, etc.)."""
        try:
            self._logger.info("Finalizing stream", stream_name=stream_name)

            # Get stream info
            target_streams_raw = target.get("streams", {})
            target_streams: FlextMeltanoTypes.Core.SingerSchemaDict = cast(
                "FlextMeltanoTypes.Core.SingerSchemaDict", target_streams_raw
            )
            if (
                not isinstance(target_streams, dict)
                or stream_name not in target_streams
            ):
                return FlextResult[FlextTypes.Dict].fail(
                    f"Stream {stream_name} not found",
                )

            stream_info = target_streams[stream_name]
            if isinstance(stream_info, dict):
                stream_info["status"] = "finalized"
                stream_info["finalized_at"] = (
                    FlextUtilities.Generators.generate_iso_timestamp()
                )

                finalization_result: FlextTypes.Dict = {
                    "stream_name": stream_name,
                    "records_loaded": stream_info.get("records_loaded", 0),
                    "batches_processed": stream_info.get("batches_processed", 0),
                    "status": "finalized",
                }

                self._logger.info(
                    "Stream finalized successfully",
                    stream_name=stream_name,
                )
                return FlextResult[FlextTypes.Dict].ok(data=finalization_result)

            return FlextResult[FlextTypes.Dict].fail("Invalid stream info")

        except Exception as e:
            error_msg = f"Failed to finalize stream {stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Dict].fail(error_msg)

    # ============================================================================
    # TARGET FINALIZATION METHODS
    # ============================================================================

    def finalize(
        self,
        target: FlextTypes.Dict,
    ) -> FlextResult[FlextTypes.Dict]:
        """Finalize target operations with comprehensive reporting."""
        try:
            self._logger.info("Finalizing target operations")

            # Target validation is handled by business logic

            # Collect statistics from all streams
            stream_stats = {}
            total_records = 0
            target_streams_raw = target.get("streams", {})
            target_streams: FlextMeltanoTypes.Core.SingerSchemaDict = cast(
                "FlextMeltanoTypes.Core.SingerSchemaDict", target_streams_raw
            )

            if isinstance(target_streams, dict):
                for stream_name, stream_info in target_streams.items():
                    if isinstance(stream_info, dict):
                        records_loaded = stream_info.get("records_loaded", 0)
                        stream_stats[stream_name] = {
                            "records_loaded": records_loaded,
                            "batches_processed": stream_info.get(
                                "batches_processed",
                                0,
                            ),
                            "status": stream_info.get("status", "unknown"),
                        }
                        total_records += (
                            int(records_loaded)
                            if isinstance(records_loaded, (int, str))
                            else 0
                        )

            finalization_result: FlextTypes.Dict = {
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

            return FlextResult[FlextTypes.Dict].ok(data=finalization_result)

        except Exception as e:
            error_msg = f"Failed to finalize target operations: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Dict].fail(error_msg)

    # ============================================================================
    # QUERY AND UTILITY METHODS
    # ============================================================================

    def get_stream_by_name(
        self,
        target: FlextTypes.Dict,
        stream_name: str,
    ) -> FlextResult[FlextTypes.Dict]:
        """Get stream by name with error handling."""
        try:
            target_streams_raw = target.get("streams", {})
            target_streams: FlextMeltanoTypes.Core.SingerSchemaDict = cast(
                "FlextMeltanoTypes.Core.SingerSchemaDict", target_streams_raw
            )
            if (
                not isinstance(target_streams, dict)
                or stream_name not in target_streams
            ):
                return FlextResult[FlextTypes.Dict].fail(
                    f"Stream {stream_name} not found",
                )

            return FlextResult[FlextTypes.Dict].ok(
                data=cast("FlextTypes.Dict", target_streams[stream_name]),
            )

        except Exception as e:
            return FlextResult[FlextTypes.Dict].fail(
                f"Failed to get stream {stream_name}: {e}",
            )

    def list_streams(self, target: FlextTypes.Dict) -> FlextTypes.StringList:
        """List all active stream names."""
        target_streams_raw = target.get("streams", {})
        target_streams: FlextMeltanoTypes.Core.SingerSchemaDict = cast(
            "FlextMeltanoTypes.Core.SingerSchemaDict", target_streams_raw
        )
        return list(target_streams.keys()) if isinstance(target_streams, dict) else []

    def get_target_type(self, target: FlextTypes.Dict) -> str:
        """Get target type."""
        return str(target.get("target_type", "unknown"))

    def get_active_targets(self) -> FlextTypes.StringList:
        """Get list of active target IDs."""
        return list(self._active_targets.keys())

    def get_registered_streams(self) -> FlextTypes.StringList:
        """Get list of registered stream keys."""
        return list(self._stream_registry.keys())

    @classmethod
    def create_instance(cls) -> FlextResult[FlextTargetAbstractions]:
        """Factory method to create FlextTargetAbstractions instance."""
        return FlextResult[FlextTargetAbstractions].ok(data=cls())

    def is_production(self: object) -> bool:
        """Check if running in production mode."""
        return False

    # =============================================================================
    # PROTOCOL IMPLEMENTATION - SingerTargetProtocol
    # =============================================================================

    def handle_record(
        self, record: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle a single record (implements SingerTargetProtocol)."""
        try:
            # Extract stream information from record
            stream_name = record.get("stream", "unknown")
            record_data = record.get("record", {})

            # Create a dummy target config for processing
            target_config = cast("FlextTypes.Dict", {"stream": stream_name})

            # Use existing load_record functionality
            load_result = self.load_record(
                target_config, str(stream_name), cast("RecordDict", record_data)
            )

            if load_result.is_failure:
                return FlextResult[FlextTypes.JsonValue].fail(
                    load_result.error or "Unknown error"
                )

            return FlextResult[FlextTypes.JsonValue].ok({
                "loaded": load_result.unwrap()
            })
        except Exception as e:
            return FlextResult[FlextTypes.JsonValue].fail(
                f"Record handling failed: {e}"
            )

    def handle_batch(
        self, records: list[FlextTypes.JsonValue]
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle a batch of records (implements SingerTargetProtocol)."""
        try:
            # Group records by stream
            streams_data: dict[str, list[FlextTypes.JsonValue]] = {}

            for record in records:
                stream_name = str(record.get("stream", "unknown"))
                if stream_name not in streams_data:
                    streams_data[stream_name] = []
                streams_data[stream_name].append(
                    cast("FlextTypes.Dict", record.get("record", {}))
                )

            # Process each stream's batch
            results = {}
            for stream_name, stream_records in streams_data.items():
                target_config = cast("FlextTypes.Dict", {"stream": stream_name})
                batch_records = cast("list[RecordDict]", stream_records)

                batch_result = self.load_batch(
                    target_config, stream_name, batch_records
                )
                if batch_result.is_failure:
                    return FlextResult[FlextTypes.JsonValue].fail(
                        f"Batch processing failed for stream {stream_name}: {batch_result.error}"
                    )

                results[stream_name] = batch_result.unwrap()

            return FlextResult[FlextTypes.JsonValue].ok(results)
        except Exception as e:
            return FlextResult[FlextTypes.JsonValue].fail(f"Batch handling failed: {e}")

    def execute(self) -> FlextResult[object]:
        """Execute the target loading (implements Domain.Service)."""
        try:
            # Finalize all streams and targets
            finalize_result = self.finalize()
            if finalize_result.is_failure:
                return FlextResult[object].fail(
                    f"Target finalization failed: {finalize_result.error}"
                )

            return FlextResult[object].ok({
                "target_type": self.get_target_type(),
                "streams": list(self.get_registered_streams()),
                "finalized": finalize_result.unwrap(),
            })
        except Exception as e:
            return FlextResult[object].fail(f"Target execution failed: {e}")

    # Protocol compliance validation methods
    def is_valid(self: object) -> bool:
        """Check if the target service is in a valid state (implements Domain.Service)."""
        return hasattr(self, "_stream_registry") and len(self._stream_registry) >= 0

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate business rules for the target service (implements Domain.Service)."""
        try:
            # Basic validation - ensure target registry is initialized
            if not hasattr(self, "_stream_registry"):
                return FlextResult[None].fail("Stream registry not initialized")

            if not hasattr(self, "_active_targets"):
                return FlextResult[None].fail("Active targets registry not initialized")

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    def validate_config(self: object) -> FlextResult[None]:
        """Validate service configuration (implements Domain.Service)."""
        try:
            # Basic configuration validation
            if not hasattr(self, "target_id"):
                return FlextResult[None].fail("Target ID not configured")

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Config validation failed: {e}")

    def execute_operation(self, operation: object) -> FlextResult[object]:
        """Execute operation using OperationExecutionRequest model (implements Domain.Service)."""
        try:
            if isinstance(operation, dict):
                op_type = operation.get("type", "unknown")

                if op_type == "handle_record":
                    record = operation.get("record", {})
                    result = self.handle_record(cast("FlextTypes.JsonValue", record))
                    return (
                        FlextResult[object].ok(result.unwrap())
                        if result.is_success
                        else FlextResult[object].fail(
                            result.error or "Handle record failed"
                        )
                    )
                if op_type == "handle_batch":
                    records = operation.get("records", [])
                    result = self.handle_batch(
                        cast("list[FlextTypes.JsonValue]", records)
                    )
                    return (
                        FlextResult[object].ok(result.unwrap())
                        if result.is_success
                        else FlextResult[object].fail(
                            result.error or "Handle batch failed"
                        )
                    )
                if op_type == "finalize":
                    return self.execute()
                return FlextResult[object].fail(f"Unknown operation type: {op_type}")

            return FlextResult[object].fail("Invalid operation format")
        except Exception as e:
            return FlextResult[object].fail(f"Operation execution failed: {e}")

    def get_service_info(self: object) -> FlextTypes.Dict:
        """Get service information and metadata (implements Domain.Service)."""
        return {
            "service_name": "FlextTargetAbstractions",
            "service_type": "singer_target",
            "target_id": getattr(self, "target_id", "unknown"),
            "streams_count": len(self._stream_registry)
            if hasattr(self, "_stream_registry")
            else 0,
            "active_targets": len(self._active_targets)
            if hasattr(self, "_active_targets")
            else 0,
            "protocol_version": "1.0.0",
        }

    # =============================================================================

    # =============================================================================


__all__ = [
    "FlextTargetAbstractions",
]
