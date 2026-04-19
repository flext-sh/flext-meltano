"""DBT Runner — MRO mixin for FlextMeltano facade.

Programmatic DBT execution via subprocess. Implements actual dbt
command execution (replaces previous stubs).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence
from pathlib import Path

from flext_meltano import FlextMeltanoServiceBase, p, r, t, u


class FlextMeltanoDbtRunnerMixin(FlextMeltanoServiceBase):
    """DBT command execution mixin for MRO composition on FlextMeltano.

    Runs dbt commands via subprocess with proper error handling.
    """

    _dbt_runner_project_root: Path | None = u.PrivateAttr(default_factory=lambda: None)

    def _build_dbt_command(
        self,
        subcommand: str,
        models: t.StrSequence | None = None,
        extra_args: t.StrSequence | None = None,
    ) -> MutableSequence[str]:
        """Build dbt CLI command with standard arguments."""
        cmd: MutableSequence[str] = ["dbt", subcommand]
        if self._dbt_runner_project_root:
            cmd.extend(["--projects-dir", str(self._dbt_runner_project_root)])
        if models:
            cmd.extend(["--models", *models])
        if extra_args:
            cmd.extend(extra_args)
        return cmd

    def _run_dbt_subprocess(
        self,
        cmd: MutableSequence[str],
        operation: str,
    ) -> p.Result[str]:
        """Execute a dbt command via subprocess."""
        try:
            self.logger.info(
                "Running dbt operation",
                operation=operation,
                command=" ".join(cmd),
            )
            result = u.Cli.run_raw(list(cmd))
            if result.failure:
                return r[str].fail(result.error or f"dbt {operation} failed")
            out = result.value
            if out.exit_code != 0:
                stderr_msg = out.stderr or f"dbt {operation} failed"
                self.logger.warning(
                    "dbt operation returned non-zero exit code",
                    operation=operation,
                    exit_code=out.exit_code,
                    stderr=stderr_msg,
                )
                return r[str].fail(stderr_msg)
            self.logger.info("dbt operation completed", operation=operation)
            return r[str].ok(out.stdout)
        except (
            ValueError,
            TypeError,
            OSError,
            RuntimeError,
        ) as e:
            self.logger.exception(
                "dbt operation failed", operation=operation, error=str(e)
            )
            return r[str].fail(f"dbt {operation} failed: {e}")

    def dbt_run_models(
        self,
        models: t.StrSequence | None = None,
    ) -> p.Result[str]:
        """Run dbt models via subprocess."""
        cmd = self._build_dbt_command("run", models=models)
        return self._run_dbt_subprocess(cmd, "run")

    def dbt_run_tests(
        self,
        models: t.StrSequence | None = None,
    ) -> p.Result[str]:
        """Run dbt tests via subprocess."""
        cmd = self._build_dbt_command("test", models=models)
        return self._run_dbt_subprocess(cmd, "test")

    def dbt_compile(
        self,
        models: t.StrSequence | None = None,
    ) -> p.Result[str]:
        """Compile dbt models via subprocess."""
        cmd = self._build_dbt_command("compile", models=models)
        return self._run_dbt_subprocess(cmd, "compile")

    def dbt_docs_generate(self) -> p.Result[str]:
        """Generate dbt documentation via subprocess."""
        cmd = self._build_dbt_command("docs", extra_args=["generate"])
        return self._run_dbt_subprocess(cmd, "docs generate")

    def configure_dbt_project_root(self, root: Path) -> None:
        """Set the dbt project root directory."""
        self._dbt_runner_project_root = root


__all__: list[str] = ["FlextMeltanoDbtRunnerMixin"]
