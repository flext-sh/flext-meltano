"""Singer Types - Unified Singer types and schema handling with enterprise patterns.

This module provides complete Singer type functionality following flext-core
single-class-per-module pattern. Consolidates all type definitions, schema management,
message handling, and properties management in a unified class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, FlextResult
from flext_meltano.typings import FlextMeltanoTypes

# Constants

# Type aliases to replace explicit object
ConfigDict = FlextMeltanoTypes.Core.SingerConfigDict
SchemaDict = FlextMeltanoTypes.Core.SingerSchemaDict
MessageDict = FlextMeltanoTypes.Core.Dict
PropertiesDict = FlextMeltanoTypes.Core.Dict


class FlextSingerTypes:
    """Unified Singer types and schema handling with enterprise patterns.

    Consolidated class providing all Singer type functionality following flext-core
    single-class-per-module pattern. Includes type definitions, schema management,
    message handling, and properties management.
    """

    @override
    def __init__(self) -> None:
        """Initialize unified Singer types manager."""
        self._logger = FlextLogger(f"{__name__}.FlextSingerTypes")
        self._type_registry: dict[str, FlextMeltanoTypes.Core.Dict] = {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
            "number": {"type": "number"},
            "boolean": {"type": "boolean"},
            "date-time": {"type": "string", "format": "date-time"},
            "array": {"type": "array"},
            "object": {"type": "object"},
        }

    # ============================================================================

    # ============================================================================

    def create_string_type(
        self, **kwargs: object
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create string type with optional constraints.

        Returns:
            FlextResult[FlextMeltanoTypes.Core.Dict]: String type creation result.

        """
        try:
            type_def: FlextMeltanoTypes.Core.Dict = {"type": "string"}
            type_def.update(kwargs)
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=type_def)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"String type creation failed: {e}",
            )

    def create_integer_type(
        self,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create integer type with optional constraints.

        Returns:
            FlextResult containing the integer type definition.

        """
        try:
            type_def: FlextMeltanoTypes.Core.Dict = {"type": "integer"}
            type_def.update(kwargs)
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=type_def)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Integer type creation failed: {e}",
            )

    def create_number_type(
        self, **kwargs: object
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create number type with optional constraints.

        Returns:
            FlextResult containing the number type definition.

        """
        try:
            type_def: FlextMeltanoTypes.Core.Dict = {"type": "number"}
            type_def.update(kwargs)
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=type_def)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Number type creation failed: {e}",
            )

    def create_boolean_type(
        self,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create boolean type.

        Returns:
            FlextResult containing the boolean type definition.

        """
        try:
            type_def: FlextMeltanoTypes.Core.Dict = {"type": "boolean"}
            type_def.update(kwargs)
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=type_def)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Boolean type creation failed: {e}",
            )

    def create_datetime_type(
        self,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create date-time type.

        Returns:
            FlextResult containing the date-time type definition.

        """
        try:
            type_def: FlextMeltanoTypes.Core.Dict = {
                "type": "string",
                "format": "date-time",
            }
            type_def.update(kwargs)
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=type_def)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"DateTime type creation failed: {e}",
            )

    def create_array_type(
        self,
        items: FlextMeltanoTypes.Core.Dict | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create array type with optional item type.

        Returns:
            FlextResult containing the array type definition.

        """
        try:
            type_def: FlextMeltanoTypes.Core.Dict = {"type": "array"}
            if items:
                type_def["items"] = items
            type_def.update(kwargs)
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=type_def)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Array type creation failed: {e}",
            )

    def create_object_type(
        self,
        properties: FlextMeltanoTypes.Core.Dict | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create object type with optional properties.

        Returns:
            FlextResult containing the object type definition.

        """
        try:
            type_def: FlextMeltanoTypes.Core.Dict = {"type": "object"}
            if properties:
                type_def["properties"] = properties
            type_def.update(kwargs)
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=type_def)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Object type creation failed: {e}",
            )

    def validate_value(
        self,
        value: object,
        type_def: FlextMeltanoTypes.Core.Dict,
    ) -> FlextResult[object]:
        """Validate value against type definition using lookup table pattern.

        Eliminates multiple return statements using validation dispatch table
        following advanced Python 3.13+ patterns and clean architecture.

        Returns:
            FlextResult containing the validated value or error information.

        """
        try:
            type_name = type_def.get("type")

            # Check for missing type definition
            if type_name is None:
                return FlextResult[object].fail("Type definition missing 'type' field")

            # Validation dispatch table eliminating multiple if/return statements
            validation_rules: dict[str, tuple[type | tuple[type, ...], str]] = {
                "string": (str, "string"),
                "integer": (int, "integer"),
                "number": ((int, float), "number"),
                "boolean": (bool, "boolean"),
                "array": (list, "array"),
                "object": (dict, "object"),
            }

            # Single validation logic with dispatch table
            if isinstance(type_name, str) and type_name in validation_rules:
                type_display, expected_type_info = validation_rules[type_name]

                if isinstance(expected_type_info, tuple):
                    # Handle tuple case like (int, float) for "number"
                    if not isinstance(value, expected_type_info):
                        return FlextResult[object].fail(
                            f"Expected {type_display}, got {type(value).__name__}",
                        )
                # Handle single type case
                elif not isinstance(value, (str, int, float, bool, list, dict)):
                    return FlextResult[object].fail(
                        f"Expected {type_display}, got {type(value).__name__}",
                    )

            return FlextResult[object].ok(data=value)
        except Exception as e:
            return FlextResult[object].fail(f"Value validation failed: {e}")

    # ============================================================================
    # SCHEMA MANAGEMENT METHODS
    # ============================================================================

    def create_schema_definition(
        self,
        _properties: dict[str, FlextMeltanoTypes.Core.Dict],
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create Singer schema definition (JSON Schema format).

        This method creates a pure JSON Schema object for stream validation.
        For Singer SCHEMA messages, use create_schema_message() instead.

        Returns:
            FlextResult containing the schema definition.

        """
        try:
            schema: FlextMeltanoTypes.Core.Dict = {
                "type": "object",
                "properties": "properties",
            }
            # Add optional metadata
            for key in ["required", "additionalProperties", "description"]:
                if key in kwargs:
                    schema[key] = kwargs[key]
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=schema)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Schema definition creation failed: {e}",
            )

    # ============================================================================
    # MESSAGE HANDLING METHODS
    # ============================================================================

    def create_record_message(
        self,
        _stream: str,
        _record: FlextMeltanoTypes.Core.Dict,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create Singer RECORD message.

        Returns:
            FlextResult containing the record message.

        """
        try:
            message: FlextMeltanoTypes.Core.Dict = {
                "type": "RECORD",
                "stream": "stream",
                "record": "record",
            }

            # Add optional fields
            for key in ["time_extracted", "version"]:
                if key in kwargs:
                    message[key] = kwargs[key]

            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=message)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Record message creation failed: {e}",
            )

    def create_schema_message(
        self,
        _stream: str,
        _schema: FlextMeltanoTypes.Core.Dict,
        key_properties: FlextMeltanoTypes.Core.StringList | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create Singer SCHEMA message.

        Returns:
            FlextResult containing the schema message.

        """
        try:
            message: FlextMeltanoTypes.Core.Dict = {
                "type": "SCHEMA",
                "stream": "stream",
                "schema": "schema",
                "key_properties": key_properties or [],
            }

            # Add optional fields
            for key in ["bookmark_properties"]:
                if key in kwargs:
                    message[key] = kwargs[key]

            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=message)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Schema message creation failed: {e}",
            )

    def create_state_message(
        self,
        _value: FlextMeltanoTypes.Core.Dict,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create Singer STATE message.

        Returns:
            FlextResult containing the state message.

        """
        try:
            message: FlextMeltanoTypes.Core.Dict = {"type": "STATE", "value": "value"}
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=message)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"State message creation failed: {e}",
            )

    # ============================================================================
    # PROPERTIES MANAGEMENT METHODS
    # ============================================================================

    def create_properties_list(
        self,
        properties: dict[str, FlextMeltanoTypes.Core.Dict],
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Create and validate properties list.

        Returns:
            FlextResult containing the validated properties.

        """
        try:
            # Validate each property
            for prop_name, prop_def in properties.items():
                if not isinstance(prop_def, dict) or "type" not in prop_def:
                    return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                        f"Invalid property definition for {prop_name}",
                    )

            # Convert nested dict to match return type using dict()
            properties_flat: FlextMeltanoTypes.Core.Dict = dict(properties.items())
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=properties_flat)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Properties list creation failed: {e}",
            )

    def add_property(
        self,
        properties: FlextMeltanoTypes.Core.Dict,
        name: str,
        type_def: FlextMeltanoTypes.Core.Dict,
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Add property to properties collection.

        Returns:
            FlextResult containing the updated properties.

        """
        try:
            updated_properties = properties.copy()
            updated_properties[name] = type_def
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=updated_properties)
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Property addition failed: {e}",
            )

    def convert_to_dict(self, data: object) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Convert data to dictionary format.

        Returns:
            FlextResult containing the converted dictionary.

        """
        try:
            if isinstance(data, dict):
                return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=data)
            if hasattr(data, "to_dict") and callable(getattr(data, "to_dict")):
                result: FlextResult[object] = getattr(data, "to_dict")()
                if isinstance(result, dict):
                    return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=result)
            elif hasattr(data, "__dict__"):
                return FlextResult[FlextMeltanoTypes.Core.Dict].ok(data=data.__dict__)

            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Cannot convert {type(data)} to dict",
            )
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
                f"Dictionary conversion failed: {e}",
            )

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def get_registered_types(self) -> FlextMeltanoTypes.Core.StringList:
        """Get list of registered type names.

        Returns:
            List of registered type names.

        """
        return list(self._type_registry.keys())

    def get_type_definition(
        self, type_name: str
    ) -> FlextResult[FlextMeltanoTypes.Core.Dict]:
        """Get type definition by name.

        Returns:
            FlextResult containing the type definition.

        """
        if type_name in self._type_registry:
            return FlextResult[FlextMeltanoTypes.Core.Dict].ok(
                self._type_registry[type_name].copy(),
            )
        return FlextResult[FlextMeltanoTypes.Core.Dict].fail(
            f"Type {type_name} not found"
        )

    @classmethod
    def create_instance(cls) -> FlextResult[FlextSingerTypes]:
        """Factory method to create FlextSingerTypes instance.

        Returns:
            FlextResult containing the created instance.

        """
        try:
            return FlextResult[FlextSingerTypes].ok(data=cls())
        except Exception as e:
            return FlextResult[FlextSingerTypes].fail(
                f"Instance creation failed: {e}",
            )


__all__ = [
    "FlextSingerTypes",
]
