"""FlextSinger Type Abstractions - Complete abstraction of Singer SDK types.

This module provides complete FlextSinger type abstractions so that projects like
flext-tap-*, flext-target-*, and flext-dbt-* never need to import singer_sdk directly.
All typing needs are provided through this module.

Architecture:
    Type Layer: Complete type abstraction from Singer SDK
    Schema Layer: Schema definitions without Singer SDK dependency
    Message Layer: Singer message types abstracted through FlextResult
    Stream Layer: Stream type definitions for tap/target operations

Features:
    - Complete typing abstraction from singer_sdk.typing
    - Schema definition types without direct Singer imports
    - Message format types for Singer protocol compliance
    - Stream configuration types for tap/target implementation
    - Zero dependency on singer_sdk for consuming projects

Examples:
    Basic typing usage:
        >>> from flext_meltano import FlextSingerTypes
        >>> types = FlextSingerTypes()
        >>> string_type = types.StringType()
        >>> integer_type = types.IntegerType()
        >>> object_type = types.ObjectType(properties={
        ...     "id": types.IntegerType(),
        ...     "name": types.StringType()
        ... })

    Schema definition:
        >>> schema = types.create_stream_schema(
        ...     stream_name="users",
        ...     properties={
        ...         "id": types.IntegerType(),
        ...         "email": types.StringType()
        ...     },
        ...     primary_keys=["id"]
        ... )

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from flext_core import FlextLogger, FlextResult

# Initialize logger
logger = FlextLogger(__name__)

# =============================================================================
# FLEXT SINGER TYPE DEFINITIONS - Complete abstraction layer
# =============================================================================


class FlextSingerType:
    """Base class for all FlextSinger type definitions.

    Provides a complete abstraction over singer_sdk typing without direct imports.
    """

    def __init__(self, description: str | None = None) -> None:
        """Initialize FlextSinger type."""
        self.description = description

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer SDK compatible dictionary format."""
        result: dict[str, object] = {"type": self.get_type_name()}
        if self.description:
            result["description"] = self.description
        return result

    @abstractmethod
    def get_type_name(self) -> str:
        """Get the Singer type name."""
        ...


class StringType(FlextSingerType):
    """FlextSinger string type abstraction."""

    def __init__(
        self,
        max_length: int | None = None,
        format: str | None = None,
        description: str | None = None,
    ) -> None:
        """Initialize string type with optional constraints."""
        super().__init__(description)
        self.max_length = max_length
        self.format = format

    def get_type_name(self) -> str:
        """Get type name for string."""
        return "string"

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer dictionary with string-specific properties."""
        result = super().to_singer_dict()
        if self.max_length is not None:
            result["maxLength"] = self.max_length
        if self.format:
            result["format"] = self.format
        return result


class IntegerType(FlextSingerType):
    """FlextSinger integer type abstraction."""

    def __init__(
        self,
        minimum: int | None = None,
        maximum: int | None = None,
        description: str | None = None,
    ) -> None:
        """Initialize integer type with optional constraints."""
        super().__init__(description)
        self.minimum = minimum
        self.maximum = maximum

    def get_type_name(self) -> str:
        """Get type name for integer."""
        return "integer"

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer dictionary with integer-specific properties."""
        result = super().to_singer_dict()
        if self.minimum is not None:
            result["minimum"] = self.minimum
        if self.maximum is not None:
            result["maximum"] = self.maximum
        return result


class NumberType(FlextSingerType):
    """FlextSinger number (float) type abstraction."""

    def __init__(
        self,
        minimum: float | None = None,
        maximum: float | None = None,
        description: str | None = None,
    ) -> None:
        """Initialize number type with optional constraints."""
        super().__init__(description)
        self.minimum = minimum
        self.maximum = maximum

    def get_type_name(self) -> str:
        """Get type name for number."""
        return "number"

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer dictionary with number-specific properties."""
        result = super().to_singer_dict()
        if self.minimum is not None:
            result["minimum"] = self.minimum
        if self.maximum is not None:
            result["maximum"] = self.maximum
        return result


class BooleanType(FlextSingerType):
    """FlextSinger boolean type abstraction."""

    def get_type_name(self) -> str:
        """Get type name for boolean."""
        return "boolean"


class DateTimeType(FlextSingerType):
    """FlextSinger datetime type abstraction."""

    def __init__(self, format: str = "date-time", description: str | None = None) -> None:
        """Initialize datetime type with format."""
        super().__init__(description)
        self.format = format

    def get_type_name(self) -> str:
        """Get type name for datetime."""
        return "string"

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer dictionary with datetime format."""
        result = super().to_singer_dict()
        result["format"] = self.format
        return result


class ArrayType(FlextSingerType):
    """FlextSinger array type abstraction."""

    def __init__(
        self,
        items: FlextSingerType,
        min_items: int | None = None,
        max_items: int | None = None,
        description: str | None = None,
    ) -> None:
        """Initialize array type with item type and constraints."""
        super().__init__(description)
        self.items = items
        self.min_items = min_items
        self.max_items = max_items

    def get_type_name(self) -> str:
        """Get type name for array."""
        return "array"

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer dictionary with array-specific properties."""
        result = super().to_singer_dict()
        result["items"] = self.items.to_singer_dict()
        if self.min_items is not None:
            result["minItems"] = self.min_items
        if self.max_items is not None:
            result["maxItems"] = self.max_items
        return result


class ObjectType(FlextSingerType):
    """FlextSinger object type abstraction."""

    def __init__(
        self,
        properties: dict[str, FlextSingerType] | None = None,
        additional_properties: bool = True,
        description: str | None = None,
    ) -> None:
        """Initialize object type with properties."""
        super().__init__(description)
        self.properties = properties or {}
        self.additional_properties = additional_properties

    def get_type_name(self) -> str:
        """Get type name for object."""
        return "object"

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer dictionary with object-specific properties."""
        result = super().to_singer_dict()
        result["properties"] = {
            name: prop_type.to_singer_dict()
            for name, prop_type in self.properties.items()
        }
        result["additionalProperties"] = self.additional_properties
        return result


# =============================================================================
# FLEXT SINGER SCHEMA ABSTRACTIONS
# =============================================================================


class FlextSingerSchemaDefinition:
    """Complete abstraction of Singer schema definitions."""

    def __init__(
        self,
        stream_name: str,
        properties: dict[str, FlextSingerType],
        primary_keys: list[str] | None = None,
        replication_keys: list[str] | None = None,
        description: str | None = None,
    ) -> None:
        """Initialize FlextSinger schema."""
        self.stream_name = stream_name
        self.properties = properties
        self.primary_keys = primary_keys or []
        self.replication_keys = replication_keys or []
        self.description = description

    def to_singer_schema(self) -> dict[str, object]:
        """Convert to Singer schema dictionary format."""
        return {
            "type": "object",
            "properties": {
                name: prop_type.to_singer_dict()
                for name, prop_type in self.properties.items()
            },
            "additionalProperties": True,
        }

    def to_catalog_entry(self) -> dict[str, object]:
        """Convert to Singer catalog entry format."""
        metadata: list[dict[str, object]] = []

        # Add table-level metadata
        table_metadata_dict: dict[str, object] = {
            "replication-method": "FULL_TABLE",
            "selected": True,
        }
        if self.replication_keys:
            table_metadata_dict["replication-method"] = "INCREMENTAL"
            table_metadata_dict["replication-key"] = self.replication_keys[0]

        table_metadata: dict[str, object] = {
            "breadcrumb": [],
            "metadata": table_metadata_dict,
        }
        metadata.append(table_metadata)

        # Add field-level metadata
        for field_name in self.properties:
            field_metadata_dict: dict[str, object] = {
                "inclusion": "automatic" if field_name in self.primary_keys else "available",
            }
            field_metadata: dict[str, object] = {
                "breadcrumb": ["properties", field_name],
                "metadata": field_metadata_dict,
            }
            metadata.append(field_metadata)

        return {
            "tap_stream_id": self.stream_name,
            "stream": self.stream_name,
            "schema": self.to_singer_schema(),
            "metadata": metadata,
        }


# =============================================================================
# FLEXT SINGER MESSAGE ABSTRACTIONS
# =============================================================================


class FlextSingerMessage:
    """Base class for Singer message abstractions."""

    def __init__(self, message_type: str) -> None:
        """Initialize Singer message."""
        self.type = message_type

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer message dictionary format."""
        return {"type": self.type}


class FlextSingerRecord(FlextSingerMessage):
    """FlextSinger RECORD message abstraction."""

    def __init__(self, stream: str, record: dict[str, object], time_extracted: str | None = None) -> None:
        """Initialize Singer RECORD message."""
        super().__init__("RECORD")
        self.stream = stream
        self.record = record
        self.time_extracted = time_extracted

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer RECORD message format."""
        result = super().to_singer_dict()
        result["stream"] = self.stream
        result["record"] = self.record
        if self.time_extracted:
            result["time_extracted"] = self.time_extracted
        return result


class FlextSingerSchema(FlextSingerMessage):
    """FlextSinger SCHEMA message abstraction."""

    def __init__(self, stream: str, schema: FlextSingerSchemaDefinition, key_properties: list[str] | None = None) -> None:
        """Initialize Singer SCHEMA message."""
        super().__init__("SCHEMA")
        self.stream = stream
        self.schema = schema
        self.key_properties = key_properties or []

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer SCHEMA message format."""
        result = super().to_singer_dict()
        result["stream"] = self.stream
        result["schema"] = self.schema.to_singer_schema()
        result["key_properties"] = self.key_properties
        return result


class FlextSingerState(FlextSingerMessage):
    """FlextSinger STATE message abstraction."""

    def __init__(self, value: dict[str, object]) -> None:
        """Initialize Singer STATE message."""
        super().__init__("STATE")
        self.value = value

    def to_singer_dict(self) -> dict[str, object]:
        """Convert to Singer STATE message format."""
        result = super().to_singer_dict()
        result["value"] = self.value
        return result


# =============================================================================
# SINGER SDK COMPATIBILITY CLASSES
# =============================================================================


class FlextPropertiesList:
    """Singer SDK PropertiesList compatibility class."""

    def __init__(self, properties: tuple[dict[str, object], ...]) -> None:
        """Initialize properties list."""
        self.properties = properties

    def to_dict(self) -> dict[str, object]:
        """Convert to Singer schema format."""
        schema_properties: dict[str, object] = {}
        required: list[str] = []

        for prop in self.properties:
            name_obj = prop["name"]
            prop_type = prop["type"]
            is_required = prop.get("required", False)

            # Type-safe extraction with proper validation
            if not isinstance(name_obj, str):
                continue
            name = name_obj
            
            schema_properties[name] = prop_type
            if is_required:
                required.append(name)

        result: dict[str, object] = {
            "type": "object",
            "properties": schema_properties,
        }

        if required:
            result["required"] = required

        return result


# =============================================================================
# MAIN FLEXT SINGER TYPES CLASS - Single interface for all typing needs
# =============================================================================


class FlextSingerTypes:
    """Main class providing complete Singer type abstractions.

    This class provides all typing functionality needed by flext-tap-*,
    flext-target-*, and flext-dbt-* projects without requiring direct
    singer_sdk imports.
    """

    def __init__(self) -> None:
        """Initialize FlextSinger types interface."""
        self._logger = FlextLogger(f"{__name__}.FlextSingerTypes")
        self._logger.info("FlextSingerTypes initialized")

    # Type creation methods
    def StringType(
        self,
        max_length: int | None = None,
        format: str | None = None,
        description: str | None = None,
    ) -> StringType:
        """Create a FlextSinger string type."""
        return StringType(max_length=max_length, format=format, description=description)

    def IntegerType(
        self,
        minimum: int | None = None,
        maximum: int | None = None,
        description: str | None = None,
    ) -> IntegerType:
        """Create a FlextSinger integer type."""
        return IntegerType(minimum=minimum, maximum=maximum, description=description)

    def NumberType(
        self,
        minimum: float | None = None,
        maximum: float | None = None,
        description: str | None = None,
    ) -> NumberType:
        """Create a FlextSinger number type."""
        return NumberType(minimum=minimum, maximum=maximum, description=description)

    def BooleanType(self, description: str | None = None) -> BooleanType:
        """Create a FlextSinger boolean type."""
        return BooleanType(description=description)

    def DateTimeType(self, format: str = "date-time", description: str | None = None) -> DateTimeType:
        """Create a FlextSinger datetime type."""
        return DateTimeType(format=format, description=description)

    def ArrayType(
        self,
        items: FlextSingerType,
        min_items: int | None = None,
        max_items: int | None = None,
        description: str | None = None,
    ) -> ArrayType:
        """Create a FlextSinger array type."""
        return ArrayType(
            items=items,
            min_items=min_items,
            max_items=max_items,
            description=description,
        )

    def ObjectType(
        self,
        properties: dict[str, FlextSingerType] | None = None,
        additional_properties: bool = True,
        description: str | None = None,
    ) -> ObjectType:
        """Create a FlextSinger object type."""
        return ObjectType(
            properties=properties,
            additional_properties=additional_properties,
            description=description,
        )

    # Schema creation methods
    def create_stream_schema(
        self,
        stream_name: str,
        properties: dict[str, FlextSingerType],
        primary_keys: list[str] | None = None,
        replication_keys: list[str] | None = None,
        description: str | None = None,
    ) -> FlextSingerSchemaDefinition:
        """Create a complete stream schema definition."""
        return FlextSingerSchemaDefinition(
            stream_name=stream_name,
            properties=properties,
            primary_keys=primary_keys,
            replication_keys=replication_keys,
            description=description,
        )

    # Message creation methods
    def create_record_message(
        self,
        stream: str,
        record: dict[str, object],
        time_extracted: str | None = None,
    ) -> FlextSingerRecord:
        """Create a Singer RECORD message."""
        return FlextSingerRecord(
            stream=stream,
            record=record,
            time_extracted=time_extracted,
        )

    def create_schema_message(
        self,
        stream: str,
        schema: FlextSingerSchemaDefinition,
        key_properties: list[str] | None = None,
    ) -> FlextSingerSchema:
        """Create a Singer SCHEMA message."""
        return FlextSingerSchema(
            stream=stream,
            schema=schema,
            key_properties=key_properties,
        )

    def create_state_message(self, value: dict[str, object]) -> FlextSingerState:
        """Create a Singer STATE message."""
        return FlextSingerState(value=value)

    # Utility methods
    # Schema property methods (Singer SDK compatibility)
    def Property(
        self,
        name: str,
        property_type: FlextSingerType,
        required: bool = False,
        description: str | None = None
    ) -> dict[str, object]:
        """Create a Singer schema property (Singer SDK compatibility)."""
        prop_def = property_type.to_singer_dict()
        if description:
            prop_def["description"] = description

        return {
            "name": name,
            "type": prop_def,
            "required": required,
        }

    def PropertiesList(self, *properties: dict[str, object]) -> FlextPropertiesList:
        """Create a properties list (Singer SDK compatibility)."""
        return FlextPropertiesList(properties)

    def validate_schema(self, schema: FlextSingerSchemaDefinition) -> FlextResult[bool]:
        """Validate a FlextSinger schema definition."""
        try:
            if not schema.stream_name:
                return FlextResult[bool].fail("Schema must have a stream name")

            if not schema.properties:
                return FlextResult[bool].fail("Schema must have at least one property")

            # Validate primary keys exist in properties
            for pk in schema.primary_keys:
                if pk not in schema.properties:
                    return FlextResult[bool].fail(f"Primary key '{pk}' not found in properties")

            # Validate replication keys exist in properties
            for rk in schema.replication_keys:
                if rk not in schema.properties:
                    return FlextResult[bool].fail(f"Replication key '{rk}' not found in properties")

            self._logger.debug("Schema validation successful", stream_name=schema.stream_name)
            return FlextResult[bool].ok(True)

        except Exception as e:
            error_msg = f"Schema validation failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "ArrayType",
    "BooleanType",
    "DateTimeType",
    # Singer SDK compatibility
    "FlextPropertiesList",
    # Message types
    "FlextSingerMessage",
    "FlextSingerRecord",
    # Schema types
    "FlextSingerSchema",
    "FlextSingerState",
    # Base types
    "FlextSingerType",
    # Main interface
    "FlextSingerTypes",
    "IntegerType",
    "NumberType",
    "ObjectType",
    "StringType",
]
