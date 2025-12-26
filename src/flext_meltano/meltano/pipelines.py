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
from pathlib import Path

from flext_core import (
    FlextResult,
    FlextService,
    t as t_core,
)

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
# u is already imported from flext_core
r = FlextResult
s = FlextService
t_base = t_core
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
p = FlextMeltanoProtocols


class FlextMeltanoOrchestrationService(s[t.MeltanoCore.MeltanoConfigDict]):
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
            return r[dict[str, str]].fail(start_result.error or "Pipeline start failed")

        plugins_result = self._find_required_plugins()
        if plugins_result.is_failure:
            return r[dict[str, str]].fail(
                plugins_result.error or "Failed to find plugins",
            )

        # Execute ELT context creation
        elt_context_result = self._create_elt_context(
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
        runner_result = self._execute_singer_runner(elt_context_result.value)
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
    def _find_required_plugins() -> r[
        tuple[
            p.Meltano.PluginProtocol[t.JsonValue], p.Meltano.PluginProtocol[t.JsonValue]
        ]
    ]:
        """Find required plugins in t.Dbt.Project."""

        # Simplified implementation - would need actual plugin discovery
        # Create simple objects that satisfy the PluginProtocol
        class MockPlugin:
            """Simple plugin implementation satisfying PluginProtocol."""

            def __init__(self, name: str) -> None:
                self.name = name
                self.default_variant: str | None = "default"
                self.variants: dict[str, t.JsonValue] | None = None

            def get_config(self) -> dict[str, t.JsonValue]:
                """Get plugin configuration."""
                return {}

            def validate_config(self, config: dict[str, t.JsonValue]) -> bool:
                """Validate plugin configuration."""
                _ = config  # Protocol requirement
                return True

            def execute(self, *args: t.JsonValue) -> t.JsonValue:
                """Execute plugin with given arguments."""
                _ = args  # Protocol requirement
                return {}

        extractor = MockPlugin(name="tap-mock")
        loader = MockPlugin(name="target-mock")
        return r[
            tuple[
                p.Meltano.PluginProtocol[t.JsonValue],
                p.Meltano.PluginProtocol[t.JsonValue],
            ]
        ].ok((extractor, loader))

    def _create_elt_context(
        self,
        project_path: str,
        extractor_name: str,
        loader_name: str,
        plugins: tuple[
            p.Meltano.PluginProtocol[t.JsonValue], p.Meltano.PluginProtocol[t.JsonValue]
        ],
    ) -> r[t.MeltanoCore.ExecutionResultDict]:
        """Create ELT context for pipeline execution."""
        try:
            # Create a simple project object that satisfies MeltanoProjectProtocol
            class MockProject:
                """Simple project implementation satisfying MeltanoProjectProtocol."""

                def __init__(self, root_dir: Path) -> None:
                    self._root_dir = root_dir

                @property
                def root_dir(self) -> Path:
                    """Get project root directory."""
                    return self._root_dir

                def find_plugins(self, plugin_type: str) -> list[t.JsonValue]:
                    """Find plugins of specified type."""
                    _ = plugin_type  # Protocol requirement
                    return []

            project_obj: p.Meltano.MeltanoProjectProtocol = MockProject(
                root_dir=Path(project_path)
            )

            elt_context_result = self._abstractions.create_elt_context(
                project_obj,
                extractor_name,
                loader_name,
            )

            if elt_context_result.is_failure:
                return r[t.MeltanoCore.ExecutionResultDict].fail(
                    f"Failed to create ELT context: {elt_context_result.error}",
                )

            elt_context_obj = elt_context_result.value

            # Extract plugin objects from the plugins tuple
            extractor_plugin_obj = plugins[0]
            loader_plugin_obj = plugins[1]

            # Execute singer pipeline
            execution_result = self._abstractions.execute_singer_pipeline(
                elt_context_obj,
                extractor_plugin_obj,
                loader_plugin_obj,
            )

            if execution_result.is_failure:
                return r[t.MeltanoCore.ExecutionResultDict].fail(
                    execution_result.error or "Pipeline execution failed",
                )

            # Build context_data with properly typed JsonValue entries
            # Store object references as string representations for JSON compatibility
            context_data: t.MeltanoCore.RunContextDict = {
                "project_root": str(project_obj.root_dir),
                "elt_context": elt_context_obj,
                "extractor_name": extractor_name,
                "loader_name": loader_name,
            }

            return r[t.MeltanoCore.ExecutionResultDict].ok(context_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.MeltanoCore.ExecutionResultDict].fail(
                f"Failed to create ELT context: {e}"
            )

    def _execute_singer_runner(
        self,
        context_data: t.MeltanoCore.RunContextDict,
    ) -> r[dict[str, t_core.JsonValue]]:
        """Execute Singer runner with context data."""
        try:
            # Extract context data
            elt_context_obj = context_data.get("elt_context")
            extractor_name = context_data.get("extractor_name")
            loader_name = context_data.get("loader_name")

            # Type narrowing: verify elt_context_obj is a properly typed dict
            if not isinstance(elt_context_obj, dict):
                return r[dict[str, t_core.JsonValue]].fail(
                    "Invalid ELT context: expected dict",
                )

            # Type narrowing for names
            if not isinstance(extractor_name, str) or not isinstance(loader_name, str):
                return r[dict[str, t_core.JsonValue]].fail(
                    "Invalid extractor/loader names: expected str",
                )

            # Create properly typed MeltanoConfigDict from elt_context_obj
            typed_elt_context: t.MeltanoCore.MeltanoConfigDict = {}
            for key, value in elt_context_obj.items():
                if isinstance(value, (str, int, float, bool, type(None), list, dict)):
                    typed_elt_context[key] = value

            # For simplified implementation, create mock plugins
            # In real implementation, would retrieve actual plugins
            class MockPlugin:
                """Simple plugin for execution."""

                def __init__(self, name: str) -> None:
                    self.name = name
                    self.default_variant: str | None = "default"
                    self.variants: dict[str, t.JsonValue] | None = None

                def get_config(self) -> dict[str, t.JsonValue]:
                    """Get plugin configuration."""
                    return {}

                def validate_config(self, config: dict[str, t.JsonValue]) -> bool:
                    """Validate plugin configuration."""
                    _ = config  # Protocol requirement
                    return True

                def execute(self, *args: t.JsonValue) -> t.JsonValue:
                    """Execute plugin with given arguments."""
                    _ = args  # Protocol requirement
                    return {}

            extractor_plugin_obj: p.Meltano.PluginProtocol[t.JsonValue] = MockPlugin(
                name=extractor_name
            )
            loader_plugin_obj: p.Meltano.PluginProtocol[t.JsonValue] = MockPlugin(
                name=loader_name
            )

            execution_result = self._abstractions.execute_singer_pipeline(
                typed_elt_context,
                extractor_plugin_obj,
                loader_plugin_obj,
            )

            if execution_result.is_failure:
                return r[dict[str, t_core.JsonValue]].fail(
                    execution_result.error or "Pipeline execution failed",
                )

            # Add execution results to context
            context_data["execution_completed"] = True
            context_data["execution_result"] = execution_result.value

            # Build properly typed result dict with JSON-compatible values
            result_data: dict[str, t_core.JsonValue] = {}
            for key, value in context_data.items():
                # Type narrowing for JSON-serializable values
                if isinstance(value, (str, int, float, bool, type(None))):
                    result_data[key] = value
                elif isinstance(value, dict):
                    # Recursively ensure dict values are JSON-compatible
                    json_dict: dict[str, t_core.JsonValue] = {
                        k: v
                        for k, v in value.items()
                        if isinstance(v, (str, int, float, bool, type(None)))
                    }
                    result_data[key] = json_dict
                elif isinstance(value, list):
                    # Filter list to only JSON-compatible items
                    json_list: list[t_core.JsonValue] = [
                        item
                        for item in value
                        if isinstance(item, (str, int, float, bool, type(None)))
                    ]
                    result_data[key] = json_list

            return r[dict[str, t_core.JsonValue]].ok(result_data)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, t_core.JsonValue]].fail(
                f"Unexpected error in ELT pipeline: {e}",
            )

    def _build_pipeline_result(
        self,
        extractor_name: str,
        loader_name: str,
        context_data: Mapping[str, t_core.JsonValue],
    ) -> r[dict[str, str]]:
        """Build successful pipeline result."""
        try:
            # Extract context data with type narrowing
            project_root_raw = context_data.get("project_root")
            execution_result_raw = context_data.get("execution_result")

            # Type narrowing
            project_root = (
                str(project_root_raw) if project_root_raw is not None else "unknown"
            )

            # Build pipeline result using available data
            pipeline_result: dict[str, str] = {
                "success": "true",
                "extractor": extractor_name,
                "loader": loader_name,
                "execution_method": "singer_runner_abstracted",
                "project_root": project_root,
                "run_id": "unknown",  # Would be extracted from elt_context in real implementation
            }

            # Add execution result data if available
            if isinstance(execution_result_raw, dict):
                # Filter for string-convertible values
                for key, value in execution_result_raw.items():
                    if isinstance(value, (str, int, bool, float)):
                        pipeline_result[key] = str(value)

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
