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

    def __init__(self, settings: FlextMeltanoSettings | None = None) -> None:
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

    @staticmethod
    def _cli_arguments(args: t.StrSequence | None) -> list[str]:
        """Resolve the effective CLI argument vector for dispatch.

        Returns:
            The resulting ``list[str]``.
        """
        return list(args) if args else sys.argv[1:]

    def _dispatch_dbt_subcommand(
        self,
        subcommand: str,
        rest: list[str],
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Dispatch one resolved dbt subcommand to its typed service call.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.
        """
        models: t.StrSequence | None = rest or None
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

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Run the main CLI entry point for dbt project.

        Returns:
            The resulting ``int``.

        Raises:
            SystemExit: If a ``c.EXC_OS_RUNTIME_TYPE`` is caught.
        """
        try:
            command_args = self._cli_arguments(args)
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
        models: t.StrSequence | None = None,
        extra_args: t.StrSequence | None = None,
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
        models: t.StrSequence | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Run dbt models.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.
        """
        return self._run_dbt_cmd(c.Meltano.DbtCommand.RUN, models=models)

    def run_tests(
        self,
        models: t.StrSequence | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Run dbt tests.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.
        """
        return self._run_dbt_cmd(c.Meltano.DbtCommand.TEST, models=models)

    def compile_models(
        self,
        models: t.StrSequence | None = None,
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

    # ------------------------------------------------------------------
    # Project management
    # ------------------------------------------------------------------

    def configure_project_root(self, root: Path) -> p.Result[bool]:
        """Set dbt project root directory.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        if not root.exists():
            return r[bool].fail(str(root))
        self._dbt_project_root = root
        return r[bool].ok(value=True)

    def _resolve_manifest_path(self, manifest_path: Path | None) -> p.Result[Path]:
        """Resolve the effective dbt manifest location.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        if manifest_path is not None:
            return r[Path].ok(manifest_path)
        if self._dbt_project_root is None:
            return r[Path].fail("No project root set")
        return r[Path].ok(
            self._dbt_project_root
            / c.Meltano.FILE_PATH_DBT_OUTPUT_DIR
            / c.Meltano.DBT_MANIFEST_FILE,
        )

    @staticmethod
    def _parse_manifest(path: Path) -> p.Result[t.Meltano.DbtManifestData]:
        """Parse the dbt manifest file into the public manifest contract.

        Returns:
            The resulting ``p.Result[t.Meltano.DbtManifestData]``.
        """
        parsed_result = u.Cli.files_read_json_model(path, m.Meltano.DbtManifest)
        if parsed_result.failure:
            return r[t.Meltano.DbtManifestData].from_failure(parsed_result)
        parsed = parsed_result.value
        manifest_data: t.Meltano.DbtManifestData = {
            "nodes": {k: v.model_dump() for k, v in parsed.nodes.items()},
        }
        return r[t.Meltano.DbtManifestData].ok(manifest_data)

    def load_manifest(
        self,
        manifest_path: Path | None = None,
    ) -> p.Result[t.Meltano.DbtManifestData]:
        """Load dbt manifest.json.

        Returns:
            The resulting ``p.Result[t.Meltano.DbtManifestData]``.
        """
        try:
            path_result = self._resolve_manifest_path(manifest_path)
            if path_result.failure:
                return r[t.Meltano.DbtManifestData].from_failure(path_result)
            path = path_result.value
            if not path.exists():
                return r[t.Meltano.DbtManifestData].fail(str(path))
            return self._parse_manifest(path)
        except c.EXC_KEY_OS_TYPE_VALUE as exc:
            return r[t.Meltano.DbtManifestData].fail(str(exc), exception=exc)

    def fetch_models(self) -> p.Result[t.SequenceOf[t.Meltano.OptionalScalarMap]]:
        """Get model list from manifest.

        Returns:
            The resulting ``p.Result[t.SequenceOf[t.Meltano.OptionalScalarMap]]``.
        """
        manifest_result = self.load_manifest()
        if manifest_result.failure:
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].from_failure(
                manifest_result,
            )
        try:
            manifest = m.Meltano.DbtManifest.model_validate(manifest_result.value)
        except c.EXC_MAPPING_TYPE as exc:
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
                str(exc),
                exception=exc,
            )
        return self._build_model_nodes(manifest)

    @staticmethod
    def _build_model_nodes(
        manifest: m.Meltano.DbtManifest,
    ) -> p.Result[t.SequenceOf[t.Meltano.OptionalScalarMap]]:
        models: list[t.Meltano.OptionalScalarMap] = []
        for node in manifest.nodes.values():
            if node.resource_type != c.Meltano.DbtResourceType.MODEL:
                continue
            node_data = node.model_dump()
            models.append({
                "name": str(node_data.get("name")),
                "path": str(node_data.get("path")),
                "description": str(node_data.get("description") or ""),
                "fqn": str(node_data.get("fqn_string") or ""),
            })
        return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].ok(models)

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
