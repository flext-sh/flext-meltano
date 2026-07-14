"""Singer protocol utilities — message emission, stdin processing, discovery.

Centralizes Singer protocol operations that were duplicated across consumer
projects. All methods return r[T] and use canonical m.Meltano.* models.

Access pattern: u.Meltano.emit_schema(), u.Meltano.process_stdin(), etc.
"""

from __future__ import annotations

import sys

from flext_cli import r, u as cli_u
from flext_core import e
from flext_meltano import (
    FlextMeltanoConstants as c,
    FlextMeltanoModels as m,
    FlextMeltanoProtocols as p,
    FlextMeltanoTypes as t,
)


class FlextMeltanoUtilitiesSinger:
    """Singer protocol utilities for message emission and stdin processing."""

    @staticmethod
    def emit_schema(
        stream_name: str,
        schema: t.JsonMapping,
        key_properties: t.StrSequence,
        bookmark_properties: t.StrSequence | None = None,
    ) -> p.Result[str]:
        """Emit a Singer SCHEMA message as JSON line to stdout.

        Args:
            stream_name: Name of the Singer stream.
            schema: JSON schema for the stream's records.
            key_properties: Primary key properties for the stream.
            bookmark_properties: Optional bookmark columns for incremental replication.

        Returns:
            r[str] with the serialized JSON line on success.

        """
        try:
            msg = m.Meltano.SingerSchemaMessage.model_validate({
                "stream": stream_name,
                "schema": schema,
                "key_properties": list(key_properties),
                "bookmark_properties": list(bookmark_properties or []),
            })
            line = msg.model_dump_json(by_alias=True)
            sys.stdout.write(line + "\n")
            sys.stdout.flush()
            return r[str].ok(line)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return e.fail_operation(
                f"emit SCHEMA for {stream_name}",
                exc,
                result_type=r[str],
            )

    @staticmethod
    def emit_record(
        stream_name: str,
        record: t.JsonMapping,
        time_extracted: str | None = None,
        version: int | None = None,
    ) -> p.Result[str]:
        """Emit a Singer RECORD message as JSON line to stdout.

        Args:
            stream_name: Name of the Singer stream.
            record: The record data payload.
            time_extracted: Optional ISO 8601 timestamp of extraction.
            version: Optional stream version for activate_version protocol.

        Returns:
            r[str] with the serialized JSON line on success.

        """
        try:
            msg = m.Meltano.SingerRecordMessage(
                stream=stream_name,
                record=record,
                time_extracted=time_extracted,
                version=version,
            )
            line = msg.model_dump_json(by_alias=True)
            sys.stdout.write(line + "\n")
            sys.stdout.flush()
            return r[str].ok(line)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return e.fail_operation(
                f"emit RECORD for {stream_name}",
                exc,
                result_type=r[str],
            )

    @staticmethod
    def emit_state(
        value: t.MutableJsonMapping,
    ) -> p.Result[str]:
        """Emit a Singer STATE message as JSON line to stdout.

        Args:
            value: State bookmark payload.

        Returns:
            r[str] with the serialized JSON line on success.

        """
        try:
            msg = m.Meltano.SingerStateMessage.model_validate({"value": value})
            line = msg.model_dump_json(by_alias=True)
            sys.stdout.write(line + "\n")
            sys.stdout.flush()
            return r[str].ok(line)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return e.fail_operation("emit STATE", exc, result_type=r[str])

    @staticmethod
    def process_stdin(
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[None]:
        """Process Singer messages from stdin and route to handler.

        Template method: parses JSON lines from stdin, identifies message
        type (SCHEMA/RECORD/STATE), validates via Pydantic models, and
        routes to the appropriate handler method.

        Args:
            handler: Implementation of SingerTargetHandler protocol.

        Returns:
            r[None] on success, r[None].fail on processing error.

        """
        try:
            for line in sys.stdin:
                result = FlextMeltanoUtilitiesSinger._process_stdin_line(
                    line,
                    handler,
                )
                if result.failure:
                    return result
            return r[None].ok(None)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return e.fail_operation("Stdin processing", exc, result_type=r[None])

    @staticmethod
    def _process_stdin_line(
        line: str,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[None]:
        """Process one Singer JSON line from stdin."""
        stripped = line.strip()
        if not stripped:
            return r[None].ok(None)
        raw_value: t.JsonValue = cli_u.Cli.json_loads(stripped).unwrap()
        if not isinstance(raw_value, dict):
            return r[None].ok(None)
        raw = t.json_dict_adapter().validate_python(raw_value)
        return FlextMeltanoUtilitiesSinger._dispatch_singer_message(raw, handler)

    @staticmethod
    def _dispatch_singer_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[None]:
        """Route a parsed Singer message to the matching handler."""
        msg_type = raw.get("type", "")
        if msg_type == c.Meltano.SingerMessageType.SCHEMA:
            return FlextMeltanoUtilitiesSinger._handle_schema_message(raw, handler)
        if msg_type == c.Meltano.SingerMessageType.RECORD:
            return FlextMeltanoUtilitiesSinger._handle_record_message(raw, handler)
        if msg_type == c.Meltano.SingerMessageType.STATE:
            return FlextMeltanoUtilitiesSinger._handle_state_message(raw, handler)
        return r[None].ok(None)

    @staticmethod
    def _handle_schema_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[None]:
        """Handle one Singer SCHEMA message."""
        schema_msg = m.Meltano.SingerSchemaMessage.model_validate(raw)
        result = handler.handle_schema(schema_msg)
        if result.failure:
            return e.fail_operation(
                f"SCHEMA handler for {schema_msg.stream}",
                result.error,
                result_type=r[None],
            )
        return r[None].ok(None)

    @staticmethod
    def _handle_record_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[None]:
        """Handle one Singer RECORD message."""
        record_msg = m.Meltano.SingerRecordMessage.model_validate(raw)
        result = handler.handle_record(record_msg)
        if result.failure:
            return e.fail_operation(
                f"RECORD handler for {record_msg.stream}",
                result.error,
                result_type=r[None],
            )
        return r[None].ok(None)

    @staticmethod
    def _handle_state_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[None]:
        """Handle one Singer STATE message."""
        state_msg = m.Meltano.SingerStateMessage.model_validate(raw)
        result = handler.handle_state(state_msg)
        if result.failure:
            return e.fail_operation("STATE handler", result.error, result_type=r[None])
        return r[None].ok(None)

    @staticmethod
    def build_catalog_entry(
        stream_name: str,
        schema: t.JsonMapping,
        key_properties: t.StrSequence,
        replication_key: str | None = None,
        *,
        is_selected: bool = True,
    ) -> p.Result[m.Meltano.SingerCatalogEntry]:
        """Build a Singer catalog entry from stream metadata.

        Generic catalog construction that domain-specific projects
        use by providing their schema/key_properties from their
        own discovery logic. Returns a proper Pydantic model.

        Args:
            stream_name: Name of the stream.
            schema: JSON schema for the stream.
            key_properties: Primary key columns.
            replication_key: Optional column for incremental sync.
            is_selected: Whether the stream is selected for sync.

        Returns:
            r[m.Meltano.SingerCatalogEntry] on success.

        """
        try:
            metadata_entry = m.Meltano.SingerCatalogMetadata(
                breadcrumb=[],
                metadata={
                    "selected": is_selected,
                    "replication-key": replication_key or "",
                    "replication-method": (
                        c.Meltano.SingerReplicationMethod.INCREMENTAL
                        if replication_key
                        else c.Meltano.SingerReplicationMethod.FULL_TABLE
                    ),
                },
            )
            entry = m.Meltano.SingerCatalogEntry.model_validate({
                "tap_stream_id": stream_name,
                "stream": stream_name,
                "schema": schema,
                "key_properties": list(key_properties),
                "metadata": [metadata_entry],
                "replication_key": replication_key,
                "replication_method": (
                    c.Meltano.SingerReplicationMethod.INCREMENTAL
                    if replication_key
                    else c.Meltano.SingerReplicationMethod.FULL_TABLE
                ),
            })
            return r[m.Meltano.SingerCatalogEntry].ok(entry)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return e.fail_operation(
                f"build catalog entry for {stream_name}",
                exc,
                result_type=r[m.Meltano.SingerCatalogEntry],
            )
