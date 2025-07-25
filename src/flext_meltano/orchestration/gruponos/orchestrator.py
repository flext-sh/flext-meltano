"""GrupoNOS Meltano Orchestrator - Consolidated Implementation.

Orchestration classes for GrupoNOS Meltano pipeline management, consolidated from
gruponos-meltano-native for centralized orchestration.
"""

from __future__ import annotations

from dataclasses import field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from flext_core import FlextResult, FlextValueObject

from flext_meltano.exceptions import (
    FlextMeltanoOrchestrationError,
    FlextMeltanoPipelineError,
)

from .config import GruponosMeltanoSettings


class PipelineStatus(Enum):
    """Pipeline execution status."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class GruponosMeltanoPipelineResult(FlextValueObject):
    """Result of a GrupoNOS Meltano pipeline execution."""

    pipeline_id: str
    status: PipelineStatus
    start_time: datetime
    end_time: datetime | None = None
    records_processed: int = 0
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> float | None:
        """Calculate execution duration in seconds."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds()

    @property
    def is_success(self) -> bool:
        """Check if pipeline execution was successful."""
        return self.status == PipelineStatus.SUCCESS

    @property
    def is_failed(self) -> bool:
        """Check if pipeline execution failed."""
        return self.status == PipelineStatus.FAILED

    @property
    def execution_time_seconds(self) -> float:
        """Get execution time in seconds (legacy compatibility)."""
        return self.duration_seconds or 0.0

    @property
    def warnings(self) -> list[str]:
        """Get warnings from pipeline execution."""
        return [error for error in self.errors if "warning" in error.lower()]

    def has_warnings(self) -> bool:
        """Check if pipeline has warnings."""
        return len(self.warnings) > 0


class GruponosMeltanoPipelineRunner:
    """Pipeline runner for GrupoNOS Meltano operations."""

    def __init__(self, settings: GruponosMeltanoSettings) -> None:
        """Initialize pipeline runner with settings."""
        self.settings = settings

    def run_extraction(self, source: str, entities: list[str] | None = None) -> FlextResult[GruponosMeltanoPipelineResult]:
        """Run data extraction pipeline."""
        pipeline_id = f"extract_{source}_{datetime.now(UTC).isoformat()}"
        start_time = datetime.now(UTC)

        try:
            # Placeholder implementation - would integrate with actual Meltano
            if self.settings.dry_run:
                result = GruponosMeltanoPipelineResult(
                    pipeline_id=pipeline_id,
                    status=PipelineStatus.SUCCESS,
                    start_time=start_time,
                    end_time=datetime.now(UTC),
                    records_processed=0,
                    metadata={"dry_run": True, "source": source, "entities": entities or []},
                )
                return FlextResult.ok(result)

            # Real implementation would execute Meltano taps here
            msg = "Real extraction not implemented yet"
            raise FlextMeltanoPipelineError(msg)

        except (FlextMeltanoPipelineError, OSError, ValueError, ImportError) as e:
            result = GruponosMeltanoPipelineResult(
                pipeline_id=pipeline_id,
                status=PipelineStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(UTC),
                errors=[str(e)],
            )
            return FlextResult.failure(result)

    def run_loading(self, target: str, data_source: str) -> FlextResult[GruponosMeltanoPipelineResult]:
        """Run data loading pipeline."""
        pipeline_id = f"load_{target}_{datetime.now(UTC).isoformat()}"
        start_time = datetime.now(UTC)

        try:
            if self.settings.dry_run:
                result = GruponosMeltanoPipelineResult(
                    pipeline_id=pipeline_id,
                    status=PipelineStatus.SUCCESS,
                    start_time=start_time,
                    end_time=datetime.now(UTC),
                    records_processed=0,
                    metadata={"dry_run": True, "target": target, "data_source": data_source},
                )
                return FlextResult.ok(result)

            # Real implementation would execute Meltano targets here
            msg = "Real loading not implemented yet"
            raise FlextMeltanoPipelineError(msg)

        except (FlextMeltanoPipelineError, OSError, ValueError, ImportError) as e:
            result = GruponosMeltanoPipelineResult(
                pipeline_id=pipeline_id,
                status=PipelineStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(UTC),
                errors=[str(e)],
            )
            return FlextResult.failure(result)

    async def run_with_retry(
        self,
        pipeline_name: str,
        max_retries: int = 3,
        retry_delay: int = 30,
    ) -> FlextResult[GruponosMeltanoPipelineResult]:
        """Run pipeline with retry logic (async compatibility)."""
        for attempt in range(max_retries + 1):
            try:
                if "extract" in pipeline_name.lower():
                    result = self.run_extraction("oracle_wms", [])
                elif "load" in pipeline_name.lower():
                    result = self.run_loading("oracle", "oracle_wms")
                else:
                    result = self.run_extraction("oracle_wms", [])

                if result.is_success:
                    return result

                if attempt < max_retries:
                    # In real implementation, would use asyncio.sleep(retry_delay)
                    continue

                return result

            except (FlextMeltanoPipelineError, OSError, ValueError, ImportError) as e:
                if attempt == max_retries:
                    pipeline_id = f"retry_{pipeline_name}_{datetime.now(UTC).isoformat()}"
                    failed_result = GruponosMeltanoPipelineResult(
                        pipeline_id=pipeline_id,
                        status=PipelineStatus.FAILED,
                        start_time=datetime.now(UTC),
                        end_time=datetime.now(UTC),
                        errors=[f"Max retries exceeded: {e}"],
                    )
                    return FlextResult.failure(failed_result)

        # Should never reach here
        pipeline_id = f"retry_{pipeline_name}_{datetime.now(UTC).isoformat()}"
        failed_result = GruponosMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            status=PipelineStatus.FAILED,
            start_time=datetime.now(UTC),
            end_time=datetime.now(UTC),
            errors=["Unexpected error in retry logic"],
        )
        return FlextResult.failure(failed_result)


class GruponosMeltanoOrchestrator:
    """Main orchestrator for GrupoNOS Meltano operations."""

    def __init__(self, settings: GruponosMeltanoSettings) -> None:
        """Initialize orchestrator with settings."""
        self.settings = settings
        self.pipeline_runner = GruponosMeltanoPipelineRunner(settings)

    def execute_full_pipeline(
        self,
        source: str,
        target: str,
        entities: list[str] | None = None,
    ) -> FlextResult[list[GruponosMeltanoPipelineResult]]:
        """Execute complete extract-load pipeline."""
        results: list[GruponosMeltanoPipelineResult] = []

        try:
            # Run extraction
            extract_result = self.pipeline_runner.run_extraction(source, entities)
            if extract_result.is_failure:
                return FlextResult.failure(
                    FlextMeltanoOrchestrationError(f"Extraction failed: {extract_result.error_message}"),
                )

            results.append(extract_result.data)

            # Run loading
            load_result = self.pipeline_runner.run_loading(target, source)
            if load_result.is_failure:
                return FlextResult.failure(
                    FlextMeltanoOrchestrationError(f"Loading failed: {load_result.error_message}"),
                )

            results.append(load_result.data)

            return FlextResult.ok(results)

        except (FlextMeltanoPipelineError, OSError, ValueError, ImportError) as e:
            return FlextResult.failure(
                FlextMeltanoOrchestrationError(f"Pipeline orchestration failed: {e}"),
            )

    def get_pipeline_status(self, pipeline_id: str) -> FlextResult[PipelineStatus]:
        """Get status of a specific pipeline."""
        # Placeholder implementation
        return FlextResult.ok(PipelineStatus.PENDING)

    def cancel_pipeline(self, pipeline_id: str) -> FlextResult[bool]:
        """Cancel a running pipeline."""
        # Placeholder implementation
        return FlextResult.ok(True)

    async def run_pipeline(self, pipeline_name: str) -> FlextResult[GruponosMeltanoPipelineResult]:
        """Run a specific pipeline by name (async compatibility)."""
        try:
            # Convert to sync call for now
            if "extract" in pipeline_name.lower():
                return self.pipeline_runner.run_extraction("oracle_wms", [])
            if "load" in pipeline_name.lower():
                return self.pipeline_runner.run_loading("oracle", "oracle_wms")
            # Run full pipeline
            result = self.execute_full_pipeline("oracle_wms", "oracle")
            if result.is_success and result.data:
                return FlextResult.ok(result.data[0])
            return FlextResult.failure(
                FlextMeltanoOrchestrationError(f"Pipeline {pipeline_name} failed"),
            )
        except (FlextMeltanoPipelineError, OSError, ValueError, ImportError) as e:
            return FlextResult.failure(
                FlextMeltanoOrchestrationError(f"Failed to run pipeline {pipeline_name}: {e}"),
            )

    async def list_pipelines(self) -> FlextResult[list[str]]:
        """List available pipelines (async compatibility)."""
        try:
            pipelines = [
                "extract-oracle-wms",
                "load-oracle",
                "full-etl-pipeline",
            ]
            return FlextResult.ok(pipelines)
        except (FlextMeltanoPipelineError, OSError, ValueError, ImportError) as e:
            return FlextResult.failure(
                FlextMeltanoOrchestrationError(f"Failed to list pipelines: {e}"),
            )



def create_gruponos_meltano_pipeline_runner(
    settings: GruponosMeltanoSettings | None = None,
) -> GruponosMeltanoPipelineRunner:
    """Factory function to create GrupoNOS Meltano pipeline runner."""
    if settings is None:
        settings = GruponosMeltanoSettings.from_env()
    return GruponosMeltanoPipelineRunner(settings)


def create_gruponos_meltano_orchestrator(
    settings: GruponosMeltanoSettings | None = None,
) -> GruponosMeltanoOrchestrator:
    """Factory function to create GrupoNOS Meltano orchestrator."""
    if settings is None:
        settings = GruponosMeltanoSettings.from_env()
    return GruponosMeltanoOrchestrator(settings)
