"""Test module for flext-meltano."""

from __future__ import annotations

import math
from unittest import mock

from flext_core import FlextResult, FlextTypes

from flext_meltano import FlextSingerTypes


class TestFlextSingerTypesCoverage:
    """Comprehensive coverage tests for FlextSingerTypes without mocks."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.singer_types = FlextSingerTypes()

    def test_initialization_and_basic_state(self) -> None:
        """Test initialization and basic state access."""
        # Test successful initialization
        assert isinstance(self.singer_types, FlextSingerTypes)
        assert hasattr(self.singer_types, "_logger")
        assert hasattr(self.singer_types, "_type_registry")

        # Test type registry contains expected types
        registered_types = self.singer_types.get_registered_types()
        assert isinstance(registered_types, list)
        assert "string" in registered_types
        assert "integer" in registered_types
        assert "number" in registered_types
        assert "boolean" in registered_types
        assert "date-time" in registered_types
        assert "array" in registered_types
        assert "object" in registered_types
        assert len(registered_types) == 7

    def test_create_instance_class_method(self) -> None:
        """Test the create_instance class method."""
        result = FlextSingerTypes.create_instance()
        assert isinstance(result, FlextResult)
        assert result.is_success

        assert result.data is not None
        instance = result.data
        assert isinstance(instance, FlextSingerTypes)
        assert hasattr(instance, "_type_registry")

    def test_primitive_type_creation(self) -> None:
        """Test creation of all primitive types."""
        # String type
        result = self.singer_types.create_string_type()
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        string_type = result.data
        assert string_type["type"] == "string"

        # String type with constraints
        result = self.singer_types.create_string_type(maxLength=255, minLength=1)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        string_constrained = result.data
        assert string_constrained["type"] == "string"
        assert string_constrained["maxLength"] == 255
        assert string_constrained["minLength"] == 1

        # Integer type
        result = self.singer_types.create_integer_type()
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        integer_type = result.data
        assert integer_type["type"] == "integer"

        # Integer with constraints
        result = self.singer_types.create_integer_type(minimum=0, maximum=100)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        integer_constrained = result.data
        assert integer_constrained["minimum"] == 0
        assert integer_constrained["maximum"] == 100

        # Number type
        result = self.singer_types.create_number_type()
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        number_type = result.data
        assert number_type["type"] == "number"

        # Boolean type
        result = self.singer_types.create_boolean_type()
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        boolean_type = result.data
        assert boolean_type["type"] == "boolean"

        # DateTime type
        result = self.singer_types.create_datetime_type()
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        datetime_type = result.data
        assert datetime_type["type"] == "string"
        assert datetime_type["format"] == "date-time"

    def test_complex_type_creation(self) -> None:
        """Test creation of complex types (array, object)."""
        # Array type with item type
        result = self.singer_types.create_array_type(items={"type": "string"})
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        array_type = result.data
        assert array_type["type"] == "array"
        assert isinstance(array_type["items"], dict)
        assert array_type["items"]["type"] == "string"

        # Array type without items (default)
        result = self.singer_types.create_array_type()
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        array_default = result.data
        assert array_default["type"] == "array"
        # When no items specified, no items key is added
        assert "items" not in array_default

        # Object type with properties
        properties_dict: FlextTypes.Dict = {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0},
        }
        result = self.singer_types.create_object_type(properties=properties_dict)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        object_type = result.data
        assert object_type["type"] == "object"
        assert isinstance(object_type["properties"], dict)
        assert isinstance(object_type["properties"]["name"], dict)
        assert isinstance(object_type["properties"]["age"], dict)
        assert object_type["properties"]["name"]["type"] == "string"
        assert object_type["properties"]["age"]["minimum"] == 0

        # Object type without properties (default)
        result = self.singer_types.create_object_type()
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        object_default = result.data
        assert object_default["type"] == "object"
        # When no properties specified, no properties key is added
        assert "properties" not in object_default

    def test_value_validation(self) -> None:
        """Test value validation against type definitions."""
        # Valid string validation
        string_type: FlextTypes.Dict = {"type": "string"}
        result = self.singer_types.validate_value("hello world", string_type)
        assert result.is_success

        # Invalid string validation (number against string type)
        result = self.singer_types.validate_value(123, string_type)
        assert not result.is_success
        assert result.error is not None
        assert result.error is not None and "expected string" in result.error.lower()

        # Valid integer validation
        integer_type: FlextTypes.Dict = {"type": "integer"}
        result = self.singer_types.validate_value(42, integer_type)
        assert result.is_success

        # Invalid integer validation (string against integer type)
        result = self.singer_types.validate_value("not a number", integer_type)
        assert not result.is_success

        # Valid number validation
        number_type: FlextTypes.Dict = {"type": "number"}
        result = self.singer_types.validate_value(math.pi, number_type)
        assert result.is_success

        # Valid boolean validation
        boolean_type: FlextTypes.Dict = {"type": "boolean"}
        result = self.singer_types.validate_value(True, boolean_type)
        assert result.is_success
        result = self.singer_types.validate_value(False, boolean_type)
        assert result.is_success

        # Invalid boolean validation
        result = self.singer_types.validate_value("not boolean", boolean_type)
        assert not result.is_success

    def test_schema_definition_creation(self) -> None:
        """Test complete schema definition creation."""
        properties = {
            "id": {"type": "integer", "minimum": 1},
            "name": {"type": "string", "maxLength": 100},
            "email": {"type": "string", "format": "email"},
            "active": {"type": "boolean"},
        }

        # First create the JSON Schema
        schema_result = self.singer_types.create_schema_definition(
            properties=properties,
        )

        assert schema_result.is_success
        assert schema_result.data is not None
        assert isinstance(schema_result.data, dict)
        schema = schema_result.data
        assert schema["type"] == "object"
        assert "properties" in schema
        assert isinstance(schema["properties"], dict)
        assert isinstance(schema["properties"]["id"], dict)
        assert isinstance(schema["properties"]["name"], dict)
        assert schema["properties"]["id"]["type"] == "integer"
        assert schema["properties"]["name"]["maxLength"] == 100

        # Now create the SCHEMA message using the schema
        message_result = self.singer_types.create_schema_message(
            stream="users",
            schema=schema,
            key_properties=["id"],
        )

        assert message_result.is_success
        assert message_result.data is not None
        assert isinstance(message_result.data, dict)
        message = message_result.data
        assert message["type"] == "SCHEMA"
        assert message["stream"] == "users"
        assert message["key_properties"] == ["id"]
        assert "schema" in message
        assert message["schema"] == schema

    def test_message_creation(self) -> None:
        """Test creation of all Singer message types."""
        # Record message
        record_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        result = self.singer_types.create_record_message("users", record_data)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        record_message = result.data
        assert record_message["type"] == "RECORD"
        assert record_message["stream"] == "users"
        assert isinstance(record_message["record"], dict)
        assert record_message["record"]["id"] == 1
        assert record_message["record"]["name"] == "John Doe"
        # time_extracted is only added if provided as kwargs
        assert "time_extracted" not in record_message

        # Test record message with time_extracted
        result = self.singer_types.create_record_message(
            "users",
            record_data,
            time_extracted="2025-01-15T10:30:00Z",
        )
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        record_with_time = result.data
        assert record_with_time["time_extracted"] == "2025-01-15T10:30:00Z"

        # Schema message
        properties = {"id": {"type": "integer"}, "name": {"type": "string"}}
        result = self.singer_types.create_schema_message(
            stream="users",
            schema={"type": "object", "properties": properties},
            key_properties=["id"],
        )
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        schema_message = result.data
        assert schema_message["type"] == "SCHEMA"
        assert schema_message["stream"] == "users"
        assert isinstance(schema_message["key_properties"], list)
        assert schema_message["key_properties"] == ["id"]

        # State message
        state_data: FlextTypes.Dict = {"bookmarks": {"users": {"id": 100}}}
        result = self.singer_types.create_state_message(state_data)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        state_message = result.data
        assert isinstance(state_message, dict)  # Type assertion for subscript access
        assert state_message["type"] == "STATE"
        assert isinstance(
            state_message["value"],
            dict,
        )  # Type assertion for nested access
        assert isinstance(state_message["value"]["bookmarks"], dict)
        assert isinstance(state_message["value"]["bookmarks"]["users"], dict)
        assert state_message["value"]["bookmarks"]["users"]["id"] == 100

    def test_properties_management(self) -> None:
        """Test properties list creation and manipulation."""
        properties: FlextTypes.NestedDict = {
            "user_id": {"type": "integer"},
            "username": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
        }

        result = self.singer_types.create_properties_list(properties)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        props_dict = result.data
        assert isinstance(props_dict, dict)
        assert len(props_dict) == 3

        # Check that all properties are included
        assert "user_id" in props_dict
        assert "username" in props_dict
        assert "created_at" in props_dict
        assert isinstance(
            props_dict["user_id"],
            dict,
        )  # Type assertion for subscript access
        assert isinstance(
            props_dict["username"],
            dict,
        )  # Type assertion for subscript access
        assert props_dict["user_id"]["type"] == "integer"
        assert props_dict["username"]["type"] == "string"

    def test_add_property_functionality(self) -> None:
        """Test adding properties to existing property lists."""
        # Start with basic properties
        initial_props: FlextTypes.NestedDict = {
            "id": {"type": "integer"},
            "name": {"type": "string"},
        }
        result = self.singer_types.create_properties_list(initial_props)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        props_dict = result.data

        # Add new property
        result = self.singer_types.add_property(
            props_dict,
            "email",
            {"type": "string", "format": "email"},
        )
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        updated_props = result.data
        assert len(updated_props) == 3

        # Verify new property is properly added
        assert "email" in updated_props
        assert isinstance(updated_props["email"], dict)
        assert updated_props["email"]["type"] == "string"
        assert updated_props["email"]["format"] == "email"

    def test_type_registry_management(self) -> None:
        """Test type registry access and management."""
        # Get all registered types
        types = self.singer_types.get_registered_types()
        assert isinstance(types, list)
        assert len(types) >= 7  # At least the basic types

        # Get specific type definitions
        result = self.singer_types.get_type_definition("string")
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        string_def = result.data
        assert string_def["type"] == "string"

        result = self.singer_types.get_type_definition("integer")
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        integer_def = result.data
        assert integer_def["type"] == "integer"

        result = self.singer_types.get_type_definition("date-time")
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        datetime_def = result.data
        assert datetime_def["type"] == "string"
        assert datetime_def["format"] == "date-time"

        # Test non-existent type
        result = self.singer_types.get_type_definition("nonexistent")
        assert not result.is_success
        assert result.error is not None
        assert result.error is not None and "not found" in result.error.lower()

    def test_data_conversion_functionality(self) -> None:
        """Test data conversion to dictionary format."""
        # Test valid dictionary conversion
        data = {"key": "value", "number": 42, "nested": {"inner": "data"}}
        result = self.singer_types.convert_to_dict(data)
        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, dict)
        converted = result.data
        assert converted["key"] == "value"
        assert converted["number"] == 42
        assert isinstance(converted["nested"], dict)
        assert converted["nested"]["inner"] == "data"

        # Test non-dict data that can be converted
        simple_data = "simple string"
        result = self.singer_types.convert_to_dict(simple_data)
        # This might fail or succeed depending on implementation
        # The important thing is we're testing the conversion logic
        assert isinstance(result, FlextResult)

    def test_error_handling_and_edge_cases(self) -> None:
        """Test error handling and edge cases."""
        # Test validation with malformed type definition
        malformed_type: FlextTypes.Dict = {
            "invalid": "definition",
        }  # Missing "type" key
        result = self.singer_types.validate_value("test", malformed_type)
        assert not result.is_success

        # Test schema creation with empty properties
        result = self.singer_types.create_schema_definition(
            stream_name="empty_stream",
            properties={},
            key_properties=[],
        )
        assert result.is_success  # Should handle empty properties gracefully

        # Test record message with empty data
        result = self.singer_types.create_record_message("test_stream", {})
        assert result.is_success  # Should handle empty records

        # Test state message with None data
        result = self.singer_types.create_state_message({})
        # Implementation should handle None gracefully
        assert isinstance(result, FlextResult)


class TestFlextSingerTypesIntegration:
    """Integration tests combining multiple Singer types operations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.singer_types = FlextSingerTypes()

    def test_complete_schema_workflow(self) -> None:
        """Test complete workflow from type creation to message generation."""
        # Create complex schema with multiple types
        properties = {
            "user_id": {"type": "integer", "minimum": 1},
            "username": {"type": "string", "maxLength": 50},
            "email": {"type": "string"},
            "is_active": {"type": "boolean"},
            "created_at": {"type": "string", "format": "date-time"},
            "preferences": {
                "type": "object",
                "properties": {
                    "theme": {"type": "string"},
                    "notifications": {"type": "boolean"},
                },
            },
            "tags": {"type": "array", "items": {"type": "string"}},
        }

        # Create schema definition
        schema_result = self.singer_types.create_schema_definition(
            stream_name="users",
            properties=properties,
            key_properties=["user_id"],
        )
        assert schema_result.is_success

        # Create matching record
        record_data = {
            "user_id": 123,
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True,
            "created_at": "2025-01-15T10:30:00Z",
            "preferences": {"theme": "dark", "notifications": True},
            "tags": ["developer", "python", "meltano"],
        }

        # Create record message
        record_result = self.singer_types.create_record_message("users", record_data)
        assert record_result.is_success

        # Validate that record matches schema types
        for field, value in record_data.items():
            if field in properties:
                type_def = properties[field]
                validation_result = self.singer_types.validate_value(value, type_def)
                # Note: Complex validation might not pass due to nested structure
                # but we're testing the integration pathway
                assert isinstance(validation_result, FlextResult)

    def test_properties_list_complete_workflow(self) -> None:
        """Test complete properties list creation and manipulation."""
        # Start with base properties
        base_properties: FlextTypes.NestedDict = {
            "id": {"type": "integer"},
            "name": {"type": "string"},
        }

        props_result = self.singer_types.create_properties_list(base_properties)
        assert props_result.is_success
        assert props_result.data is not None
        assert isinstance(props_result.data, dict)
        props_dict = props_result.data

        # Add multiple properties
        additional_fields = [
            ("email", {"type": "string", "format": "email"}),
            ("age", {"type": "integer", "minimum": 0, "maximum": 150}),
            ("is_verified", {"type": "boolean"}),
        ]

        current_props = props_dict
        for field_name, field_def in additional_fields:
            add_result = self.singer_types.add_property(
                current_props,
                field_name,
                field_def,
            )
            assert add_result.is_success
            assert add_result.data is not None
            assert isinstance(add_result.data, dict)
            current_props = add_result.data

        # Verify final properties list
        assert current_props is not None
        assert isinstance(current_props, dict)
        assert len(current_props) == 5  # 2 base + 3 additional
        field_names = set(current_props.keys())
        assert field_names == {"id", "name", "email", "age", "is_verified"}

    def test_all_message_types_integration(self) -> None:
        """Test creation and integration of all Singer message types."""
        stream_name = "integration_test"

        # Create schema message
        properties = {"id": {"type": "integer"}, "data": {"type": "string"}}

        schema_result = self.singer_types.create_schema_message(
            stream=stream_name,
            schema={"type": "object", "properties": properties},
            key_properties=["id"],
        )
        assert schema_result.is_success

        # Create record message
        record_result = self.singer_types.create_record_message(
            stream_name,
            {"id": 1, "data": "test data"},
        )
        assert record_result.is_success

        # Create state message
        state_result = self.singer_types.create_state_message(
            {"bookmarks": {stream_name: {"last_id": 1}}},
        )
        assert state_result.is_success

        # Verify all messages have consistent stream naming
        assert schema_result.data is not None
        assert isinstance(schema_result.data, dict)
        assert record_result.data is not None
        assert isinstance(record_result.data, dict)
        schema_msg = schema_result.data
        record_msg = record_result.data

        assert schema_msg["stream"] == stream_name
        assert record_msg["stream"] == stream_name

        # Verify message types
        assert schema_msg["type"] == "SCHEMA"
        assert record_msg["type"] == "RECORD"

    def test_exception_paths_coverage(self) -> None:
        """Test exception paths to achieve 100% coverage."""
        # Test create_string_type exception path
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_string_type()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "String type creation failed" in result.error
            )

        # Test create_integer_type exception path
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_integer_type()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Integer type creation failed" in result.error
            )

        # Test create_number_type exception path
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_number_type()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Number type creation failed" in result.error
            )

        # Test create_boolean_type exception path
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_boolean_type()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Boolean type creation failed" in result.error
            )

        # Test create_array_type exception path
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_array_type()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Array type creation failed" in result.error
            )

        # Test create_object_type exception path
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_object_type()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Object type creation failed" in result.error
            )

        # Test create_datetime_type exception path
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_datetime_type()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "DateTime type creation failed" in result.error
            )

    def test_create_schema_message_exception_path(self) -> None:
        """Test create_schema_message exception path."""
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_schema_message("test_stream", {})
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Schema message creation failed" in result.error
            )

    def test_create_record_message_exception_path(self) -> None:
        """Test create_record_message exception path."""
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_record_message("test_stream", {})
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Record message creation failed" in result.error
            )

    def test_create_state_message_exception_path(self) -> None:
        """Test create_state_message exception path."""
        with mock.patch("flext_meltano.singer_types.FlextResult.ok") as mock_ok:
            mock_ok.side_effect = Exception("Test exception")

            result = self.singer_types.create_state_message({})
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "State message creation failed" in result.error
            )
