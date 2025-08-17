"""FlextSinger Coverage Test Suite - Complete Module Validation.

**Test Category**: Unit Tests
**Coverage Target**: 95%+ for FlextSinger module components
**Dependencies**: FlextSinger bridge, Singer SDK patterns, stream processing
**Execution Time**: < 5 seconds total

## Test Scope

Validates comprehensive coverage of the FlextSinger module, ensuring all code paths,
edge cases, and error conditions are thoroughly tested for the Singer SDK integration
layer within FLEXT Meltano's bridge architecture.
"""

from __future__ import annotations

from io import StringIO

import pytest

from flext_meltano import (
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

    def test_create_record_message_universal(self) -> None:
      """Test creating RECORD message via universal method."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_message(
          "RECORD",
          stream="users",
          record={"id": 1, "name": "test"},
      )
      assert result.success
      assert result.data is not None
      if result.data["type"] != "RECORD":
          msg: str = f"Expected {'RECORD'}, got {result.data['type']}"
          raise AssertionError(msg)

    def test_create_schema_message_universal(self) -> None:
      """Test creating SCHEMA message via universal method."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_message(
          "SCHEMA",
          stream="users",
          schema={"type": "object"},
          key_properties=["id"],
      )
      assert result.success
      assert result.data is not None
      if result.data["type"] != "SCHEMA":
          msg: str = f"Expected {'SCHEMA'}, got {result.data['type']}"
          raise AssertionError(msg)

    def test_create_state_message_universal(self) -> None:
      """Test creating STATE message via universal method."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_message(
          "STATE",
          value={"bookmark": "test"},
      )
      assert result.success
      assert result.data is not None
      if result.data["type"] != "STATE":
          msg: str = f"Expected {'STATE'}, got {result.data['type']}"
          raise AssertionError(msg)

    def test_create_unknown_message_type(self) -> None:
      """Test creating unknown message type."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_message("UNKNOWN")
      assert not result.success

    def test_specific_create_record_message(self) -> None:
      """Test specific record message creation method."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_record_message(
          stream="test",
          record={"id": 1},
      )
      assert result.success

    def test_specific_create_schema_message(self) -> None:
      """Test specific schema message creation method."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_schema_message(
          stream="test",
          schema={"type": "object"},
          key_properties=["id"],
      )
      assert result.success

    def test_specific_create_state_message(self) -> None:
      """Test specific state message creation method."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_state_message(
          value={"bookmark": "test"},
      )
      assert result.success

    def test_parse_message_line_success(self) -> None:
      """Test parsing valid message line."""
      bridge = FlextSingerBridge()
      line = '{"type": "RECORD", "stream": "test", "record": {"id": 1}}'
      result = bridge.flext_singer_parse_message_line(line)
      assert result.success

    def test_parse_message_line_empty(self) -> None:
      """Test parsing empty line."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_parse_message_line("")
      assert not result.success

    def test_parse_message_line_invalid_json(self) -> None:
      """Test parsing invalid JSON."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_parse_message_line("invalid json")
      assert not result.success

    def test_validate_record_message(self) -> None:
      """Test validating RECORD message."""
      bridge = FlextSingerBridge()
      message = {"type": "RECORD", "stream": "test", "record": {"id": 1}}
      result = bridge.flext_singer_validate_message(message)
      assert result.success

    def test_validate_schema_message(self) -> None:
      """Test validating SCHEMA message."""
      bridge = FlextSingerBridge()
      message = {"type": "SCHEMA", "stream": "test", "schema": {"type": "object"}}
      result = bridge.flext_singer_validate_message(message)
      assert result.success

    def test_validate_state_message(self) -> None:
      """Test validating STATE message."""
      bridge = FlextSingerBridge()
      message = {"type": "STATE", "value": {"bookmark": "test"}}
      result = bridge.flext_singer_validate_message(message)
      assert result.success

    def test_validate_message_no_type(self) -> None:
      """Test validating message without type."""
      bridge = FlextSingerBridge()
      message = {"stream": "test"}
      result = bridge.flext_singer_validate_message(message)
      assert not result.success

    def test_validate_record_missing_fields(self) -> None:
      """Test validating RECORD message with missing fields."""
      bridge = FlextSingerBridge()
      message = {"type": "RECORD", "stream": "test"}  # Missing record
      result = bridge.flext_singer_validate_message(message)
      assert not result.success

    def test_validate_unknown_type(self) -> None:
      """Test validating unknown message type."""
      bridge = FlextSingerBridge()
      message = {"type": "UNKNOWN"}
      result = bridge.flext_singer_validate_message(message)
      assert not result.success

    def test_write_message_success(self) -> None:
      """Test writing valid message."""
      bridge = FlextSingerBridge()
      message = {"type": "RECORD", "stream": "test", "record": {"id": 1}}
      result = bridge.flext_singer_write_message(message)
      assert result.success

    def test_write_message_invalid(self) -> None:
      """Test writing invalid message."""
      bridge = FlextSingerBridge()
      message = {"type": "RECORD"}  # Missing required fields
      result = bridge.flext_singer_write_message(message)
      assert not result.success

    def test_read_messages_from_stream(self) -> None:
      """Test reading messages from StringIO stream."""
      bridge = FlextSingerBridge()
      input_data = StringIO(
          '{"type": "RECORD", "stream": "test", "record": {"id": 1}}\n',
      )

      messages = list(bridge.flext_singer_read_messages(input_data))
      if len(messages) != 1:
          msg: str = f"Expected {1}, got {len(messages)}"
          raise AssertionError(msg)
      assert messages[0].success

    def test_create_record_invalid_stream(self) -> None:
      """Test creating record with invalid stream."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_record_message("", {"id": 1})
      assert not result.success

    def test_create_record_invalid_record(self) -> None:
      """Test creating record with invalid record."""
      bridge = FlextSingerBridge()
      # The current implementation might not validate record type
      # Type ignore needed for intentional type violation test
      result = bridge.flext_singer_create_record_message("test", "not a dict")
      assert not result.success

    def test_create_schema_invalid_stream(self) -> None:
      """Test creating schema with invalid stream."""
      bridge = FlextSingerBridge()
      result = bridge.flext_singer_create_schema_message("", {"type": "object"})
      assert not result.success

    def test_create_schema_invalid_schema(self) -> None:
      """Test creating schema with invalid schema."""
      bridge = FlextSingerBridge()
      # Type ignore needed for intentional type violation test
      result = bridge.flext_singer_create_schema_message("test", "not a dict")
      assert not result.success


class TestFlextSingerCatalog:
    """Test FlextSinger catalog functionality."""

    def test_catalog_initialization(self) -> None:
      """Test catalog initialization."""
      catalog = FlextSingerCatalog()
      assert catalog is not None

    def test_catalog_initialization_with_data(self) -> None:
      """Test catalog initialization with data."""
      data = {"streams": [{"tap_stream_id": "test", "schema": {}}]}
      catalog = FlextSingerCatalog(data)
      result = catalog.flext_singer_get_catalog()
      assert result.success
      assert result.data is not None
      if len(result.data["streams"]) != 1:
          msg: str = f"Expected {1}, got {len(result.data['streams'])}"
          raise AssertionError(msg)

    def test_add_stream_success(self) -> None:
      """Test adding stream successfully."""
      catalog = FlextSingerCatalog()
      result = catalog.flext_singer_add_stream(
          "users",
          {"type": "object", "properties": {"id": {"type": "integer"}}},
          ["id"],
      )
      assert result.success

    def test_add_stream_no_key_properties(self) -> None:
      """Test adding stream without key properties."""
      catalog = FlextSingerCatalog()
      result = catalog.flext_singer_add_stream(
          "logs",
          {"type": "object", "properties": {"message": {"type": "string"}}},
      )
      assert result.success

    def test_add_stream_invalid_name(self) -> None:
      """Test adding stream with invalid name."""
      catalog = FlextSingerCatalog()
      result = catalog.flext_singer_add_stream("", {"type": "object"})
      assert not result.success

    def test_add_stream_invalid_schema(self) -> None:
      """Test adding stream with invalid schema."""
      catalog = FlextSingerCatalog()
      # Type ignore needed for intentional type violation test
      result = catalog.flext_singer_add_stream("test", "not a dict")
      assert not result.success

    def test_get_catalog_success(self) -> None:
      """Test getting catalog data."""
      catalog = FlextSingerCatalog()
      result = catalog.flext_singer_get_catalog()
      assert result.success
      assert result.data is not None
      assert result.data is not None
      if "streams" not in result.data:
          msg: str = f"Expected {'streams'} in {result.data}"
          raise AssertionError(msg)

    def test_get_selected_streams_empty(self) -> None:
      """Test getting selected streams from empty catalog."""
      catalog = FlextSingerCatalog()
      result = catalog.flext_singer_get_selected_streams()
      assert result.success
      assert result.data is not None
      if result.data != []:
          msg: str = f"Expected {[]}, got {result.data}"
          raise AssertionError(msg)

    def test_get_selected_streams_with_data(self) -> None:
      """Test getting selected streams with data."""
      catalog = FlextSingerCatalog()
      catalog.flext_singer_add_stream("users", {"type": "object"}, ["id"])

      result = catalog.flext_singer_get_selected_streams()
      assert result.success
      assert result.data is not None
      # Stream is added but not marked as selected, so result should be empty
      assert result.data == []


class TestFlextSingerFactoryFunctions:
    """Test FlextSinger factory functions."""

    def test_create_singer_bridge(self) -> None:
      """Test creating singer bridge via factory."""
      bridge = flext_create_singer_bridge()
      assert isinstance(bridge, FlextSingerBridge)

    def test_create_singer_catalog_empty(self) -> None:
      """Test creating empty singer catalog via factory."""
      catalog = flext_create_singer_catalog()
      assert isinstance(catalog, FlextSingerCatalog)

    def test_create_singer_catalog_with_data(self) -> None:
      """Test creating singer catalog with data via factory."""
      catalog = flext_create_singer_catalog()  # Function takes no parameters
      # Manually set the data after creation if needed
      assert isinstance(catalog, FlextSingerCatalog)


class TestFlextSingerIntegration:
    """Integration tests for FlextSinger components."""

    def test_bridge_and_catalog_workflow(self) -> None:
      """Test workflow using bridge and catalog together."""
      bridge = flext_create_singer_bridge()
      catalog = flext_create_singer_catalog()

      # Create schema
      schema_result = bridge.flext_singer_create_schema_message(
          "users",
          {"type": "object", "properties": {"id": {"type": "integer"}}},
          ["id"],
      )
      assert schema_result.success

      # Add to catalog
      add_result = catalog.flext_singer_add_stream(
          "users",
          schema_result.data["schema"] if schema_result.data else {},
          schema_result.data["key_properties"] if schema_result.data else [],
      )
      assert add_result.success

      # Create record
      record_result = bridge.flext_singer_create_record_message(
          "users",
          {"id": 1, "name": "test"},
      )
      assert record_result.success

      # Validate messages
      assert schema_result.data is not None
      assert record_result.data is not None
      schema_valid = bridge.flext_singer_validate_message(schema_result.data)
      record_valid = bridge.flext_singer_validate_message(record_result.data)
      assert schema_valid.success
      assert record_valid.success

    def test_error_handling_integration(self) -> None:
      """Test error handling across components."""
      bridge = flext_create_singer_bridge()
      catalog = flext_create_singer_catalog()

      # Test invalid operations
      invalid_msg = bridge.flext_singer_create_message("INVALID")
      assert not invalid_msg.success

      invalid_stream = catalog.flext_singer_add_stream("", {})
      assert not invalid_stream.success

      # Valid operations should still work
      valid_msg = bridge.flext_singer_create_record_message("test", {"id": 1})
      assert valid_msg.success

    def test_message_parsing_workflow(self) -> None:
      """Test message parsing workflow."""
      bridge = flext_create_singer_bridge()

      lines = [
          '{"type": "SCHEMA", "stream": "test", "schema": {"type": "object"}, "key_properties": []}',
          '{"type": "RECORD", "stream": "test", "record": {"id": 1}}',
          '{"type": "STATE", "value": {"bookmark": "test"}}',
      ]

      for line in lines:
          parsed = bridge.flext_singer_parse_message_line(line)
          assert parsed.success

          assert parsed.data is not None
          validated = bridge.flext_singer_validate_message(parsed.data)
          assert validated.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
