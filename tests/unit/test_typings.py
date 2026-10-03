"""FLEXT Meltano Typings Unit Tests - Enterprise ELT testing patterns.

Behavioral contract tests for the flattened Meltano type namespace
(``t.Meltano``) and its companion domain models (``m.Meltano``). Tests
assert the OBSERVABLE public contract: which symbols the flat namespace
exposes, which legacy nested namespaces and duplicate aliases it refuses,
where runtime Singer SDK wrappers live, and the public model behavior of
the exported Singer catalog model.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import m, t


class TestsFlextMeltanoTypingsUnit:
    """Behavioral contract for the flat ``t.Meltano`` namespace and models."""

    @staticmethod
    @pytest.mark.parametrize("dbt_type_name", ["DbtProject", "DbtManifestData"])
    def test_dbt_types_are_flat_members_of_meltano_namespace(
        dbt_type_name: str,
    ) -> None:
        """DBT types are exposed flat (``Dbt`` prefix) directly on ``t.Meltano``."""
        assert hasattr(t.Meltano, dbt_type_name)
        tm.that(getattr(t.Meltano, dbt_type_name), none=False)

    @staticmethod
    @pytest.mark.parametrize(
        "composition_type_name",
        [
            "NestedStrMapping",
            "OptionalScalarMap",
            "ServicePayload",
            "ValidatorInput",
            "EnvironmentInput",
        ],
    )
    def test_composition_types_are_exposed_on_meltano_namespace(
        composition_type_name: str,
    ) -> None:
        """Composed types that add value over base ``t.*``.

        Exposed on ``t.Meltano``.
        """
        assert hasattr(t.Meltano, composition_type_name)

    @staticmethod
    def test_composition_types_are_distinct_symbols() -> None:
        """Each composed type is a distinct object, not a shared re-alias."""
        composed = {
            t.Meltano.NestedStrMapping,
            t.Meltano.OptionalScalarMap,
            t.Meltano.ServicePayload,
            t.Meltano.ValidatorInput,
            t.Meltano.EnvironmentInput,
        }
        tm.that(len(composed), eq=5)

    @staticmethod
    @pytest.mark.parametrize(
        "legacy_namespace",
        ["Singer", "Dbt", "Project", "Pipeline", "Bridge", "CLI", "ELT", "Processing"],
    )
    def test_legacy_nested_namespaces_are_absent(legacy_namespace: str) -> None:
        """Flat namespace refuses the old nested sub-namespaces."""
        assert not hasattr(t.Meltano, legacy_namespace)

    @staticmethod
    @pytest.mark.parametrize(
        "removed_alias",
        [
            "MeltanoConfigDict",
            "ExecutionResultDict",
            "ResultDict",
            "DbtResultDict",
            "PluginConfiguration",
            "PluginConfigDict",
            "JsonValue",
            "JsonMapping",
            "JsonMappingList",
            "PluginDefinition",
            "FileConfigDict",
            "CliProcessResult",
            "SingerCatalogEntry",
            "SingerStreamCatalog",
            "PluginCatalog",
        ],
    )
    def test_duplicate_aliases_are_absent(removed_alias: str) -> None:
        """Simple aliases duplicating existing ``t.*`` types.

        Not exposed on ``t.Meltano``.
        """
        assert not hasattr(t.Meltano, removed_alias)

    @staticmethod
    def test_jsonmapping_remains_a_top_level_type_alias() -> None:
        """``JsonMapping`` stays available at the top ``t.*`` level.

        Not exposed on ``t.Meltano``.
        """
        assert hasattr(t, "JsonMapping")
        assert not hasattr(t.Meltano, "JsonMapping")

    @staticmethod
    @pytest.mark.parametrize("wrapper_name", ["SingerProperty", "SingerStringType"])
    def test_runtime_singer_sdk_wrappers_live_on_models_not_typings(
        wrapper_name: str,
    ) -> None:
        """Runtime Singer SDK wrappers are exposed via ``m.Meltano``.

        Never on ``t.Meltano``.
        """
        tm.that(getattr(m.Meltano, wrapper_name), none=False)
        assert not hasattr(t.Meltano, wrapper_name)

    @staticmethod
    def test_singer_catalog_entry_is_exposed_as_domain_model() -> None:
        """The Singer catalog entry is exposed as a real model on ``m.Meltano``."""
        entry = m.Meltano.SingerCatalogEntry.model_validate({
            "tap_stream_id": "users",
            "stream": "users",
            "schema": {"type": "object"},
        })

        tm.that(m.Meltano.SingerCatalogEntry, is_=type)
        tm.that(entry.model_dump(), has="tap_stream_id")

    @staticmethod
    def test_singer_catalog_entry_constructs_and_exposes_public_state() -> None:
        """A valid Singer catalog entry constructs and exposes its fields publicly."""
        entry = m.Meltano.SingerCatalogEntry.model_validate({
            "tap_stream_id": "users",
            "stream": "users",
            "schema": {"type": "object"},
        })

        tm.that(entry.tap_stream_id, eq="users")
        tm.that(entry.stream, eq="users")

    @staticmethod
    def test_singer_catalog_entry_model_dump_round_trips() -> None:
        """``model_dump`` output re-validates to an equal public state (idempotence)."""
        entry = m.Meltano.SingerCatalogEntry.model_validate({
            "tap_stream_id": "orders",
            "stream": "orders",
            "schema": {"type": "object"},
        })

        dumped = entry.model_dump(by_alias=True)
        restored = m.Meltano.SingerCatalogEntry.model_validate(dumped)

        tm.that(restored.model_dump(by_alias=True), eq=dumped)
        tm.that(restored.tap_stream_id, eq=entry.tap_stream_id)

    @staticmethod
    def test_singer_catalog_entry_rejects_missing_required_fields() -> None:
        """Constructing without required fields raises a validation error."""
        with pytest.raises(m.ValidationError):
            m.Meltano.SingerCatalogEntry.model_validate({})
