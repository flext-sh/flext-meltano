"""Singer protocol utilities — stdin processing and catalog discovery.

Centralizes Singer protocol operations that were duplicated across consumer
projects. All methods return r[T] and use canonical m.Meltano.* models.

Access pattern: u.Meltano.process_stdin(), u.Meltano.build_catalog_entry().

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import sys
from collections.abc import Sequence
from typing import TYPE_CHECKING

from flext_cli import u

from flext_meltano import c, e, m, r, t

if TYPE_CHECKING:
    from flext_meltano import p


class FlextMeltanoUtilitiesSinger:
    """Singer protocol utilities for stdin processing and catalog discovery."""

    @staticmethod
    def process_stdin(handler: p.Meltano.SingerTargetHandler) -> p.Result[bool]:
        """Process Singer messages from stdin and route to handler.

        Template method: parses JSON lines from stdin, identifies message
        type (SCHEMA/RECORD/STATE), validates via Pydantic models, and
        routes to the appropriate handler method.

        Args:
            handler: Implementation of SingerTargetHandler protocol.

        Returns:
            r[bool] on success, r[bool].fail on processing error.

        """
        try:
            for line in sys.stdin:
                result = FlextMeltanoUtilitiesSinger._process_stdin_line(line, handler)
                if result.failure:
                    return result
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return e.fail_operation("Stdin processing", exc, result_type=r[bool])

    @staticmethod
    def _process_stdin_line(
        line: str,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[bool]:
        """Process one Singer JSON line from stdin.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        stripped = line.strip()
        if not stripped:
            return r[bool].ok(value=True)
        raw_value: t.JsonValue = u.Cli.json_loads(stripped).unwrap()
        if not isinstance(raw_value, dict):
            return r[bool].ok(value=True)
        raw = u.json_dict_adapter().validate_python(raw_value)
        return FlextMeltanoUtilitiesSinger._dispatch_singer_message(raw, handler)

    @staticmethod
    def _dispatch_singer_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[bool]:
        """Route a parsed Singer message to the matching handler.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        msg_type = raw.get("type", "")
        if msg_type == c.Meltano.SingerMessageType.SCHEMA:
            return FlextMeltanoUtilitiesSinger._handle_schema_message(raw, handler)
        if msg_type == c.Meltano.SingerMessageType.RECORD:
            return FlextMeltanoUtilitiesSinger._handle_record_message(raw, handler)
        if msg_type == c.Meltano.SingerMessageType.STATE:
            return FlextMeltanoUtilitiesSinger._handle_state_message(raw, handler)
        return r[bool].ok(value=True)

    @staticmethod
    def _handle_schema_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[bool]:
        """Handle one Singer SCHEMA message.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        schema_msg = m.Meltano.SingerSchemaMessage.model_validate(raw)
        result = handler.handle_schema(schema_msg)
        if result.failure:
            return e.fail_operation(
                f"SCHEMA handler for {schema_msg.stream}",
                result.error,
                result_type=r[bool],
            )
        return r[bool].ok(value=True)

    @staticmethod
    def _handle_record_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[bool]:
        """Handle one Singer RECORD message.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        record_msg = m.Meltano.SingerRecordMessage.model_validate(raw)
        result = handler.handle_record(record_msg)
        if result.failure:
            return e.fail_operation(
                f"RECORD handler for {record_msg.stream}",
                result.error,
                result_type=r[bool],
            )
        return r[bool].ok(value=True)

    @staticmethod
    def _handle_state_message(
        raw: t.JsonMapping,
        handler: p.Meltano.SingerTargetHandler,
    ) -> p.Result[bool]:
        """Handle one Singer STATE message.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        state_msg = m.Meltano.SingerStateMessage.model_validate(raw)
        result = handler.handle_state(state_msg)
        if result.failure:
            return e.fail_operation("STATE handler", result.error, result_type=r[bool])
        return r[bool].ok(value=True)

    @staticmethod
    def build_catalog_entry(
        stream_name: str,
        schema: t.JsonMapping,
        key_properties: Sequence[str],
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
        replication_method = (
            c.Meltano.SingerReplicationMethod.INCREMENTAL
            if replication_key
            else c.Meltano.SingerReplicationMethod.FULL_TABLE
        )
        try:
            metadata_entry = m.Meltano.SingerCatalogMetadata(
                breadcrumb=(),
                metadata={
                    "selected": is_selected,
                    "replication-key": replication_key or "",
                    "replication-method": replication_method,
                },
            )
            entry = m.Meltano.SingerCatalogEntry.model_validate({
                "tap_stream_id": stream_name,
                c.ProcessingMode.STREAM: stream_name,
                "schema": schema,
                "key_properties": list(key_properties),
                "metadata": [metadata_entry],
                "replication_key": replication_key,
                "replication_method": replication_method,
            })
            return r[m.Meltano.SingerCatalogEntry].ok(entry)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            return e.fail_operation(
                f"build catalog entry for {stream_name}",
                exc,
                result_type=r[m.Meltano.SingerCatalogEntry],
            )


__all__: list[str] = ["FlextMeltanoUtilitiesSinger"]
