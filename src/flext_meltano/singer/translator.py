"""Singer CLI Translator - Pydantic Model to Singer SDK Command Translation.

Converts Pydantic parameter models (TapRunParams, TargetRunParams, etc.) to
Singer SDK CLI commands with automatic parameter validation through r.

## Three-Layer Architecture

This module is the middle layer in the model-driven CLI architecture:

```
Layer 1: CLI Arguments (string list)
    ↓ (parsed by FlextMeltanoCLI._parse_*_args methods)
Layer 2: Dictionary (key-value pairs)
    ↓ (converted by FlextCliModels.CliModelConverter)
Layer 3: Pydantic Models (TapRunParams, TargetRunParams, etc.)
    ↓ (translated by FlextMeltanoSingerCliTranslator) ← THIS MODULE
Layer 4: Singer SDK Commands (list of strings)
    ↓ (executed by subprocess)
Layer 5: Singer SDK Execution
```

## Usage Examples

### For flext-tap-* Projects

```python
from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.singer.translator import FlextMeltanoSingerCliTranslator

# Create source parameters
source_params = m.Meltano.CliParameters.DataSourceParams(
    source_name="source-postgres",
    config_file="config/source-config.json",
    catalog_file="config/catalog.json",
    state_file="state/state.json",
)

# Translate to Singer SDK command
command_result = FlextMeltanoSingerCliTranslator.translate_tap_run(source_params)
if command_result.is_success:
    singer_command = command_result.value
    # singer_command = ["tap-postgres", "--config", "config/tap-config.json", ...]

    # Execute Singer SDK command
    execution_result = FlextMeltanoSingerCliTranslator.execute_singer_command(
        singer_command
    )
    if execution_result.success:
        output = execution_result.value
        logger = structlog.get_logger(__name__)
        logger.info("Source executed", stdout=output["stdout"])
```

### For Complete Pipelines

```python
# Create pipeline parameters
pipeline_params = m.PipelineRunParams(
    tap_name="tap-postgres",
    target_name="target-jsonl",
    tap_config="config/tap-config.json",
    target_config="config/target-config.json",
    catalog_file="config/catalog.json",
)

# Translate to tap and target commands
commands_result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(
    pipeline_params
)
if commands_result.is_success:
    tap_command, target_command = commands_result.value
    # Execute as pipeline: tap_command | target_command
```

## Railway-Oriented Programming

All methods return `r[T]` for type-safe error handling:

```python
# Example: Chain operations with r
result = (
    FlextMeltanoSingerCliTranslator
    .translate_tap_run(tap_params)
    .flat_map(lambda cmd: FlextMeltanoSingerCliTranslator.execute_singer_command(cmd))
    .map(lambda output: output["stdout"])
)

if result.is_failure:
    logger = structlog.get_logger(__name__)
    logger.error("Pipeline failed", error=str(result.error))
```

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import subprocess

from flext_core.result import r

from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoSingerCliTranslator:
    """Translates Pydantic models to Singer SDK CLI commands.

    Provides model-driven CLI command generation for Singer sources, sinks,
    and complete data pipelines with automatic parameter validation.
    """

    @staticmethod
    def execute_singer_command(
        command: list[str],
        input_data: str | None = None,
        timeout: int = 300,
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

        def is_string_argument(arg: str) -> bool:
            match arg:
                case str():
                    return True
                case _:
                    return False

        if not all(is_string_argument(arg) for arg in command):
            return r[t.Meltano.CLI.ProcessResult].fail(
                "Invalid command: all arguments must be strings",
            )
        try:
            process_input = input_data.encode() if input_data else None
            # Intentional subprocess usage: Singer SDK command execution
            proc_result = subprocess.run(
                command,
                capture_output=True,
                input=process_input,
                timeout=timeout,
                check=False,
                shell=False,
            )
            output_dict: t.Meltano.CLI.ProcessResult = {
                "stdout": proc_result.stdout.decode() if proc_result.stdout else "",
                "stderr": proc_result.stderr.decode() if proc_result.stderr else "",
                "returncode": proc_result.returncode,
            }
            if proc_result.returncode != 0:
                stderr_msg = str(output_dict.get("stderr", "Command execution failed"))
                return r[t.Meltano.CLI.ProcessResult].fail(stderr_msg)
            return r[t.Meltano.CLI.ProcessResult].ok(output_dict)
        except subprocess.TimeoutExpired as e:
            return r[t.Meltano.CLI.ProcessResult].fail(f"Command timeout: {e}")
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[t.Meltano.CLI.ProcessResult].fail(f"Command execution failed: {e}")

    @staticmethod
    def translate_dbt_run(
        params: m.Meltano.CliParameters.TransformationParams,
    ) -> r[list[str]]:
        """Convert TransformationParams to transformation CLI command.

        Args:
        params: Validated TransformationParams model

        Returns:
        r containing list of DBT CLI command arguments

        """
        command: list[str] = ["dbt", "run", "--project-dir", params.project_dir]
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
        return r[list[str]].ok(command)

    @staticmethod
    def translate_pipeline_run(
        params: m.Meltano.CliParameters.PipelineParams,
    ) -> r[tuple[list[str], list[str]]]:
        """Convert PipelineParams to source and sink CLI commands.

        Args:
        params: Validated PipelineParams model

        Returns:
        r containing tuple of (source_command, sink_command)

        """
        source_command: list[str] = [params.source_name]
        if params.source_config:
            source_command.extend(["--config", params.source_config])
        if params.catalog_file:
            source_command.extend(["--catalog", params.catalog_file])
        if params.state_file:
            source_command.extend(["--state", params.state_file])
        sink_command: list[str] = [params.sink_name]
        if params.sink_config:
            sink_command.extend(["--config", params.sink_config])
        return r[tuple[list[str], list[str]]].ok((source_command, sink_command))

    @staticmethod
    def translate_tap_run(
        params: m.Meltano.CliParameters.DataSourceParams,
    ) -> r[list[str]]:
        """Convert DataSourceParams to Singer SDK source CLI command.

        Args:
            params: Validated DataSourceParams model

        Returns:
            r containing list of CLI command arguments

        """
        command: list[str] = [params.source_name]
        if params.discover:
            command.append("--discover")
            return r[list[str]].ok(command)
        if params.config_file:
            command.extend(["--config", params.config_file])
        if params.catalog_file:
            command.extend(["--catalog", params.catalog_file])
        if params.state_file:
            command.extend(["--state", params.state_file])
        if params.catalog_file:
            command.extend(["--properties", params.catalog_file])
        return r[list[str]].ok(command)

    @staticmethod
    def translate_target_run(
        params: m.Meltano.CliParameters.DataSinkParams,
    ) -> r[list[str]]:
        """Convert DataSinkParams to Singer SDK sink CLI command.

        Args:
        params: Validated DataSinkParams model

        Returns:
        r containing list of CLI command arguments

        """
        command: list[str] = [params.sink_name]
        if params.config_file:
            command.extend(["--config", params.config_file])
        if params.input_file:
            command.extend(["--input", params.input_file])
        return r[list[str]].ok(command)


__all__ = ["FlextMeltanoSingerCliTranslator"]
