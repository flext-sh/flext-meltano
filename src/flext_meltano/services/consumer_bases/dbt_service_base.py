"""Base service for FLEXT dbt consumer projects.

Provides dbt project management, model/test execution, manifest parsing,
and CLI dispatch via MRO. Consumer dbt projects override
``get_connection_profile()`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, ClassVar, Self, override

from flext_infra import FlextInfraUtilitiesSubprocess
from pydantic import Field, PrivateAttr

from flext_core import r
from flext_meltano import FlextMeltanoServiceBase, c, m, t


class FlextMeltanoDbtServiceBase(FlextMeltanoServiceBase):
    """Base for all FLEXT dbt service projects.

    Subclasses MUST define:
    - ``dbt_project_name``: canonical dbt project name
    - ``get_connection_profile()``: returns dbt connection profile dict

    This base provides via MRO:
    - dbt command execution (``run_models``, ``run_tests``, ``compile_models``)
    - Manifest parsing and model/test discovery
    - Documentation generation
    - CLI dispatch
    - Singleton accessor (``get_instance``)
    """

    dbt_project_name: Annotated[
        t.NonEmptyStr,
        Field(description="Canonical dbt project name"),
    ] = "dbt"

    _dbt_project_root: Path | None = PrivateAttr(default=None)
    _instance: ClassVar[Self | None] = None

    @classmethod
    def get_instance(cls) -> Self:
        """Return the shared facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @abstractmethod
    def get_connection_profile(self) -> t.ContainerMapping:
        """Return dbt connection profile for this project.

        Consumer implements with domain-specific connection config
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
                case "run":
                    models = command_args[1:] if len(command_args) > 1 else None
                    result = self.run_models(models)
                case "test":
                    models = command_args[1:] if len(command_args) > 1 else None
                    result = self.run_tests(models)
                case "compile":
                    models = command_args[1:] if len(command_args) > 1 else None
                    result = self.compile_models(models)
                case "docs":
                    result = self.generate_docs()
                case _:
                    result = r[str].fail(str(subcommand))
            if result.is_failure:
                self.logger.warning(
                    "dbt command failed",
                    subcommand=subcommand,
                    error=result.error,
                )
                return 1
            return 0
        except (ValueError, TypeError, OSError, RuntimeError) as exc:
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
    ) -> Sequence[str]:
        """Build dbt CLI command."""
        cmd: list[str] = ["dbt", subcommand]
        if self._dbt_project_root:
            cmd.extend(["--project-dir", str(self._dbt_project_root)])
        if models:
            cmd.extend(["--models", *models])
        if extra_args:
            cmd.extend(extra_args)
        return cmd

    def _run_dbt_cmd(self, cmd: Sequence[str], operation: str) -> r[str]:
        """Execute a dbt command via subprocess."""
        try:
            self.logger.info(
                "Running dbt command",
                operation=operation,
                command=" ".join(cmd),
            )
            result = FlextInfraUtilitiesSubprocess.run_raw(list(cmd))
            if result.is_failure:
                return r[str].fail(result.error or operation)
            out = result.value
            if out.exit_code != 0:
                return r[str].fail(out.stderr or operation)
            self.logger.info("dbt command completed", operation=operation)
            return r[str].ok(out.stdout)
        except (ValueError, TypeError, OSError, RuntimeError) as exc:
            return r[str].fail(str(exc))

    def run_models(self, models: t.StrSequence | None = None) -> r[str]:
        """Run dbt models."""
        return self._run_dbt_cmd(self._build_dbt_cmd("run", models=models), "run")

    def run_tests(self, models: t.StrSequence | None = None) -> r[str]:
        """Run dbt tests."""
        return self._run_dbt_cmd(self._build_dbt_cmd("test", models=models), "test")

    def compile_models(self, models: t.StrSequence | None = None) -> r[str]:
        """Compile dbt models."""
        return self._run_dbt_cmd(
            self._build_dbt_cmd("compile", models=models), "compile"
        )

    def generate_docs(self) -> r[str]:
        """Generate dbt documentation."""
        return self._run_dbt_cmd(
            self._build_dbt_cmd("docs", extra_args=["generate"]),
            "docs generate",
        )

    # ------------------------------------------------------------------
    # Project management
    # ------------------------------------------------------------------

    def set_project_root(self, root: Path) -> r[None]:
        """Set dbt project root directory."""
        if not root.exists():
            return r[None].fail(str(root))
        self._dbt_project_root = root
        return r[None].ok(None)

    def load_manifest(
        self, manifest_path: Path | None = None
    ) -> r[t.Meltano.Dbt.ManifestData]:
        """Load dbt manifest.json."""
        try:
            path = manifest_path
            if path is None:
                if self._dbt_project_root is None:
                    return r[t.Meltano.Dbt.ManifestData].fail("No project root set")
                path = self._dbt_project_root / "target" / "manifest.json"
            if not path.exists():
                return r[t.Meltano.Dbt.ManifestData].fail(str(path))
            parsed = m.Meltano.DbtManifest.model_validate_json(
                path.read_text(encoding="utf-8"),
            )
            manifest_data: t.Meltano.Dbt.ManifestData = {
                "nodes": {k: v.model_dump() for k, v in parsed.nodes.items()},
            }
            return r[t.Meltano.Dbt.ManifestData].ok(manifest_data)
        except (ValueError, TypeError, KeyError, OSError) as exc:
            return r[t.Meltano.Dbt.ManifestData].fail(str(exc))

    def get_models(self) -> r[Sequence[t.Meltano.Dbt.ModelConfiguration]]:
        """Get model list from manifest."""
        manifest_result = self.load_manifest()
        if manifest_result.is_failure:
            return r[Sequence[t.Meltano.Dbt.ModelConfiguration]].fail(
                manifest_result.error or "Manifest load failed"
            )
        try:
            manifest = m.Meltano.DbtManifest.model_validate(manifest_result.value)
            models: Sequence[t.Meltano.Dbt.ModelConfiguration] = [
                {
                    "name": str(node.name),
                    "path": str(node.path),
                    "description": str(node.description or ""),
                    "fqn": str(node.fqn_string),
                }
                for node in manifest.nodes.values()
                if node.resource_type == "model"
            ]
            return r[Sequence[t.Meltano.Dbt.ModelConfiguration]].ok(models)
        except (ValueError, TypeError, KeyError) as exc:
            return r[Sequence[t.Meltano.Dbt.ModelConfiguration]].fail(str(exc))

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute dbt service — returns status."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "service": self.dbt_project_name,
            "status": c.CommonStatus.ACTIVE.value,
            "type": "dbt",
        })


__all__ = ["FlextMeltanoDbtServiceBase"]
