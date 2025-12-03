"""FLEXT Pipeline Orchestration Service - Single unified class for pipeline operations.

This module provides the FlextMeltanoOrchestrationService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with r
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from flext_core import (
    FlextResult,
    FlextService,
    t as FlextTypes,  # noqa: N812
    u,
)

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
# u is already imported from flext_core
r = FlextResult
s = FlextService
t = FlextMeltanoTypes
t_base = FlextTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
p = FlextMeltanoProtocols


class FlextMeltanoOrchestrationService(s[t.MeltanoCore.MeltanoConfigDict]):
    """Service for data pipeline operations.

    Handles pipeline execution, validation, and monitoring
    following FLEXT patterns with railway-oriented programming.
    """

    # Instance attributes for type checker
    _config: FlextMeltanoConfig
    _abstractions: FlextMeltanoAbstractions

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize pipeline service with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
        self._abstractions = FlextMeltanoAbstractions()

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
        project_obj = project_path

        # Execute synchronous steps first
        start_result = self._log_pipeline_start(source_name, sink_name)
        if start_result.is_failure:
            return r[dict[str, str]].fail(
                start_result.error or "Pipeline start failed"
            )

        plugins_result = self._find_required_plugins()
        if plugins_result.is_failure:
            return r[dict[str, str]].fail(
                plugins_result.error or "Failed to find plugins"
            )

        # Execute ELT context creation
        elt_context_result = self._create_elt_context(
            project_obj, source_name, sink_name, plugins_result.unwrap()
        )
        if elt_context_result.is_failure:
            return r[dict[str, str]].fail(
                elt_context_result.error or "Failed to create ELT context"
            )

        # Execute singer runner
        runner_result = self._execute_singer_runner(elt_context_result.unwrap())
        if runner_result.is_failure:
            return r[dict[str, str]].fail(
                runner_result.error or "Failed to execute singer runner"
            )

        # Execute final synchronous step
        final_result = self._build_pipeline_result(
            source_name,
            sink_name,
            runner_result.unwrap(),
        )
        return final_result.or_else_get(
            lambda: r[dict[str, str]].fail(
                f"Pipeline execution failed for {source_name} -> {sink_name}"
            )
        )

    # Private helper methods (extracted from adapters.py)

    def _log_pipeline_start(
        self, extractor_name: str, loader_name: str
    ) -> r[None]:
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

    def _create_elt_context(
        self,
        project_path: str,
        extractor_name: str,
        loader_name: str,
        plugins: tuple[object, object],
    ) -> r[t.MeltanoCore.ExecutionResultDict]:
        """Create ELT context for pipeline execution."""
        try:
            # Use abstraction layer to create ELT context
            elt_context_result = self._abstractions.create_elt_context(
                cast("object", project_path), extractor_name, loader_name
            )

            if elt_context_result.is_failure:
                return r[t.MeltanoCore.ExecutionResultDict].fail(
                    f"Failed to create ELT context: {elt_context_result.error}"
                )

            elt_context_obj = elt_context_result.unwrap()

            # Create plugin objects from the plugins tuple
            extractor_plugin_obj = plugins[0]
            loader_plugin_obj = plugins[1]

            # Execute singer pipeline
            execution_result = self._abstractions.execute_singer_pipeline(
                elt_context_obj,
                extractor_plugin_obj,
                loader_plugin_obj,
            )

            if execution_result.is_failure:
                return r[dict[str, object]].fail(
                    execution_result.error or "Pipeline execution failed"
                )

            if elt_context_result.is_failure:
                return r[dict[str, object]].fail(
                    elt_context_result.error or "Failed to create ELT context"
                )

            elt_context_result.unwrap()

            context_data: t.MeltanoCore.RunContextDict = {
                "t.Dbt.Project": "t.Dbt.Project",
                "elt_context": "elt_context",
                "extractor_plugin": "extractor_plugin",
                "loader_plugin": "loader_plugin",
            }

            return r[dict[str, object]].ok(context_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, object]].fail(
                f"Failed to create ELT context: {e}"
            )

    def _execute_singer_runner(
        self, context_data: t.MeltanoCore.RunContextDict
    ) -> r[dict[str, FlextTypes.JsonValue]]:
        """Execute Singer runner with context data."""
        try:
            # Extract context data
            elt_context_obj = context_data["elt_context"]
            extractor_plugin_obj = context_data["extractor_plugin"]
            loader_plugin_obj = context_data["loader_plugin"]

            # Use duck typing for plugin validation
            if not hasattr(extractor_plugin_obj, "name") or not hasattr(
                extractor_plugin_obj, "type"
            ):
                return r[dict[str, FlextTypes.JsonValue]].fail(
                    "Invalid extractor plugin: missing required attributes"
                )
            if not hasattr(loader_plugin_obj, "name") or not hasattr(
                loader_plugin_obj, "type"
            ):
                return r[dict[str, FlextTypes.JsonValue]].fail(
                    "Invalid loader plugin: missing required attributes"
                )

            # Use abstraction layer to execute Singer pipeline
            execution_result = self._abstractions.execute_singer_pipeline(
                cast("dict[str, object]", elt_context_obj),
                extractor_plugin_obj,
                loader_plugin_obj,
            )

            if execution_result.is_failure:
                return r[dict[str, FlextTypes.JsonValue]].fail(
                    execution_result.error or "Pipeline execution failed"
                )

            # Add execution results to context
            context_data["execution_completed"] = True
            context_data["execution_result"] = execution_result.unwrap()

            return r[dict[str, FlextTypes.JsonValue]].ok(
                cast("dict[str, FlextTypes.JsonValue]", context_data)
            )

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, FlextTypes.JsonValue]].fail(
                f"Unexpected error in ELT pipeline: {e}"
            )

    def _build_pipeline_result(
        self,
        extractor_name: str,
        loader_name: str,
        context_data: Mapping[str, object],
    ) -> r[dict[str, str]]:
        """Build successful pipeline result."""
        try:
            # Extract context data
            elt_context_obj = context_data["elt_context"]
            project_obj = context_data["t.Dbt.Project"]
            execution_result_raw = u.get(context_data, "execution_result", default={})
            execution_result = u.guard(execution_result_raw, dict, return_value=True) or {}

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
                filtered_items = u.filter(
                    list(execution_result.items()) if isinstance(execution_result, Mapping) else [],
                    lambda item: isinstance(item[1], (str, int, bool)),
                )
                if filtered_items:
                    pipeline_result.update({
                        k: str(v) for k, v in filtered_items
                    })

            self.logger.info(
                "ELT pipeline executed successfully",
                extractor=extractor_name,
                loader=loader_name,
            )

            return r[dict[str, str]].ok(pipeline_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, str]].fail(
                f"Failed to build pipeline result: {e}"
            )


__all__ = [
    "FlextMeltanoOrchestrationService",
]
