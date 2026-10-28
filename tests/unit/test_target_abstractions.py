"""Behavioral tests for the public target factory of FlextMeltano.

Exercises only the observable contract of the flat ``meltano`` facade's
``target`` factory — asserting returned ``r[T]`` outcomes and public model
state, never private attributes or internal collaborators.

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

import pytest

from tests import meltano, tm


class TestsFlextMeltanoTargetAbstractions:
    """Validate target-related behavior through the current public facade."""

    @staticmethod
    def test_target_factory_binds_sink_name_and_leaves_other_roles_unset() -> None:
        """target() returns a success bound to the sink name, source/xform unset."""
        result = meltano.target("target-jsonl")

        tm.ok(result)
        service = result.value
        tm.that(service.sink_name, eq="target-jsonl")
        tm.that(service.source_name, none=True)
        tm.that(service.transformation_name, none=True)

    @staticmethod
    @pytest.mark.parametrize(
        "sink_name",
        ["target-jsonl", "target-postgres", "target-snowflake"],
    )
    def test_target_factory_echoes_requested_sink_name(sink_name: str) -> None:
        """target() binds exactly the requested sink name for any target kind."""
        result = meltano.target(sink_name)

        tm.ok(result)
        tm.that(result.value.sink_name, eq=sink_name)
