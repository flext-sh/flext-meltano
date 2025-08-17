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

from collections.abc import Iterator
from typing import Any, ClassVar

from singer_sdk import Stream, Tap, Target, typing as singer_typing

from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    create_flext_meltano_bridge,
)

# =============================================================================
# EXAMPLE 1: Basic Bridge Integration
# =============================================================================


def basic_bridge_example() -> dict[str, Any]:
    """Demonstrates basic Singer SDK bridge usage with REAL APIs."""
    # Create REAL bridge
    bridge = create_flext_meltano_bridge()

    try:
      # Test bridge health
      health_result = bridge.validate_bridge_health()

      # Get service information
      service_info = bridge.get_service_info()

      return {
          "bridge_healthy": health_result.success,
          "service_available": service_info.success,
          "bridge_version": bridge.get_bridge_version(),
          "status": "bridge_integration_successful",
      }
    except Exception as e:
      return {
          "bridge_healthy": False,
          "error": str(e),
          "status": "bridge_integration_failed",
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
          description="Database host",
      ),
      singer_typing.Property(
          "port",
          singer_typing.IntegerType,
          default=5432,
          description="Database port",
      ),
      singer_typing.Property(
          "username",
          singer_typing.StringType,
          required=True,
          description="Database username",
      ),
      singer_typing.Property(
          "password",
          singer_typing.StringType,
          required=True,
          secret=True,
          description="Database password",
      ),
      singer_typing.Property(
          "database",
          singer_typing.StringType,
          required=True,
          description="Database name",
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

    name: ClassVar[str] = "users"
    primary_keys: ClassVar[list[str]] = ["id"]
    replication_key: ClassVar[str] = "updated_at"

    # Schema definition using Singer SDK typing
    schema = singer_typing.PropertiesList(
      singer_typing.Property(
          "id",
          singer_typing.IntegerType,
          description="User ID",
      ),
      singer_typing.Property(
          "name",
          singer_typing.StringType,
          description="User name",
      ),
      singer_typing.Property(
          "email",
          singer_typing.StringType,
          description="User email",
      ),
      singer_typing.Property(
          "updated_at",
          singer_typing.DateTimeType,
          description="Last updated timestamp",
      ),
    ).to_dict()

    def get_records(self, context: dict[str, Any] | None) -> Iterator[dict[str, Any]]:
      """Generate sample user records.

      When provided, "context" can be used to filter or adjust the output
      (e.g., by replication bookmark). Here, respect a trivial filter if passed.
      """
      # Simulate data extraction
      sample_users = [
          {
              "id": 1,
              "name": "Alice Johnson",
              "email": "alice@example.com",
              "updated_at": "2025-01-01T10:00:00Z",
          },
          {
              "id": 2,
              "name": "Bob Smith",
              "email": "bob@example.com",
              "updated_at": "2025-01-01T11:00:00Z",
          },
          {
              "id": 3,
              "name": "Carol Davis",
              "email": "carol@example.com",
              "updated_at": "2025-01-01T12:00:00Z",
          },
      ]
      # If a context with a "min_id" is provided, filter accordingly
      min_id = None
      if isinstance(context, dict):
          raw_min = context.get("min_id")
          if isinstance(raw_min, (int, str)):
              try:
                  min_id = int(raw_min)
              except ValueError:
                  min_id = None

      filtered = (
          (u for u in sample_users if (min_id is None or int(u["id"]) >= min_id))
          if min_id is not None
          else iter(sample_users)
      )

      yield from filtered


class ExampleOrdersStream(Stream):
    """Example orders stream using Singer SDK patterns."""

    name: ClassVar[str] = "orders"
    primary_keys: ClassVar[list[str]] = ["id"]
    replication_key: ClassVar[str] = "created_at"

    # Schema definition
    schema = singer_typing.PropertiesList(
      singer_typing.Property(
          "id",
          singer_typing.IntegerType,
          description="Order ID",
      ),
      singer_typing.Property(
          "user_id",
          singer_typing.IntegerType,
          description="User ID",
      ),
      singer_typing.Property(
          "total",
          singer_typing.NumberType,
          description="Order total",
      ),
      singer_typing.Property(
          "created_at",
          singer_typing.DateTimeType,
          description="Order creation timestamp",
      ),
    ).to_dict()

    def get_records(self, context: dict[str, Any] | None) -> Iterator[dict[str, Any]]:
      """Generate sample order records.

      Uses optional context to filter by "user_id" when provided.
      """
      sample_orders = [
          {
              "id": 101,
              "user_id": 1,
              "total": 29.99,
              "created_at": "2025-01-01T13:00:00Z",
          },
          {
              "id": 102,
              "user_id": 2,
              "total": 49.99,
              "created_at": "2025-01-01T14:00:00Z",
          },
          {
              "id": 103,
              "user_id": 1,
              "total": 19.99,
              "created_at": "2025-01-01T15:00:00Z",
          },
      ]
      user_id_filter = None
      if isinstance(context, dict):
          raw_uid = context.get("user_id")
          if isinstance(raw_uid, (int, str)):
              try:
                  user_id_filter = int(raw_uid)
              except ValueError:
                  user_id_filter = None

      filtered = (
          (
              o
              for o in sample_orders
              if (user_id_filter is None or int(o["user_id"]) == user_id_filter)
          )
          if user_id_filter is not None
          else iter(sample_orders)
      )

      yield from filtered


def professional_tap_example() -> dict[str, Any]:
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
          "status": "professional_tap_successful",
      }
    except Exception as e:
      return {
          "tap_created": False,
          "error": str(e),
          "status": "professional_tap_failed",
      }


# =============================================================================
# EXAMPLE 3: Professional Singer Target Implementation
# =============================================================================


class ExampleSink:
    """Example sink for the professional target."""

    def __init__(
      self,
      target: Target,
      stream_name: str,
      schema: dict[str, Any],
      key_properties: list[str],
    ) -> None:
      """Initialize sink."""
      self.target = target
      self.stream_name = stream_name
      self.schema = schema
      self.key_properties = key_properties
      self.records_processed = 0

    def process_record(self, record: dict[str, Any], context: dict[str, Any]) -> None:
      """Process a single record respecting context flags when present."""
      # Example: skip records when context requests dry-run
      if isinstance(context, dict) and context.get("dry_run") is True:
          return

      # Simulate record processing
      if isinstance(record, dict):
          self.records_processed += 1

      # In real implementation, this would write to destination

    def process_batch(self, context: dict[str, Any]) -> None:
      """Process a batch of records."""
      # Simulate batch processing


class ProfessionalExampleTarget(Target):
    """Professional Singer target using real Singer SDK patterns."""

    name = "professional-example-target"

    # Configuration schema
    config_jsonschema = singer_typing.PropertiesList(
      singer_typing.Property(
          "output_path",
          singer_typing.StringType,
          required=True,
          description="Output file path",
      ),
      singer_typing.Property(
          "batch_size",
          singer_typing.IntegerType,
          default=1000,
          description="Batch size for processing",
      ),
    ).to_dict()

    default_sink_class = ExampleSink


def professional_target_example() -> dict[str, Any]:
    """Demonstrates professional target implementation."""
    # Configuration
    config = {
      "output_path": "./.tmp_target_output",
      "batch_size": 100,
    }

    try:
      # Create target instance
      ProfessionalExampleTarget(config=config)

      # Simulate processing some records
      sample_records = [
          {"type": "RECORD", "stream": "users", "record": {"id": 1, "name": "Alice"}},
          {"type": "RECORD", "stream": "users", "record": {"id": 2, "name": "Bob"}},
          {
              "type": "RECORD",
              "stream": "orders",
              "record": {"id": 101, "user_id": 1, "total": 29.99},
          },
      ]

      records_processed = len(sample_records)

      return {
          "target_created": True,
          "records_processed": records_processed,
          "output_path": config["output_path"],
          "batch_size": config["batch_size"],
          "status": "professional_target_successful",
      }
    except Exception as e:
      return {
          "target_created": False,
          "error": str(e),
          "status": "professional_target_failed",
      }


# =============================================================================
# EXAMPLE 4: Bridge-Integrated Pipeline
# =============================================================================


def bridge_integrated_pipeline_example() -> dict[str, Any]:
    """Demonstrates complete pipeline using bridge integration."""
    # Create FLEXT Meltano configuration
    FlextMeltanoConfig(
      project_root="./demo_project",
      environment="development",
    )

    # Create bridge
    bridge = FlextMeltanoBridge()

    try:
      # Validate bridge health
      health_result = bridge.validate_bridge_health()
      if not health_result.success:
          return {
              "pipeline_executed": False,
              "error": f"Bridge health check failed: {health_result.error}",
              "status": "bridge_unhealthy",
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
          "service_info": service_info.data
          if service_info.success
          else "Not available",
          "status": "complete_pipeline_successful",
      }
    except Exception as e:
      return {
          "pipeline_executed": False,
          "error": str(e),
          "status": "complete_pipeline_failed",
      }


# =============================================================================
# MAIN EXECUTION
# =============================================================================


def main() -> None:
    """Execute all examples."""
    # Example 1: Basic bridge integration
    basic_bridge_example()

    # Example 2: Professional tap
    tap_result = professional_tap_example()
    if tap_result.get("streams_discovered"):
      pass

    # Example 3: Professional target
    professional_target_example()

    # Example 4: Complete pipeline
    bridge_integrated_pipeline_example()


if __name__ == "__main__":
    main()
