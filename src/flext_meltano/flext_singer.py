"""FlextSinger - Ponte de simplificação entre Singer SDK e flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Fornece simplificação e ponte entre Singer SDK e padrões flext-core,
sem duplicar funcionalidades básicas.
"""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, Any, TextIO, cast

from flext_core import FlextContainer, FlextResult, get_logger

if TYPE_CHECKING:
    from collections.abc import Iterator

# ============================================================================
# PONTE SINGER SDK <-> FLEXT-CORE
# ============================================================================


class FlextSingerBridge:
    """Ponte inteligente entre Singer SDK e flext-core com composição."""

    def __init__(self) -> None:
        """Initialize Singer bridge using flext-core patterns."""
        self._logger = get_logger(self.__class__.__name__)

        # Use flext-core container for composição inteligente
        self._container = FlextContainer()
        self._container.register("logger", self._logger)

        # Message types registry - composição inteligente
        self._message_types: dict[str, Any] = {
            "RECORD": self._create_record_message,
            "SCHEMA": self._create_schema_message,
            "STATE": self._create_state_message,
        }

    def flext_singer_create_message(
        self,
        message_type: str,
        **kwargs: object,
    ) -> FlextResult[dict[str, Any]]:
        """Create Singer message using intelligent composition - método universal."""
        try:
            if message_type not in self._message_types:
                return FlextResult(error=f"Unknown message type: {message_type}")

            # Use composition pattern - delega para método específico
            creator_func = self._message_types[message_type]
            return cast("FlextResult[dict[str, Any]]", creator_func(**kwargs))

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult(error=f"Failed to create Singer message: {e}")

    def _create_record_message(
        self,
        stream: str,
        record: dict[str, Any],
        time_extracted: str | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create record message internally."""
        if not stream or not isinstance(record, dict):
            return FlextResult(error="Invalid stream name or record format")

        message = {"type": "RECORD", "stream": stream, "record": record}
        if time_extracted:
            message["time_extracted"] = time_extracted

        return FlextResult(data=message)

    def _create_schema_message(
        self,
        stream: str,
        schema: dict[str, Any],
        key_properties: list[str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create schema message internally."""
        if not stream or not isinstance(schema, dict):
            return FlextResult(error="Invalid stream name or schema format")

        message = {
            "type": "SCHEMA",
            "stream": stream,
            "schema": schema,
            "key_properties": key_properties or [],
        }

        return FlextResult(data=message)

    def _create_state_message(
        self,
        value: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Create state message internally."""
        message = {"type": "STATE", "value": value}
        return FlextResult(data=message)

    # Mantém métodos específicos para compatibilidade mas usa composição
    def flext_singer_create_record_message(
        self,
        stream: str,
        record: dict[str, Any],
        time_extracted: str | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create Singer RECORD message - uses composition."""
        return self._create_record_message(
            stream=stream,
            record=record,
            time_extracted=time_extracted,
        )

    def flext_singer_create_schema_message(
        self,
        stream: str,
        schema: dict[str, Any],
        key_properties: list[str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Create Singer SCHEMA message - uses composition."""
        return self._create_schema_message(
            stream=stream,
            schema=schema,
            key_properties=key_properties,
        )

    def flext_singer_create_state_message(
        self,
        value: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Create Singer STATE message - uses composition."""
        return self._create_state_message(value=value)

    def flext_singer_parse_message_line(self, line: str) -> FlextResult[dict[str, Any]]:
        """Parse Singer message line using flext-core patterns."""
        try:
            line = line.strip()
            if not line:
                return FlextResult(error="Empty message line")

            message = json.loads(line)

            if not isinstance(message, dict) or "type" not in message:
                return FlextResult(error="Invalid Singer message format")

            return FlextResult(data=message)

        except json.JSONDecodeError as e:
            return FlextResult(error=f"Invalid JSON in Singer message: {e}")
        except (ValueError, TypeError) as e:
            return FlextResult(error=f"Failed to parse Singer message: {e}")

    def flext_singer_validate_message(
        self,
        message: object,
    ) -> FlextResult[str]:
        """Validate Singer message format using flext-core patterns."""
        try:
            if not isinstance(message, dict):
                return FlextResult(error="Message must be a dictionary")

            msg_type = message.get("type")
            if not msg_type:
                return FlextResult(error="Message must have 'type' field")

            if msg_type == "RECORD":
                required_fields = ["stream", "record"]
            elif msg_type == "SCHEMA":
                required_fields = ["stream", "schema"]
            elif msg_type == "STATE":
                required_fields = ["value"]
            else:
                return FlextResult(error=f"Unknown message type: {msg_type}")

            for field in required_fields:
                if field not in message:
                    return FlextResult(error=f"Missing required field: {field}")

            return FlextResult(data=msg_type)

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult(error=f"Failed to validate Singer message: {e}")

    def flext_singer_write_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Write Singer message to stdout using flext-core patterns."""
        try:
            validation_result = self.flext_singer_validate_message(message)
            if not validation_result.is_success:
                return FlextResult(error=f"Invalid message: {validation_result.error}")

            json.dumps(message, separators=(",", ":"))
            sys.stdout.flush()

            return FlextResult(data=None)

        except (OSError, ValueError) as e:
            return FlextResult(error=f"Failed to write Singer message: {e}")

    def flext_singer_read_messages(
        self,
        input_stream: TextIO | None = None,
    ) -> Iterator[FlextResult[dict[str, Any]]]:
        """Read Singer messages from input stream using flext-core patterns."""
        stream = input_stream or sys.stdin

        try:
            for line in stream:
                yield self.flext_singer_parse_message_line(line)
        except (OSError, ValueError) as e:
            yield FlextResult(error=f"Failed to read Singer messages: {e}")


class FlextSingerCatalog:
    """Simplified Singer catalog management using flext-core patterns."""

    def __init__(self, catalog: dict[str, Any] | None = None) -> None:
        """Initialize with optional catalog data."""
        self._logger = get_logger(self.__class__.__name__)
        self._catalog = catalog or {"streams": []}

    def flext_singer_add_stream(
        self,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: list[str] | None = None,
    ) -> FlextResult[None]:
        """Add stream to catalog using flext-core patterns."""
        try:
            if not stream_name or not isinstance(schema, dict):
                return FlextResult(error="Invalid stream name or schema")

            stream_entry = {
                "tap_stream_id": stream_name,
                "schema": schema,
                "metadata": [
                    {
                        "breadcrumb": [],
                        "metadata": {"inclusion": "available", "selected": True},
                    },
                ],
            }

            if key_properties:
                stream_entry["key_properties"] = key_properties

            self._catalog["streams"].append(stream_entry)
            return FlextResult(data=None)

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult(error=f"Failed to add stream to catalog: {e}")

    def flext_singer_get_catalog(self) -> FlextResult[dict[str, Any]]:
        """Get catalog data using flext-core patterns."""
        try:
            return FlextResult(data=self._catalog.copy())
        except (ValueError, TypeError) as e:
            return FlextResult(error=f"Failed to get catalog: {e}")

    def flext_singer_get_selected_streams(self) -> FlextResult[list[str]]:
        """Get list of selected stream names using flext-core patterns."""
        try:
            selected_streams = []

            for stream in self._catalog.get("streams", []):
                metadata = stream.get("metadata", [])
                for meta in metadata:
                    if meta.get("breadcrumb") == [] and meta.get("metadata", {}).get(
                        "selected",
                    ):
                        selected_streams.append(stream.get("tap_stream_id"))
                        break

            return FlextResult(data=selected_streams)

        except (ValueError, TypeError, KeyError) as e:
            return FlextResult(error=f"Failed to get selected streams: {e}")


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def flext_create_singer_bridge() -> FlextSingerBridge:
    """Create Singer bridge instance."""
    return FlextSingerBridge()


def flext_create_singer_catalog(
    catalog: dict[str, Any] | None = None,
) -> FlextSingerCatalog:
    """Create Singer catalog instance."""
    return FlextSingerCatalog(catalog)


__all__ = [
    "FlextSingerBridge",
    "FlextSingerCatalog",
    "flext_create_singer_bridge",
    "flext_create_singer_catalog",
]
