"""Behavioral tests for the public Meltano facade."""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_meltano import meltano
from tests import c, u

pytestmark = pytest.mark.unit


class TestsFlextMeltanoApi:
    """Behavioral test suite for the public Meltano facade."""

    def test_public_facade_contract(self) -> None:
        """The public singleton stays callable and stable."""
        u.Tests.Matchers.that(type(meltano).fetch_instance() is meltano, eq=True)
        u.Tests.Matchers.that(callable(meltano.Tap), eq=True)
        u.Tests.Matchers.that(callable(meltano.Target), eq=True)
        u.Tests.Matchers.that(callable(meltano.Dbt), eq=True)
        u.Tests.Matchers.that(meltano.service_name, none=False, empty=False)

    def test_execute_returns_success_payload(
        self,
        meltano_execute_field: str,
    ) -> None:
        """The public execute payload exposes the canonical fields."""
        payload = u.Tests.Matchers.ok(meltano.execute(), is_=dict)
        u.Tests.Matchers.that(payload, contains=meltano_execute_field)

    def test_create_project_rejects_empty_name(
        self,
        tmp_path: Path,
    ) -> None:
        """Project creation fails fast on invalid input."""
        u.Tests.Matchers.fail(
            meltano.create_project(project_name="", project_dir=tmp_path),
            has="empty",
        )

    def test_create_project_writes_meltano_project_file(
        self,
        tmp_path: Path,
    ) -> None:
        """Project creation persists the canonical Meltano project file."""
        result = meltano.create_project(
            project_name="config_test", project_dir=tmp_path
        )
        u.Tests.Matchers.that(result, ok=True)
        assert result.success
        payload = result.value
        u.Tests.Matchers.that(payload, is_=dict)
        project_path = Path(str(payload["project_path"]))
        u.Tests.Matchers.that(
            (project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE).exists(),
            eq=True,
        )

    def test_validate_project_missing_path_fails(
        self,
        tmp_path: Path,
    ) -> None:
        """Validation fails on a missing project path."""
        error = u.Tests.Matchers.fail(meltano.validate_project(tmp_path / "missing"))
        u.Tests.Matchers.that(error.lower(), has=["project"])

    def test_install_component_rejects_invalid_type(self) -> None:
        """Component installation enforces canonical Meltano component types."""
        error = u.Tests.Matchers.fail(
            meltano.install_component(
                component_type="invalid_type",
                component_name="tap-csv",
            )
        )
        u.Tests.Matchers.that(error.lower(), has=["invalid"])

    def test_discover_plugins_requires_active_project(self) -> None:
        """Plugin discovery fails clearly without an active Meltano project."""
        error = u.Tests.Matchers.fail(meltano.discover_plugins())
        u.Tests.Matchers.that(error.lower(), has=["project"])

    def test_create_project_failure_path_returns_meaningful_error(self) -> None:
        """The public API keeps failure reporting concrete on invalid paths."""
        error = u.Tests.Matchers.fail(
            meltano.create_project(
                project_name="test",
                project_dir=Path("/nonexistent/impossible/path/that/cannot/exist"),
            )
        )
        u.Tests.Matchers.that(
            error.lower(),
            match=r"(failed|permission|not found|project creation)",
        )
