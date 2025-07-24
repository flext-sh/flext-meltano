"""FlextMeltano Singer Catalog Management.

Singer catalog handling and schema management following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoCatalog(BaseModel):
    """Singer catalog model with comprehensive validation.

    Represents a Singer catalog containing stream definitions and metadata.
    """

    streams: list[dict[str, Any]] = Field(
        default_factory=list, description="List of stream definitions",
    )

    version: str = Field(
        default="1.0",
        description="Catalog schema version",
        pattern=r"^\d+\.\d+$",
    )

    def get_stream_by_name(self, stream_name: str) -> dict[str, Any] | None:
        """Get stream definition by name.

        Args:
            stream_name: Name of the stream to find

        Returns:
            Stream definition dictionary or None if not found

        """
        for stream in self.streams:
            if stream.get("stream") == stream_name:
                return stream
        return None

    def add_stream(self, stream_definition: dict[str, Any]) -> FlextResult[None]:
        """Add stream definition to catalog.

        Args:
            stream_definition: Stream definition to add

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Basic validation
            if not stream_definition.get("stream"):
                return FlextResult.fail("Stream definition missing 'stream' field")

            if not stream_definition.get("schema"):
                return FlextResult.fail("Stream definition missing 'schema' field")

            # Check for duplicates
            existing = self.get_stream_by_name(stream_definition["stream"])
            if existing:
                return FlextResult.fail(
                    f"Stream '{stream_definition['stream']}' already exists",
                )

            self.streams.append(stream_definition)
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to add stream: {e}")

    def remove_stream(self, stream_name: str) -> FlextResult[None]:
        """Remove stream definition from catalog.

        Args:
            stream_name: Name of the stream to remove

        Returns:
            FlextResult indicating success or failure

        """
        try:
            original_count = len(self.streams)
            self.streams = [s for s in self.streams if s.get("stream") != stream_name]

            if len(self.streams) == original_count:
                return FlextResult.fail(f"Stream '{stream_name}' not found")

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to remove stream: {e}")

    @classmethod
    def from_file(cls, catalog_path: Path) -> FlextResult[FlextMeltanoCatalog]:
        """Load catalog from file.

        Args:
            catalog_path: Path to catalog file

        Returns:
            FlextResult containing loaded catalog

        """
        try:
            import json

            if not catalog_path.exists():
                return FlextResult.fail(f"Catalog file not found: {catalog_path}")

            with catalog_path.open() as f:
                catalog_data = json.load(f)

            return FlextResult.ok(cls(**catalog_data))

        except Exception as e:
            return FlextResult.fail(f"Failed to load catalog: {e}")

    def to_file(self, catalog_path: Path) -> FlextResult[None]:
        """Save catalog to file.

        Args:
            catalog_path: Path to save catalog

        Returns:
            FlextResult indicating success or failure

        """
        try:
            import json

            # Ensure parent directory exists
            catalog_path.parent.mkdir(parents=True, exist_ok=True)

            with catalog_path.open("w") as f:
                json.dump(self.model_dump(), f, indent=2)

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to save catalog: {e}")
