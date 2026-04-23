"""FLEXT Meltano Pipeline Manager - Handler methods for pipeline CLI commands.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import (
    FlextMeltanoPipelineCrudOperations,
    FlextMeltanoPipelineLifecycleOperations,
    c,
    m,
    p,
    r,
    t,
    u,
)


class FlextMeltanoPipelineManager(
    FlextMeltanoPipelineCrudOperations,
    FlextMeltanoPipelineLifecycleOperations,
):
    """Pipeline manager for FLEXT Meltano CLI.

    Handles pipeline-related CLI commands using composition and r[T].
    """

    def __init__(self, cli: p.Meltano.PipelineCli) -> None:
        """Initialize pipeline manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = u.fetch_logger(__name__)

    def handle_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle pipeline command using composition."""
        if c.Meltano.CMD_HELP_OPTION in args or c.Meltano.CMD_SHORT_HELP_OPTION in args:
            self.cli.show_pipeline_help()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP)
        subcommand = args[0]
        subcommand_args = args[1:]
        return self._dispatch_pipeline(subcommand, subcommand_args)

    def _create_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Create new pipeline."""
        if not args:
            return r[str].fail(
                "Pipeline creation requires pipeline name and JSON configuration",
            )
        pipeline_name = args[0]
        config_payload: t.JsonMapping | None = None
        if len(args) >= c.Meltano.CLI_DEFAULT_MIN_ARGS_WITH_CONFIG:
            try:
                config_mapping = m.Meltano.ConfigMappingPayload.model_validate_json(
                    args[1],
                )
            except ValueError as exc:
                return r[str].fail(f"Invalid pipeline configuration JSON: {exc}")
            config_payload = config_mapping.values
        result = FlextMeltanoPipelineManager.create_pipeline(
            pipeline_name,
            config_payload,
        )
        if result.failure:
            return r[str].fail(result.error)
        self.logger.info("Pipeline created", pipeline=pipeline_name)
        return r[str].ok(result.value)

    def _delete_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Delete pipeline."""
        if not args:
            return r[str].fail("Pipeline delete requires pipeline name")
        result = FlextMeltanoPipelineManager.delete_pipeline(args[0])
        if result.failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)

    def _dispatch_pipeline(
        self,
        subcommand: str,
        args: t.StrSequence,
    ) -> p.Result[str]:
        """Dispatch pipeline operation to the matching handler."""
        match subcommand:
            case c.Meltano.PipelineCommand.CREATE:
                return self._create_pipeline(args)
            case c.Meltano.PipelineCommand.RUN:
                return self._run_pipeline(args)
            case c.Meltano.PipelineCommand.LIST:
                return self._list_pipelines()
            case c.Meltano.PipelineCommand.STATUS:
                return self._get_pipeline_status(args)
            case c.Meltano.PipelineCommand.STOP:
                return self._stop_pipeline(args)
            case c.Meltano.PipelineCommand.DELETE:
                return self._delete_pipeline(args)
            case _:
                return r[str].fail(f"Unknown pipeline command: {subcommand}")

    def _get_pipeline_status(self, args: t.StrSequence) -> p.Result[str]:
        """Get pipeline status."""
        if not args:
            return r[str].fail("Pipeline status requires pipeline name")
        status_result = FlextMeltanoPipelineManager.get_pipeline_status(args[0])
        if status_result.failure:
            return r[str].fail(status_result.error)
        self.logger.info(
            "Pipeline status",
            pipeline=args[0],
            status=status_result.value,
        )
        return r[str].ok(status_result.value)

    def _list_pipelines(self) -> p.Result[str]:
        """List pipelines."""
        result = FlextMeltanoPipelineManager.list_pipelines()
        if result.failure:
            return r[str].fail(result.error)
        self.logger.info("Configured pipelines", pipelines=", ".join(result.value))
        return r[str].ok(", ".join(result.value) or "none")

    def _run_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Run pipeline."""
        if not args:
            return r[str].fail("Pipeline execution requires pipeline name")
        pipeline_name = args[0]
        command_args = args[1:] if len(args) > 1 else None
        result = FlextMeltanoPipelineManager.execute_pipeline(
            pipeline_name,
            command_args,
        )
        if result.failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)

    def _stop_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Stop pipeline."""
        if not args:
            return r[str].fail("Pipeline stop requires pipeline name")
        result = FlextMeltanoPipelineManager.stop_pipeline(args[0])
        if result.failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)
