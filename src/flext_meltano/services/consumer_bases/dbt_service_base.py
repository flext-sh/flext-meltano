"""Base service for FLEXT dbt consumer projects.

Provides dbt project management, model/test execution, manifest parsing,
and CLI dispatch via MRO. Consumer dbt projects override
``connection_profile`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import abstractmethod
from pathlib import Path
from typing import Annotated, ClassVar, Self, override

from flext_meltano import (
    FlextMeltanoServiceBase,
    c,
    m,
    p,
    r,
    t,
    u,
)


class FlextMeltanoDbtServiceBase(FlextMeltanoServiceBase):
    """Base for all FLEXT dbt service projects.

    Subclasses MUST define:
    - ``dbt_project_name``: canonical dbt project name
    - ``connection_profile``: returns dbt connection profile dict

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
    _instance: ClassVar[Self | None] = None

    def __init__(
        self,
        settings: p.Settings | None = None,
    ) -> None:
        """Expose the canonical settings bootstrap for dbt consumers."""
        super().__init__(runtime_settings=settings)

    @classmethod
    def fetch_instance(cls) -> Self:
        """Return the shared facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    @abstractmethod
    def connection_profile(self) -> t.JsonMapping:
        """Dbt connection profile for this project.

        Consumer implements with domain-specific connection settings
        (e.g. Oracle DSN, LDAP bind DN, etc.).
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Main CLI entry point for dbt project."""
        try:
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
                    result = r[str].fail(subcommand)
            if result.failure:
                self.logger.warning(
                    "dbt command failed",
                    subcommand=subcommand,
                    error=result.error or "",
                )
                return 1
            return 0
        except c.EXC_OS_RUNTIME_TYPE as exc:
            self.logger.exception("dbt CLI failed", error=str(exc))
            return 1

    # ------------------------------------------------------------------
    # dbt command execution
    # ------------------------------------------------------------------

    def _build_dbt_cmd(
        self,
        subcommand: str,
        models: t.StrSequence | None = None,
        extra_args: t.StrSequence | None = None,
    ) -> t.StrSequence:
        """Build dbt CLI command."""
        cmd: list[str] = [c.Meltano.DBT_BINARY, subcommand]
        if self._dbt_project_root:
            cmd.extend([
                c.Meltano.DbtOption.PROJECTS_DIR,
                str(self._dbt_project_root),
            ])
        if models:
            cmd.extend([c.Meltano.DbtOption.MODELS, *models])
        if extra_args:
            cmd.extend(extra_args)
        return cmd

    def _run_dbt_cmd(self, cmd: t.StrSequence, operation: str) -> p.Result[str]:
        """Execute a dbt command via subprocess."""
        try:
            self.logger.info(
                "Running dbt command",
                operation=operation,
                command=" ".join(cmd),
            )
            result = u.Cli.run_raw(list(cmd))
            if result.failure:
                return r[str].fail(result.error or operation)
            out = result.value
            if out.exit_code != 0:
                return r[str].fail(out.stderr or operation)
            self.logger.info("dbt command completed", operation=operation)
            return r[str].ok(out.stdout)
        except c.EXC_OS_RUNTIME_TYPE as exc:
            return r[str].fail(str(exc))

    def run_models(self, models: t.StrSequence | None = None) -> p.Result[str]:
        """Run dbt models."""
        return self._run_dbt_cmd(
            self._build_dbt_cmd(c.Meltano.DbtCommand.RUN, models=models),
            c.Meltano.DbtCommand.RUN,
        )

    def run_tests(self, models: t.StrSequence | None = None) -> p.Result[str]:
        """Run dbt tests."""
        return self._run_dbt_cmd(
            self._build_dbt_cmd(c.Meltano.DbtCommand.TEST, models=models),
            c.Meltano.DbtCommand.TEST,
        )

    def compile_models(self, models: t.StrSequence | None = None) -> p.Result[str]:
        """Compile dbt models."""
        return self._run_dbt_cmd(
            self._build_dbt_cmd(c.Meltano.DbtCommand.COMPILE, models=models),
            c.Meltano.DbtCommand.COMPILE,
        )

    def generate_docs(self) -> p.Result[str]:
        """Generate dbt documentation."""
        return self._run_dbt_cmd(
            self._build_dbt_cmd(
                c.Meltano.DbtCommand.DOCS,
                extra_args=list(c.Meltano.DBT_DEFAULT_DOCS_ARGS),
            ),
            f"{c.Meltano.DbtCommand.DOCS} {c.Meltano.DbtCommand.GENERATE}",
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
        self, manifest_path: Path | None = None
    ) -> p.Result[t.Meltano.DbtManifestData]:
        """Load dbt manifest.json."""
        try:
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

            parsed_result = u.Cli.files_read_json_model(path, m.Meltano.DbtManifest)
            if parsed_result.failure:
                return r[t.Meltano.DbtManifestData].fail(
                    parsed_result.error or "manifest read failed"
                )
            parsed = parsed_result.value
            manifest_data: t.Meltano.DbtManifestData = {
                "nodes": {k: v.model_dump() for k, v in parsed.nodes.items()},
            }
            return r[t.Meltano.DbtManifestData].ok(manifest_data)
        except (ValueError, TypeError, KeyError, OSError) as exc:
            return r[t.Meltano.DbtManifestData].fail(str(exc))

    def fetch_models(self) -> p.Result[t.SequenceOf[t.Meltano.OptionalScalarMap]]:
        """Get model list from manifest."""
        manifest_result = self.load_manifest()
        if manifest_result.failure:
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
                manifest_result.error or "Manifest load failed"
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
