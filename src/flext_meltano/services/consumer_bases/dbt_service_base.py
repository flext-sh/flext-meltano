"""Base service for FLEXT dbt consumer projects.

Provides dbt model/test execution and CLI dispatch via MRO. Consumer dbt
projects override ``connection_profile`` only.

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

import sys
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Annotated, override

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t
from flext_meltano.services import FlextMeltanoExecutor


class FlextMeltanoDbtServiceBase(FlextMeltanoServiceBase, ABC):
    """Base for all FLEXT dbt service projects.

    Subclasses MUST define:
    - ``dbt_project_name``: canonical dbt project name
    - ``connection_profile``: returns the typed dbt connection profile model

    This base provides via MRO:
    - dbt command execution (``run_models``, ``run_tests``, ``compile_models``)
    - Documentation generation
    - CLI dispatch
    """

    dbt_project_name: Annotated[
        t.NonEmptyStr,
        m.Field(description="Canonical dbt project name"),
    ] = c.Meltano.ServiceType.DBT

    _executor: p.Meltano.MeltanoExecutor = m.PrivateAttr(
        default_factory=FlextMeltanoExecutor,
    )

    def __init__(self, settings: p.Settings | None = None) -> None:
        """Expose the canonical settings bootstrap for dbt consumers."""
        super().__init__(runtime_settings=settings)

    @property
    @abstractmethod
    def connection_profile(self) -> p.Meltano.DbtConnectionProfile:
        """The typed dbt connection profile model for this project.

        Consumer returns its own domain ``m.<Ns>.DbtConnectionProfile`` model
        satisfying the protocol — a typed model, never a dict.
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def _dispatch_dbt_subcommand(
        self,
        subcommand: str,
        rest: list[str],
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Dispatch one resolved dbt subcommand to its typed service call.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        models: Sequence[str] | None = rest or None
        match subcommand:
            case c.Meltano.DbtCommand.RUN:
                return self.run_models(models)
            case c.Meltano.DbtCommand.TEST:
                return self.run_tests(models)
            case c.Meltano.DbtCommand.COMPILE:
                return self.compile_models(models)
            case c.Meltano.DbtCommand.DOCS:
                return self.generate_docs()
            case _:
                return r[m.Meltano.CommandExecutionResult].fail(subcommand)

    def _finalize_dbt_cli_result(
        self,
        subcommand: str,
        result: p.Result[m.Meltano.CommandExecutionResult],
    ) -> int:
        """Translate one dbt command result into the CLI exit contract.

        Returns:
            The resulting ``int``.

        Raises:
            SystemExit: If ``result.failure``.

        """
        if result.failure:
            self.logger.warning(
                "dbt command failed",
                subcommand=subcommand,
                error=result.error or "",
            )
            raise SystemExit(1)
        return 0

    def cli_main(self, args: Sequence[str] | None = None) -> int:
        """Run the main CLI entry point for dbt project.

        Returns:
            The resulting ``int``.

        Raises:
            SystemExit: If a ``c.EXC_OS_RUNTIME_TYPE`` is caught.

        """
        try:
            command_args = list(args) if args else sys.argv[1:]
            if not command_args:
                self.logger.info("dbt CLI: no arguments, showing help")
                return 0
            subcommand = command_args[0]
            result = self._dispatch_dbt_subcommand(subcommand, command_args[1:])
            return self._finalize_dbt_cli_result(subcommand, result)
        except c.EXC_OS_RUNTIME_TYPE as exc:
            self.logger.exception("dbt CLI failed", error=str(exc))
            raise SystemExit(1) from exc

    # ------------------------------------------------------------------
    # dbt command execution
    # ------------------------------------------------------------------

    def _run_dbt_cmd(
        self,
        subcommand: str,
        models: Sequence[str] | None = None,
        extra_args: Sequence[str] | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Execute a dbt command via the canonical typed executor (SSOT).

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        # NOTE (multi-agent, bead mro-wfc8.3.9): delegate to the single typed
        # executor (FlextMeltanoExecutorBase.execute_dbt_command) — no parallel
        # u.Cli.run_raw path, no str degradation. Returns CommandExecutionResult.
        args: list[str] = list(models) if models else []
        if extra_args:
            args.extend(extra_args)
        return self._executor.execute_dbt_command(subcommand, args or None)

    def run_models(
        self,
        models: Sequence[str] | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Run dbt models.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        return self._run_dbt_cmd(c.Meltano.DbtCommand.RUN, models=models)

    def run_tests(
        self,
        models: Sequence[str] | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Run dbt tests.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        return self._run_dbt_cmd(c.Meltano.DbtCommand.TEST, models=models)

    def compile_models(
        self,
        models: Sequence[str] | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Compile dbt models.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        return self._run_dbt_cmd(c.Meltano.DbtCommand.COMPILE, models=models)

    def generate_docs(self) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Generate dbt documentation.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        return self._run_dbt_cmd(
            c.Meltano.DbtCommand.DOCS,
            extra_args=list(c.Meltano.DBT_DEFAULT_DOCS_ARGS),
        )

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute dbt service — returns status.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        return r[t.JsonMapping].ok({
            "service": self.dbt_project_name,
            "status": "active",
            "type": c.Meltano.ServiceType.DBT,
        })


__all__: list[str] = ["FlextMeltanoDbtServiceBase"]
