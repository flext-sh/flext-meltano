"""Singer Types - Unified Singer types and schema handling with enterprise patterns.

This module provides complete Singer type functionality following flext-core
single-class-per-module pattern. Consolidates all type definitions, schema management,
message handling, and properties management in a unified class.

Architecture:
    Core: Unified FlextSingerTypes class handling all Singer functionality
    Types: String, Integer, Number, Boolean, DateTime, Array, Object types
    Schema: Schema definition and validation
    Messages: RECORD, SCHEMA, STATE message creation
    Properties: Properties list management and validation

Features:
    - Single unified class following flext-core patterns
    - Complete Singer type system abstraction
    - FlextResult railway-oriented programming
    - Type-safe schema and message handling
    - Enterprise error handling and validation

Examples:
    Create types:
        >>> singer_types = FlextSingerTypes()
        >>> string_result = singer_types.create_string_type(maxLength=255)
        >>> array_result = singer_types.create_array_type({"type": "string"})

    Create messages:
        >>> record_result = singer_types.create_record_message(
        ...     "users", {"id": 1, "name": "John"}
        ... )
        >>> schema_result = singer_types.create_schema_message(
        ...     "users", {"type": "object", "properties": {...}}
        ... )

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextLogger, FlextResult

# Constants

# Type aliases to replace explicit object
ConfigDict = dict[str, object]
SchemaDict = dict[str, object]
MessageDict = dict[str, object]
PropertiesDict = dict[str, object]


class FlextSingerTypes:
    """Unified Singer types and schema handling with enterprise patterns.

    Consolidated class providing all Singer type functionality following flext-core
    single-class-per-module pattern. Includes type definitions, schema management,
    message handling, and properties management.
    """

    def __init__(self) -> None:
        """Initialize unified Singer types manager."""
        self._logger = FlextLogger(f"{__name__}.FlextSingerTypes")
        self._type_registry: dict[str, dict[str, object]] = {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
            "number": {"type": "number"},
            "boolean": {"type": "boolean"},
            "date-time": {"type": "string", "format": "date-time"},
            "array": {"type": "array"},
            "object": {"type": "object"},
        }

    # ============================================================================
    # TYPE CREATION AND VALIDATION METHODS
    # ============================================================================

    def create_string_type(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Create string type with optional constraints."""
        try:
            type_def: dict[str, object] = {"type": "string"}
            type_def.update(kwargs)
            return FlextResult[dict[str, object]].ok(type_def)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"String type creation failed: {e}"
            )

    def create_integer_type(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Create integer type with optional constraints."""
        try:
            type_def: dict[str, object] = {"type": "integer"}
            type_def.update(kwargs)
            return FlextResult[dict[str, object]].ok(type_def)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Integer type creation failed: {e}"
            )

    def create_number_type(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Create number type with optional constraints."""
        try:
            type_def: dict[str, object] = {"type": "number"}
            type_def.update(kwargs)
            return FlextResult[dict[str, object]].ok(type_def)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Number type creation failed: {e}"
            )

    def create_boolean_type(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Create boolean type."""
        try:
            type_def: dict[str, object] = {"type": "boolean"}
            type_def.update(kwargs)
            return FlextResult[dict[str, object]].ok(type_def)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Boolean type creation failed: {e}"
            )

    def create_datetime_type(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Create date-time type."""
        try:
            type_def: dict[str, object] = {"type": "string", "format": "date-time"}
            type_def.update(kwargs)
            return FlextResult[dict[str, object]].ok(type_def)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"DateTime type creation failed: {e}"
            )

    def create_array_type(
        self, items: dict[str, object] | None = None, **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        """Create array type with optional item type."""
        try:
            type_def: dict[str, object] = {"type": "array"}
            if items:
                type_def["items"] = items
            type_def.update(kwargs)
            return FlextResult[dict[str, object]].ok(type_def)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Array type creation failed: {e}"
            )

    def create_object_type(
        self, properties: dict[str, object] | None = None, **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        """Create object type with optional properties."""
        try:
            type_def: dict[str, object] = {"type": "object"}
            if properties:
                type_def["properties"] = properties
            type_def.update(kwargs)
            return FlextResult[dict[str, object]].ok(type_def)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Object type creation failed: {e}"
            )

    def validate_value(
        self, value: object, type_def: dict[str, object]
    ) -> FlextResult[object]:
        """Validate value against type definition."""
        try:
            type_name = type_def.get("type")

            if type_name == "string" and not isinstance(value, str):
                return FlextResult[object].fail(
                    f"Expected string, got {type(value).__name__}"
                )
            if type_name == "integer" and not isinstance(value, int):
                return FlextResult[object].fail(
                    f"Expected integer, got {type(value).__name__}"
                )
            if type_name == "number" and not isinstance(value, (int, float)):
                return FlextResult[object].fail(
                    f"Expected number, got {type(value).__name__}"
                )
            if type_name == "boolean" and not isinstance(value, bool):
                return FlextResult[object].fail(
                    f"Expected boolean, got {type(value).__name__}"
                )
            if type_name == "array" and not isinstance(value, list):
                return FlextResult[object].fail(
                    f"Expected array, got {type(value).__name__}"
                )
            if type_name == "object" and not isinstance(value, dict):
                return FlextResult[object].fail(
                    f"Expected object, got {type(value).__name__}"
                )

            return FlextResult[object].ok(value)
        except Exception as e:
            return FlextResult[object].fail(f"Value validation failed: {e}")

    # ============================================================================
    # SCHEMA MANAGEMENT METHODS
    # ============================================================================

    def create_schema_definition(
        self, properties: dict[str, dict[str, object]], **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        """Create Singer schema definition."""
        try:
            schema: dict[str, object] = {"type": "object", "properties": properties}

            # Add optional metadata
            for key in ["required", "additionalProperties", "description"]:
                if key in kwargs:
                    schema[key] = kwargs[key]

            return FlextResult[dict[str, object]].ok(schema)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Schema definition creation failed: {e}"
            )

    # ============================================================================
    # MESSAGE HANDLING METHODS
    # ============================================================================

    def create_record_message(
        self, stream: str, record: dict[str, object], **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        """Create Singer RECORD message."""
        try:
            message: dict[str, object] = {"type": "RECORD", "stream": stream, "record": record}

            # Add optional fields
            for key in ["time_extracted", "version"]:
                if key in kwargs:
                    message[key] = kwargs[key]

            return FlextResult[dict[str, object]].ok(message)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Record message creation failed: {e}"
            )

    def create_schema_message(
        self,
        stream: str,
        schema: dict[str, object],
        key_properties: list[str] | None = None,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Create Singer SCHEMA message."""
        try:
            message: dict[str, object] = {
                "type": "SCHEMA",
                "stream": stream,
                "schema": schema,
                "key_properties": key_properties or [],
            }

            # Add optional fields
            for key in ["bookmark_properties"]:
                if key in kwargs:
                    message[key] = kwargs[key]

            return FlextResult[dict[str, object]].ok(message)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Schema message creation failed: {e}"
            )

    def create_state_message(
        self, value: dict[str, object]
    ) -> FlextResult[dict[str, object]]:
        """Create Singer STATE message."""
        try:
            message: dict[str, object] = {"type": "STATE", "value": value}
            return FlextResult[dict[str, object]].ok(message)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"State message creation failed: {e}"
            )

    # ============================================================================
    # PROPERTIES MANAGEMENT METHODS
    # ============================================================================

    def create_properties_list(
        self, properties: dict[str, dict[str, object]]
    ) -> FlextResult[dict[str, object]]:
        """Create and validate properties list."""
        try:
            # Validate each property
            for prop_name, prop_def in properties.items():
                if not isinstance(prop_def, dict) or "type" not in prop_def:
                    return FlextResult[dict[str, object]].fail(
                        f"Invalid property definition for {prop_name}"
                    )

            # Convert nested dict to match return type using dict()
            properties_flat: dict[str, object] = dict(properties.items())
            return FlextResult[dict[str, object]].ok(properties_flat)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Properties list creation failed: {e}"
            )

    def add_property(
        self, properties: dict[str, object], name: str, type_def: dict[str, object]
    ) -> FlextResult[dict[str, object]]:
        """Add property to properties collection."""
        try:
            updated_properties = properties.copy()
            updated_properties[name] = type_def
            return FlextResult[dict[str, object]].ok(updated_properties)
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Property addition failed: {e}")

    def convert_to_dict(self, data: object) -> FlextResult[dict[str, object]]:
        """Convert data to dictionary format."""
        try:
            if isinstance(data, dict):
                return FlextResult[dict[str, object]].ok(data)
            if hasattr(data, "to_dict") and callable(getattr(data, "to_dict")):
                result = getattr(data, "to_dict")()
                if isinstance(result, dict):
                    return FlextResult[dict[str, object]].ok(result)
            elif hasattr(data, "__dict__"):
                return FlextResult[dict[str, object]].ok(data.__dict__)

            return FlextResult[dict[str, object]].fail(
                f"Cannot convert {type(data)} to dict"
            )
        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Dictionary conversion failed: {e}"
            )

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def get_registered_types(self) -> list[str]:
        """Get list of registered type names."""
        return list(self._type_registry.keys())

    def get_type_definition(self, type_name: str) -> FlextResult[dict[str, object]]:
        """Get type definition by name."""
        if type_name in self._type_registry:
            return FlextResult[dict[str, object]].ok(
                self._type_registry[type_name].copy()
            )
        return FlextResult[dict[str, object]].fail(f"Type {type_name} not found")

    @classmethod
    def create_instance(cls) -> FlextResult[FlextSingerTypes]:
        """Factory method to create FlextSingerTypes instance."""
        try:
            return FlextResult["FlextSingerTypes"].ok(cls())
        except Exception as e:
            return FlextResult["FlextSingerTypes"].fail(
                f"Instance creation failed: {e}"
            )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "FlextSingerTypes",
]
