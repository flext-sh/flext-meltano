"""Behavioral tests for the c.Meltano constants contract.

Asserts the OBSERVABLE public invariants promised by the c.Meltano plugin
type enumeration (enum membership, uniqueness, immutability) rather than any
implementation detail.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum

import pytest

from tests import c, tm


class TestsFlextMeltanoConstantsUnit:
    """Public-contract test suite for c.Meltano constants."""

    @staticmethod
    @pytest.mark.parametrize(
        ("member", "expected"),
        [
            ("EXTRACTORS", "extractors"),
            ("LOADERS", "loaders"),
            ("TRANSFORMS", "transforms"),
            ("ORCHESTRATORS", "orchestrators"),
        ],
    )
    def test_plugin_type_member_exposes_expected_value(
        member: str,
        expected: str,
    ) -> None:
        """Each PluginType member maps to its documented plugin folder name."""
        value = getattr(c.Meltano.PluginType, member)
        tm.that(value, is_=StrEnum)
        tm.that(value, eq=expected)

    @staticmethod
    def test_plugin_type_members_are_unique() -> None:
        """PluginType values form a distinct, collision-free set."""
        values = [member.value for member in c.Meltano.PluginType]
        tm.that(len(values), eq=len(set(values)))

    @staticmethod
    def test_plugin_type_enum_is_immutable() -> None:
        """PluginType members cannot be reassigned through the public enum."""
        tm.rejects_assignment(
            c.Meltano.PluginType,
            "EXTRACTORS",
            "mutated",
            expected=(AttributeError, TypeError),
        )
