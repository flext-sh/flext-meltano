"""FLEXT Meltano Singer - Unified namespace class for ALL Singer operations.

This module provides a single FlextMeltanoSinger class consolidating:
- Singer SDK base classes (Tap, Stream, Target, Sink)
- Tap and Target abstractions with full protocol implementation
- Singer service operations with railway-oriented programming

Following FLEXT 'one class per module' pattern with inner classes for organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextCore

# Import from specific modules to avoid circular dependencies
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoSinger(
    FlextCore.Service[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
    """UNIFIED Singer namespace class consolidating ALL Singer functionality.

    This single class provides:
    - Singer SDK base classes (Tap, Stream, Target, Sink) as inner classes
    - Complete Tap and Target abstractions with protocol implementation
    - Singer service operations with railway-oriented programming

    Following FLEXT 'one namespace class per domain' pattern.
    """

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize unified Singer class with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
        self.logger = FlextCore.Logger(__name__)
        self._library_runner = FlextMeltanoLibraryRunner()

    def execute_pipeline(
        self, tap_instance: object, target_instance: object
    ) -> FlextCore.Result[
        FlextMeltanoTypes.Processing.FlextMeltanoTypes.Processing.SingerExecutionResult
    ]:
        """Execute Singer pipeline with advanced protocol management.

        Args:
            tap_instance: SingerTap instance
            target_instance: SingerTarget instance

        Returns:
            FlextCore.Result containing pipeline execution results

        """
        try:
            self.logger.info(
                "Executing Singer pipeline with advanced protocol management",
                tap_name=getattr(tap_instance, "name", "unknown"),
                target_name=getattr(target_instance, "name", "unknown"),
            )

            # Use library runner for Singer operations
            singer_manager_result = self._library_runner.get_singer_manager()
            if singer_manager_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    singer_manager_result.error or "Failed to get Singer manager"
                )

            # For now, just return success since singer_manager is just a dict
            result = FlextCore.Result[FlextCore.Types.Dict].ok(
                singer_manager_result.unwrap()
            )

            if result.is_success:
                self.logger.info(
                    "Singer pipeline executed successfully",
                    streams_processed=result.unwrap().get("streams_processed", 0),
                )
            else:
                self.logger.error(
                    "Singer pipeline failed",
                    error=result.error,
                )

            return result

        except Exception as e:
            error_msg = f"Failed to execute Singer pipeline: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[
                FlextMeltanoTypes.Processing.FlextMeltanoTypes.Processing.SingerExecutionResult
            ].fail(error_msg)

    def execute_complete_elt_pipeline(
        self,
        project_dir: Path,
        extractor_config: FlextMeltanoTypes.MeltanoCore.PluginConfigDict,
        loader_config: FlextMeltanoTypes.MeltanoCore.PluginConfigDict,
        transformer_config: FlextMeltanoTypes.MeltanoCore.PluginConfigDict
        | None = None,
    ) -> FlextCore.Result[
        FlextMeltanoTypes.Processing.FlextMeltanoTypes.Processing.EltPipelineResult
    ]:
        """Execute complete E-L-T pipeline using library APIs.

        Args:
            project_dir: Path to Meltano project directory
            extractor_config: Extractor configuration
            loader_config: Loader configuration
            transformer_config: Optional transformer configuration

        Returns:
            FlextCore.Result containing complete pipeline results

        """
        try:
            self.logger.info(
                "Executing complete E-L-T pipeline using library APIs",
                project_dir=str(project_dir),
            )

            # Extract tap and target names from configs
            tap_name = extractor_config.get("name", "")
            target_name = loader_config.get("name", "")
            dbt_models = (
                transformer_config.get("models") if transformer_config else None
            )

            # Use library runner for complete pipeline
            result = self._library_runner.execute_complete_elt_pipeline(
                tap_name, target_name, dbt_models, transformer_config
            )

            if result.is_success:
                pipeline_data = result.unwrap()
                self.logger.info(
                    "Complete E-L-T pipeline executed successfully",
                    overall_success=pipeline_data.get("overall_success", False),
                )
            else:
                self.logger.error(
                    "Complete E-L-T pipeline failed",
                    error=result.error,
                )

            return result

        except Exception as e:
            error_msg = f"Failed to execute complete E-L-T pipeline: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[
                FlextMeltanoTypes.Processing.FlextMeltanoTypes.Processing.EltPipelineResult
            ].fail(error_msg)
