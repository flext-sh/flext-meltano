"""DBT Project Integration - Deep integration with dbt-core.

This module provides project management for DBT with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flext_core import FlextResult, FlextService
from pydantic import Field

from flext_meltano.models import FlextMeltanoModels


class FlextMeltanoDbtProjectManager(FlextService):
    """Manages DBT projects with deep SDK integration.

    Provides programmatic access to DBT projects, manifests, and
    configurations through wrapped dbt-core APIs.

    Attributes:
        project_root: Root directory of DBT project
        manifest: Parsed DBT manifest

    """

    class ProjectInfo(FlextMeltanoModels):
        """Information about a DBT project."""

        root: Path = Field(description="Project root directory")
        name: str = Field(description="Project name")
        dbt_version: str | None = Field(default=None, description="DBT version")
        models_count: int = Field(default=0, description="Number of models")
        tests_count: int = Field(default=0, description="Number of tests")

    def __init__(self, root: Path | None = None) -> None:
        """Initialize DBT project manager.

        Args:
            root: Root directory of DBT project (optional)

        """
        super().__init__()
        self.project_root = root
        self.manifest = None

    def load_project(
        self, root: Path
    ) -> FlextResult[FlextMeltanoDbtProjectManager.ProjectInfo]:
        """Load a DBT project.

        Args:
            root: Root directory of the DBT project

        Returns:
            FlextResult containing project information

        """
        try:
            if not root.exists():
                return FlextResult[FlextMeltanoDbtProjectManager.ProjectInfo].fail(
                    f"DBT project directory not found: {root}"
                )

            self.project_root = root

            info = FlextMeltanoDbtProjectManager.ProjectInfo(
                root=root,
                name=root.name,
            )

            self.logger.info(
                "DBT project loaded",
                root=str(root),
            )
            return FlextResult[FlextMeltanoDbtProjectManager.ProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return FlextResult[FlextMeltanoDbtProjectManager.ProjectInfo].fail(
                f"Failed to load DBT project: {e}"
            )

    def load_manifest(
        self, manifest_path: Path | None = None
    ) -> FlextResult[dict[str, Any]]:
        """Load DBT manifest.

        Args:
            manifest_path: Path to manifest file (optional)

        Returns:
            FlextResult containing manifest dictionary

        """
        try:
            if manifest_path is None:
                if self.project_root is None:
                    return FlextResult[dict[str, Any]].fail("No project loaded")
                manifest_path = self.project_root / "target" / "manifest.json"

            if not manifest_path.exists():
                return FlextResult[dict[str, Any]].fail(
                    f"Manifest not found: {manifest_path}"
                )

            with manifest_path.open() as f:
                self.manifest = json.load(f)

            self.logger.info(
                "DBT manifest loaded",
                file=str(manifest_path),
            )
            return FlextResult[dict[str, Any]].ok(self.manifest)
        except Exception as e:
            self.logger.exception("Failed to load manifest", error=str(e))
            return FlextResult[dict[str, Any]].fail(f"Failed to load manifest: {e}")

    def get_models(self) -> FlextResult[list[dict[str, Any]]]:
        """Get all models from manifest.

        Returns:
            FlextResult containing list of models

        """
        try:
            if not self.manifest:
                manifest_result = self.load_manifest()
                if manifest_result.is_failure:
                    return FlextResult[list[dict[str, Any]]].fail(manifest_result.error)

            models = []
            if self.manifest and "nodes" in self.manifest:
                models.extend(
                    {
                        "name": node.get("name"),
                        "path": node.get("path"),
                        "description": node.get("description"),
                        "fqn": ".".join(node.get("fqn", [])),
                    }
                    for node in self.manifest["nodes"].values()
                    if node.get("resource_type") == "model"
                )

            self.logger.info("Models retrieved", count=len(models))
            return FlextResult[list[dict[str, Any]]].ok(models)
        except Exception as e:
            self.logger.exception("Failed to get models", error=str(e))
            return FlextResult[list[dict[str, Any]]].fail(f"Failed to get models: {e}")

    def get_tests(self) -> FlextResult[list[dict[str, Any]]]:
        """Get all tests from manifest.

        Returns:
            FlextResult containing list of tests

        """
        try:
            if not self.manifest:
                manifest_result = self.load_manifest()
                if manifest_result.is_failure:
                    return FlextResult[list[dict[str, Any]]].fail(manifest_result.error)

            tests = []
            if self.manifest and "nodes" in self.manifest:
                tests.extend(
                    {
                        "name": node.get("name"),
                        "path": node.get("path"),
                        "description": node.get("description"),
                        "fqn": ".".join(node.get("fqn", [])),
                    }
                    for node in self.manifest["nodes"].values()
                    if node.get("resource_type") == "test"
                )

            self.logger.info("Tests retrieved", count=len(tests))
            return FlextResult[list[dict[str, Any]]].ok(tests)
        except Exception as e:
            self.logger.exception("Failed to get tests", error=str(e))
            return FlextResult[list[dict[str, Any]]].fail(f"Failed to get tests: {e}")

    def execute(self) -> FlextResult[str]:
        """Execute (implements Domain.Service pattern)."""
        if self.project_root:
            msg = f"DBT project: {self.project_root}"
            return FlextResult[str].ok(msg)
        return FlextResult[str].fail("No project loaded")


__all__ = [
    "FlextMeltanoDbtProjectManager",
]
