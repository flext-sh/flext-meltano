"""Singer CLI Translator - Pydantic Model to Singer SDK Command Translation.

Converts Pydantic parameter models (TapRunParams, TargetRunParams, etc.) to
Singer SDK CLI commands with automatic parameter validation through FlextCore.Result.

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
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.singer_cli_translator import FlextMeltanoSingerCliTranslator

# Create tap parameters
tap_params = FlextMeltanoModels.TapRunParams(
    tap_name="tap-postgres",
    config_file="config/tap-config.json",
    catalog_file="config/catalog.json",
    state_file="state/state.json",
)

# Translate to Singer SDK command
command_result = FlextMeltanoSingerCliTranslator.translate_tap_run(tap_params)
if command_result.is_success:
    singer_command = command_result.unwrap()
    # singer_command = ["tap-postgres", "--config", "config/tap-config.json", ...]

    # Execute Singer SDK command
    execution_result = FlextMeltanoSingerCliTranslator.execute_singer_command(
        singer_command
    )
    if execution_result.is_success:
        output = execution_result.unwrap()
        print(f"Tap executed: {output['stdout']}")
```

### For Complete Pipelines

```python
# Create pipeline parameters
pipeline_params = FlextMeltanoModels.PipelineRunParams(
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
    tap_command, target_command = commands_result.unwrap()
    # Execute as pipeline: tap_command | target_command
```

## Railway-Oriented Programming

All methods return `FlextCore.Result[T]` for type-safe error handling:

```python
# Example: Chain operations with FlextCore.Result
result = (
    FlextMeltanoSingerCliTranslator.translate_tap_run(tap_params)
    .flat_map(lambda cmd: FlextMeltanoSingerCliTranslator.execute_singer_command(cmd))
    .map(lambda output: output["stdout"])
)

if result.is_failure:
    print(f"Pipeline failed: {result.error}")
```

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextCore

from flext_meltano.models import FlextMeltanoModels


class FlextMeltanoSingerCliTranslator:
    """Translates Pydantic models to Singer SDK CLI commands.

    Provides model-driven CLI command generation for Singer taps, targets,
    and complete ELT pipelines with automatic parameter validation.
    """

    @staticmethod
    def translate_tap_run(
        params: FlextMeltanoModels.TapRunParams,
    ) -> FlextCore.Result[FlextCore.Types.StringList]:
        """Convert TapRunParams to Singer SDK tap CLI command.

        Args:
            params: Validated TapRunParams model

        Returns:
            FlextCore.Result containing list of CLI command arguments

        """
        command: FlextCore.Types.StringList = [params.tap_name]

        if params.discover:
            command.append("--discover")
            return FlextCore.Result[FlextCore.Types.StringList].ok(command)

        if params.config_file:
            command.extend(["--config", params.config_file])

        if params.catalog_file:
            command.extend(["--catalog", params.catalog_file])

        if params.state_file:
            command.extend(["--state", params.state_file])

        if params.properties_file:
            command.extend(["--properties", params.properties_file])

        return FlextCore.Result[FlextCore.Types.StringList].ok(command)

    @staticmethod
    def translate_target_run(
        params: FlextMeltanoModels.TargetRunParams,
    ) -> FlextCore.Result[FlextCore.Types.StringList]:
        """Convert TargetRunParams to Singer SDK target CLI command.

        Args:
            params: Validated TargetRunParams model

        Returns:
            FlextCore.Result containing list of CLI command arguments

        """
        command: FlextCore.Types.StringList = [params.target_name]

        if params.config_file:
            command.extend(["--config", params.config_file])

        if params.input_file:
            command.extend(["--input", params.input_file])

        return FlextCore.Result[FlextCore.Types.StringList].ok(command)

    @staticmethod
    def translate_pipeline_run(
        params: FlextMeltanoModels.PipelineRunParams,
    ) -> FlextCore.Result[
        tuple[FlextCore.Types.StringList, FlextCore.Types.StringList]
    ]:
        """Convert PipelineRunParams to tap and target CLI commands.

        Args:
            params: Validated PipelineRunParams model

        Returns:
            FlextCore.Result containing tuple of (tap_command, target_command)

        """
        # Build tap command
        tap_command: FlextCore.Types.StringList = [params.tap_name]

        if params.tap_config:
            tap_command.extend(["--config", params.tap_config])

        if params.catalog_file:
            tap_command.extend(["--catalog", params.catalog_file])

        if params.state_file:
            tap_command.extend(["--state", params.state_file])

        # Build target command
        target_command: FlextCore.Types.StringList = [params.target_name]

        if params.target_config:
            target_command.extend(["--config", params.target_config])

        return FlextCore.Result[
            tuple[FlextCore.Types.StringList, FlextCore.Types.StringList]
        ].ok((
            tap_command,
            target_command,
        ))

    @staticmethod
    def translate_dbt_run(
        params: FlextMeltanoModels.DbtRunParams,
    ) -> FlextCore.Result[FlextCore.Types.StringList]:
        """Convert DbtRunParams to DBT CLI command.

        Args:
            params: Validated DbtRunParams model

        Returns:
            FlextCore.Result containing list of DBT CLI command arguments

        """
        command: FlextCore.Types.StringList = [
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

        if params.vars:
            command.extend(["--vars", params.vars])

        return FlextCore.Result[FlextCore.Types.StringList].ok(command)

    @staticmethod
    def execute_singer_command(
        command: FlextCore.Types.StringList,
        input_data: str | None = None,
        timeout: int = 300,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Execute Singer SDK command and capture output.

        Args:
            command: CLI command as list of arguments
            input_data: Optional input data for stdin (for targets)
            timeout: Command timeout in seconds

        Returns:
            FlextCore.Result containing execution results with stdout/stderr

        """
        # Use FlextCore.Utilities.run_external_command for standardized subprocess execution
        process_input = input_data.encode() if input_data else None

        # Execute command with FlextCore.Utilities (includes comprehensive error handling)
        result = FlextCore.Utilities.run_external_command(
            cmd=command,
            capture_output=True,
            check=False,  # Don't raise exception on non-zero exit
            timeout=timeout,
            command_input=process_input,
            text=True,  # Get string output automatically
        )

        # Handle execution failure
        if result.is_failure:
            return FlextCore.Result[FlextCore.Types.Dict].fail(result.error)

        # Extract completed process
        completed_process = result.value

        # Check for non-zero exit code
        if completed_process.returncode != 0:
            error_msg = completed_process.stderr or "Unknown error"
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Command failed with code {completed_process.returncode}: {error_msg}"
            )

        # Prepare output data with decoded strings
        output_data: FlextCore.Types.Dict = {
            "stdout": completed_process.stdout or "",
            "stderr": completed_process.stderr or "",
            "returncode": completed_process.returncode,
            "command": " ".join(command),
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(output_data)

    @staticmethod
    def validate_file_path(file_path: str | None) -> FlextCore.Result[Path | None]:
        """Validate file path exists if provided.

        Args:
            file_path: Optional file path to validate

        Returns:
            FlextCore.Result containing Path object or None if not provided

        """
        if not file_path:
            return FlextCore.Result[Path | None].ok(None)

        path = Path(file_path)
        if not path.exists():
            return FlextCore.Result[Path | None].fail(f"File not found: {file_path}")

        if not path.is_file():
            return FlextCore.Result[Path | None].fail(f"Not a file: {file_path}")

        return FlextCore.Result[Path | None].ok(path)


__all__ = ["FlextMeltanoSingerCliTranslator"]
