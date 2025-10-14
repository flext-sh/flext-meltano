"""FLEXT Meltano Pipeline Service - Single unified class for pipeline operations.

This module provides the FlextMeltanoPipelineService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextCore.Result
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import cast

from flext_core import FlextCore

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoPipelineService(
    FlextCore.Service[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
    """Service for Meltano pipeline operations.

    Handles ELT pipeline execution, validation, and monitoring
    following FLEXT patterns with railway-oriented programming.
    """

    # Instance attributes for type checker
    _config: FlextMeltanoConfig
    logger: FlextCore.Logger
    _abstractions: FlextMeltanoAbstractions

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize pipeline service with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
        self.logger = FlextCore.Logger(__name__)
        self._abstractions = FlextMeltanoAbstractions()

    def execute_pipeline(
        self,
        project: FlextMeltanoTypes.Dbt.Project,
        extractor_name: str,
        loader_name: str,
    ) -> FlextCore.Result[FlextCore.Types.StringDict]:
        """Execute ELT pipeline using railway-oriented programming.

        Consolidates ELTCoordinator class functionality into unified service method
        using FlextCore.Result railway patterns to eliminate nested error handling
        and provide composable pipeline execution.

        Args:
            project: Meltano FlextMeltanoTypes.Dbt.Project instance
            extractor_name: Name of the extractor plugin
            loader_name: Name of the loader plugin

        Returns:
            FlextCore.Result containing pipeline execution results

        """
        # RAILWAY PATTERN: Chain all pipeline operations with automatic error handling
        project_obj = project

        # Execute synchronous steps first
        start_result = self._log_pipeline_start(extractor_name, loader_name)
        if start_result.is_failure:
            return FlextCore.Result[FlextCore.Types.StringDict].fail(
                start_result.error or "Pipeline start failed"
            )

        plugins_result = self._find_required_plugins()
        if plugins_result.is_failure:
            return FlextCore.Result[FlextCore.Types.StringDict].fail(
                plugins_result.error or "Failed to find plugins"
            )

        # Execute ELT context creation
        elt_context_result = self._create_elt_context(
            project_obj, extractor_name, loader_name, plugins_result.unwrap()
        )
        if elt_context_result.is_failure:
            return FlextCore.Result[FlextCore.Types.StringDict].fail(
                elt_context_result.error or "Failed to create ELT context"
            )

        # Execute singer runner
        runner_result = self._execute_singer_runner(elt_context_result.unwrap())
        if runner_result.is_failure:
            return FlextCore.Result[FlextCore.Types.StringDict].fail(
                runner_result.error or "Failed to execute singer runner"
            )

        # Execute final synchronous step
        final_result = self._build_pipeline_result(
            extractor_name,
            loader_name,
            cast(
                "FlextMeltanoTypes.MeltanoCore.RunContextDict", runner_result.unwrap()
            ),
        )
        return final_result.or_else_get(
            lambda: FlextCore.Result[FlextCore.Types.StringDict].fail(
                f"Pipeline execution failed for {extractor_name} -> {loader_name}"
            )
        )

    # Private helper methods (extracted from adapters.py)

    def _log_pipeline_start(
        self, extractor_name: str, loader_name: str
    ) -> FlextCore.Result[None]:
        """Log pipeline execution start."""
        self.logger.info(
            "Executing ELT pipeline",
            extractor=extractor_name,
            loader=loader_name,
        )
        return FlextCore.Result.ok(data=None)

    def _find_required_plugins(
        self,
    ) -> FlextCore.Result[tuple[object, object]]:
        """Find required plugins in FlextMeltanoTypes.Dbt.Project."""
        # Simplified implementation - would need actual plugin discovery
        return FlextCore.Result[tuple[object, object]].ok(data=(object(), object()))

    def _create_elt_context(
        self,
        project: FlextMeltanoTypes.Dbt.Project,
        extractor_name: str,
        loader_name: str,
        plugins: tuple[object, object],
    ) -> FlextCore.Result[FlextMeltanoTypes.MeltanoCore.ExecutionResultDict]:
        """Create ELT context for pipeline execution."""
        try:
            # Use abstraction layer to create ELT context
            elt_context_result = self._abstractions.create_elt_context(
                project, extractor_name, loader_name
            )

            if elt_context_result.is_failure:
                return FlextCore.Result[
                    FlextMeltanoTypes.MeltanoCore.ExecutionResultDict
                ].fail(f"Failed to create ELT context: {elt_context_result.error}")

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
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    execution_result.error or "Pipeline execution failed"
                )

            if elt_context_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    elt_context_result.error or "Failed to create ELT context"
                )

            elt_context_result.unwrap()

            context_data: FlextMeltanoTypes.MeltanoCore.RunContextDict = {
                "FlextMeltanoTypes.Dbt.Project": "FlextMeltanoTypes.Dbt.Project",
                "elt_context": "elt_context",
                "extractor_plugin": "extractor_plugin",
                "loader_plugin": "loader_plugin",
            }

            return FlextCore.Result[FlextCore.Types.Dict].ok(data=context_data)
        except Exception as e:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Failed to create ELT context: {e}"
            )

    def _execute_singer_runner(
        self, context_data: FlextMeltanoTypes.MeltanoCore.RunContextDict
    ) -> FlextCore.Result[dict[str, FlextCore.Types.JsonValue]]:
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
                return FlextCore.Result[dict[str, FlextCore.Types.JsonValue]].fail(
                    "Invalid extractor plugin: missing required attributes"
                )
            if not hasattr(loader_plugin_obj, "name") or not hasattr(
                loader_plugin_obj, "type"
            ):
                return FlextCore.Result[dict[str, FlextCore.Types.JsonValue]].fail(
                    "Invalid loader plugin: missing required attributes"
                )

            # Use abstraction layer to execute Singer pipeline
            execution_result = self._abstractions.execute_singer_pipeline(
                cast("FlextMeltanoTypes.MeltanoCore.ELTContext", elt_context_obj),
                cast("FlextMeltanoTypes.Plugin.ProjectPlugin", extractor_plugin_obj),
                cast("FlextMeltanoTypes.Plugin.ProjectPlugin", loader_plugin_obj),
            )

            if execution_result.is_failure:
                return FlextCore.Result[dict[str, FlextCore.Types.JsonValue]].fail(
                    execution_result.error or "Pipeline execution failed"
                )

            # Add execution results to context
            context_data["execution_completed"] = True
            context_data["execution_result"] = execution_result.unwrap()

            return FlextCore.Result[dict[str, FlextCore.Types.JsonValue]].ok(
                cast("dict[str, FlextCore.Types.JsonValue]", context_data)
            )

        except Exception as e:
            return FlextCore.Result[dict[str, FlextCore.Types.JsonValue]].fail(
                f"Unexpected error in ELT pipeline: {e}"
            )

    def _build_pipeline_result(
        self,
        extractor_name: str,
        loader_name: str,
        context_data: FlextMeltanoTypes.MeltanoCore.RunContextDict,
    ) -> FlextCore.Result[FlextCore.Types.StringDict]:
        """Build successful pipeline result."""
        try:
            # Extract context data
            elt_context_obj = context_data["elt_context"]
            project_obj = context_data["FlextMeltanoTypes.Dbt.Project"]
            execution_result = context_data.get("execution_result", {})

            # Build pipeline result using available data
            pipeline_result: FlextCore.Types.StringDict = {
                "success": "true",
                "extractor": extractor_name,
                "loader": loader_name,
                "execution_method": "singer_runner_abstracted",
                "project_root": str(getattr(project_obj, "root", "unknown")),
                "run_id": str(getattr(elt_context_obj, "run_id", "unknown")),
            }

            # Add execution result data if available
            if isinstance(execution_result, dict):
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

            return FlextCore.Result[FlextCore.Types.StringDict].ok(pipeline_result)
        except Exception as e:
            return FlextCore.Result[FlextCore.Types.StringDict].fail(
                f"Failed to build pipeline result: {e}"
            )


__all__ = [
    "FlextMeltanoPipelineService",
]
