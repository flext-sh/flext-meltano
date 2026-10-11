"""Behavioral tests for flext-meltano Singer catalog contracts.

Exercises the OBSERVABLE public contract of the m.Meltano Singer catalog
models (validation, defaults, aliasing, roundtrip, error paths) plus the
canonical t.JsonMapping plugin-definition contract. No private attributes,
collaborators, or internal data structures are asserted.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from tests import c, m, t, tm


class TestsFlextMeltanoPluginProtocols:
    """Public-contract tests for the Meltano Singer catalog models."""

    # --- construction / return values -----------------------------------

    @staticmethod
    def test_catalog_builds_entries_from_payload() -> None:
        """model_validate exposes stream identifiers on the built entries."""
        catalog = m.Meltano.SingerCatalog.model_validate({
            "streams": [{"stream": "users", "tap_stream_id": "users", "schema": {}}],
        })

        entry = catalog.streams[0]
        tm.that(entry.stream, eq="users")
        tm.that(entry.tap_stream_id, eq="users")

    @staticmethod
    def test_catalog_defaults_message_type_to_catalog() -> None:
        """A catalog without an explicit type defaults to the CATALOG marker."""
        catalog = m.Meltano.SingerCatalog.model_validate({"streams": []})

        tm.that(catalog.type.value, eq="CATALOG")

    @staticmethod
    def test_empty_streams_validate_to_empty_sequence() -> None:
        """An empty stream list is a valid catalog with no entries."""
        catalog = m.Meltano.SingerCatalog.model_validate({"streams": []})

        tm.that(len(catalog.streams), eq=0)

    @staticmethod
    @pytest.mark.parametrize(
        "stream_names",
        [("users",), ("users", "orders"), ("a", "b", "c")],
    )
    def test_multiple_streams_preserve_input_order(
        stream_names: t.VariadicTuple[str],
    ) -> None:
        """Stream entries preserve the order of the validated payload."""
        payload: t.JsonMapping = {
            "streams": [
                {"stream": name, "tap_stream_id": name, "schema": {}}
                for name in stream_names
            ],
        }

        catalog = m.Meltano.SingerCatalog.model_validate(payload)

        tm.that(tuple(entry.stream for entry in catalog.streams), eq=stream_names)

    # --- aliasing / roundtrip -------------------------------------------

    @staticmethod
    def test_schema_alias_populates_schema_definition() -> None:
        """The 'schema' input key is exposed via the schema_definition field."""
        catalog = m.Meltano.SingerCatalog.model_validate({
            "streams": [
                {
                    "stream": "users",
                    "tap_stream_id": "users",
                    "schema": {"type": "object"},
                },
            ],
        })

        tm.that(catalog.streams[0].schema_definition, eq={"type": "object"})

    @staticmethod
    def test_dump_by_alias_re_emits_schema_key() -> None:
        """Serializing by alias round-trips schema_definition back to 'schema'."""
        entry = m.Meltano.SingerCatalogEntry.model_validate({
            "stream": "users",
            "tap_stream_id": "users",
            "schema": {"type": "object"},
        })

        dumped = entry.model_dump(by_alias=True)

        tm.that(dumped["schema"], eq={"type": "object"})

    @staticmethod
    def test_catalog_roundtrip_is_idempotent() -> None:
        """Re-validating a by-alias dump reproduces the same public payload."""
        source: t.JsonMapping = {
            "streams": [
                {"stream": "users", "tap_stream_id": "users", "schema": {}},
                {"stream": "orders", "tap_stream_id": "orders", "schema": {}},
            ],
        }

        first = m.Meltano.SingerCatalog.model_validate(source)
        second = m.Meltano.SingerCatalog.model_validate(first.model_dump(by_alias=True))

        tm.that(second.model_dump(by_alias=True), eq=first.model_dump(by_alias=True))

    # --- optional fields / invariants -----------------------------------

    @staticmethod
    def test_optional_entry_fields_default_to_none() -> None:
        """Unset optional entry fields expose None through the public API."""
        entry = m.Meltano.SingerCatalogEntry.model_validate({
            "stream": "users",
            "tap_stream_id": "users",
            "schema": {},
        })

        tm.that(entry.replication_key, none=True)
        tm.that(entry.is_view, none=True)
        tm.that(entry.table_name, none=True)
        tm.that(entry.row_count, none=True)

    @staticmethod
    def test_entry_accepts_replication_method_enum_value() -> None:
        """A supplied replication method surfaces as the typed enum value."""
        entry = m.Meltano.SingerCatalogEntry.model_validate({
            "stream": "users",
            "tap_stream_id": "users",
            "schema": {},
            "replication_method": "INCREMENTAL",
        })

        tm.that(
            entry.replication_method,
            eq=c.Meltano.SingerReplicationMethod.INCREMENTAL,
        )

    # --- error paths -----------------------------------------------------

    @staticmethod
    @pytest.mark.parametrize(
        ("omitted", "payload"),
        [
            ("tap_stream_id", {"stream": "users", "schema": {}}),
            ("stream", {"tap_stream_id": "users", "schema": {}}),
            ("schema", {"stream": "users", "tap_stream_id": "users"}),
        ],
    )
    def test_missing_required_entry_field_raises_validation_error(
        omitted: str,
        payload: t.JsonMapping,
    ) -> None:
        """Omitting any required entry field fails validation for that field."""
        with pytest.raises(m.ValidationError) as excinfo:
            m.Meltano.SingerCatalogEntry.model_validate(payload)

        reported = {
            str(part) for error in excinfo.value.errors() for part in error["loc"]
        }
        tm.that(reported, has=omitted)

    # --- plugin definition mapping contract -----------------------------

    @staticmethod
    def test_plugin_definition_honors_json_mapping_contract() -> None:
        """Plugin definitions behave as the canonical JSON mapping contract."""
        plugin_def: t.JsonMapping = {
            "name": "tap-postgres",
            "namespace": "tap_postgres",
            "pip_url": "git+https://github.com/example/tap-postgres.git",
        }

        tm.that(plugin_def["name"], eq="tap-postgres")
        tm.that(len(plugin_def), eq=3)

    @staticmethod
    def test_meltano_typing_namespace_excludes_legacy_singer_aliases() -> None:
        """t.Meltano exposes no legacy Singer/plugin typing aliases."""
        for legacy in (
            "SingerCatalogEntry",
            "SingerStreamCatalog",
            "PluginCatalog",
            "PluginDefinition",
        ):
            assert not hasattr(t.Meltano, legacy)
