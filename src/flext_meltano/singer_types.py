"""Singer Types - Unified Singer types and schema handling with enterprise patterns.

This module provides complete Singer type functionality following flext-core
single-class-per-module pattern. Consolidates all type definitions, schema management,
message handling, and properties management in a unified class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextLogger, FlextResult, FlextTypes

# Constants

# Type aliases to replace explicit object
ConfigDict = FlextTypes.Core.Dict
SchemaDict = FlextTypes.Core.Dict
MessageDict = FlextTypes.Core.Dict
PropertiesDict = FlextTypes.Core.Dict


class FlextSingerTypes:
    """Unified Singer types and schema handling with enterprise patterns.

    Consolidated class providing all Singer type functionality following flext-core
    single-class-per-module pattern. Includes type definitions, schema management,
    message handling, and properties management.
    """

    def __init__(self) -> None:
        """Initialize unified Singer types manager."""
        self._logger = FlextLogger(f"{__name__}.FlextSingerTypes")
        self._type_registry: dict[str, FlextTypes.Core.Dict] = {
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

    def create_string_type(self, **kwargs: object) -> FlextResult[FlextTypes.Core.Dict]:
        """Create string type with optional constraints.

        Returns:
            FlextResult[FlextTypes.Core.Dict]: String type creation result.

        """
        try:
            type_def: FlextTypes.Core.Dict = {"type": "string"}
            type_def.update(kwargs)
            return FlextResult[FlextTypes.Core.Dict].ok(type_def)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"String type creation failed: {e}"
            )

    def create_integer_type(
        self, **kwargs: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create integer type with optional constraints."""
        try:
            type_def: FlextTypes.Core.Dict = {"type": "integer"}
            type_def.update(kwargs)
            return FlextResult[FlextTypes.Core.Dict].ok(type_def)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Integer type creation failed: {e}"
            )

    def create_number_type(self, **kwargs: object) -> FlextResult[FlextTypes.Core.Dict]:
        """Create number type with optional constraints."""
        try:
            type_def: FlextTypes.Core.Dict = {"type": "number"}
            type_def.update(kwargs)
            return FlextResult[FlextTypes.Core.Dict].ok(type_def)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Number type creation failed: {e}"
            )

    def create_boolean_type(
        self, **kwargs: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create boolean type."""
        try:
            type_def: FlextTypes.Core.Dict = {"type": "boolean"}
            type_def.update(kwargs)
            return FlextResult[FlextTypes.Core.Dict].ok(type_def)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Boolean type creation failed: {e}"
            )

    def create_datetime_type(
        self, **kwargs: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create date-time type."""
        try:
            type_def: FlextTypes.Core.Dict = {"type": "string", "format": "date-time"}
            type_def.update(kwargs)
            return FlextResult[FlextTypes.Core.Dict].ok(type_def)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"DateTime type creation failed: {e}"
            )

    def create_array_type(
        self, items: FlextTypes.Core.Dict | None = None, **kwargs: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create array type with optional item type."""
        try:
            type_def: FlextTypes.Core.Dict = {"type": "array"}
            if items:
                type_def["items"] = items
            type_def.update(kwargs)
            return FlextResult[FlextTypes.Core.Dict].ok(type_def)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Array type creation failed: {e}"
            )

    def create_object_type(
        self, properties: FlextTypes.Core.Dict | None = None, **kwargs: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create object type with optional properties."""
        try:
            type_def: FlextTypes.Core.Dict = {"type": "object"}
            if properties:
                type_def["properties"] = properties
            type_def.update(kwargs)
            return FlextResult[FlextTypes.Core.Dict].ok(type_def)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Object type creation failed: {e}"
            )

    def validate_value(
        self, value: object, type_def: FlextTypes.Core.Dict
    ) -> FlextResult[object]:
        """Validate value against type definition using lookup table pattern.

        Eliminates multiple return statements using validation dispatch table
        following advanced Python 3.13+ patterns and clean architecture.
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
                expected_type_info, type_display = validation_rules[type_name]
                # Type narrowing for isinstance check - proper union handling
                if isinstance(expected_type_info, tuple):
                    # Handle tuple case like (int, float) for "number"
                    if not isinstance(value, expected_type_info):
                        return FlextResult[object].fail(
                            f"Expected {type_display}, got {type(value).__name__}"
                        )
                # Handle single type case
                elif not isinstance(value, expected_type_info):
                    return FlextResult[object].fail(
                        f"Expected {type_display}, got {type(value).__name__}"
                    )

            return FlextResult[object].ok(value)
        except Exception as e:
            return FlextResult[object].fail(f"Value validation failed: {e}")

    # ============================================================================
    # SCHEMA MANAGEMENT METHODS
    # ============================================================================

    def create_schema_definition(
        self,
        stream_name: str | None = None,
        properties: dict[str, FlextTypes.Core.Dict] | None = None,
        key_properties: FlextTypes.Core.StringList | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create Singer schema definition or SCHEMA message."""
        try:
            # Handle legacy call with just properties
            if stream_name is None and properties is not None:
                schema: FlextTypes.Core.Dict = {
                    "type": "object",
                    "properties": properties,
                }
                # Add optional metadata
                for key in ["required", "additionalProperties", "description"]:
                    if key in kwargs:
                        schema[key] = kwargs[key]
                return FlextResult[FlextTypes.Core.Dict].ok(schema)

            # Handle Singer SCHEMA message creation
            if stream_name is not None:
                schema_obj: FlextTypes.Core.Dict = {
                    "type": "object",
                    "properties": properties or {},
                }
                message: FlextTypes.Core.Dict = {
                    "type": "SCHEMA",
                    "stream": stream_name,
                    "schema": schema_obj,
                    "key_properties": key_properties or [],
                }
                return FlextResult[FlextTypes.Core.Dict].ok(message)

            return FlextResult[FlextTypes.Core.Dict].fail(
                "Either properties (for schema) or stream_name (for SCHEMA message) must be provided"
            )
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Schema definition creation failed: {e}"
            )

    # ============================================================================
    # MESSAGE HANDLING METHODS
    # ============================================================================

    def create_record_message(
        self, stream: str, record: FlextTypes.Core.Dict, **kwargs: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create Singer RECORD message."""
        try:
            message: FlextTypes.Core.Dict = {
                "type": "RECORD",
                "stream": stream,
                "record": record,
            }

            # Add optional fields
            for key in ["time_extracted", "version"]:
                if key in kwargs:
                    message[key] = kwargs[key]

            return FlextResult[FlextTypes.Core.Dict].ok(message)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Record message creation failed: {e}"
            )

    def create_schema_message(
        self,
        stream: str,
        schema: FlextTypes.Core.Dict,
        key_properties: FlextTypes.Core.StringList | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create Singer SCHEMA message."""
        try:
            message: FlextTypes.Core.Dict = {
                "type": "SCHEMA",
                "stream": stream,
                "schema": schema,
                "key_properties": key_properties or [],
            }

            # Add optional fields
            for key in ["bookmark_properties"]:
                if key in kwargs:
                    message[key] = kwargs[key]

            return FlextResult[FlextTypes.Core.Dict].ok(message)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Schema message creation failed: {e}"
            )

    def create_state_message(
        self, value: FlextTypes.Core.Dict
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create Singer STATE message."""
        try:
            message: FlextTypes.Core.Dict = {"type": "STATE", "value": value}
            return FlextResult[FlextTypes.Core.Dict].ok(message)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"State message creation failed: {e}"
            )

    # ============================================================================
    # PROPERTIES MANAGEMENT METHODS
    # ============================================================================

    def create_properties_list(
        self, properties: dict[str, FlextTypes.Core.Dict]
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create and validate properties list."""
        try:
            # Validate each property
            for prop_name, prop_def in properties.items():
                if not isinstance(prop_def, dict) or "type" not in prop_def:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        f"Invalid property definition for {prop_name}"
                    )

            # Convert nested dict to match return type using dict()
            properties_flat: FlextTypes.Core.Dict = dict(properties.items())
            return FlextResult[FlextTypes.Core.Dict].ok(properties_flat)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Properties list creation failed: {e}"
            )

    def add_property(
        self,
        properties: FlextTypes.Core.Dict,
        name: str,
        type_def: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Add property to properties collection."""
        try:
            updated_properties = properties.copy()
            updated_properties[name] = type_def
            return FlextResult[FlextTypes.Core.Dict].ok(updated_properties)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Property addition failed: {e}"
            )

    def convert_to_dict(self, data: object) -> FlextResult[FlextTypes.Core.Dict]:
        """Convert data to dictionary format."""
        try:
            if isinstance(data, dict):
                return FlextResult[FlextTypes.Core.Dict].ok(data)
            if hasattr(data, "to_dict") and callable(getattr(data, "to_dict")):
                result = getattr(data, "to_dict")()
                if isinstance(result, dict):
                    return FlextResult[FlextTypes.Core.Dict].ok(result)
            elif hasattr(data, "__dict__"):
                return FlextResult[FlextTypes.Core.Dict].ok(data.__dict__)

            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Cannot convert {type(data)} to dict"
            )
        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Dictionary conversion failed: {e}"
            )

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def get_registered_types(self) -> FlextTypes.Core.StringList:
        """Get list of registered type names."""
        return list(self._type_registry.keys())

    def get_type_definition(self, type_name: str) -> FlextResult[FlextTypes.Core.Dict]:
        """Get type definition by name."""
        if type_name in self._type_registry:
            return FlextResult[FlextTypes.Core.Dict].ok(
                self._type_registry[type_name].copy()
            )
        return FlextResult[FlextTypes.Core.Dict].fail(f"Type {type_name} not found")

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
