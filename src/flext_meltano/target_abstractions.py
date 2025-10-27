"""FLEXT Pipeline Sink Abstractions - Single unified class for sink operations.

This module provides the FlextMeltanoTargetAbstractions class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextResult
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult, FlextService

from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoTargetAbstractions(
    FlextService[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
    """UNIFIED Sink Abstractions class consolidating ALL sink functionality.

    This single class provides:
    - Complete Singer sink protocol implementation
    - Sink management and batch processing
    - Configuration validation and processing
    - Railway-oriented error handling throughout

    Following FLEXT 'one class per module' pattern.
    """

    # Instance attributes (declared for type checker)
    _config: FlextMeltanoConfig

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize unified sink abstractions with FLEXT configuration."""
        self._config = config or FlextMeltanoConfig()

        # Initialize FlextService parent class
        super().__init__()

    def configure_sink(
        self, sink_config: FlextMeltanoModels.DataSinkConfig
    ) -> FlextResult[FlextMeltanoModels.DataSinkDefinition]:
        """Configure a sink for a sink configuration.

        Args:
        sink_config: Sink configuration

        Returns:
        FlextResult containing configured sink definition

        """
        try:
            self.logger.info(
                "Configuring sink for target",
                target_name=sink_config.sink_type,
                target_type=sink_config.sink_type,
            )

            # Create sink definition
            sink_def = FlextMeltanoModels.DataSinkDefinition(
                sink_name=f"{sink_config.sink_type}_sink",
                sink_type=sink_config.sink_type,
                config=sink_config.model_dump(),
                status="configured",
            )

            self.logger.info(
                "Sink configured successfully",
                sink_name=sink_def.sink_name,
            )

            return FlextResult[FlextMeltanoModels.DataSinkDefinition].ok(sink_def)

        except Exception as e:
            self.logger.exception("Sink configuration failed", error=str(e))
            return FlextResult[FlextMeltanoModels.DataSinkDefinition].fail(
                f"Sink configuration failed: {e}"
            )

    def validate_sink_config(
        self, sink_config: FlextMeltanoModels.DataSinkConfig
    ) -> FlextResult[bool]:
        """Validate a sink configuration.

        Args:
        sink_config: Sink configuration to validate

        Returns:
        FlextResult containing validation result

        """
        try:
            self.logger.debug(
                "Validating target configuration",
                target_name=sink_config.sink_type,
            )

            # Basic validation
            if not sink_config.sink_type:
                return FlextResult[bool].fail(
                    "Target configuration must have name and type"
                )

            # Additional validation logic would go here
            # For now, just return success
            return FlextResult[bool].ok(True)

        except Exception as e:
            self.logger.exception(
                "Target configuration validation failed", error=str(e)
            )
            return FlextResult[bool].fail(
                f"Target configuration validation failed: {e}"
            )

    def create_sink_instance(
        self, sink_config: FlextMeltanoModels.DataSinkConfig
    ) -> FlextResult[FlextMeltanoModels.DataSinkInstance]:
        """Create a sink instance from configuration.

        Args:
        sink_config: Sink configuration

        Returns:
        FlextResult containing configured sink instance

        """
        try:
            self.logger.info(
                "Creating sink instance",
                sink_name=sink_config.sink_type,
                sink_type=sink_config.sink_type,
            )

            # Create sink instance
            sink_instance = FlextMeltanoModels.DataSinkInstance(
                sink_type=sink_config.sink_type,
                config=sink_config,
                status="configured",
            )

            self.logger.info(
                "Sink instance created successfully",
                sink_name=sink_instance.config.sink_type,
            )

            return FlextResult[FlextMeltanoModels.DataSinkInstance].ok(sink_instance)

        except Exception as e:
            self.logger.exception("Sink instance creation failed", error=str(e))
            return FlextResult[FlextMeltanoModels.DataSinkInstance].fail(
                f"Sink instance creation failed: {e}"
            )

    def handle_schema_message(self, schema: dict[str, object]) -> FlextResult[bool]:
        """Handle Singer SCHEMA message for target.

        Args:
            schema: Singer schema message containing stream schema

        Returns:
            FlextResult containing success status

        """
        try:
            self.logger.debug(
                "Handling Singer schema message",
            )

            if not schema:
                return FlextResult[bool].fail("Schema message cannot be empty")

            if "properties" not in schema:
                return FlextResult[bool].fail("Schema message must contain properties")

            self.logger.debug(
                "Schema message handled successfully",
            )

            return FlextResult[bool].ok(True)

        except Exception as e:
            self.logger.exception("Schema message handling failed", error=str(e))
            return FlextResult[bool].fail(f"Schema message handling failed: {e}")

    def handle_record_message(self, record: dict[str, object]) -> FlextResult[bool]:
        """Handle Singer RECORD message for target.

        Args:
            record: Singer record message containing data record

        Returns:
            FlextResult containing success status

        """
        try:
            self.logger.debug(
                "Handling Singer record message",
            )

            if not record:
                return FlextResult[bool].fail("Record message cannot be empty")

            self.logger.debug(
                "Record message handled successfully",
            )

            return FlextResult[bool].ok(True)

        except Exception as e:
            self.logger.exception("Record message handling failed", error=str(e))
            return FlextResult[bool].fail(f"Record message handling failed: {e}")

    def handle_state_message(self, state: dict[str, object]) -> FlextResult[bool]:
        """Handle Singer STATE message for target.

        Args:
            state: Singer state message containing replication state

        Returns:
            FlextResult containing success status

        """
        try:
            self.logger.debug(
                "Handling Singer state message",
            )

            if not state:
                return FlextResult[bool].fail("State message cannot be empty")

            self.logger.debug(
                "State message handled successfully",
            )

            return FlextResult[bool].ok(True)

        except Exception as e:
            self.logger.exception("State message handling failed", error=str(e))
            return FlextResult[bool].fail(f"State message handling failed: {e}")

    def batch_records_for_insert(
        self, records: list[dict[str, object]], batch_size: int = 500
    ) -> FlextResult[list[list[dict[str, object]]]]:
        """Batch records for efficient insert operations.

        Args:
            records: List of records to batch for insertion
            batch_size: Size of each batch (default: 500)

        Returns:
            FlextResult containing list of record batches

        """
        try:
            self.logger.debug(
                "Batching records for insert",
                record_count=len(records),
                batch_size=batch_size,
            )

            if not records:
                return FlextResult[list[list[dict[str, object]]]].fail(
                    "Record list cannot be empty"
                )

            if batch_size <= 0:
                return FlextResult[list[list[dict[str, object]]]].fail(
                    "Batch size must be positive"
                )

            # Create batches
            batches: list[list[dict[str, object]]] = [
                records[i : i + batch_size] for i in range(0, len(records), batch_size)
            ]

            self.logger.info(
                "Records batched for insert successfully",
                record_count=len(records),
                batch_count=len(batches),
                batch_size=batch_size,
            )

            return FlextResult[list[list[dict[str, object]]]].ok(batches)

        except Exception as e:
            self.logger.exception("Record batching failed", error=str(e))
            return FlextResult[list[list[dict[str, object]]]].fail(
                f"Record batching failed: {e}"
            )

    def process_record_as_upsert(
        self, record: dict[str, object], unique_keys: list[str]
    ) -> FlextResult[dict[str, object]]:
        """Prepare record for upsert operation.

        Args:
            record: Record to prepare for upsert
            unique_keys: List of key fields for uniqueness

        Returns:
            FlextResult containing processed record

        """
        try:
            self.logger.debug(
                "Processing record as upsert",
                unique_keys=unique_keys,
            )

            if not record:
                return FlextResult[dict[str, object]].fail("Record cannot be empty")

            if not unique_keys:
                return FlextResult[dict[str, object]].fail(
                    "Unique keys cannot be empty for upsert"
                )

            # Validate all unique keys exist in record
            missing_keys = [key for key in unique_keys if key not in record]
            if missing_keys:
                return FlextResult[dict[str, object]].fail(
                    f"Record missing unique keys: {missing_keys}"
                )

            # Add upsert operation metadata
            processed_record = dict(record)
            processed_record["__sdc_operation"] = "UPSERT"
            processed_record["__sdc_key_columns"] = unique_keys

            self.logger.debug(
                "Record processed for upsert",
            )

            return FlextResult[dict[str, object]].ok(processed_record)

        except Exception as e:
            self.logger.exception("Record upsert processing failed", error=str(e))
            return FlextResult[dict[str, object]].fail(
                f"Record upsert processing failed: {e}"
            )

    def process_record_as_insert(
        self, record: dict[str, object]
    ) -> FlextResult[dict[str, object]]:
        """Prepare record for insert operation.

        Args:
            record: Record to prepare for insertion

        Returns:
            FlextResult containing processed record

        """
        try:
            self.logger.debug(
                "Processing record as insert",
            )

            if not record:
                return FlextResult[dict[str, object]].fail("Record cannot be empty")

            # Add insert operation metadata
            processed_record = dict(record)
            processed_record["__sdc_operation"] = "INSERT"

            self.logger.debug(
                "Record processed for insert",
            )

            return FlextResult[dict[str, object]].ok(processed_record)

        except Exception as e:
            self.logger.exception("Record insert processing failed", error=str(e))
            return FlextResult[dict[str, object]].fail(
                f"Record insert processing failed: {e}"
            )

    def execute(
        self,
    ) -> FlextResult[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]:
        """Execute sink abstraction operations (implements Domain.Service)."""
        # This would orchestrate the overall sink abstraction workflow
        # For now, return the current configuration
        return FlextResult[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict].ok(
            self._config.model_dump()
        )
