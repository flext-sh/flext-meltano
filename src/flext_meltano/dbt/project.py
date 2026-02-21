"""DBT Project Integration - Deep integration with dbt-core.

This module provides project management for DBT with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar

from flext_core import r, s
from pydantic import BaseModel, Field, ValidationError

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes as mt

m = FlextMeltanoModels


class DbtProjectInfo(BaseModel):
    """Information about a DBT project."""

    root: Path = Field(description="Project root directory")
    name: str = Field(description="Project name")
    dbt_version: str | None = Field(default=None, description="DBT version")
    models_count: int = Field(default=0, description="Number of models")
    tests_count: int = Field(default=0, description="Number of tests")


class FlextMeltanoDbtProjectManager(s[DbtProjectInfo]):
    """Manages DBT projects with deep SDK integration.

    Provides programmatic access to DBT projects, manifests, and
    configurations through wrapped dbt-core APIs.

    Attributes:
    project_root: Root directory of DBT project
    manifest: Parsed DBT manifest

    """

    # Alias for backward compatibility
    ProjectInfo: ClassVar[type[DbtProjectInfo]] = DbtProjectInfo

    def __init__(self, root: Path | None = None) -> None:
        """Initialize DBT project manager.

        Args:
        root: Root directory of DBT project (optional)

        """
        super().__init__()
        self.project_root = root
        self.manifest: mt.Dbt.ManifestData | None = None

    def load_project(self, root: Path) -> r[DbtProjectInfo]:
        """Load a DBT project.

        Args:
        root: Root directory of the DBT project

        Returns:
        r containing project information

        """
        try:
            if not root.exists():
                return r[DbtProjectInfo].fail(
                    f"DBT project directory not found: {root}",
                )

            self.project_root = root

            info = DbtProjectInfo(
                root=root,
                name=str(root.name),
            )

            self.logger.info(
                "DBT project loaded",
                root=str(root),
            )
            return r[DbtProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return r[DbtProjectInfo].fail(
                f"Failed to load DBT project: {e}",
            )

    def load_manifest(
        self, manifest_path: Path | None = None
    ) -> r[mt.Dbt.ManifestData]:
        """Load DBT manifest.

        Args:
        manifest_path: Path to manifest file (optional)

        Returns:
        r containing manifest dictionary

        """
        try:
            if manifest_path is None:
                if self.project_root is None:
                    return r[mt.Dbt.ManifestData].fail("No project loaded")
                manifest_path = self.project_root / "target" / "manifest.json"

            if not manifest_path.exists():
                return r[mt.Dbt.ManifestData].fail(
                    f"Manifest not found: {manifest_path}"
                )

            with manifest_path.open() as f:
                manifest_data: mt.Dbt.ManifestData = json.load(f)
                self.manifest = manifest_data

            self.logger.info(
                "DBT manifest loaded",
                file=str(manifest_path),
            )
            return r[mt.Dbt.ManifestData].ok(self.manifest)
        except Exception as e:
            self.logger.exception("Failed to load manifest", error=str(e))
            return r[mt.Dbt.ManifestData].fail(f"Failed to load manifest: {e}")

    def get_models(self) -> r[list[mt.Dbt.ModelConfiguration]]:
        """Get all models from manifest.

        Returns:
        r containing list of models

        """
        try:
            if not self.manifest:
                manifest_result = self.load_manifest()
                if manifest_result.is_failure:
                    return r[list[mt.Dbt.ModelConfiguration]].fail(
                        manifest_result.error or "Unknown error",
                    )

            models: list[mt.Dbt.ModelConfiguration] = []
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
            return r[list[mt.Dbt.ModelConfiguration]].ok(models)
        except Exception as e:
            self.logger.exception("Failed to get models", error=str(e))
            return r[list[mt.Dbt.ModelConfiguration]].fail(f"Failed to get models: {e}")

    def get_tests(self) -> r[list[mt.Dbt.TestConfiguration]]:
        """Get all tests from manifest.

        Returns:
        r containing list of tests

        """
        try:
            if not self.manifest:
                manifest_result = self.load_manifest()
                if manifest_result.is_failure:
                    return r[list[mt.Dbt.TestConfiguration]].fail(
                        manifest_result.error or "Unknown error",
                    )

            tests: list[mt.Dbt.TestConfiguration] = []
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
            return r[list[mt.Dbt.TestConfiguration]].ok(tests)
        except (ValidationError, OSError, ValueError, TypeError) as e:
            self.logger.exception("Failed to get tests", error=str(e))
            return r[list[mt.Dbt.TestConfiguration]].fail(f"Failed to get tests: {e}")

    def execute(self, **_kwargs: object) -> r[DbtProjectInfo]:
        """Execute (implements Service pattern)."""
        if self.project_root:
            info = DbtProjectInfo(
                root=self.project_root,
                name=str(self.project_root.name),
            )
            return r[DbtProjectInfo].ok(info)
        return r[DbtProjectInfo].fail("No project loaded")


__all__ = [
    "FlextMeltanoDbtProjectManager",
]
