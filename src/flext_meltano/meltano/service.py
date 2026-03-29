"""Meltano Orchestration Service - ELT pipeline orchestration.

This module provides Meltano ELT pipeline orchestration with deep SDK integration,
FLEXT ecosystem patterns, and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, override

from flext_core import s
from pydantic import Field

from flext_meltano import (
    FlextMeltanoProjectManager,
    m,
    r,
    t,
)


class FlextMeltanoMeltanoService(s[str]):
    """Orchestrates Meltano ELT operations with deep SDK integration.

    Provides complete Meltano orchestration including:
    - Project lifecycle management
    - Plugin discovery and management
    - Pipeline configuration and execution
    - Environment and context management
    - Error handling with r[T]

    This service integrates directly with meltano-sdk, providing a
    programmatic API for complete ELT operations.

    Attributes:
    project_manager: Manages Meltano projects

    """

    class PipelineConfig(m):
        """Configuration for a Meltano pipeline."""

        project_root: Annotated[Path, Field(description="Meltano project root")]
        run_config: Annotated[str, Field(description="Run configuration name")]
        select: Annotated[
            str | None,
            Field(default=None, description="Stream/table selection"),
        ]
        select_filter: Annotated[
            str | None,
            Field(default=None, description="Additional selection filter"),
        ]

    def __init__(self) -> None:
        """Initialize Meltano orchestration service."""
        super().__init__()
        self.project_manager = FlextMeltanoProjectManager()

    def create_project(self, root: Path) -> r[t.Meltano.Project.ProjectMetadata]:
        """Create a new Meltano project.

        Args:
            root: Root directory for the project

        Returns:
            r containing project information

        """
        self.logger.info("Creating Meltano project", root=str(root))
        return self.project_manager.initialize_project(root)

    def discover_plugins(
        self,
        plugin_type: str | None = None,
    ) -> r[Sequence[t.Meltano.PluginDefinition]]:
        """Discover plugins in the project.

        Args:
            plugin_type: Optional plugin type to filter

        Returns:
            r containing list of plugins

        """
        self.logger.info("Discovering plugins", type=plugin_type or "")
        return self.project_manager.get_plugins(plugin_type)

    @override
    def execute(self) -> r[str]:
        """Execute (implements Service pattern)."""
        return r[str].ok("Meltano service ready")

    def execute_pipeline(
        self,
        config: FlextMeltanoMeltanoService.PipelineConfig,
    ) -> r[t.Meltano.ELT.PipelineResult]:
        """Execute a Meltano pipeline.

        Args:
            config: Pipeline configuration

        Returns:
            r containing pipeline result

        """
        return r[t.Meltano.ELT.PipelineResult].fail(
            f"Pipeline execution requires meltano-core SDK integration: "
            f"run_config={config.run_config!r}, project_root={config.project_root!r}"
        )

    def load_project(self, root: Path) -> r[t.Meltano.Project.ProjectMetadata]:
        """Load an existing Meltano project.

        Args:
            root: Root directory of the project

        Returns:
            r containing project information

        """
        self.logger.info("Loading Meltano project", root=str(root))
        return self.project_manager.load_project(root)


__all__ = ["FlextMeltanoMeltanoService"]
