"""DBT Orchestration — MRO mixin for FlextMeltano facade.

High-level dbt lifecycle coordination using project and runner mixins
available via MRO on the facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, m, t


class FlextMeltanoDbtOrchestrationMixin(FlextMeltanoServiceBase):
    """DBT orchestration mixin for MRO composition on FlextMeltano.

    Coordinates dbt operations using project and runner methods
    provided by sibling mixins via MRO:
    - ``load_dbt_project``, ``get_dbt_models`` from ``FlextMeltanoDbtProjectMixin``
    - ``dbt_run_models``, ``dbt_run_tests`` from ``FlextMeltanoDbtRunnerMixin``
    """

    def orchestrate_dbt_load_project(self, root: Path) -> r[m.Meltano.DbtProjectInfo]:
        """Load a DBT project and set runner project root.

        Delegates to ``self.load_dbt_project()`` (from ProjectMixin)
        and ``self.set_dbt_project_root()`` (from RunnerMixin).
        """
        try:
            self.logger.info("Loading DBT project", root=str(root))
            result = self.load_dbt_project(root)  # type: ignore[attr-defined]
            if result.is_success:
                self.set_dbt_project_root(root)  # type: ignore[attr-defined]
                self.logger.info("DBT project loaded")
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return r[m.Meltano.DbtProjectInfo].fail(f"Failed to load DBT project: {e}")

    def orchestrate_dbt_get_models(
        self,
    ) -> r[Sequence[t.Meltano.Dbt.ModelConfiguration]]:
        """Get all models from the loaded project.

        Delegates to ``self.get_dbt_models()`` (from ProjectMixin).
        """
        try:
            self.logger.info("Retrieving DBT models")
            result = self.get_dbt_models()  # type: ignore[attr-defined]
            if result.is_success:
                models = result.value
                self.logger.info("DBT models retrieved", count=len(models))
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:
            self.logger.exception("Failed to get models", error=str(e))
            return r[Sequence[t.Meltano.Dbt.ModelConfiguration]].fail(
                f"Failed to get models: {e}",
            )

    def orchestrate_dbt_run(
        self,
        models: t.StrSequence | None = None,
    ) -> r[str]:
        """Run DBT models.

        Delegates to ``self.dbt_run_models()`` (from RunnerMixin).
        """
        return self.dbt_run_models(models)  # type: ignore[attr-defined]

    def orchestrate_dbt_test(
        self,
        models: t.StrSequence | None = None,
    ) -> r[str]:
        """Run DBT tests.

        Delegates to ``self.dbt_run_tests()`` (from RunnerMixin).
        """
        return self.dbt_run_tests(models)  # type: ignore[attr-defined]

    def orchestrate_dbt_docs(self) -> r[str]:
        """Generate DBT documentation.

        Delegates to ``self.dbt_docs_generate()`` (from RunnerMixin).
        """
        return self.dbt_docs_generate()  # type: ignore[attr-defined]


__all__ = ["FlextMeltanoDbtOrchestrationMixin"]
