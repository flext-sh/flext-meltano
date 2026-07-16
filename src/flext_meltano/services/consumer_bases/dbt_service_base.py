"""Base service for FLEXT dbt consumer projects.

Provides dbt project management, model/test execution, manifest parsing,
and CLI dispatch via MRO. Consumer dbt projects override
``connection_profile`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Annotated, override

from flext_meltano import (
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    m,
    p,
    r,
    t,
    u,
)
from flext_meltano.services.executor import FlextMeltanoExecutor


class FlextMeltanoDbtServiceBase(FlextMeltanoServiceBase, ABC):
    """Base for all FLEXT dbt service projects.

    Subclasses MUST define:
    - ``dbt_project_name``: canonical dbt project name
    - ``connection_profile``: returns the typed dbt connection profile model

    This base provides via MRO:
    - dbt command execution (``run_models``, ``run_tests``, ``compile_models``)
    - Manifest parsing and model/test discovery
    - Documentation generation
    - CLI dispatch
    - Singleton accessor (``get_instance``)
    """

    dbt_project_name: Annotated[
        t.NonEmptyStr,
        u.Field(description="Canonical dbt project name"),
    ] = c.Meltano.ServiceType.DBT

    _dbt_project_root: Path | None = u.PrivateAttr(default_factory=lambda: None)
    _executor: p.Meltano.MeltanoExecutor = u.PrivateAttr(
        default_factory=FlextMeltanoExecutor,
    )

    def __init__(
        self,
        settings: FlextMeltanoSettings | None = None,
    ) -> None:
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

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Run the main CLI entry point for dbt project."""

        def _run_cli_main() -> int:
            command_args = list(args) if args else sys.argv[1:]
            if not command_args:
                self.logger.info("dbt CLI: no arguments, showing help")
                return 0
            subcommand = command_args[0]
            match subcommand:
                case c.Meltano.DbtCommand.RUN:
                    models = command_args[1:] if len(command_args) > 1 else None
                    result = self.run_models(models)
                case c.Meltano.DbtCommand.TEST:
                    models = command_args[1:] if len(command_args) > 1 else None
                    result = self.run_tests(models)
                case c.Meltano.DbtCommand.COMPILE:
                    models = command_args[1:] if len(command_args) > 1 else None
                    result = self.compile_models(models)
                case c.Meltano.DbtCommand.DOCS:
                    result = self.generate_docs()
                case _:
                    result = r[p.Meltano.CommandExecutionResult].fail(subcommand)
            if result.failure:
                self.logger.warning(
                    "dbt command failed",
                    subcommand=subcommand,
                    error=result.error or "",
                )
                return 1
            return 0

        try:
            return _run_cli_main()
        except c.EXC_OS_RUNTIME_TYPE as exc:
            self.logger.exception("dbt CLI failed", error=str(exc))
            return 1

    # ------------------------------------------------------------------
    # dbt command execution
    # ------------------------------------------------------------------

    def _run_dbt_cmd(
        self,
        subcommand: str,
        models: t.StrSequence | None = None,
        extra_args: t.StrSequence | None = None,
    ) -> p.Result[p.Meltano.CommandExecutionResult]:
        """Execute a dbt command via the canonical typed executor (SSOT)."""
        # NOTE (multi-agent, bead mro-wfc8.3.9): delegate to the single typed
        # executor (FlextMeltanoExecutorBase.execute_dbt_command) — no parallel
        # u.Cli.run_raw path, no str degradation. Returns CommandExecutionResult.
        args: list[str] = list(models) if models else []
        if extra_args:
            args.extend(extra_args)
        return self._executor.execute_dbt_command(subcommand, args or None)

    def run_models(
        self,
        models: t.StrSequence | None = None,
    ) -> p.Result[p.Meltano.CommandExecutionResult]:
        """Run dbt models."""
        return self._run_dbt_cmd(c.Meltano.DbtCommand.RUN, models=models)

    def run_tests(
        self,
        models: t.StrSequence | None = None,
    ) -> p.Result[p.Meltano.CommandExecutionResult]:
        """Run dbt tests."""
        return self._run_dbt_cmd(c.Meltano.DbtCommand.TEST, models=models)

    def compile_models(
        self,
        models: t.StrSequence | None = None,
    ) -> p.Result[p.Meltano.CommandExecutionResult]:
        """Compile dbt models."""
        return self._run_dbt_cmd(c.Meltano.DbtCommand.COMPILE, models=models)

    def generate_docs(self) -> p.Result[p.Meltano.CommandExecutionResult]:
        """Generate dbt documentation."""
        return self._run_dbt_cmd(
            c.Meltano.DbtCommand.DOCS,
            extra_args=list(c.Meltano.DBT_DEFAULT_DOCS_ARGS),
        )

    # ------------------------------------------------------------------
    # Project management
    # ------------------------------------------------------------------

    def configure_project_root(self, root: Path) -> p.Result[None]:
        """Set dbt project root directory."""
        if not root.exists():
            return r[None].fail(str(root))
        self._dbt_project_root = root
        return r[None].ok(None)

    def load_manifest(
        self,
        manifest_path: Path | None = None,
    ) -> p.Result[t.Meltano.DbtManifestData]:
        """Load dbt manifest.json."""

        def _run_load_manifest() -> p.Result[t.Meltano.DbtManifestData]:
            path = manifest_path
            if path is None:
                if self._dbt_project_root is None:
                    return r[t.Meltano.DbtManifestData].fail("No project root set")
                path = (
                    self._dbt_project_root
                    / c.Meltano.FILE_PATH_DBT_OUTPUT_DIR
                    / c.Meltano.DBT_MANIFEST_FILE
                )
            if not path.exists():
                return r[t.Meltano.DbtManifestData].fail(str(path))

            parsed_result = u.Cli.json_read_files_model(path, m.Meltano.DbtManifest)
            if parsed_result.failure:
                return r[t.Meltano.DbtManifestData].fail(
                    parsed_result.error or "manifest read failed",
                )
            parsed = parsed_result.value
            manifest_data: t.Meltano.DbtManifestData = {
                "nodes": {k: v.model_dump() for k, v in parsed.nodes.items()},
            }
            return r[t.Meltano.DbtManifestData].ok(manifest_data)

        try:
            return _run_load_manifest()
        except c.EXC_KEY_OS_TYPE_VALUE as exc:
            return r[t.Meltano.DbtManifestData].fail(str(exc))

    def fetch_models(self) -> p.Result[t.SequenceOf[t.Meltano.OptionalScalarMap]]:
        """Get model list from manifest."""
        manifest_result = self.load_manifest()
        if manifest_result.failure:
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
                manifest_result.error or "Manifest load failed",
            )
        try:
            manifest = m.Meltano.DbtManifest.model_validate(manifest_result.value)
            models: t.SequenceOf[t.Meltano.OptionalScalarMap] = [
                {
                    "name": str(node.name),
                    "path": str(node.path),
                    "description": node.description or "",
                    "fqn": node.fqn_string,
                }
                for node in manifest.nodes.values()
                if node.resource_type == c.Meltano.DbtResourceType.MODEL
            ]
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].ok(models)
        except c.EXC_MAPPING_TYPE as exc:
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(str(exc))

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute dbt service — returns status."""
        return r[t.JsonMapping].ok({
            "service": self.dbt_project_name,
            "status": "active",
            "type": c.Meltano.ServiceType.DBT,
        })


__all__: list[str] = ["FlextMeltanoDbtServiceBase"]
