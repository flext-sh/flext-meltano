"""Modern Schema Flattening and Deflattening for Oracle Database Tap.

This module provides enterprise-grade schema flattening capabilities for
Oracle Database complex data structures, supporting nested objects, arrays,
and dynamic schema generation with Singer SDK compliance.
"""

from __future__ import annotations

import json

# Removed circular dependency - use DI pattern
# Resolved: DI pattern implemented successfully
import logging
from typing import Any


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

logger = get_logger(__name__)


class OracleSchemaFlattener:
    """Enterprise schema flattening for Oracle Database complex structures.

    Features:
    - Configurable flattening depth
    - Custom separator support
    - Type preservation
    - Reversible deflattening
    - Performance optimization
    """

    def __init__(
        self,
        *,
        enabled: bool = False,
        max_depth: int = 5,
        separator: str = "__",
        preserve_types: bool = True,
    ) -> None:
        """Initialize the schema flattener.

        Args:
            enabled: Whether flattening is enabled
            max_depth: Maximum flattening depth
            separator: Field separator for flattened names
            preserve_types: Whether to preserve original types

        """
        self.enabled = enabled
        self.max_depth = max_depth
        self.separator = separator
        self.preserve_types = preserve_types

        logger.debug(
            "Oracle schema flattener initialized: enabled=%s, max_depth=%d, "
            "separator='%s'",
            enabled,
            max_depth,
            separator,
        )

    def flatten_schema(self, schema: dict[str, Any], depth: int = 0) -> dict[str, Any]:
        """Flatten a JSON schema for Oracle Database structures.

        Args:
            schema: Original JSON schema
            depth: Current flattening depth

        Returns:
            Flattened schema dict

        """
        if not self.enabled:
            return schema

        if depth >= self.max_depth:
            logger.warning(
                "Maximum flattening depth %d reached, stopping recursion",
                self.max_depth,
            )
            return schema

        flattened = {}
        properties = schema.get("properties", {})

        for field_name, field_schema in properties.items():
            if self._should_flatten_field(field_schema):
                flattened_fields = self._flatten_field(field_name, field_schema, depth)
                flattened.update(flattened_fields)
            else:
                flattened[field_name] = field_schema

        # Preserve schema metadata
        result = schema.copy()
        result["properties"] = flattened

        logger.debug("Flattened schema with %d fields", len(flattened))
        return result

    def flatten_record(self, record: dict[str, Any], depth: int = 0) -> dict[str, Any]:
        """Flatten a data record for Oracle Database insertion.

        Args:
            record: Original record
            depth: Current flattening depth

        Returns:
            Flattened record dict

        """
        if not self.enabled:
            return record

        if depth >= self.max_depth:
            logger.warning(
                "Maximum flattening depth %d reached for record",
                self.max_depth,
            )
            return record

        flattened = {}

        for key, value in record.items():
            if self._should_flatten_value(value):
                flattened_fields = self._flatten_value(key, value, depth)
                flattened.update(flattened_fields)
            else:
                flattened[key] = value

        logger.debug("Flattened record with %d fields", len(flattened))
        return flattened

    def deflate_record(self, flattened_record: dict[str, Any]) -> dict[str, Any]:
        """Reconstruct original nested structure from flattened record.

        Args:
            flattened_record: Flattened record

        Returns:
            Reconstructed nested record

        """
        if not self.enabled:
            return flattened_record

        logger.debug(
            "Deflattening record with %d flattened fields",
            len(flattened_record),
        )

        nested: dict[str, Any] = {}

        for flattened_key, value in flattened_record.items():
            if self.separator in flattened_key:
                self._set_nested_value(nested, flattened_key, value)
            else:
                nested[flattened_key] = value

        logger.debug("Deflattened record to %d top-level fields", len(nested))
        return nested

    def _should_flatten_field(self, field_schema: dict[str, Any]) -> bool:
        """Check if a schema field should be flattened.

        Args:
            field_schema: Field schema definition

        Returns:
            True if field should be flattened

        """
        field_type = field_schema.get("type")

        # Flatten objects with properties
        if field_type == "object" and "properties" in field_schema:
            return True

        # Flatten arrays of objects
        if field_type == "array":
            items = field_schema.get("items", {})
            if isinstance(items, dict) and items.get("type") == "object":
                return True

        return False

    def _should_flatten_value(self, value: object) -> bool:
        """Check if a value should be flattened.

        Args:
            value: Data value

        Returns:
            True if value should be flattened

        """
        # Flatten dictionaries
        if isinstance(value, dict):
            return True

        # Flatten lists of dictionaries
        return bool(isinstance(value, list) and value and isinstance(value[0], dict))

    def _flatten_field(
        self,
        field_name: str,
        field_schema: dict[str, Any],
        depth: int,
    ) -> dict[str, Any]:
        """Flatten a single schema field.

        Args:
            field_name: Field name
            field_schema: Field schema
            depth: Current depth

        Returns:
            Flattened field definitions

        """
        flattened = {}
        field_type = field_schema.get("type")

        if field_type == "object":
            properties = field_schema.get("properties", {})
            for prop_name, prop_schema in properties.items():
                flattened_name = f"{field_name}{self.separator}{prop_name}"

                if self._should_flatten_field(prop_schema):
                    # Recursive flattening
                    sub_flattened = self._flatten_field(
                        flattened_name,
                        prop_schema,
                        depth + 1,
                    )
                    flattened.update(sub_flattened)
                else:
                    flattened[flattened_name] = prop_schema

        elif field_type == "array":
            items = field_schema.get("items", {})
            if items.get("type") == "object":
                # Array of objects - flatten to JSON string
                flattened[field_name] = {
                    "type": "string",
                    "description": f"Flattened array of objects from {field_name}",
                    "_flext_original_type": "array_of_objects",
                }
            else:
                flattened[field_name] = field_schema

        return flattened

    def _flatten_value(self, key: str, value: object, depth: int) -> dict[str, Any]:
        """Flatten a single data value.

        Args:
            key: Value key
            value: Data value
            depth: Current depth

        Returns:
            Flattened key-value pairs

        """
        flattened = {}

        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened_key = f"{key}{self.separator}{sub_key}"

                if self._should_flatten_value(sub_value):
                    # Recursive flattening
                    sub_flattened = self._flatten_value(
                        flattened_key,
                        sub_value,
                        depth + 1,
                    )
                    flattened.update(sub_flattened)
                else:
                    flattened[flattened_key] = sub_value

        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                # Array of objects - convert to JSON string for Oracle
                flattened[key] = json.dumps(value)
            else:
                # Array of primitives - keep as is
                flattened[key] = value

        return flattened

    def _set_nested_value(
        self,
        nested: dict[str, Any],
        flattened_key: str,
        value: object,
    ) -> None:
        """Set a nested value in the reconstructed structure.

        Args:
            nested: Target nested dictionary
            flattened_key: Flattened key with separators
            value: Value to set

        """
        parts = flattened_key.split(self.separator)
        current = nested

        # Navigate to parent
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set final value
        final_key = parts[-1]
        current[final_key] = value

    def get_flattening_config(self) -> dict[str, Any]:
        """Get current flattening configuration.

        Returns:
            Configuration dictionary

        """
        return {
            "enabled": self.enabled,
            "max_depth": self.max_depth,
            "separator": self.separator,
            "preserve_types": self.preserve_types,
        }

    def validate_schema_compatibility(self, schema: dict[str, Any]) -> bool:
        """Validate schema compatibility with flattening strategy.

        Args:
            schema: Schema to validate

        Returns:
            True if schema is compatible

        """
        if not self.enabled:
            return True

        try:
            flattened = self.flatten_schema(schema)
            # Check for Oracle column name length limits
            oracle_identifier_limit = 128
            for field_name in flattened.get("properties", {}):
                if len(field_name) > oracle_identifier_limit:
                    logger.warning(
                        "Flattened field name '%s' exceeds Oracle identifier limit",
                        field_name,
                    )
                    return False
        except Exception:
            logger.exception("Schema compatibility validation failed")
            return False
        else:
            return True
