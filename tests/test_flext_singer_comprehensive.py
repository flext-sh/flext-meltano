"""Comprehensive tests for FlextSinger module.

Tests all functionality in flext_singer.py to achieve high coverage.
"""

from __future__ import annotations

from flext_meltano.flext_singer import (
    FlextSingerBridge,
    FlextSingerCatalog,
    flext_create_singer_bridge,
    flext_create_singer_catalog,
)


class TestFlextSingerBridge:
    """Test FlextSinger bridge functionality."""

    def test_bridge_initialization(self) -> None:
        """Test bridge initialization."""
        bridge = FlextSingerBridge()
        assert bridge is not None
        assert hasattr(bridge, "_logger")
        assert hasattr(bridge, "_container")
        assert hasattr(bridge, "_message_types")

    def test_create_record_message(self) -> None:
        """Test creating RECORD message."""
        bridge = FlextSingerBridge()

        record_data = {"id": 1, "name": "test"}
        result = bridge.flext_singer_create_record_message("users", record_data)

        assert result.success
        if result.data is not None:
            assert result.data["type"] == "RECORD"
            assert result.data["stream"] == "users"
            assert result.data["record"] == {"id": 1, "name": "test"}

    def test_create_schema_message(self) -> None:
        """Test creating SCHEMA message."""
        bridge = FlextSingerBridge()

        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }

        result = bridge.flext_singer_create_schema_message("users", schema)

        assert result.success
        if result.data is not None:
            assert result.data["type"] == "SCHEMA"
            assert result.data["stream"] == "users"
            assert result.data["schema"] == schema

    def test_create_state_message(self) -> None:
        """Test creating STATE message."""
        bridge = FlextSingerBridge()

        state = {"bookmarks": {"users": {"timestamp": "2023-01-01T00:00:00Z"}}}
        result = bridge.flext_singer_create_state_message(state)

        assert result.success
        if result.data is not None:
            assert result.data["type"] == "STATE"
            assert result.data["value"] == state

    def test_parse_message_line(self) -> None:
        """Test parsing Singer message line."""
        bridge = FlextSingerBridge()

        message_line = '{"type": "RECORD", "stream": "users", "record": {"id": 1}}'
        result = bridge.flext_singer_parse_message_line(message_line)

        assert result.success
        if result.data is not None:
            assert result.data["type"] == "RECORD"
            assert result.data["stream"] == "users"


class TestFlextSingerCatalog:
    """Test FlextSinger catalog functionality."""

    def test_catalog_initialization(self) -> None:
        """Test catalog initialization."""
        catalog = FlextSingerCatalog()
        assert catalog is not None
        assert hasattr(catalog, "_catalog")
        assert hasattr(catalog, "_logger")

    def test_catalog_add_stream(self) -> None:
        """Test adding stream to catalog."""
        catalog = FlextSingerCatalog()

        stream_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }

        result = catalog.flext_singer_add_stream("users", stream_schema)
        assert result.success

    def test_catalog_get_catalog(self) -> None:
        """Test getting catalog."""
        catalog = FlextSingerCatalog()

        result = catalog.flext_singer_get_catalog()
        assert result.success
        assert result.data is not None


class TestFlextSingerFactoryFunctions:
    """Test factory functions."""

    def test_flext_create_singer_bridge(self) -> None:
        """Test creating singer bridge."""
        bridge = flext_create_singer_bridge()
        assert bridge is not None
        assert isinstance(bridge, FlextSingerBridge)

    def test_flext_create_singer_catalog(self) -> None:
        """Test creating singer catalog."""
        catalog = flext_create_singer_catalog()
        assert catalog is not None
        assert isinstance(catalog, FlextSingerCatalog)
