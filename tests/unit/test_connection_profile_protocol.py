"""Behavior contract for the canonical dbt connection profile protocol.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import m, p, u


class _Profile(m.Value):
    type: str = u.Field(description="Dbt adapter type")
    project: str = u.Field(description="Dbt project name")


def _accept_profile(
    profile: p.Meltano.DbtConnectionProfile,
) -> p.Meltano.DbtConnectionProfile:
    return profile


def test_dbt_connection_profile_accepts_typed_serializable_model() -> None:
    """Test dbt connection profile accepts typed serializable model."""
    profile = _Profile(type="test", project="dbt-test")

    accepted = _accept_profile(profile)

    assert accepted.model_dump() == {"type": "test", "project": "dbt-test"}
