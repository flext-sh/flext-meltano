"""Test FlextSinger bridge functionality.

Tests for the Singer SDK bridge that connects Singer SDK to flext-core patterns.
"""

from __future__ import annotations

import pytest

from flext_meltano.flext_singer import (
    FlextSingerBridge,
    FlextSingerCatalog,
    flext_create_singer_bridge,
    flext_create_singer_catalog,
)


class TestFlextSingerBridge:
    """Test FlextSinger bridge functionality."""

    @pytest.fixture
    def bridge(self) -> FlextSingerBridge:
        """Create FlextSinger bridge instance."""
        return FlextSingerBridge()

    def test_bridge_initialization(self, bridge: FlextSingerBridge) -> None:
        """Test bridge initialization."""
        assert bridge is not None
        assert hasattr(bridge, "_logger")
        assert hasattr(bridge, "_container")
        assert hasattr(bridge, "_message_types")

    def test_create_record_message_success(self, bridge: FlextSingerBridge) -> None:
        """Test successful record message creation."""
        result = bridge.flext_singer_create_message(
            "RECORD",
            stream="test_stream",
            record={"id": 1, "name": "test"},
            time_extracted="2023-01-01T00:00:00Z",
        )

        assert result.is_success
        assert result.data is not None
        data = result.data
        if data["type"] != "RECORD":
            msg = f"Expected {"RECORD"}, got {data["type"]}"
            raise AssertionError(msg)
        assert data["stream"] == "test_stream"
        if data["record"] != {"id": 1, "name": "test"}:
            expected_record = {"id": 1, "name": "test"}
            msg = f"Expected {expected_record}, got {data['record']}"
            raise AssertionError(msg)
        assert data["time_extracted"] == "2023-01-01T00:00:00Z"

    def test_create_record_message_without_time(self, bridge: FlextSingerBridge) -> None:
        """Test record message creation without time_extracted."""
        result = bridge.flext_singer_create_message(
            "RECORD",
            stream="test_stream",
            record={"id": 1, "name": "test"},
        )

        assert result.is_success
        assert result.data is not None
        data = result.data
        if data["type"] != "RECORD":
            msg = f"Expected {"RECORD"}, got {data["type"]}"
            raise AssertionError(msg)
        assert data["stream"] == "test_stream"
        if data["record"] != {"id": 1, "name": "test"}:
            expected_record = {"id": 1, "name": "test"}
            msg = f"Expected {expected_record}, got {data['record']}"
            raise AssertionError(msg)
        if "time_extracted" in data:
            msg = f"Expected time_extracted not to be in {data}"
            raise AssertionError(msg)

    def test_create_record_message_invalid_stream(self, bridge: FlextSingerBridge) -> None:
        """Test record message creation with invalid stream."""
        result = bridge.flext_singer_create_message(
            "RECORD",
            stream="",
            record={"id": 1},
        )

        assert not result.is_success
        assert result.error is not None
        assert result.error is not None
        assert result.error is not None
        if "Invalid stream name" not in result.error:
            msg = f"Expected {"Invalid stream name"} in {result.error}"
            raise AssertionError(msg)

    def test_create_record_message_invalid_record(self, bridge: FlextSingerBridge) -> None:
        """Test record message creation with invalid record."""
        result = bridge.flext_singer_create_message(
            "RECORD",
            stream="test_stream",
            record="not_a_dict",
        )

        assert not result.is_success
        assert result.error is not None
        assert result.error is not None
        assert result.error is not None
        if "Invalid stream name or record format" not in result.error:
            msg = f"Expected {"Invalid stream name or record format"} in {result.error}"
            raise AssertionError(msg)

    def test_create_schema_message_success(self, bridge: FlextSingerBridge) -> None:
        """Test successful schema message creation."""
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }

        result = bridge.flext_singer_create_message(
            "SCHEMA",
            stream="test_stream",
            schema=schema,
            key_properties=["id"],
        )

        assert result.is_success
        assert result.data is not None
        data = result.data
        if data["type"] != "SCHEMA":
            msg = f"Expected {"SCHEMA"}, got {data["type"]}"
            raise AssertionError(msg)
        assert data["stream"] == "test_stream"
        if data["schema"] != schema:
            msg = f"Expected {schema}, got {data["schema"]}"
            raise AssertionError(msg)
        assert data["key_properties"] == ["id"]

    def test_create_schema_message_without_keys(self, bridge: FlextSingerBridge) -> None:
        """Test schema message creation without key properties."""
        schema = {"type": "object", "properties": {"id": {"type": "integer"}}}

        result = bridge.flext_singer_create_message(
            "SCHEMA",
            stream="test_stream",
            schema=schema,
        )

        assert result.is_success
        assert result.data is not None
        data = result.data
        if data["type"] != "SCHEMA":
            msg = f"Expected {"SCHEMA"}, got {data["type"]}"
            raise AssertionError(msg)
        assert data["key_properties"] == []

    def test_create_schema_message_invalid_stream(self, bridge: FlextSingerBridge) -> None:
        """Test schema message creation with invalid stream."""
        result = bridge.flext_singer_create_message(
            "SCHEMA",
            stream="",
            schema={"type": "object"},
        )

        assert not result.is_success
        assert result.error is not None
        assert result.error is not None
        assert result.error is not None
        if "Invalid stream name" not in result.error:
            msg = f"Expected {"Invalid stream name"} in {result.error}"
            raise AssertionError(msg)

    def test_create_state_message_success(self, bridge: FlextSingerBridge) -> None:
        """Test successful state message creation."""
        state_value = {"bookmarks": {"test_stream": {"timestamp": "2023-01-01T00:00:00Z"}}}

        result = bridge.flext_singer_create_message(
            "STATE",
            value=state_value,
        )

        assert result.is_success
        assert result.data is not None
        data = result.data
        if data["type"] != "STATE":
            msg = f"Expected {"STATE"}, got {data["type"]}"
            raise AssertionError(msg)
        assert data["value"] == state_value

    def test_create_unknown_message_type(self, bridge: FlextSingerBridge) -> None:
        """Test creation of unknown message type."""
        result = bridge.flext_singer_create_message(
            "UNKNOWN_TYPE",
            test_param="value",
        )

        assert not result.is_success
        assert result.error is not None
        assert result.error is not None
        assert result.error is not None
        if "Unknown message type: UNKNOWN_TYPE" not in result.error:
            msg = f"Expected {"Unknown message type: UNKNOWN_TYPE"} in {result.error}"
            raise AssertionError(msg)


class TestFlextSingerCatalog:
    """Test FlextSinger catalog functionality."""

    @pytest.fixture
    def catalog(self) -> FlextSingerCatalog:
        """Create FlextSinger catalog instance."""
        return FlextSingerCatalog()

    @pytest.fixture
    def catalog_with_data(self) -> FlextSingerCatalog:
        """Create FlextSinger catalog with sample data."""
        initial_catalog = {
            "streams": [
                {
                    "tap_stream_id": "existing_stream",
                    "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {"selected": True, "replication-method": "FULL_TABLE"},
                        },
                    ],
                },
            ],
        }
        return FlextSingerCatalog(initial_catalog)

    def test_catalog_initialization_empty(self, catalog: FlextSingerCatalog) -> None:
        """Test catalog initialization without data."""
        assert catalog is not None

        result = catalog.flext_singer_get_catalog()
        assert result.is_success
        if result.data != {"streams": []}:
            expected_data = {"streams": []}
            msg = f"Expected {expected_data}, got {result.data}"
            raise AssertionError(msg)

    def test_catalog_initialization_with_data(self, catalog_with_data: FlextSingerCatalog) -> None:
        """Test catalog initialization with data."""
        result = catalog_with_data.flext_singer_get_catalog()
        assert result.is_success

        assert result.data is not None
        data = result.data
        if "streams" not in data:
            msg = f"Expected {"streams"} in {data}"
            raise AssertionError(msg)
        if len(data["streams"]) != 1:
            msg = f"Expected {1}, got {len(data["streams"])}"
            raise AssertionError(msg)
        assert data["streams"][0]["tap_stream_id"] == "existing_stream"

    def test_add_stream_success(self, catalog: FlextSingerCatalog) -> None:
        """Test successful stream addition to catalog."""
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }

        result = catalog.flext_singer_add_stream(
            stream_name="test_stream",
            schema=schema,
            key_properties=["id"],
        )

        assert result.is_success

        # Verify stream was added
        catalog_result = catalog.flext_singer_get_catalog()
        assert catalog_result.is_success

        assert catalog_result.data is not None
        streams = catalog_result.data["streams"]
        if len(streams) != 1:
            msg = f"Expected {1}, got {len(streams)}"
            raise AssertionError(msg)
        assert streams[0]["tap_stream_id"] == "test_stream"
        if streams[0]["schema"] != schema:
            msg = f"Expected {schema}, got {streams[0]["schema"]}"
            raise AssertionError(msg)
        assert streams[0]["key_properties"] == ["id"]

    def test_add_stream_without_key_properties(self, catalog: FlextSingerCatalog) -> None:
        """Test stream addition without key properties."""
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}

        result = catalog.flext_singer_add_stream(
            stream_name="test_stream",
            schema=schema,
        )

        assert result.is_success

        catalog_result = catalog.flext_singer_get_catalog()
        assert catalog_result.data is not None
        streams = catalog_result.data["streams"]
        if len(streams) != 1:
            msg = f"Expected {1}, got {len(streams)}"
            raise AssertionError(msg)
        # key_properties may or may not be present, depending on implementation

    def test_get_selected_streams(self, catalog_with_data: FlextSingerCatalog) -> None:
        """Test getting selected streams from catalog."""
        result = catalog_with_data.flext_singer_get_selected_streams()
        assert result.is_success

        selected_streams = result.data
        assert isinstance(selected_streams, list)
        if "existing_stream" not in selected_streams:
            msg = f"Expected {"existing_stream"} in {selected_streams}"
            raise AssertionError(msg)

    def test_get_selected_streams_empty_catalog(self, catalog: FlextSingerCatalog) -> None:
        """Test getting selected streams from empty catalog."""
        result = catalog.flext_singer_get_selected_streams()
        assert result.is_success

        selected_streams = result.data
        assert isinstance(selected_streams, list)
        if len(selected_streams) != 0:
            msg = f"Expected {0}, got {len(selected_streams)}"
            raise AssertionError(msg)


class TestFlextSingerFactoryFunctions:
    """Test factory functions for FlextSinger components."""

    def test_flext_create_singer_bridge(self) -> None:
        """Test bridge factory function."""
        bridge = flext_create_singer_bridge()
        assert isinstance(bridge, FlextSingerBridge)
        assert hasattr(bridge, "_logger")
        assert hasattr(bridge, "_container")

    def test_flext_create_singer_catalog_empty(self) -> None:
        """Test catalog factory function without data."""
        catalog = flext_create_singer_catalog()
        assert isinstance(catalog, FlextSingerCatalog)

        result = catalog.flext_singer_get_catalog()
        assert result.is_success
        if result.data != {"streams": []}:
            expected_data = {"streams": []}
            msg = f"Expected {expected_data}, got {result.data}"
            raise AssertionError(msg)

    def test_flext_create_singer_catalog_with_data(self) -> None:
        """Test catalog factory function with data."""
        initial_data = {
            "streams": [
                {
                    "tap_stream_id": "test_stream",
                    "schema": {"type": "object"},
                    "metadata": [],
                },
            ],
        }

        catalog = flext_create_singer_catalog(initial_data)
        assert isinstance(catalog, FlextSingerCatalog)

        result = catalog.flext_singer_get_catalog()
        assert result.is_success
        if result.data != initial_data:
            msg = f"Expected {initial_data}, got {result.data}"
            raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
