#!/usr/bin/env python3
"""Singer SDK Bridge Usage Example - Professional Tap and Target Development.

**Purpose**: Demonstrate real Singer SDK bridge integration with flext-core patterns
**Scope**: Professional tap and target creation, enterprise Singer implementation
**Target Audience**: Developers creating production Singer components
**Dependencies**: Singer SDK, flext-core patterns, bridge integration

## Overview

This example demonstrates how to use the real Singer SDK bridge with flext-core
to create professional taps and targets with enterprise standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any, Dict, Iterator

# Import REAL APIs from flext-meltano
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    create_flext_meltano_bridge,
)

# Import Singer SDK for real tap/target development
from singer_sdk import Stream, Tap, Target
from singer_sdk import typing as singer_typing


# =============================================================================
# EXAMPLE 1: Basic Bridge Integration
# =============================================================================


def basic_bridge_example() -> Dict[str, Any]:
    """Demonstrates basic Singer SDK bridge usage with REAL APIs."""
    # Create REAL bridge
    bridge = create_flext_meltano_bridge()

    try:
        # Test bridge health
        health_result = bridge.validate_bridge_health()

        # Get service information
        service_info = bridge.get_service_info()

        return {
            "bridge_healthy": health_result.is_success,
            "service_available": service_info.is_success,
            "bridge_version": bridge.get_bridge_version(),
            "status": "bridge_integration_successful"
        }
    except Exception as e:
        return {
            "bridge_healthy": False,
            "error": str(e),
            "status": "bridge_integration_failed"
        }


# =============================================================================
# EXAMPLE 2: Professional Singer Tap Implementation
# =============================================================================


class ProfessionalExampleTap(Tap):
    """Professional Singer tap using real Singer SDK patterns."""

    name = "professional-example-tap"

    # Configuration schema using Singer SDK typing
    config_jsonschema = singer_typing.PropertiesList(
        singer_typing.Property(
            "host",
            singer_typing.StringType,
            required=True,
            description="Database host"
        ),
        singer_typing.Property(
            "port",
            singer_typing.IntegerType,
            default=5432,
            description="Database port"
        ),
        singer_typing.Property(
            "username",
            singer_typing.StringType,
            required=True,
            description="Database username"
        ),
        singer_typing.Property(
            "password",
            singer_typing.StringType,
            required=True,
            secret=True,
            description="Database password"
        ),
        singer_typing.Property(
            "database",
            singer_typing.StringType,
            required=True,
            description="Database name"
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Discover available streams using Singer SDK patterns."""
        return [
            ExampleUsersStream(self),
            ExampleOrdersStream(self),
        ]


class ExampleUsersStream(Stream):
    """Example users stream using Singer SDK patterns."""

    name = "users"
    primary_keys = ["id"]
    replication_key = "updated_at"

    # Schema definition using Singer SDK typing
    schema = singer_typing.PropertiesList(
        singer_typing.Property(
            "id",
            singer_typing.IntegerType,
            description="User ID"
        ),
        singer_typing.Property(
            "name",
            singer_typing.StringType,
            description="User name"
        ),
        singer_typing.Property(
            "email",
            singer_typing.StringType,
            description="User email"
        ),
        singer_typing.Property(
            "updated_at",
            singer_typing.DateTimeType,
            description="Last updated timestamp"
        ),
    ).to_dict()

    def get_records(self, context: Dict[str, Any] | None) -> Iterator[Dict[str, Any]]:
        """Generate sample user records."""
        # Simulate data extraction
        sample_users = [
            {
                "id": 1,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "updated_at": "2025-01-01T10:00:00Z"
            },
            {
                "id": 2,
                "name": "Bob Smith",
                "email": "bob@example.com",
                "updated_at": "2025-01-01T11:00:00Z"
            },
            {
                "id": 3,
                "name": "Carol Davis",
                "email": "carol@example.com",
                "updated_at": "2025-01-01T12:00:00Z"
            },
        ]

        for user in sample_users:
            yield user


class ExampleOrdersStream(Stream):
    """Example orders stream using Singer SDK patterns."""

    name = "orders"
    primary_keys = ["id"]
    replication_key = "created_at"

    # Schema definition
    schema = singer_typing.PropertiesList(
        singer_typing.Property(
            "id",
            singer_typing.IntegerType,
            description="Order ID"
        ),
        singer_typing.Property(
            "user_id",
            singer_typing.IntegerType,
            description="User ID"
        ),
        singer_typing.Property(
            "total",
            singer_typing.NumberType,
            description="Order total"
        ),
        singer_typing.Property(
            "created_at",
            singer_typing.DateTimeType,
            description="Order creation timestamp"
        ),
    ).to_dict()

    def get_records(self, context: Dict[str, Any] | None) -> Iterator[Dict[str, Any]]:
        """Generate sample order records."""
        sample_orders = [
            {
                "id": 101,
                "user_id": 1,
                "total": 29.99,
                "created_at": "2025-01-01T13:00:00Z"
            },
            {
                "id": 102,
                "user_id": 2,
                "total": 49.99,
                "created_at": "2025-01-01T14:00:00Z"
            },
            {
                "id": 103,
                "user_id": 1,
                "total": 19.99,
                "created_at": "2025-01-01T15:00:00Z"
            },
        ]

        for order in sample_orders:
            yield order


def professional_tap_example() -> Dict[str, Any]:
    """Demonstrates professional tap implementation."""
    # Configuration
    config = {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "password",
        "database": "example_db",
    }

    try:
        # Create tap instance
        tap = ProfessionalExampleTap(config=config)

        # Discover streams
        streams = tap.discover_streams()

        # Get catalog
        catalog = tap.catalog

        return {
            "tap_created": True,
            "streams_discovered": len(streams),
            "stream_names": [stream.name for stream in streams],
            "catalog_available": catalog is not None,
            "status": "professional_tap_successful"
        }
    except Exception as e:
        return {
            "tap_created": False,
            "error": str(e),
            "status": "professional_tap_failed"
        }


# =============================================================================
# EXAMPLE 3: Professional Singer Target Implementation
# =============================================================================


class ExampleSink:
    """Example sink for the professional target."""

    def __init__(self, target: Target, stream_name: str, schema: Dict[str, Any], key_properties: list[str]):
        """Initialize sink."""
        self.target = target
        self.stream_name = stream_name
        self.schema = schema
        self.key_properties = key_properties
        self.records_processed = 0

    def process_record(self, record: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Process a single record."""
        # Simulate record processing
        self.records_processed += 1

        # In real implementation, this would write to destination
        print(f"Processing record {self.records_processed} for stream {self.stream_name}: {record}")

    def process_batch(self, context: Dict[str, Any]) -> None:
        """Process a batch of records."""
        # Simulate batch processing
        print(f"Processed batch of {self.records_processed} records for stream {self.stream_name}")


class ProfessionalExampleTarget(Target):
    """Professional Singer target using real Singer SDK patterns."""

    name = "professional-example-target"

    # Configuration schema
    config_jsonschema = singer_typing.PropertiesList(
        singer_typing.Property(
            "output_path",
            singer_typing.StringType,
            required=True,
            description="Output file path"
        ),
        singer_typing.Property(
            "batch_size",
            singer_typing.IntegerType,
            default=1000,
            description="Batch size for processing"
        ),
    ).to_dict()

    default_sink_class = ExampleSink


def professional_target_example() -> Dict[str, Any]:
    """Demonstrates professional target implementation."""
    # Configuration
    config = {
        "output_path": "/tmp/target_output",
        "batch_size": 100,
    }

    try:
        # Create target instance
        target = ProfessionalExampleTarget(config=config)

        # Simulate processing some records
        sample_records = [
            {"type": "RECORD", "stream": "users", "record": {"id": 1, "name": "Alice"}},
            {"type": "RECORD", "stream": "users", "record": {"id": 2, "name": "Bob"}},
            {"type": "RECORD", "stream": "orders", "record": {"id": 101, "user_id": 1, "total": 29.99}},
        ]

        records_processed = len(sample_records)

        return {
            "target_created": True,
            "records_processed": records_processed,
            "output_path": config["output_path"],
            "batch_size": config["batch_size"],
            "status": "professional_target_successful"
        }
    except Exception as e:
        return {
            "target_created": False,
            "error": str(e),
            "status": "professional_target_failed"
        }


# =============================================================================
# EXAMPLE 4: Bridge-Integrated Pipeline
# =============================================================================


def bridge_integrated_pipeline_example() -> Dict[str, Any]:
    """Demonstrates complete pipeline using bridge integration."""
    # Create FLEXT Meltano configuration
    config = FlextMeltanoConfig(
        project_root="./demo_project",
        environment="development"
    )

    # Create bridge
    bridge = FlextMeltanoBridge()

    try:
        # Validate bridge health
        health_result = bridge.validate_bridge_health()
        if not health_result.is_success:
            return {
                "pipeline_executed": False,
                "error": f"Bridge health check failed: {health_result.error}",
                "status": "bridge_unhealthy"
            }

        # Execute professional tap
        tap_result = professional_tap_example()

        # Execute professional target
        target_result = professional_target_example()

        # Get service information
        service_info = bridge.get_service_info()

        return {
            "pipeline_executed": True,
            "bridge_healthy": True,
            "tap_result": tap_result,
            "target_result": target_result,
            "service_info": service_info.data if service_info.is_success else "Not available",
            "status": "complete_pipeline_successful"
        }
    except Exception as e:
        return {
            "pipeline_executed": False,
            "error": str(e),
            "status": "complete_pipeline_failed"
        }


# =============================================================================
# MAIN EXECUTION
# =============================================================================


def main() -> None:
    """Execute all examples."""
    print("🎵 FLEXT Meltano Singer Bridge Examples - Professional Implementation")
    print("=" * 70)

    # Example 1: Basic bridge integration
    print("\n🌉 Basic Bridge Integration:")
    bridge_result = basic_bridge_example()
    print(f"   Bridge Status: {bridge_result['status']}")

    # Example 2: Professional tap
    print("\n📥 Professional Tap Implementation:")
    tap_result = professional_tap_example()
    print(f"   Tap Status: {tap_result['status']}")
    if tap_result.get('streams_discovered'):
        print(f"   Streams: {tap_result['stream_names']}")

    # Example 3: Professional target
    print("\n📤 Professional Target Implementation:")
    target_result = professional_target_example()
    print(f"   Target Status: {target_result['status']}")

    # Example 4: Complete pipeline
    print("\n🔄 Complete Bridge-Integrated Pipeline:")
    pipeline_result = bridge_integrated_pipeline_example()
    print(f"   Pipeline Status: {pipeline_result['status']}")

    print("\n✅ All Singer bridge examples completed!")


if __name__ == "__main__":
    main()
