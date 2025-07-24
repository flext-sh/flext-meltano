"""FlextMeltano Singer Stream Management.

Singer stream processing utilities following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult
from pydantic import BaseModel, Field


class FlextMeltanoStream(BaseModel):
    """Singer stream model with comprehensive validation.

    Represents a Singer data stream with schema and metadata.
    """

    name: str = Field(description="Stream name", min_length=1, max_length=255)

    stream_schema: dict[str, Any] = Field(
        description="JSON schema for the stream",
        default_factory=dict,
        alias="schema",
    )

    metadata: list[dict[str, Any]] = Field(
        default_factory=list, description="Stream metadata entries",
    )

    selected: bool = Field(
        default=True,
        description="Whether this stream is selected for extraction",
    )

    replication_method: str = Field(
        default="FULL_TABLE",
        description="Replication method (FULL_TABLE, INCREMENTAL)",
    )

    replication_key: str | None = Field(
        default=None, description="Field used for incremental replication",
    )

    def get_field_metadata(self, field_path: str) -> dict[str, Any] | None:
        """Get metadata for a specific field.

        Args:
            field_path: JSONPath to the field

        Returns:
            Field metadata or None if not found

        """
        for entry in self.metadata:
            if entry.get("breadcrumb") == field_path.split("."):
                metadata_value = entry.get("metadata", {})
                return dict(metadata_value) if metadata_value else {}
        return None

    def set_field_selection(self, field_path: str, selected: bool) -> FlextResult[None]:
        """Set field selection state.

        Args:
            field_path: JSONPath to the field
            selected: Whether field should be selected

        Returns:
            FlextResult indicating success or failure

        """
        try:
            breadcrumb = field_path.split(".")

            # Find existing metadata entry
            for entry in self.metadata:
                if entry.get("breadcrumb") == breadcrumb:
                    if "metadata" not in entry:
                        entry["metadata"] = {}
                    entry["metadata"]["selected"] = selected
                    return FlextResult.ok(None)

            # Create new metadata entry if not found
            self.metadata.append(
                {"breadcrumb": breadcrumb, "metadata": {"selected": selected}},
            )

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to set field selection: {e}")

    def get_selected_fields(self) -> list[str]:
        """Get list of selected field paths.

        Returns:
            List of selected field paths

        """
        selected_fields = []

        for entry in self.metadata:
            metadata = entry.get("metadata", {})
            if metadata.get("selected", True):  # Default to selected
                breadcrumb = entry.get("breadcrumb", [])
                if breadcrumb:
                    selected_fields.append(".".join(breadcrumb))

        return selected_fields

    def validate_schema(self) -> FlextResult[None]:
        """Validate the stream schema.

        Returns:
            FlextResult indicating validation success or failure

        """
        try:
            # Basic schema validation
            if not self.stream_schema:
                return FlextResult.fail("Stream schema is empty")

            if "type" not in self.stream_schema:
                return FlextResult.fail("Schema missing 'type' field")

            if "properties" not in self.stream_schema:
                return FlextResult.fail("Schema missing 'properties' field")

            # Validate replication key exists in schema if specified
            if self.replication_method == "INCREMENTAL" and self.replication_key:
                properties = self.stream_schema.get("properties", {})
                if self.replication_key not in properties:
                    return FlextResult.fail(
                        f"Replication key '{self.replication_key}' not found "
                        "in schema properties",
                    )

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Schema validation failed: {e}")

    def to_catalog_entry(self) -> dict[str, Any]:
        """Convert stream to catalog entry format.

        Returns:
            Dictionary representing catalog entry

        """
        return {
            "stream": self.name,
            "tap_stream_id": self.name,
            "schema": self.stream_schema,
            "metadata": self.metadata,
        }

    @classmethod
    def from_catalog_entry(
        cls, catalog_entry: dict[str, Any],
    ) -> FlextResult[FlextMeltanoStream]:
        """Create stream from catalog entry.

        Args:
            catalog_entry: Catalog entry dictionary

        Returns:
            FlextResult containing created stream

        """
        try:
            stream_name = catalog_entry.get("stream")
            if not stream_name:
                return FlextResult.fail("Catalog entry missing 'stream' field")

            schema = catalog_entry.get("schema", {})
            metadata = catalog_entry.get("metadata", [])

            # Extract replication info from metadata
            replication_method = "FULL_TABLE"
            replication_key = None

            for entry in metadata:
                if entry.get("breadcrumb") == []:
                    stream_metadata = entry.get("metadata", {})
                    replication_method = stream_metadata.get(
                        "replication-method", "FULL_TABLE",
                    )
                    replication_key = stream_metadata.get("replication-key")
                    break

            return FlextResult.ok(
                cls(
                    name=stream_name,
                    schema=schema,
                    metadata=metadata,
                    replication_method=replication_method,
                    replication_key=replication_key,
                ),
            )

        except Exception as e:
            return FlextResult.fail(f"Failed to create stream from catalog: {e}")
