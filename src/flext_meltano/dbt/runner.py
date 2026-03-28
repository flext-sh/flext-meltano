"""DBT Runner - Programmatic DBT execution integration.

This module provides programmatic DBT execution with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import r, s

from flext_meltano import t


class FlextMeltanoDbtRunner(s[str]):
    """Executes DBT commands programmatically.

    Attributes:
    project_root: Root directory of DBT project

    """

    def __init__(self, project_root: Path | None = None) -> None:
        """Initialize DBT runner.

        Args:
        project_root: Root directory of DBT project (optional)

        """
        super().__init__()
        self.project_root: Path | None = project_root

    def docs_generate(self, **_kwargs: t.Scalar) -> None:
        """Generate DBT documentation.

        Raises:
        NotImplementedError: Requires dbt-core programmatic API or subprocess integration.

        """
        msg = "DBT docs generate: requires dbt-core programmatic API or subprocess integration"
        raise NotImplementedError(msg)

    @override
    def execute(self, **_kwargs: t.Scalar) -> r[str]:
        """Execute (implements Service pattern)."""
        if self.project_root:
            return r[str].ok(f"DBT runner: {self.project_root}")
        return r[str].fail("No project root set")

    def run_models(
        self,
        models: t.StrSequence | None = None,
        **_kwargs: t.Scalar,
    ) -> None:
        """Run DBT models.

        Raises:
        NotImplementedError: Requires dbt-core programmatic API or subprocess integration.

        """
        msg = "DBT run models: requires dbt-core programmatic API or subprocess integration"
        raise NotImplementedError(msg)

    def run_tests(
        self,
        models: t.StrSequence | None = None,
        **_kwargs: t.Scalar,
    ) -> None:
        """Run DBT tests.

        Raises:
        NotImplementedError: Requires dbt-core programmatic API or subprocess integration.

        """
        msg = "DBT run tests: requires dbt-core programmatic API or subprocess integration"
        raise NotImplementedError(msg)


__all__ = ["FlextMeltanoDbtRunner"]
