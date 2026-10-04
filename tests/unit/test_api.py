"""Behavioral tests for the public Meltano facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest
from flext_tests import tm

from flext_meltano import meltano
from tests import c

pytestmark = pytest.mark.unit


class TestsFlextMeltanoApi:
    """Behavioral test suite for the public Meltano facade."""

    @staticmethod
    def test_public_facade_contract() -> None:
        """The public singleton stays callable and stable."""
        tm.that(type(meltano).fetch_global() is meltano, eq=True)
        tm.that(callable(meltano.tap), eq=True)
        tm.that(callable(meltano.target), eq=True)
        tm.that(callable(meltano.dbt), eq=True)
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
    def test_create_project_rejects_empty_name(tmp_path: Path) -> None:
        """Project creation fails fast on invalid input."""
        tm.fail(
            meltano.create_project(project_name="", project_dir=tmp_path),
            has="empty",
        )

    @staticmethod
    def test_create_project_writes_meltano_project_file(tmp_path: Path) -> None:
        """Project creation persists the canonical Meltano project file."""
        result = meltano.create_project(
            project_name="config_test",
            project_dir=tmp_path,
        )
        tm.that(result, ok=True)
        tm.ok(result)
        payload = result.value
        tm.that(payload, is_=dict)
        project_path = Path(payload["project_path"])
        tm.that((project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE).exists(), eq=True)
        config_text = (project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE).read_text(
            encoding="utf-8",
        )
        tm.that(config_text, has="requires_meltano")
        tm.that("version:" in config_text, eq=False)

    @staticmethod
    def test_validate_project_missing_path_fails(tmp_path: Path) -> None:
        """Validation fails on a missing project path."""
        error = tm.fail(meltano.validate_project(tmp_path / "missing"))
        tm.that(error.lower(), has=["project"])

    @staticmethod
    def test_install_component_rejects_invalid_type() -> None:
        """Component installation enforces canonical Meltano component types."""
        error = tm.fail(
            meltano.install_component(
                component_type="invalid_type",
                component_name="tap-csv",
            ),
        )
        tm.that(error.lower(), has=["invalid"])

    @staticmethod
    def test_discover_plugins_requires_active_project() -> None:
        """Plugin discovery fails clearly without an active Meltano project."""
        error = tm.fail(meltano.discover_plugins())
        tm.that(error.lower(), has=["project"])

    @staticmethod
    def test_create_project_failure_path_returns_meaningful_error() -> None:
        """The public API keeps failure reporting concrete on invalid paths."""
        error = tm.fail(
            meltano.create_project(
                project_name="test",
                project_dir=Path("/nonexistent/impossible/path/that/cannot/exist"),
            ),
        )
        tm.that(error.lower(), match=r"(failed|permission|not found|project creation)")
