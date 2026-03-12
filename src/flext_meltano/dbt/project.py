"""DBT Project Integration - Deep integration with dbt-core.

This module provides project management for DBT with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import override

from flext_core import r, s
from pydantic import ValidationError

from flext_meltano import m, t


class FlextMeltanoDbtProjectManager(s[m.Meltano.DbtProjectInfo]):
    """Manages DBT projects with deep SDK integration.

    Provides programmatic access to DBT projects, manifests, and
    configurations through wrapped dbt-core APIs.

    Attributes:
    project_root: Root directory of DBT project
    manifest: Parsed DBT manifest

    """

    def __init__(self, root: Path | None = None) -> None:
        """Initialize DBT project manager.

        Args:
        root: Root directory of DBT project (optional)

        """
        super().__init__()
        self.project_root = root
        self.manifest: t.Meltano.Dbt.ManifestData | None = None

    @override
    def execute(self, **_kwargs: object) -> r[m.Meltano.DbtProjectInfo]:
        """Execute (implements Service pattern)."""
        if self.project_root:
            info = m.Meltano.DbtProjectInfo(
                root=self.project_root, name=str(self.project_root.name)
            )
            return r[m.Meltano.DbtProjectInfo].ok(info)
        return r[m.Meltano.DbtProjectInfo].fail("No project loaded")

    def get_models(self) -> r[list[t.Meltano.Dbt.ModelConfiguration]]:
        """Get all models from manifest.

        Returns:
        r containing list of models

        """
        try:
            if not self.manifest:
                manifest_result = self.load_manifest()
                if manifest_result.is_failure:
                    return r[list[t.Meltano.Dbt.ModelConfiguration]].fail(
                        manifest_result.error or "Unknown error"
                    )
            models: list[t.Meltano.Dbt.ModelConfiguration] = []
            if self.manifest:
                manifest_model = m.Meltano.DbtManifest.model_validate(self.manifest)
                parsed_nodes = [
                    m.Meltano.DbtManifestNode.model_validate(node)
                    for node in manifest_model.nodes.values()
                ]
                model_nodes = [
                    node for node in parsed_nodes if node.resource_type == "model"
                ]
                models = [
                    {
                        "name": str(node.name),
                        "path": str(node.path),
                        "description": str(node.description)
                        if node.description is not None
                        else "",
                        "fqn": str(node.fqn_string),
                    }
                    for node in model_nodes
                ]
            self.logger.info("Models retrieved", count=len(models))
            return r[list[t.Meltano.Dbt.ModelConfiguration]].ok(models)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to get models", error=str(e))
            return r[list[t.Meltano.Dbt.ModelConfiguration]].fail(
                f"Failed to get models: {e}"
            )

    def get_tests(self) -> r[list[t.Meltano.Dbt.TestConfiguration]]:
        """Get all tests from manifest.

        Returns:
        r containing list of tests

        """
        try:
            if not self.manifest:
                manifest_result = self.load_manifest()
                if manifest_result.is_failure:
                    return r[list[t.Meltano.Dbt.TestConfiguration]].fail(
                        manifest_result.error or "Unknown error"
                    )
            tests: list[t.Meltano.Dbt.TestConfiguration] = []
            if self.manifest:
                manifest_model = m.Meltano.DbtManifest.model_validate(self.manifest)
                parsed_nodes = [
                    m.Meltano.DbtManifestNode.model_validate(node)
                    for node in manifest_model.nodes.values()
                ]
                test_nodes = [
                    node for node in parsed_nodes if node.resource_type == "test"
                ]
                tests = [
                    {
                        "name": str(node.name),
                        "path": str(node.path),
                        "description": str(node.description)
                        if node.description is not None
                        else "",
                        "fqn": str(node.fqn_string),
                    }
                    for node in test_nodes
                ]
            self.logger.info("Tests retrieved", count=len(tests))
            return r[list[t.Meltano.Dbt.TestConfiguration]].ok(tests)
        except (ValidationError, OSError, ValueError, TypeError) as e:
            self.logger.exception("Failed to get tests", error=str(e))
            return r[list[t.Meltano.Dbt.TestConfiguration]].fail(
                f"Failed to get tests: {e}"
            )

    def load_manifest(
        self, manifest_path: Path | None = None
    ) -> r[t.Meltano.Dbt.ManifestData]:
        """Load DBT manifest.

        Args:
        manifest_path: Path to manifest file (optional)

        Returns:
        r containing manifest dictionary

        """
        try:
            if manifest_path is None:
                if self.project_root is None:
                    return r[t.Meltano.Dbt.ManifestData].fail("No project loaded")
                manifest_path = self.project_root / "target" / "manifest.json"
            if not manifest_path.exists():
                return r[t.Meltano.Dbt.ManifestData].fail(
                    f"Manifest not found: {manifest_path}"
                )
            with manifest_path.open() as f:
                manifest_data: t.Meltano.Dbt.ManifestData = json.load(f)
                self.manifest = manifest_data
            self.logger.info("DBT manifest loaded", file=str(manifest_path))
            return r[t.Meltano.Dbt.ManifestData].ok(self.manifest)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load manifest", error=str(e))
            return r[t.Meltano.Dbt.ManifestData].fail(f"Failed to load manifest: {e}")

    def load_project(self, root: Path) -> r[m.Meltano.DbtProjectInfo]:
        """Load a DBT project.

        Args:
        root: Root directory of the DBT project

        Returns:
        r containing project information

        """
        try:
            if not root.exists():
                return r[m.Meltano.DbtProjectInfo].fail(
                    f"DBT project directory not found: {root}"
                )
            self.project_root = root
            info = m.Meltano.DbtProjectInfo(root=root, name=str(root.name))
            self.logger.info("DBT project loaded", root=str(root))
            return r[m.Meltano.DbtProjectInfo].ok(info)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return r[m.Meltano.DbtProjectInfo].fail(f"Failed to load DBT project: {e}")


__all__ = ["FlextMeltanoDbtProjectManager"]
