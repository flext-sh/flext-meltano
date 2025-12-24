"""FLEXT Pipeline Orchestration Service - Single unified class for pipeline operations.

This module provides the FlextMeltanoOrchestrationService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with r
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext import (
    FlextService,
)
    FlextResult,
    u

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.settings import FlextMeltanoSettings

# Import aliases for concise usage
r = FlextResult
s = FlextService
c = FlextMeltanoConstants
m = FlextMeltanoModels


class FlextMeltanoOrchestrationService(s[dict[str, str]]):
    """Service for data pipeline operations.

    Handles pipeline execution, validation, and monitoring
    following FLEXT patterns with railway-oriented programming.
    """

    # Instance attributes for type checker
    _abstractions: FlextMeltanoAbstractions

    def __init__(self, config: FlextMeltanoSettings | None = None) -> None:
        """Initialize pipeline service with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoSettings()
        self._abstractions = FlextMeltanoAbstractions()

    @staticmethod
    def execute() -> r[dict[str, str]]:
        """Execute the main domain operation (Service protocol).

        Returns:
        r[dict[str, str]]: Pipeline execution results or failure with error

        """
        return r.fail(
            "Pipeline execution requires specific parameters. Use execute_pipeline() method instead.",
        )

    def execute_pipeline(
        self,
        project_path: str,
        source_name: str,
        sink_name: str,
    ) -> r[dict[str, str]]:
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
        # RAILWAY PATTERN: Chain all pipeline operations with automatic error handling
        project_obj = {"path": project_path, "name": "meltano_project"}

        # Execute synchronous steps first
        start_result = self._log_pipeline_start(source_name, sink_name)
        if start_result.is_failure:
            return r[dict[str, str]].fail(start_result.error or "Pipeline start failed")

        plugins_result = FlextMeltanoOrchestrationService._find_required_plugins()
        if plugins_result.is_failure:
            return r[dict[str, str]].fail(
                plugins_result.error or "Failed to find plugins",
            )

        # Execute ELT context creation
        elt_context_result = FlextMeltanoOrchestrationService._create_elt_context(
            project_obj,
            source_name,
            sink_name,
            plugins_result.value,
        )
        if elt_context_result.is_failure:
            return r[dict[str, str]].fail(
                elt_context_result.error or "Failed to create ELT context",
            )

        # Execute singer runner
        runner_result = FlextMeltanoOrchestrationService._execute_singer_runner(
            elt_context_result.value,
        )
        if runner_result.is_failure:
            return r[dict[str, str]].fail(
                runner_result.error or "Failed to execute singer runner",
            )

        # Execute final synchronous step
        final_result = self._build_pipeline_result(
            source_name,
            sink_name,
            runner_result.value,
        )
        if final_result.is_failure:
            return r[dict[str, str]].fail(
                final_result.error
                or f"Pipeline execution failed for {source_name} -> {sink_name}",
            )
        return final_result

    # Private helper methods (extracted from adapters.py)

    def _log_pipeline_start(self, extractor_name: str, loader_name: str) -> r[None]:
        """Log pipeline execution start."""
        self.logger.info(
            "Executing ELT pipeline",
            extractor=extractor_name,
            loader=loader_name,
        )
        return r.ok(None)

    @staticmethod
    def _find_required_plugins() -> r[tuple[object, object]]:
        """Find required plugins in t.Dbt.Project."""
        # Simplified implementation - would need actual plugin discovery
        return r[tuple[object, object]].ok((object(), object()))

    @staticmethod
    def _create_elt_context(
        project: dict[str, str],
        extractor_name: str,
        loader_name: str,
        plugins: tuple[object, object],
    ) -> r[dict[str, object]]:
        """Create ELT context for pipeline execution."""
        try:
            # Create a simple ELT context for now (placeholder implementation)
            elt_context_result = r[dict[str, object]].ok({
                "project": project,
                "extractor": extractor_name,
                "loader": loader_name,
                "plugins": plugins,
            })
            elt_context_obj = elt_context_result.value

            # Create plugin objects from the plugins tuple
            extractor_plugin_obj = plugins[0]
            loader_plugin_obj = plugins[1]

            # Create a simple execution result for now (placeholder implementation)
            execution_result = r[dict[str, object]].ok({
                "status": "completed",
                "extractor": extractor_name,
                "loader": loader_name,
            })

            if execution_result.is_failure:
                return r[dict[str, object]].fail(
                    execution_result.error or "Pipeline execution failed",
                )

            context_data: dict[str, object] = {
                "project": project,
                "elt_context": elt_context_obj,
                "extractor_plugin": extractor_plugin_obj,
                "loader_plugin": loader_plugin_obj,
                "execution_result": execution_result.value,
            }

            return r[dict[str, object]].ok(context_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, object]].fail(f"Failed to create ELT context: {e}")

    @staticmethod
    def _execute_singer_runner(
        context_data: dict[str, object],
    ) -> r[dict[str, object]]:
        """Execute Singer runner with context data."""
        try:
            # Extract context data
            _elt_context_obj = context_data["elt_context"]
            extractor_plugin_obj = context_data["extractor_plugin"]
            loader_plugin_obj = context_data["loader_plugin"]

            # Use duck typing for plugin validation
            if not hasattr(extractor_plugin_obj, "name") or not hasattr(
                extractor_plugin_obj,
                "type",
            ):
                return r[dict[str, object]].fail(
                    "Invalid extractor plugin: missing required attributes",
                )
            if not hasattr(loader_plugin_obj, "name") or not hasattr(
                loader_plugin_obj,
                "type",
            ):
                return r[dict[str, object]].fail(
                    "Invalid loader plugin: missing required attributes",
                )

            # Add execution results to context
            context_data["execution_completed"] = True
            context_data["execution_result"] = {"status": "completed"}

            return r[dict[str, object]].ok(context_data)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, object]].fail(f"Unexpected error in ELT pipeline: {e}")

    def _build_pipeline_result(
        self,
        extractor_name: str,
        loader_name: str,
        context_data: dict[str, object],
    ) -> r[dict[str, str]]:
        """Build successful pipeline result."""
        try:
            # Extract context data
            elt_context_obj = context_data["elt_context"]
            project_obj = context_data["project"]
            execution_result_raw = u.get(context_data, "execution_result", default={})
            execution_result = (
                execution_result_raw if isinstance(execution_result_raw, dict) else {}
            )

            # Build pipeline result using available data
            pipeline_result: dict[str, str] = {
                "success": "true",
                "extractor": extractor_name,
                "loader": loader_name,
                "execution_method": "singer_runner_abstracted",
                "project_root": str(getattr(project_obj, "root", "unknown")),
                "run_id": str(getattr(elt_context_obj, "run_id", "unknown")),
            }

            # Add execution result data if available
            if execution_result:
                pipeline_result.update({
                    k: str(v)
                    for k, v in execution_result.items()
                    if isinstance(v, (str, int, bool))
                })

            self.logger.info(
                "ELT pipeline executed successfully",
                extractor=extractor_name,
                loader=loader_name,
            )

            return r[dict[str, str]].ok(pipeline_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, str]].fail(f"Failed to build pipeline result: {e}")


__all__ = [
    "FlextMeltanoOrchestrationService",
]
