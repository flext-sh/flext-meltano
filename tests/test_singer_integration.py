"""Test Singer SDK integration.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Tests for Singer SDK integration including:
- Tap and Target creation
- Stream processing
- Catalog discovery
- Testing utilities
"""

from typing import ClassVar

import pytest

from flext_meltano import (
    FlextMeltanoConfig,
    PropertiesList,
    Property,
    Sink,
    Stream,
    Tap,
    Target,
    get_tap_test_class,
    singer_typing,
)
from flext_meltano.base import (
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    create_meltano_tap_service,
    create_meltano_target_service,
)

# Constants
EXPECTED_DATA_COUNT = 3


class TestSingerSDKReExports:
    """Test Singer SDK re-exports."""

    def test_core_classes_available(self) -> None:
        """Test core Singer SDK classes are available."""
        assert Tap is not None
        assert Target is not None
        assert Stream is not None
        assert Sink is not None

    def test_typing_utilities(self) -> None:
        """Test Singer SDK typing utilities."""
        assert singer_typing is not None
        assert PropertiesList is not None
        assert Property is not None

    def test_testing_utilities(self) -> None:
        """Test Singer SDK testing utilities."""
        assert get_tap_test_class is not None
        assert callable(get_tap_test_class)


class TestTapServiceIntegration:
    """Test tap service integration."""

    def test_tap_service_creation(self) -> None:
        """Test tap service creation."""
        config = FlextMeltanoConfig()
        result = create_meltano_tap_service(config)

        assert result.is_success
        assert isinstance(result.data, FlextMeltanoTapService)

    def test_tap_service_validation(self) -> None:
        """Test tap service validation."""
        config = FlextMeltanoConfig()
        tap_service = FlextMeltanoTapService(config)

        # Should fail validation without tap class
        validation_result = tap_service.validate_ready_for_use()
        assert not validation_result.is_success
        assert validation_result.error is not None
        if "Tap class not configured" not in validation_result.error:
            msg = f"Expected {'Tap class not configured'} in {validation_result.error}"
            raise AssertionError(msg)

    def test_tap_service_health(self) -> None:
        """Test tap service health status."""
        config = FlextMeltanoConfig()
        tap_service = FlextMeltanoTapService(config)

        health_result = tap_service.get_health_status()
        assert health_result.is_success
        assert health_result.data is not None
        if health_result.data["service"] != "tap":
            msg = f"Expected {'tap'}, got {health_result.data['service']}"
            raise AssertionError(msg)
        if health_result.data["tap_configured"]:
            msg = f"Expected False, got {health_result.data['tap_configured']}"
            raise AssertionError(msg)

    def test_tap_class_setting(self) -> None:
        """Test setting tap class."""
        config = FlextMeltanoConfig()
        tap_service = FlextMeltanoTapService(config)

        # Create a mock tap class
        class MockTap(Tap):
            name = "tap-mock"
            config_jsonschema: ClassVar = {
                "type": "object",
                "properties": {
                    "test_config": {"type": "string"},
                },
            }

            def discover_streams(self) -> list[Stream]:
                return []

        # Set tap class
        result = tap_service.set_tap_class(MockTap)
        assert result.is_success

        # Validation should now pass
        validation_result = tap_service.validate_ready_for_use()
        assert validation_result.is_success


class TestTargetServiceIntegration:
    """Test target service integration."""

    def test_target_service_creation(self) -> None:
        """Test target service creation."""
        config = FlextMeltanoConfig()
        result = create_meltano_target_service(config)

        assert result.is_success
        assert isinstance(result.data, FlextMeltanoTargetService)

    def test_target_service_validation(self) -> None:
        """Test target service validation."""
        config = FlextMeltanoConfig()
        target_service = FlextMeltanoTargetService(config)

        # Should fail ready-for-use validation without target class
        validation_result = target_service.validate_ready_for_use()
        assert not validation_result.is_success
        assert validation_result.error is not None
        if "Target class not configured" not in validation_result.error:
            msg = (
                f"Expected {'Target class not configured'} in {validation_result.error}"
            )
            raise AssertionError(msg)

    def test_target_service_health(self) -> None:
        """Test target service health status."""
        config = FlextMeltanoConfig()
        target_service = FlextMeltanoTargetService(config)

        health_result = target_service.get_health_status()
        assert health_result.is_success
        assert health_result.data is not None
        if health_result.data["service"] != "target":
            msg = f"Expected {'target'}, got {health_result.data['service']}"
            raise AssertionError(msg)
        if health_result.data["target_configured"]:
            msg = f"Expected False, got {health_result.data['target_configured']}"
            raise AssertionError(msg)

    def test_target_class_setting(self) -> None:
        """Test setting target class."""
        config = FlextMeltanoConfig()
        target_service = FlextMeltanoTargetService(config)

        # Create a mock target class
        class MockTarget(Target):
            name = "target-mock"
            config_jsonschema: ClassVar = {
                "type": "object",
                "properties": {
                    "test_config": {"type": "string"},
                },
            }

        # Set target class
        result = target_service.set_target_class(MockTarget)
        assert result.is_success

        # Ready-for-use validation should now pass
        validation_result = target_service.validate_ready_for_use()
        assert validation_result.is_success


class TestSingerTypingUtilities:
    """Test Singer typing utilities."""

    def test_property_creation(self) -> None:
        """Test Property creation."""
        prop = Property("test_field", singer_typing.StringType)
        assert prop is not None

    def test_properties_list_creation(self) -> None:
        """Test PropertiesList creation."""
        props = PropertiesList(
            Property("id", singer_typing.StringType),
            Property("name", singer_typing.StringType),
            Property("count", singer_typing.IntegerType),
        )
        assert props is not None
        # PropertiesList doesn't support len(), check it has properties
        prop_list = list(props)
        if len(prop_list) != EXPECTED_DATA_COUNT:
            msg = f"Expected {3}, got {len(prop_list)}"
            raise AssertionError(msg)

    def test_singer_types_available(self) -> None:
        """Test Singer types are available."""
        assert hasattr(singer_typing, "StringType")
        assert hasattr(singer_typing, "IntegerType")
        assert hasattr(singer_typing, "NumberType")
        assert hasattr(singer_typing, "BooleanType")
        assert hasattr(singer_typing, "DateTimeType")


class TestTapTestingUtilities:
    """Test tap testing utilities."""

    def test_get_tap_test_class(self) -> None:
        """Test get_tap_test_class utility."""

        # Create a mock tap class
        class MockTap(Tap):
            name = "tap-test"
            config_jsonschema: ClassVar = {
                "type": "object",
                "properties": {
                    "api_url": {"type": "string"},
                },
            }

            def discover_streams(self) -> list[Stream]:
                return []

        # Get test class
        test_class = get_tap_test_class(
            tap_class=MockTap,
            config={"api_url": "https://api.example.com"},
        )

        assert test_class is not None
        # Test class should be a test case class
        # Check for any test methods (Singer SDK interface may vary)
        test_methods = [attr for attr in dir(test_class) if attr.startswith("test_")]
        assert len(test_methods) > 0, (
            f"No test methods found. Available methods: {test_methods}"
        )


class TestStreamProcessing:
    """Test stream processing capabilities."""

    def test_stream_creation(self) -> None:
        """Test stream creation."""

        # Create a mock tap
        class MockTap(Tap):
            name = "tap-mock"

            def discover_streams(self) -> list[Stream]:
                return [MockStream(self)]

        class MockStream(Stream):
            name = "test_stream"
            path = "/test"
            primary_keys: ClassVar = ["id"]

            schema: ClassVar = {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                },
            }

            def get_records(self, context: dict[str, object] | None = None) -> object:
                yield {"id": "1", "name": "test"}

        tap = MockTap(config={})
        streams = tap.discover_streams()

        if len(streams) != 1:
            msg = f"Expected {1}, got {len(streams)}"
            raise AssertionError(msg)
        assert streams[0].name == "test_stream"

    def test_stream_schema(self) -> None:
        """Test stream schema definition."""
        schema = PropertiesList(
            Property("id", singer_typing.StringType),
            Property("name", singer_typing.StringType),
            Property("created_at", singer_typing.DateTimeType),
            Property("active", singer_typing.BooleanType),
        )

        # PropertiesList doesn't support len(), check via list conversion
        schema_list = list(schema)
        if len(schema_list) != 4:
            msg = f"Expected {4}, got {len(schema_list)}"
            raise AssertionError(msg)
        # Schema should be iterable
        fields = list(schema)
        if len(fields) != 4:
            msg = f"Expected {4}, got {len(fields)}"
            raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
