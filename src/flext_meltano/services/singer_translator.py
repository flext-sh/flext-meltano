"""Singer CLI Translator — MRO mixin for FlextMeltano facade.

Converts Pydantic parameter models to Singer SDK CLI commands.
Moved from singer/translator.py (already stateless static class).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

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
    ) -> p.Result[t.JsonMapping]:
        """Execute Singer SDK command and capture output."""
        if not command:
            return r[t.JsonMapping].fail("Invalid command: must be non-empty list")
        process_input = input_data.encode() if input_data else None
        cmd_result = u.Cli.run_raw(
            list(command), timeout=timeout, input_data=process_input
        )
        if cmd_result.failure:
            return r[t.JsonMapping].from_failure(cmd_result)
        out = cmd_result.value
        output_dict: t.JsonMapping = {
            "stdout": out.stdout,
            "stderr": out.stderr,
            "returncode": out.exit_code,
        }
        if out.exit_code != 0:
            stderr_msg = out.stderr or "Command execution failed"
            return r[t.JsonMapping].fail(stderr_msg)
        return r[t.JsonMapping].ok(output_dict)

    @staticmethod
    def translate_dbt_run(
        params: m.Meltano.CliTransformationParams,
    ) -> p.Result[t.StrSequence]:
        """Convert TransformationParams to dbt CLI command."""
        command: t.MutableSequenceOf[str] = [
            c.Meltano.DBT_BINARY,
            c.Meltano.DbtCommand.RUN,
            c.Meltano.DbtOption.PROJECTS_DIR,
            params.project_dir,
        ]
        if params.models:
            command.extend([c.Meltano.DbtOption.MODELS, params.models])
        if params.select:
            command.extend([c.Meltano.DbtOption.SELECT, params.select])
        if params.exclude:
            command.extend([c.Meltano.DbtOption.EXCLUDE, params.exclude])
        if params.full_refresh:
            command.append(c.Meltano.DbtOption.FULL_REFRESH)
        return r[t.StrSequence].ok(command)

    @staticmethod
    def translate_pipeline_run(
        params: m.Meltano.CliPipelineParams,
    ) -> p.Result[tuple[t.StrSequence, t.StrSequence]]:
        """Convert PipelineParams to source and sink CLI commands."""
        source_command: t.MutableSequenceOf[str] = [params.source_name]
        if params.source_config:
            source_command.extend(["--config", params.source_config])
        if params.catalog_file:
            source_command.extend(["--catalog", params.catalog_file])
        if params.state_file:
            source_command.extend(["--state", params.state_file])
        sink_command: t.MutableSequenceOf[str] = [params.sink_name]
        if params.sink_config:
            sink_command.extend(["--config", params.sink_config])
        return r[tuple[t.StrSequence, t.StrSequence]].ok((source_command, sink_command))

    @staticmethod
    def translate_tap_run(
        params: m.Meltano.CliDataSourceParams,
    ) -> p.Result[t.StrSequence]:
        """Convert DataSourceParams to Singer SDK source CLI command."""
        command: t.MutableSequenceOf[str] = [params.source_name]
        if params.discover:
            command.append(c.Meltano.SingerCliOption.DISCOVER)
            return r[t.StrSequence].ok(command)
        if params.config_file:
            command.extend([c.Meltano.SingerCliOption.CONFIG, params.config_file])
        if params.catalog_file:
            command.extend([c.Meltano.SingerCliOption.CATALOG, params.catalog_file])
        if params.state_file:
            command.extend([c.Meltano.SingerCliOption.STATE, params.state_file])
        if params.catalog_file:
            command.extend([c.Meltano.SingerCliOption.PROPERTIES, params.catalog_file])
        return r[t.StrSequence].ok(command)

    @staticmethod
    def translate_target_run(
        params: m.Meltano.CliDataSinkParams,
    ) -> p.Result[t.StrSequence]:
        """Convert DataSinkParams to Singer SDK sink CLI command."""
        command: t.MutableSequenceOf[str] = [params.sink_name]
        if params.config_file:
            command.extend([c.Meltano.SingerCliOption.CONFIG, params.config_file])
        if params.input_file:
            command.extend([c.Meltano.SingerCliOption.INPUT, params.input_file])
        return r[t.StrSequence].ok(command)


__all__: list[str] = ["FlextMeltanoSingerCliTranslator"]
