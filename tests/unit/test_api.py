"""Behavioral tests for the public Meltano facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_meltano import meltano
from tests import tm


class TestsFlextMeltanoApi:
    """Behavioral test suite for the public Meltano facade."""

    pytestmark = pytest.mark.unit

    @staticmethod
    def test_public_facade_contract() -> None:
        """The public singleton stays callable and stable."""
        tm.ok(type(meltano).fetch_global() is meltano)
        tm.ok(callable(meltano.tap))
        tm.ok(callable(meltano.target))
        tm.ok(callable(meltano.dbt))
        tm.that(meltano.service_name, none=False, empty=False)

    @staticmethod
    def test_execute_returns_success_payload(meltano_execute_field: str) -> None:
        """The public execute payload exposes the canonical fields."""
        result = meltano.execute()
        tm.ok(result)
        tm.ok(result)
        payload = result.value
        tm.that(payload, is_=dict)
        tm.that(payload, contains=meltano_execute_field)

    @staticmethod
    def test_discover_plugins_requires_active_project() -> None:
        """Plugin discovery fails clearly without an active Meltano project."""
        error = tm.fail(meltano.discover_plugins())
        tm.that(error.lower(), has=["project"])
