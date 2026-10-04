"""FLEXT Meltano Singer Types Tests - behavioral contract of the type namespace.

Asserts the OBSERVABLE public contract of the Meltano Singer typing surface
exposed through ``t`` (``TestsFlextMeltanoTypes``): MRO composition of the
Singer surface, the exposed ``t.Meltano`` type aliases, their resolved values,
and stable/idempotent access. No private access, no mocks, no I/O.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import FlextTestsTypes, tm

from flext_meltano import FlextMeltanoTypes
from tests import TestsFlextMeltanoTypes, t

# (alias name, resolved __value__ repr fragment) — real public contract table.
_MELTANO_TYPE_ALIASES: tuple[tuple[str, str], ...] = (
    ("DbtManifestData", "JsonMapping"),
    ("DbtProject", "JsonMapping"),
    ("EnvironmentInput", "Environment"),
    ("NestedStrMapping", "Mapping"),
    ("OptionalScalarMap", "Scalar"),
    ("ServicePayload", "JsonMapping"),
    ("ValidatorInput", "JsonValue"),
)


class TestsFlextMeltanoSingerTypes:
    """Behavioral contract for the Meltano Singer typing namespace."""

    @staticmethod
    def test_t_is_the_public_tests_meltano_types_facade() -> None:
        """``t`` exported from tests.typings IS the test types facade class."""
        assert t is TestsFlextMeltanoTypes

    @staticmethod
    def test_facade_composes_meltano_and_tests_type_surfaces() -> None:
        """The facade composes both the Meltano and flext-tests type systems."""
        assert FlextMeltanoTypes in t.__mro__
        assert FlextTestsTypes in t.__mro__

    @staticmethod
    def test_meltano_namespace_composes_singer_surface() -> None:
        """Documented contract: Singer typing surface is composed into t.Meltano."""
        assert hasattr(t.Meltano, "SingerArrayType")
        assert hasattr(t.Meltano, "SingerBooleanType")
        assert hasattr(t.Meltano, "SingerPropertiesList")

    @staticmethod
    def test_meltano_namespace_exposes_tests_subnamespace() -> None:
        """Meltano namespace exposes the nested Tests type namespace."""
        assert hasattr(t.Meltano, "Tests")
        assert issubclass(t.Meltano.Tests, FlextTestsTypes.Tests)

    @staticmethod
    @pytest.mark.parametrize("alias_name", [n for n, _ in _MELTANO_TYPE_ALIASES])
    def test_meltano_exposes_public_type_alias(alias_name: str) -> None:
        """Each documented Singer/Meltano type alias is publicly reachable."""
        assert hasattr(t.Meltano, alias_name)

    @staticmethod
    @pytest.mark.parametrize(("alias_name", "value_fragment"), _MELTANO_TYPE_ALIASES)
    def test_type_alias_resolves_to_expected_value(
        alias_name: str,
        value_fragment: str,
    ) -> None:
        """Each type alias is a PEP 695 alias resolving to its contracted target."""
        alias = getattr(t.Meltano, alias_name)
        tm.that(hasattr(alias, "__value__"), eq=True)
        tm.that(str(alias.__value__), has=value_fragment)

    @staticmethod
    @pytest.mark.parametrize("alias_name", [n for n, _ in _MELTANO_TYPE_ALIASES])
    def test_type_alias_access_is_idempotent(alias_name: str) -> None:
        """Repeated access yields the same stable alias object (no rebuild)."""
        assert getattr(t.Meltano, alias_name) is getattr(t.Meltano, alias_name)
