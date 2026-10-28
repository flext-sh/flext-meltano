"""FLEXT Meltano Singer Types Tests - behavioral contract of the type namespace.

Asserts the OBSERVABLE public contract of the Meltano Singer typing surface
exposed through ``t`` (``TestsFlextMeltanoTypes``): the exposed ``t.Meltano``
type aliases, their resolved values, and stable/idempotent access.
No private access, no mocks, no I/O.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from tests import TestsFlextMeltanoTypes, t, tm


class TestsFlextMeltanoTypesSinger:
    """Behavioral contract for the Meltano Singer typing namespace."""

    # (alias name, resolved __value__ repr fragment) — real public contract table.
    _MELTANO_TYPE_ALIASES: tuple[tuple[str, str], ...] = (
        ("DbtProject", "JsonMapping"),
        ("NestedStrMapping", "Mapping"),
        ("ValidatorInput", "JsonValue"),
    )

    @staticmethod
    def test_t_is_the_public_tests_meltano_types_facade() -> None:
        """``t`` exported from tests.typings IS the test types facade class."""
        tm.that(t is TestsFlextMeltanoTypes, truth=True)

    @staticmethod
    def test_meltano_namespace_composes_singer_surface() -> None:
        """Singer schema alias is composed into t.Meltano; SDK wrappers live on m."""
        tm.that(hasattr(t.Meltano, "SingerSchema"), truth=True)
        tm.that(not hasattr(t.Meltano, "SingerArrayType"), truth=True)

    @staticmethod
    def test_meltano_namespace_exposes_tests_subnamespace() -> None:
        """Meltano namespace exposes the nested Tests type namespace."""
        tm.that(hasattr(t.Meltano, "Tests"), truth=True)

    @staticmethod
    @pytest.mark.parametrize("alias_name", [n for n, _ in _MELTANO_TYPE_ALIASES])
    def test_meltano_exposes_public_type_alias(alias_name: str) -> None:
        """Each documented Singer/Meltano type alias is publicly reachable."""
        tm.that(hasattr(t.Meltano, alias_name), truth=True)

    @staticmethod
    @pytest.mark.parametrize(("alias_name", "value_fragment"), _MELTANO_TYPE_ALIASES)
    def test_type_alias_resolves_to_expected_value(
        alias_name: str,
        value_fragment: str,
    ) -> None:
        """Each type alias is a PEP 695 alias resolving to its contracted target."""
        alias = getattr(t.Meltano, alias_name)
        tm.ok(hasattr(alias, "__value__"))
        tm.that(str(alias.__value__), has=value_fragment)

    @staticmethod
    @pytest.mark.parametrize("alias_name", [n for n, _ in _MELTANO_TYPE_ALIASES])
    def test_type_alias_access_is_idempotent(alias_name: str) -> None:
        """Repeated access yields the same stable alias object (no rebuild)."""
        tm.that(
            getattr(t.Meltano, alias_name) is getattr(t.Meltano, alias_name),
            truth=True,
        )
