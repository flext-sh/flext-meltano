"""Comprehensive Coverage Tests for FLEXT Singer Module.

**Purpose**: Test all classes and methods in flext_singer.py to achieve maximum coverage
**Scope**: FlextSingerBridge, FlextSingerCatalog, and factory functions
**Target**: Increase flext_singer.py coverage from 0% to maximum possible

This module provides complete functional tests for Singer SDK bridge integration
with comprehensive message processing and catalog management testing.
"""

from __future__ import annotations

import json
from io import StringIO
from unittest.mock import patch

from flext_meltano import (
    FlextSingerBridge,
    FlextSingerCatalog,
    __all__ as _singer_all,
    flext_create_singer_bridge,
    flext_create_singer_catalog,
)


class TestFlextSingerBridgeComplete:
    """Complete tests for FlextSingerBridge class."""

    def test_singer_bridge_initialization(self) -> None:
        """Test Singer bridge initialization."""
        bridge = FlextSingerBridge()

        assert bridge is not None
        assert hasattr(bridge, "_logger")
        assert hasattr(bridge, "_container")
        assert hasattr(bridge, "_message_types")
        assert len(bridge._message_types) == 3
        assert "RECORD" in bridge._message_types
        assert "SCHEMA" in bridge._message_types
        assert "STATE" in bridge._message_types

    def test_create_record_message_success(self) -> None:
        """Test creating record message successfully."""
        bridge = FlextSingerBridge()

        record = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        result = bridge.flext_singer_create_record_message(
            stream="customers",
            record=record,
            time_extracted="2025-08-05T10:00:00Z",
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "RECORD"
        assert result.data["stream"] == "customers"
        assert result.data["record"] == record
        assert result.data["time_extracted"] == "2025-08-05T10:00:00Z"

    def test_create_record_message_without_time(self) -> None:
        """Test creating record message without time_extracted."""
        bridge = FlextSingerBridge()

        record = {"id": 2, "name": "Jane Smith"}
        result = bridge.flext_singer_create_record_message(
            stream="users",
            record=record,
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "RECORD"
        assert result.data["stream"] == "users"
        assert result.data["record"] == record
        assert "time_extracted" not in result.data

    def test_create_record_message_invalid_stream(self) -> None:
        """Test creating record message with invalid stream."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_create_record_message(
            stream="",  # Empty stream
            record={"id": 1},
        )

        assert not result.success
        assert "Invalid stream name or record format" in result.error

    def test_create_record_message_invalid_record(self) -> None:
        """Test creating record message with invalid record."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_create_record_message(
            stream="test",
            record="invalid",  # Not a dict
        )

        assert not result.success
        assert "Invalid stream name or record format" in result.error

    def test_create_schema_message_success(self) -> None:
        """Test creating schema message successfully."""
        bridge = FlextSingerBridge()

        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }
        key_properties = ["id"]

        result = bridge.flext_singer_create_schema_message(
            stream="customers",
            schema=schema,
            key_properties=key_properties,
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "SCHEMA"
        assert result.data["stream"] == "customers"
        assert result.data["schema"] == schema
        assert result.data["key_properties"] == key_properties

    def test_create_schema_message_without_key_properties(self) -> None:
        """Test creating schema message without key properties."""
        bridge = FlextSingerBridge()

        schema = {"type": "object", "properties": {"name": {"type": "string"}}}

        result = bridge.flext_singer_create_schema_message(
            stream="test",
            schema=schema,
        )

        assert result.success
        assert result.data is not None
        assert result.data["key_properties"] == []

    def test_create_schema_message_invalid_stream(self) -> None:
        """Test creating schema message with invalid stream."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_create_schema_message(
            stream="",  # Empty stream
            schema={"type": "object"},
        )

        assert not result.success
        assert "Invalid stream name or schema format" in result.error

    def test_create_schema_message_invalid_schema(self) -> None:
        """Test creating schema message with invalid schema."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_create_schema_message(
            stream="test",
            schema="invalid",  # Not a dict
        )

        assert not result.success
        assert "Invalid stream name or schema format" in result.error

    def test_create_state_message_success(self) -> None:
        """Test creating state message successfully."""
        bridge = FlextSingerBridge()

        state_value = {
            "bookmarks": {
                "customers": {"replication_key_value": "2025-08-05T10:00:00Z"},
            },
        }

        result = bridge.flext_singer_create_state_message(value=state_value)

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "STATE"
        assert result.data["value"] == state_value

    def test_create_message_universal_method_record(self) -> None:
        """Test universal message creation method for RECORD."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_create_message(
            message_type="RECORD",
            stream="test_stream",
            record={"id": 1, "name": "test"},
            time_extracted="2025-08-05T10:00:00Z",
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "RECORD"
        assert result.data["stream"] == "test_stream"

    def test_create_message_universal_method_schema(self) -> None:
        """Test universal message creation method for SCHEMA."""
        bridge = FlextSingerBridge()

        schema = {"type": "object", "properties": {"id": {"type": "integer"}}}

        result = bridge.flext_singer_create_message(
            message_type="SCHEMA",
            stream="test_stream",
            schema=schema,
            key_properties=["id"],
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "SCHEMA"
        assert result.data["stream"] == "test_stream"

    def test_create_message_universal_method_state(self) -> None:
        """Test universal message creation method for STATE."""
        bridge = FlextSingerBridge()

        state_value = {"bookmarks": {}}

        result = bridge.flext_singer_create_message(
            message_type="STATE",
            value=state_value,
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "STATE"
        assert result.data["value"] == state_value

    def test_create_message_unknown_type(self) -> None:
        """Test universal message creation with unknown type."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_create_message(
            message_type="UNKNOWN",
            some_param="value",
        )

        assert not result.success
        assert "Unknown message type: UNKNOWN" in result.error

    def test_parse_message_line_success(self) -> None:
        """Test parsing valid Singer message line."""
        bridge = FlextSingerBridge()

        message_dict = {"type": "RECORD", "stream": "test", "record": {"id": 1}}
        message_line = json.dumps(message_dict)

        result = bridge.flext_singer_parse_message_line(message_line)

        assert result.success
        assert result.data == message_dict

    def test_parse_message_line_with_whitespace(self) -> None:
        """Test parsing message line with whitespace."""
        bridge = FlextSingerBridge()

        message_dict = {"type": "SCHEMA", "stream": "test", "schema": {}}
        message_line = f"  {json.dumps(message_dict)}  "

        result = bridge.flext_singer_parse_message_line(message_line)

        assert result.success
        assert result.data == message_dict

    def test_parse_message_line_empty(self) -> None:
        """Test parsing empty message line."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_parse_message_line("")

        assert not result.success
        assert "Empty message line" in result.error

    def test_parse_message_line_invalid_json(self) -> None:
        """Test parsing invalid JSON message line."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_parse_message_line("invalid json {")

        assert not result.success
        assert "Invalid JSON in Singer message" in result.error

    def test_parse_message_line_missing_type(self) -> None:
        """Test parsing message line without type field."""
        bridge = FlextSingerBridge()

        message_line = json.dumps({"stream": "test", "record": {"id": 1}})

        result = bridge.flext_singer_parse_message_line(message_line)

        assert not result.success
        assert "Invalid Singer message format" in result.error

    def test_validate_message_record_success(self) -> None:
        """Test validating valid RECORD message."""
        bridge = FlextSingerBridge()

        message = {
            "type": "RECORD",
            "stream": "customers",
            "record": {"id": 1, "name": "John"},
        }

        result = bridge.flext_singer_validate_message(message)

        assert result.success
        assert result.data == "RECORD"

    def test_validate_message_schema_success(self) -> None:
        """Test validating valid SCHEMA message."""
        bridge = FlextSingerBridge()

        message = {
            "type": "SCHEMA",
            "stream": "customers",
            "schema": {"type": "object"},
        }

        result = bridge.flext_singer_validate_message(message)

        assert result.success
        assert result.data == "SCHEMA"

    def test_validate_message_state_success(self) -> None:
        """Test validating valid STATE message."""
        bridge = FlextSingerBridge()

        message = {
            "type": "STATE",
            "value": {"bookmarks": {}},
        }

        result = bridge.flext_singer_validate_message(message)

        assert result.success
        assert result.data == "STATE"

    def test_validate_message_not_dict(self) -> None:
        """Test validating non-dictionary message."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_validate_message("not a dict")

        assert not result.success
        assert "Message must be a dictionary" in result.error

    def test_validate_message_missing_type(self) -> None:
        """Test validating message without type field."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_validate_message({"stream": "test"})

        assert not result.success
        assert "Message must have 'type' field" in result.error

    def test_validate_message_unknown_type(self) -> None:
        """Test validating message with unknown type."""
        bridge = FlextSingerBridge()

        result = bridge.flext_singer_validate_message({"type": "UNKNOWN"})

        assert not result.success
        assert "Unknown message type: UNKNOWN" in result.error

    def test_validate_message_record_missing_fields(self) -> None:
        """Test validating RECORD message missing required fields."""
        bridge = FlextSingerBridge()

        # Missing 'record' field
        result = bridge.flext_singer_validate_message(
            {
                "type": "RECORD",
                "stream": "test",
            },
        )

        assert not result.success
        assert "Missing required field: record" in result.error

    def test_validate_message_schema_missing_fields(self) -> None:
        """Test validating SCHEMA message missing required fields."""
        bridge = FlextSingerBridge()

        # Missing 'schema' field
        result = bridge.flext_singer_validate_message(
            {
                "type": "SCHEMA",
                "stream": "test",
            },
        )

        assert not result.success
        assert "Missing required field: schema" in result.error

    def test_validate_message_state_missing_fields(self) -> None:
        """Test validating STATE message missing required fields."""
        bridge = FlextSingerBridge()

        # Missing 'value' field
        result = bridge.flext_singer_validate_message({"type": "STATE"})

        assert not result.success
        assert "Missing required field: value" in result.error

    @patch("sys.stdout")
    def test_write_message_success(self, mock_stdout: object) -> None:
        """Test writing valid message to stdout."""
        bridge = FlextSingerBridge()

        message = {
            "type": "RECORD",
            "stream": "test",
            "record": {"id": 1},
        }

        result = bridge.flext_singer_write_message(message)

        assert result.success
        assert result.data is None
        # Verify stdout.flush was called
        mock_stdout.flush.assert_called_once()

    @patch("sys.stdout")
    def test_write_message_invalid(self, mock_stdout: object) -> None:
        """Test writing invalid message."""
        bridge = FlextSingerBridge()

        # Invalid message (missing required fields)
        message = {"type": "RECORD"}

        result = bridge.flext_singer_write_message(message)

        assert not result.success
        assert "Invalid message" in result.error
        # Verify stdout.flush was not called
        mock_stdout.flush.assert_not_called()

    def test_read_messages_from_string_io(self) -> None:
        """Test reading messages from StringIO."""
        bridge = FlextSingerBridge()

        # Create test input with multiple messages
        messages = [
            {"type": "SCHEMA", "stream": "test", "schema": {}},
            {"type": "RECORD", "stream": "test", "record": {"id": 1}},
            {"type": "STATE", "value": {}},
        ]

        input_lines = [json.dumps(msg) for msg in messages]
        input_stream = StringIO("\n".join(input_lines))

        results = list(bridge.flext_singer_read_messages(input_stream))

        assert len(results) == 3
        for i, result in enumerate(results):
            assert result.success
            assert result.data == messages[i]

    def test_read_messages_default_stdin(self) -> None:
        """Test reading messages using default stdin."""
        bridge = FlextSingerBridge()

        # Mock stdin with test data
        test_message = {"type": "RECORD", "stream": "test", "record": {"id": 1}}
        test_input = StringIO(json.dumps(test_message))

        with patch("sys.stdin", test_input):
            results = list(bridge.flext_singer_read_messages())

            assert len(results) == 1
            assert results[0].success
            assert results[0].data == test_message

    def test_read_messages_with_invalid_line(self) -> None:
        """Test reading messages with invalid JSON line."""
        bridge = FlextSingerBridge()

        input_stream = StringIO("invalid json line")
        results = list(bridge.flext_singer_read_messages(input_stream))

        assert len(results) == 1
        assert not results[0].success
        assert "Invalid JSON in Singer message" in results[0].error


class TestFlextSingerCatalogComplete:
    """Complete tests for FlextSingerCatalog class."""

    def test_catalog_initialization_empty(self) -> None:
        """Test catalog initialization without data."""
        catalog = FlextSingerCatalog()

        assert catalog is not None
        assert hasattr(catalog, "_logger")
        assert hasattr(catalog, "_catalog")
        assert catalog._catalog == {"streams": []}

    def test_catalog_initialization_with_data(self) -> None:
        """Test catalog initialization with existing data."""
        existing_catalog = {
            "streams": [
                {"tap_stream_id": "existing_stream", "schema": {}},
            ],
        }

        catalog = FlextSingerCatalog(existing_catalog)

        assert catalog._catalog == existing_catalog

    def test_add_stream_success(self) -> None:
        """Test adding stream to catalog successfully."""
        catalog = FlextSingerCatalog()

        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }
        key_properties = ["id"]

        result = catalog.flext_singer_add_stream(
            stream_name="customers",
            schema=schema,
            key_properties=key_properties,
        )

        assert result.success
        assert result.data is None

        # Verify stream was added
        catalog_data = catalog.flext_singer_get_catalog()
        assert catalog_data.success
        streams = catalog_data.data["streams"]
        assert len(streams) == 1

        stream = streams[0]
        assert stream["tap_stream_id"] == "customers"
        assert stream["schema"] == schema
        assert stream["key_properties"] == key_properties

    def test_add_stream_without_key_properties(self) -> None:
        """Test adding stream without key properties."""
        catalog = FlextSingerCatalog()

        schema = {"type": "object", "properties": {"name": {"type": "string"}}}

        result = catalog.flext_singer_add_stream(
            stream_name="users",
            schema=schema,
        )

        assert result.success

        # Verify stream was added without key_properties field
        catalog_data = catalog.flext_singer_get_catalog()
        assert catalog_data.success
        streams = catalog_data.data["streams"]
        assert len(streams) == 1

        stream = streams[0]
        assert stream["tap_stream_id"] == "users"
        assert "key_properties" not in stream

    def test_add_stream_invalid_name(self) -> None:
        """Test adding stream with invalid name."""
        catalog = FlextSingerCatalog()

        result = catalog.flext_singer_add_stream(
            stream_name="",  # Empty name
            schema={"type": "object"},
        )

        assert not result.success
        assert "Invalid stream name or schema" in result.error

    def test_add_stream_invalid_schema(self) -> None:
        """Test adding stream with invalid schema."""
        catalog = FlextSingerCatalog()

        result = catalog.flext_singer_add_stream(
            stream_name="test",
            schema="invalid",  # Not a dict
        )

        assert not result.success
        assert "Invalid stream name or schema" in result.error

    def test_add_multiple_streams(self) -> None:
        """Test adding multiple streams to catalog."""
        catalog = FlextSingerCatalog()

        # Add first stream
        result1 = catalog.flext_singer_add_stream(
            stream_name="customers",
            schema={"type": "object", "properties": {"id": {"type": "integer"}}},
        )
        assert result1.success

        # Add second stream
        result2 = catalog.flext_singer_add_stream(
            stream_name="orders",
            schema={"type": "object", "properties": {"order_id": {"type": "integer"}}},
        )
        assert result2.success

        # Verify both streams exist
        catalog_data = catalog.flext_singer_get_catalog()
        streams = catalog_data.data["streams"]
        assert len(streams) == 2

        stream_names = [stream["tap_stream_id"] for stream in streams]
        assert "customers" in stream_names
        assert "orders" in stream_names

    def test_get_catalog_success(self) -> None:
        """Test getting catalog data successfully."""
        initial_data = {"streams": [{"tap_stream_id": "test", "schema": {}}]}
        catalog = FlextSingerCatalog(initial_data)

        result = catalog.flext_singer_get_catalog()

        assert result.success
        assert result.data == initial_data
        # Verify it's a copy, not the original
        assert result.data is not catalog._catalog

    def test_get_selected_streams_with_selection(self) -> None:
        """Test getting selected streams when streams are selected."""
        catalog = FlextSingerCatalog()

        # Add a stream (automatically selected by default)
        catalog.flext_singer_add_stream(
            stream_name="selected_stream",
            schema={"type": "object"},
        )

        result = catalog.flext_singer_get_selected_streams()

        assert result.success
        assert result.data == ["selected_stream"]

    def test_get_selected_streams_empty_catalog(self) -> None:
        """Test getting selected streams from empty catalog."""
        catalog = FlextSingerCatalog()

        result = catalog.flext_singer_get_selected_streams()

        assert result.success
        assert result.data == []

    def test_get_selected_streams_complex_metadata(self) -> None:
        """Test getting selected streams with complex metadata structure."""
        # Create catalog with manually crafted streams for testing edge cases
        catalog_data = {
            "streams": [
                {
                    "tap_stream_id": "stream1",
                    "schema": {},
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {"selected": True},
                        },
                    ],
                },
                {
                    "tap_stream_id": "stream2",
                    "schema": {},
                    "metadata": [
                        {
                            "breadcrumb": ["properties", "field"],
                            "metadata": {"selected": True},
                        },
                    ],
                },
                {
                    "tap_stream_id": "stream3",
                    "schema": {},
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {"selected": False},
                        },
                    ],
                },
            ],
        }

        catalog = FlextSingerCatalog(catalog_data)
        result = catalog.flext_singer_get_selected_streams()

        assert result.success
        # Only stream1 should be selected (empty breadcrumb and selected=True)
        assert result.data == ["stream1"]

    def test_get_selected_streams_invalid_streams_format(self) -> None:
        """Test getting selected streams with invalid streams format."""
        catalog_data = {"streams": "invalid"}  # Not a list
        catalog = FlextSingerCatalog(catalog_data)

        # Constructor is defensive and ignores invalid data, uses default empty list
        result = catalog.flext_singer_get_selected_streams()

        assert result.success
        assert result.data == []  # Empty because invalid data was ignored


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_singer_bridge(self) -> None:
        """Test creating Singer bridge via factory function."""
        bridge = flext_create_singer_bridge()

        assert bridge is not None
        assert isinstance(bridge, FlextSingerBridge)

    def test_create_singer_catalog_empty(self) -> None:
        """Test creating Singer catalog via factory function without data."""
        catalog = flext_create_singer_catalog()

        assert catalog is not None
        assert isinstance(catalog, FlextSingerCatalog)
        catalog_data = catalog.flext_singer_get_catalog()
        assert catalog_data.data == {"streams": []}

    def test_create_singer_catalog_with_data(self) -> None:
        """Test creating Singer catalog via factory function with data."""
        # Factory function takes no parameters, so create empty catalog and add data
        catalog = flext_create_singer_catalog()

        # Add a stream to the catalog
        result = catalog.flext_singer_add_stream("test", {"type": "object"}, ["id"])
        assert result.success

        assert catalog is not None
        assert isinstance(catalog, FlextSingerCatalog)
        catalog_data = catalog.flext_singer_get_catalog()
        assert catalog_data.success
        assert len(catalog_data.data["streams"]) == 1
        assert catalog_data.data["streams"][0]["tap_stream_id"] == "test"


class TestModuleExports:
    """Test module exports."""

    def test_module_exports_defined(self) -> None:
        """Test that __all__ is properly defined."""
        expected_exports = [
            "FlextSingerBridge",
            "FlextSingerCatalog",
            "flext_create_singer_bridge",
            "flext_create_singer_catalog",
        ]

        assert isinstance(_singer_all, list)
        assert len(_singer_all) == 4
        for export in expected_exports:
            assert export in _singer_all

    def test_all_exports_importable(self) -> None:
        """Test that all exported items can be imported."""
        # Verify all items are callable/instantiable
        assert callable(FlextSingerBridge)
        assert callable(FlextSingerCatalog)
        assert callable(flext_create_singer_bridge)
        assert callable(flext_create_singer_catalog)


class TestIntegrationWorkflows:
    """Integration tests for complete Singer workflows."""

    def test_complete_singer_workflow(self) -> None:
        """Test complete Singer workflow from catalog to message processing."""
        # Create catalog
        catalog = flext_create_singer_catalog()

        # Add stream to catalog
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
        }

        add_result = catalog.flext_singer_add_stream(
            stream_name="customers",
            schema=schema,
            key_properties=["id"],
        )
        assert add_result.success

        # Get selected streams
        selected_result = catalog.flext_singer_get_selected_streams()
        assert selected_result.success
        assert "customers" in selected_result.data

        # Create bridge for message processing
        bridge = flext_create_singer_bridge()

        # Create schema message
        schema_result = bridge.flext_singer_create_schema_message(
            stream="customers",
            schema=schema,
            key_properties=["id"],
        )
        assert schema_result.success

        # Create record message
        record_result = bridge.flext_singer_create_record_message(
            stream="customers",
            record={"id": 1, "name": "John Doe", "email": "john@example.com"},
        )
        assert record_result.success

        # Create state message
        state_result = bridge.flext_singer_create_state_message(
            value={"bookmarks": {"customers": {"replication_key_value": "1"}}},
        )
        assert state_result.success

        # Validate all messages
        schema_validation = bridge.flext_singer_validate_message(schema_result.data)
        record_validation = bridge.flext_singer_validate_message(record_result.data)
        state_validation = bridge.flext_singer_validate_message(state_result.data)

        assert schema_validation.success
        assert record_validation.success
        assert state_validation.success

    def test_error_handling_throughout_workflow(self) -> None:
        """Test error handling throughout Singer workflow."""
        bridge = flext_create_singer_bridge()
        catalog = flext_create_singer_catalog()

        # Test catalog errors
        invalid_stream_result = catalog.flext_singer_add_stream("", {})
        assert not invalid_stream_result.success

        # Test bridge errors
        invalid_record_result = bridge.flext_singer_create_record_message("", {})
        assert not invalid_record_result.success

        # Test message validation errors
        invalid_validation_result = bridge.flext_singer_validate_message({})
        assert not invalid_validation_result.success

        # Test parsing errors
        invalid_parse_result = bridge.flext_singer_parse_message_line("invalid json")
        assert not invalid_parse_result.success
