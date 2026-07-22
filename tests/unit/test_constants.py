"""Behavioral tests for the c.Meltano constants contract.

Asserts the OBSERVABLE public values and invariants promised by
c.Meltano (versions, metadata, Singer/DBT identifiers, plugin
types, validation thresholds, logging defaults) rather than any
implementation detail. Constants are a value contract: the public
promise is the exact value and its invariants (type, non-emptiness,
enum membership, immutability).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum

import pytest

from flext_tests import tm
from tests import c

__all__: list[str] = ["TestsFlextMeltanoConstantsUnit"]


class TestsFlextMeltanoConstantsUnit:
    """Public-contract test suite for c.Meltano constants."""

    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            ("FLEXT_MELTANO_VERSION", "0.9.0"),
            ("METADATA_APPLICATION_NAME", "flext-pipeline"),
            (
                "METADATA_APPLICATION_DESCRIPTION",
                "FLEXT Generic Data Pipeline Framework",
            ),
            ("PATH_PROJECT_FILE", "meltano.yml"),
            ("PATH_STATE_DIR", ".pipeline"),
            ("SDK_VERSION_REQUIRED", "0.48.0"),
            ("DEFAULT_VARIANT", "meltano"),
            ("LOGGING_DEFAULT_LEVEL", "INFO"),
        ],
    )
    def test_string_constant_exposes_expected_value(
        self, name: str, expected: str
    ) -> None:
        """String constants expose their exact documented public value."""
        tm.that(getattr(c.Meltano, name), eq=expected)

    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            ("SINGER_MESSAGE_TYPE_SCHEMA", "SCHEMA"),
            ("SINGER_MESSAGE_TYPE_RECORD", "RECORD"),
            ("DBT_PROJECT_FILE", "dbt_project.yml"),
            ("DBT_COMMAND_RUN", "run"),
            ("DBT_COMMAND_TEST", "test"),
        ],
    )
    def test_enum_backed_constant_compares_as_its_string_value(
        self, name: str, expected: str
    ) -> None:
        """Enum-backed identifiers behave as their StrEnum string value."""
        value = getattr(c.Meltano, name)
        tm.that(value, is_=StrEnum)
        tm.that(value, eq=expected)
        tm.that(str(value), eq=expected)

    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            ("SERVICE_MIN_NAME_LENGTH", 3),
            ("VALIDATION_MATURITY_MATURE_ENV_COUNT", 3),
            ("VALIDATION_MATURITY_DEVELOPING_ENV_COUNT", 2),
            ("VALIDATION_COMPLEXITY_MINIMAL_SETTINGS", 0),
            ("VALIDATION_COMPLEXITY_SIMPLE_MAX_SETTINGS", 5),
        ],
    )
    def test_integer_threshold_exposes_expected_value(
        self, name: str, expected: int
    ) -> None:
        """Numeric thresholds expose their exact documented value."""
        tm.that(getattr(c.Meltano, name), eq=expected)

    @pytest.mark.parametrize(
        ("name", "value"),
        [
            ("LOGGING_INCLUDE_TRANSFORM_NAME", True),
            ("LOGGING_INCLUDE_RECORD_COUNT", True),
        ],
    )
    def test_logging_flag_exposes_expected_value(self, name: str, value: bool) -> None:
        """Logging feature flags expose their documented boolean default."""
        assert getattr(c.Meltano, name) is value

    def test_maturity_thresholds_are_strictly_ordered(self) -> None:
        """Mature environments require strictly more envs than developing."""
        assert (
            c.Meltano.VALIDATION_MATURITY_MATURE_ENV_COUNT
            > c.Meltano.VALIDATION_MATURITY_DEVELOPING_ENV_COUNT
        )

    def test_complexity_thresholds_are_ordered(self) -> None:
        """Simple-max setting count is above the minimal-settings floor."""
        assert (
            c.Meltano.VALIDATION_COMPLEXITY_SIMPLE_MAX_SETTINGS
            > c.Meltano.VALIDATION_COMPLEXITY_MINIMAL_SETTINGS
        )

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
        self, member: str, expected: str
    ) -> None:
        """Each PluginType member maps to its documented plugin folder name."""
        value = getattr(c.Meltano.PluginType, member)
        tm.that(value, is_=StrEnum)
        tm.that(value, eq=expected)

    def test_plugin_type_members_are_unique(self) -> None:
        """PluginType values form a distinct, collision-free set."""
        values = [member.value for member in c.Meltano.PluginType]
        tm.that(len(values), eq=len(set(values)))

    def test_default_variant_is_a_known_reference(self) -> None:
        """DEFAULT_VARIANT is a non-empty identifier callers can rely on."""
        assert c.Meltano.DEFAULT_VARIANT
        tm.that(c.Meltano.DEFAULT_VARIANT.strip(), eq=c.Meltano.DEFAULT_VARIANT)

    def test_singer_schema_and_record_are_distinct(self) -> None:
        """Schema and record message identifiers are not interchangeable."""
        assert (
            c.Meltano.SINGER_MESSAGE_TYPE_SCHEMA != c.Meltano.SINGER_MESSAGE_TYPE_RECORD
        )

    def test_dbt_run_and_test_commands_are_distinct(self) -> None:
        """DBT run and test commands resolve to different invocations."""
        tm.that(c.Meltano.DBT_COMMAND_RUN, ne=c.Meltano.DBT_COMMAND_TEST)

    def test_plugin_type_enum_is_immutable(self) -> None:
        """PluginType members cannot be reassigned through the public enum."""
        with pytest.raises((AttributeError, TypeError)):
            setattr(c.Meltano.PluginType, "EXTRACTORS", "mutated")
