"""Behavioral contract for Meltano service settings resolution.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_meltano import meltano, settings
from tests import tm

pytestmark = pytest.mark.unit


class TestsFlextMeltanoServiceSettingsContract:
    """Tests for the settings contract of ``FlextMeltanoServiceBase`` services."""

    @staticmethod
    def test_facade_settings_resolve_project_settings() -> None:
        """The public facade resolves the project settings type and SSOT values."""
        tm.that(meltano.settings_type, eq=type(settings))
        resolved = meltano.settings
        tm.that(resolved, is_=type(settings))
        tm.that(resolved.model_dump(), eq=settings.model_dump())
