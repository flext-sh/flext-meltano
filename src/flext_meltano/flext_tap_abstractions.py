"""FlextTap Abstractions - Complete abstraction of Singer Tap functionality.

This module provides complete FlextTap abstractions so that projects like
flext-tap-* never need to import singer_sdk directly. All tap functionality
is provided through FlextResult patterns with enterprise error handling.

Architecture:
    Tap Layer: Complete tap abstraction from Singer SDK
    Stream Layer: Stream abstractions with FlextResult integration  
    Discovery Layer: Schema discovery abstractions without Singer SDK dependency
    Config Layer: Configuration abstractions for tap implementations

Features:
    - Complete tap abstraction from singer_sdk.Tap
    - Stream discovery and data extraction with FlextResult error handling
    - Configuration management without Singer SDK dependency
    - Schema generation and catalog creation abstracted
    - Zero dependency on singer_sdk for consuming projects

Examples:
    Basic tap usage:
        >>> from flext_meltano import FlextMeltanoTypeAdapters
        >>> adapters = FlextMeltanoTypeAdapters()
        >>> tap_result = adapters.create_flext_tap(tap_config)
        >>> if tap_result.success:
        ...     tap = tap_result.value
        ...     streams_result = tap.discover_streams()

    Stream extraction:
        >>> stream_result = tap.get_stream_by_name("users")
        >>> if stream_result.success:
        ...     stream = stream_result.value
        ...     records_result = stream.extract_records()

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generator, Protocol, runtime_checkable

from flext_core import FlextLogger, FlextResult

# Initialize logger
logger = FlextLogger(__name__)

# =============================================================================
# FLEXT TAP PROTOCOLS - Abstract interfaces for tap operations
# =============================================================================


@runtime_checkable
class FlextStreamExtractor(Protocol):
    """Protocol for FlextStream data extraction operations."""

    def extract_records(self, config: dict[str, Any] | None = None) -> FlextResult[Generator[dict[str, Any], None, None]]:
        """Extract records from stream."""
        ...

    def get_record_count(self) -> FlextResult[int]:
        """Get total record count if available."""
        ...

    def supports_incremental(self) -> bool:
        """Check if stream supports incremental extraction."""
        ...


@runtime_checkable
class FlextTapDiscovery(Protocol):
    """Protocol for FlextTap discovery operations."""

    def discover_streams(self) -> FlextResult[list[FlextTapStream]]:
        """Discover available streams."""
        ...

    def generate_catalog(self) -> FlextResult[dict[str, Any]]:
        """Generate Singer catalog."""
        ...

    def validate_config(self) -> FlextResult[bool]:
        """Validate tap configuration."""
        ...


# =============================================================================
# FLEXT TAP CONFIGURATION ABSTRACTIONS
# =============================================================================


class FlextTapConfig:
    """Base configuration abstraction for FlextTap implementations.
    
    Provides configuration management without requiring Singer SDK imports.
    """

    def __init__(
        self,
        tap_type: str,
        connection_config: dict[str, Any],
        stream_config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize FlextTap configuration."""
        self.tap_type = tap_type
        self.connection_config = connection_config
        self.stream_config = stream_config or {}
        self.additional_config = kwargs
        
    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary format."""
        return {
            "tap_type": self.tap_type,
            "connection_config": self.connection_config,
            "stream_config": self.stream_config,
            **self.additional_config,
        }

    def validate(self) -> FlextResult[bool]:
        """Validate tap configuration."""
        if not self.tap_type:
            return FlextResult[bool].fail("Tap type is required")
            
        if not self.connection_config:
            return FlextResult[bool].fail("Connection configuration is required")
            
        return FlextResult[bool].ok(True)

    def get_stream_config(self, stream_name: str) -> dict[str, Any]:
        """Get configuration for specific stream."""
        return self.stream_config.get(stream_name, {})


# =============================================================================
# FLEXT TAP STREAM ABSTRACTIONS
# =============================================================================


class FlextTapStream:
    """FlextTap stream abstraction with FlextResult error handling."""

    def __init__(
        self, 
        stream_name: str, 
        schema: dict[str, Any], 
        tap_config: FlextTapConfig,
        adapter: FlextMeltanoTypeAdapters,
    ) -> None:
        """Initialize FlextTap stream."""
        self.stream_name = stream_name
        self.schema = schema
        self.tap_config = tap_config
        self._adapter = adapter
        self._logger = FlextLogger(f"{__name__}.FlextTapStream")
        self._records_extracted = 0

    def get_schema(self) -> FlextResult[dict[str, Any]]:
        """Get stream schema with error handling."""
        try:
            if not self.schema:
                return FlextResult[dict[str, Any]].fail(
                    f"No schema available for stream {self.stream_name}"
                )

            self._logger.debug("Schema retrieved for stream", stream_name=self.stream_name)
            return FlextResult[dict[str, Any]].ok(self.schema)

        except Exception as e:
            error_msg = f"Failed to get schema for stream {self.stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, Any]].fail(error_msg)

    def extract_records(self, limit: int | None = None) -> FlextResult[list[dict[str, Any]]]:
        """Extract records from stream with error handling.

        Args:
            limit: Maximum number of records to extract

        Returns:
            FlextResult containing list of records or error

        """
        try:
            self._logger.info("Starting record extraction", stream_name=self.stream_name, limit=limit)

            # This would be implemented by concrete stream classes
            # For now, return empty result as placeholder
            records: list[dict[str, Any]] = []
            
            # Update extraction count
            self._records_extracted = len(records)
            
            self._logger.info(
                "Record extraction completed",
                stream_name=self.stream_name,
                records_extracted=self._records_extracted
            )

            return FlextResult[list[dict[str, Any]]].ok(records)

        except Exception as e:
            error_msg = f"Failed to extract records from stream {self.stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[list[dict[str, Any]]].fail(error_msg)

    def get_catalog_entry(self) -> FlextResult[dict[str, Any]]:
        """Generate Singer catalog entry for this stream."""
        try:
            # Extract primary keys from schema
            primary_keys = []
            if "properties" in self.schema:
                # This is a simple heuristic - real implementations would be more sophisticated
                for prop_name, prop_def in self.schema["properties"].items():
                    if isinstance(prop_def, dict) and prop_def.get("primary_key"):
                        primary_keys.append(prop_name)

            # Create metadata entries
            metadata = [
                {
                    "breadcrumb": [],
                    "metadata": {
                        "replication-method": "FULL_TABLE",
                        "selected": True,
                    },
                }
            ]

            # Add field-level metadata
            if "properties" in self.schema:
                for field_name in self.schema["properties"]:
                    field_metadata = {
                        "breadcrumb": ["properties", field_name],
                        "metadata": {
                            "inclusion": "automatic" if field_name in primary_keys else "available",
                        },
                    }
                    metadata.append(field_metadata)

            catalog_entry = {
                "tap_stream_id": self.stream_name,
                "stream": self.stream_name,
                "schema": self.schema,
                "metadata": metadata,
            }

            return FlextResult[dict[str, Any]].ok(catalog_entry)

        except Exception as e:
            error_msg = f"Failed to generate catalog entry for stream {self.stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, Any]].fail(error_msg)

    def get_stats(self) -> dict[str, object]:
        """Get stream extraction statistics."""
        return {
            "stream_name": self.stream_name,
            "records_extracted": self._records_extracted,
            "has_schema": bool(self.schema),
            "schema_properties": len(self.schema.get("properties", {})) if self.schema else 0,
        }

    @property
    def name(self) -> str:
        """Get stream name."""
        return self.stream_name


# =============================================================================
# MAIN FLEXT TAP CLASS - Complete Tap abstraction
# =============================================================================


class FlextTap:
    """Complete FlextTap abstraction for Singer tap functionality.
    
    Provides enterprise-grade tap functionality without requiring Singer SDK:
    - FlextResult railway-oriented programming for all operations
    - Type-safe stream discovery and data extraction
    - Comprehensive error handling and logging
    - Integration with flext-core patterns
    """

    def __init__(self, config: FlextTapConfig, adapter: FlextMeltanoTypeAdapters) -> None:
        """Initialize FlextTap.

        Args:
            config: Tap configuration
            adapter: Parent type adapter for context

        """
        self.config = config
        self._adapter = adapter
        self._logger = FlextLogger(f"{__name__}.FlextTap")
        self._streams: dict[str, FlextTapStream] = {}
        self._discovered = False

    def discover_streams(self) -> FlextResult[list[FlextTapStream]]:
        """Discover available streams with type safety and error handling.

        Returns:
            FlextResult containing list of FlextTapStream objects or error

        """
        try:
            self._logger.info("Starting stream discovery", tap_type=self.config.tap_type)

            # This would be implemented by concrete tap classes
            # For now, create empty streams list as placeholder
            streams: list[FlextTapStream] = []
            
            # Update internal streams registry
            self._streams = {stream.name: stream for stream in streams}
            self._discovered = True

            self._logger.info(
                "Stream discovery completed",
                tap_type=self.config.tap_type,
                stream_count=len(streams)
            )

            return FlextResult[list[FlextTapStream]].ok(streams)

        except Exception as e:
            error_msg = f"Stream discovery failed for tap {self.config.tap_type}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[list[FlextTapStream]].fail(error_msg)

    def get_stream_by_name(self, stream_name: str) -> FlextResult[FlextTapStream]:
        """Get stream by name with error handling."""
        try:
            if not self._discovered:
                discovery_result = self.discover_streams()
                if discovery_result.failure:
                    return FlextResult[FlextTapStream].fail(
                        f"Stream discovery failed: {discovery_result.error}"
                    )

            if stream_name not in self._streams:
                return FlextResult[FlextTapStream].fail(f"Stream {stream_name} not found")

            stream = self._streams[stream_name]
            self._logger.debug("Stream retrieved", stream_name=stream_name)
            
            return FlextResult[FlextTapStream].ok(stream)

        except Exception as e:
            error_msg = f"Failed to get stream {stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTapStream].fail(error_msg)

    def generate_catalog(self) -> FlextResult[dict[str, Any]]:
        """Generate Singer catalog with all discovered streams."""
        try:
            self._logger.info("Generating Singer catalog")

            if not self._discovered:
                discovery_result = self.discover_streams()
                if discovery_result.failure:
                    return FlextResult[dict[str, Any]].fail(
                        f"Stream discovery failed: {discovery_result.error}"
                    )

            # Generate catalog entries for all streams
            streams_catalog = []
            for stream in self._streams.values():
                entry_result = stream.get_catalog_entry()
                if entry_result.failure:
                    return FlextResult[dict[str, Any]].fail(
                        f"Failed to generate catalog entry for {stream.name}: {entry_result.error}"
                    )
                streams_catalog.append(entry_result.value)

            catalog = {
                "version": 1,
                "streams": streams_catalog,
            }

            self._logger.info("Singer catalog generated successfully", stream_count=len(streams_catalog))
            return FlextResult[dict[str, Any]].ok(catalog)

        except Exception as e:
            error_msg = f"Failed to generate catalog: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, Any]].fail(error_msg)

    def sync_stream(self, stream_name: str, target: FlextTarget | None = None) -> FlextResult[dict[str, object]]:
        """Sync stream data to target or return extraction results.

        Args:
            stream_name: Name of stream to sync
            target: Optional target for data loading

        Returns:
            FlextResult with sync statistics

        """
        try:
            self._logger.info("Starting stream sync", stream_name=stream_name)

            # Get stream
            stream_result = self.get_stream_by_name(stream_name)
            if stream_result.failure:
                return FlextResult[dict[str, object]].fail(stream_result.error)

            stream = stream_result.value

            # Extract records
            records_result = stream.extract_records()
            if records_result.failure:
                return FlextResult[dict[str, object]].fail(records_result.error)

            records = records_result.value

            # If target provided, load data
            if target:
                # Process schema message
                schema_result = stream.get_schema()
                if schema_result.failure:
                    return FlextResult[dict[str, object]].fail(schema_result.error)

                schema_process_result = target.process_schema_message(stream_name, schema_result.value)
                if schema_process_result.failure:
                    return FlextResult[dict[str, object]].fail(schema_process_result.error)

                # Process records
                for record in records:
                    record_process_result = target.process_record_message(stream_name, record)
                    if record_process_result.failure:
                        return FlextResult[dict[str, object]].fail(record_process_result.error)

            sync_stats: dict[str, object] = {
                "stream_name": stream_name,
                "records_processed": len(records),
                "target_loaded": target is not None,
                "status": "completed",
            }

            self._logger.info(
                "Stream sync completed successfully",
                stream_name=stream_name,
                records_processed=len(records)
            )

            return FlextResult[dict[str, object]].ok(sync_stats)

        except Exception as e:
            error_msg = f"Failed to sync stream {stream_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)

    def list_streams(self) -> list[str]:
        """List all discovered stream names."""
        return list(self._streams.keys())

    def validate_config(self) -> FlextResult[bool]:
        """Validate tap configuration."""
        return self.config.validate()

    @property
    def tap_type(self) -> str:
        """Get tap type."""
        return self.config.tap_type


# =============================================================================
# FLEXT TAP FACTORY FUNCTIONS
# =============================================================================


def create_flext_tap_config(
    tap_type: str,
    connection_config: dict[str, Any],
    stream_config: dict[str, Any] | None = None,
    **kwargs: Any,
) -> FlextResult[FlextTapConfig]:
    """Create FlextTap configuration with validation."""
    try:
        config = FlextTapConfig(
            tap_type=tap_type,
            connection_config=connection_config,
            stream_config=stream_config,
            **kwargs,
        )
        
        validation_result = config.validate()
        if validation_result.failure:
            return FlextResult[FlextTapConfig].fail(validation_result.error)
        
        return FlextResult[FlextTapConfig].ok(config)
        
    except Exception as e:
        error_msg = f"Failed to create FlextTap config: {e}"
        logger.exception(error_msg)
        return FlextResult[FlextTapConfig].fail(error_msg)


# Import FlextTarget here to avoid circular imports
from flext_meltano.flext_target_abstractions import FlextTarget
from flext_meltano.flext_type_adapters import FlextMeltanoTypeAdapters

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Main classes
    "FlextTap",
    "FlextTapConfig", 
    "FlextTapStream",
    
    # Protocols
    "FlextTapDiscovery",
    "FlextStreamExtractor",
    
    # Factory functions
    "create_flext_tap_config",
]