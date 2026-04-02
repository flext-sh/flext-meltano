"""FLEXT Meltano Pipeline Manager - Handler methods for pipeline CLI commands.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Protocol

from flext_core import FlextLogger, r

from flext_meltano import (
    FlextMeltanoPipelineCrudOperations,
    FlextMeltanoPipelineLifecycleOperations,
    c,
    m,
    t,
    u,
)


class _PipelineCli(Protocol):
    """Protocol for pipeline CLI help display."""

    def show_pipeline_help(self) -> None: ...


class FlextMeltanoPipelineManager(
    FlextMeltanoPipelineCrudOperations,
    FlextMeltanoPipelineLifecycleOperations,
):
    """Pipeline manager for FLEXT Meltano CLI.

    Handles pipeline-related CLI commands using composition and r[T].
    """

    def __init__(self, cli: _PipelineCli) -> None:
        """Initialize pipeline manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle pipeline command using composition."""
        if u.Meltano.is_help_request(args):
            self.cli.show_pipeline_help()
            return r[str].ok(c.Meltano.Enums.ExecutorCommand.HELP)
        subcommand = args[0]
        subcommand_args = args[1:]
        handler_result = self._get_pipeline_handler(subcommand)
        if handler_result.is_failure:
            return r[str].fail(handler_result.error)
        return handler_result.value(subcommand_args)

    def _create_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Create new pipeline."""
        if not _args:
            return r[str].fail(
                "Pipeline creation requires pipeline name and JSON configuration",
            )
        pipeline_name = _args[0]
        config_payload: (
            Mapping[
                str,
                t.Scalar
                | Sequence[t.Scalar | None]
                | Mapping[str, t.Scalar | None]
                | None,
            ]
            | None
        ) = None
        if len(_args) >= c.Meltano.CliDefaults.MIN_ARGS_WITH_CONFIG:
            try:
                config_mapping = m.Meltano.ConfigMappingPayload.model_validate_json(
                    _args[1],
                )
            except ValueError as exc:
                return r[str].fail(f"Invalid pipeline configuration JSON: {exc}")
            config_payload = config_mapping.values
        result = FlextMeltanoPipelineManager.create_pipeline(
            pipeline_name,
            config_payload,
        )
        if result.is_failure:
            return r[str].fail(result.error)
        self.logger.info("Pipeline created", pipeline=pipeline_name)
        return r[str].ok(result.value)

    def _delete_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Delete pipeline."""
        if not _args:
            return r[str].fail("Pipeline delete requires pipeline name")
        result = FlextMeltanoPipelineManager.delete_pipeline(_args[0])
        if result.is_failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)

    def _get_pipeline_handler(
        self,
        subcommand: str,
    ) -> r[Callable[[t.StrSequence], r[str]]]:
        """Get pipeline operation handler."""
        operation_map: Mapping[str, Callable[[t.StrSequence], r[str]]] = {
            c.Meltano.Enums.PipelineCommand.CREATE: self._create_pipeline,
            c.Meltano.Enums.PipelineCommand.RUN: self._run_pipeline,
            c.Meltano.Enums.PipelineCommand.LIST: self._list_pipelines,
            c.Meltano.Enums.PipelineCommand.STATUS: self._get_pipeline_status,
            c.Meltano.Enums.PipelineCommand.STOP: self._stop_pipeline,
            c.Meltano.Enums.PipelineCommand.DELETE: self._delete_pipeline,
        }
        handler = operation_map.get(subcommand)
        if handler is None:
            return r[Callable[[t.StrSequence], r[str]]].fail(
                f"Unknown pipeline command: {subcommand}",
            )
        return r[Callable[[t.StrSequence], r[str]]].ok(handler)

    def _get_pipeline_status(self, _args: t.StrSequence) -> r[str]:
        """Get pipeline status."""
        if not _args:
            return r[str].fail("Pipeline status requires pipeline name")
        status_result = FlextMeltanoPipelineManager.get_pipeline_status(_args[0])
        if status_result.is_failure:
            return r[str].fail(status_result.error)
        self.logger.info(
            "Pipeline status",
            pipeline=_args[0],
            status=status_result.value,
        )
        return r[str].ok(status_result.value)

    def _list_pipelines(self, _args: t.StrSequence) -> r[str]:
        """List pipelines."""
        result = FlextMeltanoPipelineManager.list_pipelines()
        if result.is_failure:
            return r[str].fail(result.error)
        self.logger.info("Configured pipelines", pipelines=", ".join(result.value))
        return r[str].ok(", ".join(result.value) or "none")

    def _run_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Run pipeline."""
        if not _args:
            return r[str].fail("Pipeline execution requires pipeline name")
        pipeline_name = _args[0]
        command_args = _args[1:] if len(_args) > 1 else None
        result = FlextMeltanoPipelineManager.execute_pipeline(
            pipeline_name,
            command_args,
        )
        if result.is_failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)

    def _stop_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Stop pipeline."""
        if not _args:
            return r[str].fail("Pipeline stop requires pipeline name")
        result = FlextMeltanoPipelineManager.stop_pipeline(_args[0])
        if result.is_failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)
