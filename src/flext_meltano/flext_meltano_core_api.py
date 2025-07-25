"""FlextMeltano Core API - Maximum code reduction classes.

Refactored public API focused on extreme usability and massive code reduction.
All classes use flext-core patterns as base with real framework integration.
"""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path
from typing import Any

from flext_meltano.core import (
    FlextMeltanoDbtService,
    FlextMeltanoExecutionState,
    FlextMeltanoPipelineResult,
    FlextMeltanoRepository,
    FlextMeltanoSingerService,
)
from flext_meltano.flext_meltano_ultra_helpers import (
    FlextMeltanoUltraExecutor,
    UltraPipelineConfig,
    flext_meltano_batch_execute_ultra,
    flext_meltano_discover_and_run_ultra,
    flext_meltano_get_pipeline_metrics_ultra,
    flext_meltano_manage_project_ultra,
    flext_meltano_setup_project_ultra,
)

# Import helpers with fallbacks
try:
    from flext_meltano.helpers.discovery import flext_meltano_discover_catalog
except ImportError:
    flext_meltano_discover_catalog = None

try:
    from flext_meltano.helpers.validation import flext_meltano_test_tap_connection
except ImportError:
    flext_meltano_test_tap_connection = None


class FlextMeltanoCore:
    """Unified core API for maximum code reduction.

    Replaces 100+ lines of setup code with single class instantiation.
    Real integration with Singer SDK, Meltano Core, and DBT.
    """

    def __init__(self, project_root: Path | str = ".") -> None:
        """Initialize with project root."""
        self.project_root = Path(project_root)
        self._repository = FlextMeltanoRepository()
        self._singer_service = FlextMeltanoSingerService()
        self._dbt_service = FlextMeltanoDbtService(self.project_root)

    async def flext_meltano_run(
        self,
        tap: str,
        target: str,
        **kwargs: str | int | bool | None,
    ) -> FlextMeltanoPipelineResult:
        """Run complete pipeline - replaces 50+ lines.

        Examples:
            core = FlextMeltanoCore()
            result = await core.flext_meltano_run("tap-postgres", "target-csv")

        """
        executor = FlextMeltanoUltraExecutor()
        executor.repository = self._repository
        executor.singer_service = self._singer_service

        # Create config with project_root and other parameters
        config = UltraPipelineConfig(
            project_root=self.project_root,
            environment=kwargs.get("environment", "dev"),
            selected_streams=kwargs.get("selected_streams"),
        )

        result = await executor.flext_meltano_execute_pipeline_ultra(
            tap,
            target,
            config=config,
        )

        if result.is_success:
            return result.data

        # Return failed result
        return FlextMeltanoPipelineResult(
            pipeline_id=str(uuid.uuid4()),
            state=FlextMeltanoExecutionState.FAILED,
            error_message=result.error,
        )

    async def flext_meltano_discover(self, tap: str) -> dict[str, Any]:
        """Discover tap catalog - replaces 20+ lines."""
        # Use discovery helper directly to avoid private method access
        if flext_meltano_discover_catalog is not None:
            catalog_result = await flext_meltano_discover_catalog(
                tap, self.project_root,
            )
            return catalog_result.data if catalog_result.is_success else {}
        # Fallback: return empty catalog if discovery helper not available
        return {}

    async def flext_meltano_test_connection(self, tap: str) -> bool:
        """Test tap connection - replaces 15+ lines."""
        # Use validation helper directly to avoid private method access
        if flext_meltano_test_tap_connection is not None:
            result = await flext_meltano_test_tap_connection(tap, self.project_root)
            return result.data if result.is_success else False
        # Fallback: return False if validation helper not available
        return False

    async def flext_meltano_run_dbt(
        self,
        models: list[str] | None = None,
    ) -> list[Any]:
        """Run DBT models - replaces 30+ lines."""
        result = await self._dbt_service.run_models(models)
        return result.data if result.is_success else []

    async def flext_meltano_test_dbt(
        self,
        models: list[str] | None = None,
    ) -> list[Any]:
        """Test DBT models - replaces 25+ lines."""
        result = await self._dbt_service.test_models(models)
        return result.data if result.is_success else []

    def flext_meltano_get_history(self) -> list[FlextMeltanoPipelineResult]:
        """Get pipeline execution history - replaces 10+ lines."""
        result = asyncio.run(self._repository.get_all())
        return result.data if result.is_success else []

    def flext_meltano_get_metrics(self) -> dict[str, Any]:
        """Get execution metrics - replaces 40+ lines."""
        result = asyncio.run(flext_meltano_get_pipeline_metrics_ultra())
        return result.data if result.is_success else {}


class FlextMeltanoProject:
    """Project management API for maximum code reduction.

    Replaces 150+ lines of project setup/management with simple methods.
    Real integration with meltano-core.
    """

    def __init__(self, project_path: Path | str) -> None:
        """Initialize with project path."""
        self.project_path = Path(project_path)

    async def flext_meltano_create(
        self,
        taps: list[str] | None = None,
        targets: list[str] | None = None,
        environments: list[str] | None = None,
    ) -> bool:
        """Create complete project - replaces 100+ lines."""
        result = await flext_meltano_setup_project_ultra(
            self.project_path,
            taps=taps or ["tap-csv"],
            targets=targets or ["target-csv"],
            environments=environments or ["dev"],
        )

        return result.is_success

    async def flext_meltano_status(self) -> dict[str, Any]:
        """Get project status - replaces 20+ lines."""
        result = await flext_meltano_manage_project_ultra(
            self.project_path,
            action="status",
        )

        return result.data if result.is_success else {}

    async def flext_meltano_list_plugins(self) -> dict[str, list[dict[str, Any]]]:
        """List installed plugins - replaces 25+ lines."""
        result = await flext_meltano_manage_project_ultra(
            self.project_path,
            action="plugins",
        )

        return result.data if result.is_success else {"extractors": [], "loaders": []}

    async def flext_meltano_run_pipeline(
        self,
        tap: str,
        target: str,
    ) -> dict[str, Any]:
        """Run project pipeline - replaces 35+ lines."""
        result = await flext_meltano_manage_project_ultra(
            self.project_path,
            action="run",
            tap=tap,
            target=target,
        )

        return result.data if result.is_success else {"success": False}


class FlextMeltanoBatch:
    """Batch processing API for maximum code reduction.

    Replaces 200+ lines of complex batch processing with simple methods.
    """

    def __init__(self, project_root: Path | str = ".") -> None:
        """Initialize with project root."""
        self.project_root = Path(project_root)

    async def flext_meltano_run_parallel(
        self,
        pipelines: list[tuple[str, str]],
        max_workers: int = 3,
    ) -> dict[str, FlextMeltanoPipelineResult]:
        """Run multiple pipelines in parallel - replaces 100+ lines."""
        return await flext_meltano_batch_execute_ultra(
            pipelines,
            parallel=True,
            max_workers=max_workers,
            project_root=self.project_root,
        )

    async def flext_meltano_run_sequential(
        self,
        pipelines: list[tuple[str, str]],
    ) -> dict[str, FlextMeltanoPipelineResult]:
        """Run multiple pipelines sequentially - replaces 80+ lines."""
        return await flext_meltano_batch_execute_ultra(
            pipelines,
            parallel=False,
            project_root=self.project_root,
        )

    async def flext_meltano_discover_and_run(
        self,
        tap: str,
        target: str,
    ) -> tuple[dict[str, Any], FlextMeltanoPipelineResult]:
        """Discover catalog and run pipeline - replaces 60+ lines."""
        return await flext_meltano_discover_and_run_ultra(
            tap,
            target,
            project_root=self.project_root,
        )


# One-liner functions for maximum code reduction
async def flext_meltano_pipeline(
    tap: str, target: str, **kwargs: str | int | bool | None,
) -> FlextMeltanoPipelineResult:
    """One-liner pipeline execution - replaces 50+ lines."""
    core = FlextMeltanoCore(kwargs.get("project_root", "."))
    return await core.flext_meltano_run(tap, target, **kwargs)


def flext_meltano_pipeline_sync(
    tap: str, target: str, **kwargs: str | int | bool | None,
) -> FlextMeltanoPipelineResult:
    """Execute synchronous one-liner pipeline - replaces 50+ lines."""
    return asyncio.run(flext_meltano_pipeline(tap, target, **kwargs))


async def flext_meltano_create_project(
    path: Path | str,
    taps: list[str] | None = None,
    targets: list[str] | None = None,
) -> bool:
    """One-liner project creation - replaces 100+ lines."""
    project = FlextMeltanoProject(path)
    return await project.flext_meltano_create(taps, targets)


async def flext_meltano_batch_run(
    pipelines: list[tuple[str, str]],
    **kwargs: str | int | bool | None,
) -> dict[str, FlextMeltanoPipelineResult]:
    """One-liner batch execution - replaces 100+ lines."""
    batch = FlextMeltanoBatch(kwargs.get("project_root", "."))
    return await batch.flext_meltano_run_parallel(
        pipelines, kwargs.get("max_workers", 3),
    )


__all__ = [
    "FlextMeltanoBatch",
    # Core classes
    "FlextMeltanoCore",
    "FlextMeltanoProject",
    "flext_meltano_batch_run",
    "flext_meltano_create_project",
    # One-liner functions
    "flext_meltano_pipeline",
    "flext_meltano_pipeline_sync",
]
