"""Singer CLI Translator — MRO mixin for FlextMeltano facade.

Converts Pydantic parameter models to Singer SDK CLI commands.
Moved from singer/translator.py (already stateless static class).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t, u


class FlextMeltanoSingerCliTranslator(FlextMeltanoServiceBase):
    """Translates Pydantic models to Singer SDK CLI commands.

    Composable via MRO on FlextMeltano facade.
    """

    @staticmethod
    def execute_singer_command(
        command: t.StrSequence,
        input_data: str | None = None,
        timeout: int = c.Meltano.BATCH_DEFAULT_COMMAND_TIMEOUT,
    ) -> p.Result[t.Meltano.CliProcessResult]:
        """Execute Singer SDK command and capture output."""
        if not command:
            return r[t.Meltano.CliProcessResult].fail(
                "Invalid command: must be non-empty list",
            )
        process_input = input_data.encode() if input_data else None
        cmd_result = u.Cli.run_raw(
            list(command), timeout=timeout, input_data=process_input
        )
        if cmd_result.failure:
            return r[t.Meltano.CliProcessResult].fail(
                cmd_result.error or "Command failed"
            )
        out = cmd_result.value
        output_dict: t.Meltano.CliProcessResult = {
            "stdout": out.stdout,
            "stderr": out.stderr,
            "returncode": out.exit_code,
        }
        if out.exit_code != 0:
            stderr_msg = out.stderr or "Command execution failed"
            return r[t.Meltano.CliProcessResult].fail(stderr_msg)
        return r[t.Meltano.CliProcessResult].ok(output_dict)

    @staticmethod
    def translate_dbt_run(
        params: m.Meltano.CliTransformationParams,
    ) -> p.Result[t.StrSequence]:
        """Convert TransformationParams to dbt CLI command."""
        command: MutableSequence[str] = [
            "dbt",
            "run",
            "--projects-dir",
            params.project_dir,
        ]
        if params.models:
            command.extend(["--models", params.models])
        if params.select:
            command.extend(["--select", params.select])
        if params.exclude:
            command.extend(["--exclude", params.exclude])
        if params.full_refresh:
            command.append("--full-refresh")
        return r[t.StrSequence].ok(command)

    @staticmethod
    def translate_pipeline_run(
        params: m.Meltano.CliPipelineParams,
    ) -> p.Result[tuple[t.StrSequence, t.StrSequence]]:
        """Convert PipelineParams to source and sink CLI commands."""
        source_command: MutableSequence[str] = [params.source_name]
        if params.source_config:
            source_command.extend(["--config", params.source_config])
        if params.catalog_file:
            source_command.extend(["--catalog", params.catalog_file])
        if params.state_file:
            source_command.extend(["--state", params.state_file])
        sink_command: MutableSequence[str] = [params.sink_name]
        if params.sink_config:
            sink_command.extend(["--config", params.sink_config])
        return r[tuple[t.StrSequence, t.StrSequence]].ok((source_command, sink_command))

    @staticmethod
    def translate_tap_run(
        params: m.Meltano.CliDataSourceParams,
    ) -> p.Result[t.StrSequence]:
        """Convert DataSourceParams to Singer SDK source CLI command."""
        command: MutableSequence[str] = [params.source_name]
        if params.discover:
            command.append("--discover")
            return r[t.StrSequence].ok(command)
        if params.config_file:
            command.extend(["--config", params.config_file])
        if params.catalog_file:
            command.extend(["--catalog", params.catalog_file])
        if params.state_file:
            command.extend(["--state", params.state_file])
        if params.catalog_file:
            command.extend(["--properties", params.catalog_file])
        return r[t.StrSequence].ok(command)

    @staticmethod
    def translate_target_run(
        params: m.Meltano.CliDataSinkParams,
    ) -> p.Result[t.StrSequence]:
        """Convert DataSinkParams to Singer SDK sink CLI command."""
        command: MutableSequence[str] = [params.sink_name]
        if params.config_file:
            command.extend(["--config", params.config_file])
        if params.input_file:
            command.extend(["--input", params.input_file])
        return r[t.StrSequence].ok(command)


__all__: list[str] = ["FlextMeltanoSingerCliTranslator"]
