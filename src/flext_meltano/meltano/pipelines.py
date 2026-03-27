"""FLEXT Pipeline Orchestration Service - Single unified class for pipeline operations.

This module provides the FlextMeltanoOrchestrationService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with r
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import override

from flext_core import r, s

from flext_meltano import FlextMeltanoAbstractions, FlextMeltanoSettings, c, m, p, t


class FlextMeltanoOrchestrationService(s[t.Meltano.MeltanoConfigDict]):
    """Service for data pipeline operations.

    Handles pipeline execution, validation, and monitoring
    following FLEXT patterns with railway-oriented programming.
    """

    _abstractions: FlextMeltanoAbstractions

    def __init__(self, config: FlextMeltanoSettings | None = None) -> None:
        """Initialize pipeline service with FLEXT configuration."""
        super().__init__()
        self._config = config if config is not None else FlextMeltanoSettings()
        self._abstractions = FlextMeltanoAbstractions()

    @staticmethod
    def _find_required_plugins() -> r[tuple[p.Meltano.Plugin, p.Meltano.Plugin]]:
        """Find required plugins in t.Meltano.Dbt.Project."""
        return r[tuple[p.Meltano.Plugin, p.Meltano.Plugin]].fail(
            "Plugin discovery not configured",
        )

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute orchestration service logic."""
        try:
            return r[t.Meltano.MeltanoConfigDict].ok({})
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[t.Meltano.MeltanoConfigDict].fail(f"Orchestration failed: {e}")

    def execute_pipeline(
        self,
        project_path: str,
        source_name: str,
        sink_name: str,
    ) -> r[Mapping[str, str]]:
        """Execute data pipeline using railway-oriented programming.

        Consolidates pipeline coordinator functionality into unified service method
        using r railway patterns to eliminate nested error handling
        and provide composable pipeline execution.

        Args:
        project_path: Path to pipeline project
        source_name: Name of the source component
        sink_name: Name of the sink component

        Returns:
        r containing pipeline execution results

        """
        project_obj = project_path
        start_result = self._log_pipeline_start(source_name, sink_name)
        if start_result.is_failure:
            return r[Mapping[str, str]].fail(
                start_result.error or "Pipeline start failed",
            )
        plugins_result = self._find_required_plugins()
        if plugins_result.is_failure:
            return r[Mapping[str, str]].fail(
                plugins_result.error or "Failed to find plugins",
            )
        elt_context_result = self._create_elt_context(
            project_obj,
            source_name,
            sink_name,
            plugins_result.value,
        )
        if elt_context_result.is_failure:
            return r[Mapping[str, str]].fail(
                elt_context_result.error or "Failed to create ELT context",
            )
        runner_result = self._execute_singer_runner(elt_context_result.value)
        if runner_result.is_failure:
            return r[Mapping[str, str]].fail(
                runner_result.error or "Failed to execute singer runner",
            )
        final_result = self._build_pipeline_result(
            source_name,
            sink_name,
            runner_result.value,
        )
        if final_result.is_failure:
            return r[Mapping[str, str]].fail(
                final_result.error
                or f"Pipeline execution failed for {source_name} -> {sink_name}",
            )
        return final_result

    def _build_pipeline_result(
        self,
        extractor_name: str,
        loader_name: str,
        context_data: t.ConfigurationMapping,
    ) -> r[Mapping[str, str]]:
        """Build successful pipeline result."""
        try:
            parsed_context = m.Meltano.PipelineResultContext.model_validate(
                context_data,
            )
            execution_values = m.Meltano.PipelineExecutionScalarMap.model_validate({
                "values": parsed_context.execution_result,
            }).values
            pipeline_result: MutableMapping[str, str] = {
                "success": "true",
                "extractor": extractor_name,
                "loader": loader_name,
                "execution_method": "singer_runner_abstracted",
                "project_root": parsed_context.project_root,
                "run_id": c.IDENTIFIER_UNKNOWN,
            }
            pipeline_result.update(execution_values)
            self.logger.info(
                "ELT pipeline executed successfully",
                extractor=extractor_name,
                loader=loader_name,
            )
            return r[Mapping[str, str]].ok(pipeline_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Mapping[str, str]].fail(f"Failed to build pipeline result: {e}")

    def _create_elt_context(
        self,
        project_path: str,
        extractor_name: str,
        loader_name: str,
        plugins: tuple[p.Meltano.Plugin, p.Meltano.Plugin],
    ) -> r[t.Meltano.ExecutionResultDict]:
        """Create ELT context for pipeline execution."""
        try:
            project_root = Path(project_path)
            if not project_root.exists() or not project_root.is_dir():
                return r[t.Meltano.ExecutionResultDict].fail(
                    f"Project path is not a valid directory: {project_path}",
                )
            elt_context_obj: t.Meltano.MeltanoConfigDict = {
                "project": str(project_root),
                "extractor_name": extractor_name,
                "loader_name": loader_name,
                "status": c.Meltano.Enums.StreamStatus.INITIALIZED,
            }
            extractor_plugin_obj = plugins[0]
            loader_plugin_obj = plugins[1]
            abstractions: FlextMeltanoAbstractions = FlextMeltanoAbstractions()
            execution_result: r[t.Meltano.ELT.PipelineResult] = (
                abstractions.execute_singer_pipeline(
                    elt_context_obj,
                    extractor_plugin_obj,
                    loader_plugin_obj,
                )
            )
            if execution_result.is_failure:
                return r[t.Meltano.ExecutionResultDict].fail(
                    execution_result.error or "Pipeline execution failed",
                )
            context_data: t.Meltano.RunContextDict = {
                "project_root": str(project_root),
                "elt_context": elt_context_obj,
                "extractor_name": extractor_name,
                "loader_name": loader_name,
            }
            typed_context = m.Meltano.PipelineExecutionContext.model_validate(
                context_data,
            )
            return r[t.Meltano.ExecutionResultDict].ok(
                typed_context.model_dump(mode="python"),
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Failed to create ELT context: {e}",
            )

    def _execute_singer_runner(
        self,
        context_data: t.Meltano.ExecutionResultDict,
    ) -> r[t.ConfigurationMapping]:
        """Execute Singer runner with context data."""
        try:
            _ = m.Meltano.PipelineExecutionContext.model_validate(context_data)
            return r[t.ScalarMapping].fail("Plugin discovery not configured")
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.ScalarMapping].fail(
                f"Unexpected error in ELT pipeline: {e}",
            )

    def _log_pipeline_start(self, extractor_name: str, loader_name: str) -> r[None]:
        """Log pipeline execution start."""
        self.logger.info(
            "Executing ELT pipeline",
            extractor=extractor_name,
            loader=loader_name,
        )
        return r[None].ok(None)


__all__ = ["FlextMeltanoOrchestrationService"]
