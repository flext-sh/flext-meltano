"""Behavior contract for the canonical dbt connection profile protocol.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import m, p, u


class TestsFlextMeltanoProfileModel(m.Value):
    """Tests for ``FlextMeltanoProfile``."""

    type: str = u.Field(description="Dbt adapter type")
    project: str = u.Field(description="Dbt project name")


class TestsFlextMeltanoDbtConnectionProfile:
    """Behavior contract of ``p.Meltano.DbtConnectionProfile``."""

    @staticmethod
    def _accept_profile(
        profile: p.Meltano.DbtConnectionProfile,
    ) -> p.Meltano.DbtConnectionProfile:
        """Accept one typed profile through the protocol boundary.

        Returns:
            The resulting ``p.Meltano.DbtConnectionProfile``.
        """
        return profile

    @staticmethod
    def test_dbt_connection_profile_accepts_typed_serializable_model() -> None:
        """Test dbt connection profile accepts typed serializable model."""
        profile = TestsFlextMeltanoProfileModel(type="test", project="dbt-test")

        accepted = TestsFlextMeltanoDbtConnectionProfile._accept_profile(profile)

        assert accepted.model_dump() == {"type": "test", "project": "dbt-test"}
