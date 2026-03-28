"""Singer CLI Translator - Pydantic Model to Singer SDK Command Translation.

Converts Pydantic parameter models (TapRunParams, TargetRunParams, etc.) to
Singer SDK CLI commands with automatic parameter validation through r.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import MutableSequence

from flext_core import r
from flext_infra import FlextInfraUtilitiesSubprocess

from flext_meltano import c, m, t


class FlextMeltanoSingerCliTranslator:
    """Translates Pydantic models to Singer SDK CLI commands.

    Provides model-driven CLI command generation for Singer sources, sinks,
    and complete data pipelines with automatic parameter validation.
    """

    @staticmethod
    def execute_singer_command(
        command: t.StrSequence,
        input_data: str | None = None,
        timeout: int = c.Meltano.BatchDefaults.COMMAND_TIMEOUT,
    ) -> r[t.Meltano.CLI.ProcessResult]:
        """Execute Singer SDK command and capture output.

        Args:
        command: CLI command as list of arguments
        input_data: Optional input data for stdin (for targets)
        timeout: Command timeout in seconds

        Returns:
        r containing execution results with stdout/stderr

        """
        if not command:
            return r[t.Meltano.CLI.ProcessResult].fail(
                "Invalid command: must be non-empty list",
            )
        process_input = input_data.encode() if input_data else None
        cmd_result = FlextInfraUtilitiesSubprocess.run_raw(
            list(command),
            timeout=timeout,
            input_data=process_input,
        )
        if cmd_result.is_failure:
            return r[t.Meltano.CLI.ProcessResult].fail(
                cmd_result.error or "Command failed"
            )
        out = cmd_result.value
        output_dict: t.Meltano.CLI.ProcessResult = {
            "stdout": out.stdout,
            "stderr": out.stderr,
            "returncode": out.exit_code,
        }
        if out.exit_code != 0:
            stderr_msg = out.stderr or "Command execution failed"
            return r[t.Meltano.CLI.ProcessResult].fail(stderr_msg)
        return r[t.Meltano.CLI.ProcessResult].ok(output_dict)

    @staticmethod
    def translate_dbt_run(
        params: m.Meltano.CliParameters.TransformationParams,
    ) -> r[t.StrSequence]:
        """Convert TransformationParams to transformation CLI command.

        Args:
        params: Validated TransformationParams model

        Returns:
        r containing list of DBT CLI command arguments

        """
        command: MutableSequence[str] = [
            "dbt",
            "run",
            "--project-dir",
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
        vars_val = getattr(params, "vars", None)
        if vars_val:
            vars_dict = m.Meltano.ConfigMappingPayload.model_validate({
                "values": vars_val,
            }).values
            vars_payload = m.Meltano.ConfigMappingPayload.model_validate({
                "values": vars_dict,
            })
            command.extend(["--vars", vars_payload.model_dump_json()])
        return r[t.StrSequence].ok(command)

    @staticmethod
    def translate_pipeline_run(
        params: m.Meltano.CliParameters.PipelineParams,
    ) -> r[tuple[t.StrSequence, t.StrSequence]]:
        """Convert PipelineParams to source and sink CLI commands.

        Args:
        params: Validated PipelineParams model

        Returns:
        r containing tuple of (source_command, sink_command)

        """
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
        params: m.Meltano.CliParameters.DataSourceParams,
    ) -> r[t.StrSequence]:
        """Convert DataSourceParams to Singer SDK source CLI command.

        Args:
            params: Validated DataSourceParams model

        Returns:
            r containing list of CLI command arguments

        """
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
        params: m.Meltano.CliParameters.DataSinkParams,
    ) -> r[t.StrSequence]:
        """Convert DataSinkParams to Singer SDK sink CLI command.

        Args:
        params: Validated DataSinkParams model

        Returns:
        r containing list of CLI command arguments

        """
        command: MutableSequence[str] = [params.sink_name]
        if params.config_file:
            command.extend(["--config", params.config_file])
        if params.input_file:
            command.extend(["--input", params.input_file])
        return r[t.StrSequence].ok(command)


__all__ = ["FlextMeltanoSingerCliTranslator"]
