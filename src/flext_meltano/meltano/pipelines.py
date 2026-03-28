"""FLEXT Pipeline Orchestration Service.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import cached_property
from typing import override

from flext_core import r

from flext_meltano import FlextMeltanoAbstractions, FlextMeltanoServiceBase, t


class FlextMeltanoOrchestrationService(FlextMeltanoServiceBase):
    """Service for data pipeline orchestration.

    Delegates pipeline execution to FlextMeltanoAbstractions which wraps
    the meltano-core SDK. Methods that cannot be implemented yet raise
    NotImplementedError.
    """

    @cached_property
    def _abstractions(self) -> FlextMeltanoAbstractions:
        return FlextMeltanoAbstractions()

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute orchestration service logic."""
        return r[t.Meltano.MeltanoConfigDict].ok(self.settings.model_dump())

    def execute_pipeline(
        self,
        project_path: str,
        source_name: str,
        sink_name: str,
    ) -> r[t.Meltano.ELT.PipelineResult]:
        """Execute data pipeline.

        Args:
            project_path: Path to pipeline project
            source_name: Name of the source (extractor) component
            sink_name: Name of the sink (loader) component

        Returns:
            r containing pipeline execution results

        """
        msg = (
            "Pipeline execution requires meltano-core SDK integration: "
            f"execute_pipeline({project_path!r}, {source_name!r}, {sink_name!r})"
        )
        raise NotImplementedError(msg)


__all__ = ["FlextMeltanoOrchestrationService"]
