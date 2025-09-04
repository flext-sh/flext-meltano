"""Test FlextSingerTypes - Unified class functionality.

Tests the new unified FlextSingerTypes class with real API behavior.
"""

from flext_meltano.singer_types import FlextSingerTypes


class TestFlextSingerTypesUnified:
    """Tests for unified FlextSingerTypes class."""

    def test_create_instance(self) -> None:
        """Test FlextSingerTypes instance creation."""
        result = FlextSingerTypes.create_instance()

        assert result.success
        assert isinstance(result.value, FlextSingerTypes)

    def test_string_type_creation(self) -> None:
        """Test string type creation."""
        singer_types = FlextSingerTypes()
        result = singer_types.create_string_type(maxLength=255)

        assert result.success
        type_def = result.value
        assert type_def["type"] == "string"
        assert type_def["maxLength"] == 255

    def test_integer_type_creation(self) -> None:
        """Test integer type creation."""
        singer_types = FlextSingerTypes()
        result = singer_types.create_integer_type(minimum=0)

        assert result.success
        type_def = result.value
        assert type_def["type"] == "integer"
        assert type_def["minimum"] == 0

    def test_record_message_creation(self) -> None:
        """Test Singer RECORD message creation."""
        singer_types = FlextSingerTypes()
        result = singer_types.create_record_message("users", {"id": 1, "name": "John"})

        assert result.success
        message = result.value
        assert isinstance(message, dict)
        assert message["type"] == "RECORD"
        assert message["stream"] == "users"
        record = message["record"]
        assert isinstance(record, dict)
        assert record["id"] == 1

    def test_schema_message_creation(self) -> None:
        """Test Singer SCHEMA message creation."""
        singer_types = FlextSingerTypes()
        schema: dict[str, object] = {"type": "object", "properties": {"id": {"type": "integer"}}}
        result = singer_types.create_schema_message("users", schema, ["id"])

        assert result.success
        message = result.value
        assert message["type"] == "SCHEMA"
        assert message["stream"] == "users"
        assert message["key_properties"] == ["id"]

    def test_value_validation(self) -> None:
        """Test value validation against type definitions."""
        singer_types = FlextSingerTypes()
        string_type: dict[str, object] = {"type": "string"}

        # Valid string
        result = singer_types.validate_value("test", string_type)
        assert result.success

        # Invalid type
        result = singer_types.validate_value(123, string_type)
        assert result.failure
        error_msg = result.error
        assert error_msg is not None
        assert "Expected string" in error_msg

    def test_get_registered_types(self) -> None:
        """Test getting registered types."""
        singer_types = FlextSingerTypes()
        types = singer_types.get_registered_types()

        assert isinstance(types, list)
        assert "string" in types
        assert "integer" in types
        assert "boolean" in types
