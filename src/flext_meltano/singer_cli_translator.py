"""Singer CLI Translator - Pydantic Model to Singer SDK Command Translation.

Converts Pydantic parameter models (TapRunParams, TargetRunParams, etc.) to
Singer SDK CLI commands with automatic parameter validation through FlextResult.

## Three-Layer Architecture

This module is the middle layer in the model-driven CLI architecture:

```
Layer 1: CLI Arguments (string list)
    ↓ (parsed by FlextMeltanoCLI._parse_*_args methods)
Layer 2: Dictionary (key-value pairs)
    ↓ (converted by FlextCliModels.CliModelConverter)
Layer 3: Pydantic Models (TapRunParams, TargetRunParams, etc.)
    ↓ (translated by SingerCliTranslator) ← THIS MODULE
Layer 4: Singer SDK Commands (list of strings)
    ↓ (executed by subprocess)
Layer 5: Singer SDK Execution
```

## Usage Examples

### For flext-tap-* Projects

```python
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.singer_cli_translator import SingerCliTranslator

# Create tap parameters
tap_params = FlextMeltanoModels.TapRunParams(
    tap_name="tap-postgres",
    config_file="config/tap-config.json",
    catalog_file="config/catalog.json",
    state_file="state/state.json",
)

# Translate to Singer SDK command
command_result = SingerCliTranslator.translate_tap_run(tap_params)
if command_result.is_success:
    singer_command = command_result.unwrap()
    # singer_command = ["tap-postgres", "--config", "config/tap-config.json", ...]

    # Execute Singer SDK command
    execution_result = SingerCliTranslator.execute_singer_command(singer_command)
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
commands_result = SingerCliTranslator.translate_pipeline_run(pipeline_params)
if commands_result.is_success:
    tap_command, target_command = commands_result.unwrap()
    # Execute as pipeline: tap_command | target_command
```

## Railway-Oriented Programming

All methods return `FlextResult[T]` for type-safe error handling:

```python
# Example: Chain operations with FlextResult
result = (
    SingerCliTranslator.translate_tap_run(tap_params)
    .flat_map(lambda cmd: SingerCliTranslator.execute_singer_command(cmd))
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

from flext_core import FlextResult, FlextUtilities

from flext_meltano.models import FlextMeltanoModels


class SingerCliTranslator:
    """Translates Pydantic models to Singer SDK CLI commands.

    Provides model-driven CLI command generation for Singer taps, targets,
    and complete ELT pipelines with automatic parameter validation.
    """

    @staticmethod
    def translate_tap_run(
        params: FlextMeltanoModels.TapRunParams,
    ) -> FlextResult[list[str]]:
        """Convert TapRunParams to Singer SDK tap CLI command.

        Args:
            params: Validated TapRunParams model

        Returns:
            FlextResult containing list of CLI command arguments

        """
        command: list[str] = [params.tap_name]

        if params.discover:
            command.append("--discover")
            return FlextResult[list[str]].ok(command)

        if params.config_file:
            command.extend(["--config", params.config_file])

        if params.catalog_file:
            command.extend(["--catalog", params.catalog_file])

        if params.state_file:
            command.extend(["--state", params.state_file])

        if params.properties_file:
            command.extend(["--properties", params.properties_file])

        return FlextResult[list[str]].ok(command)

    @staticmethod
    def translate_target_run(
        params: FlextMeltanoModels.TargetRunParams,
    ) -> FlextResult[list[str]]:
        """Convert TargetRunParams to Singer SDK target CLI command.

        Args:
            params: Validated TargetRunParams model

        Returns:
            FlextResult containing list of CLI command arguments

        """
        command: list[str] = [params.target_name]

        if params.config_file:
            command.extend(["--config", params.config_file])

        if params.input_file:
            command.extend(["--input", params.input_file])

        return FlextResult[list[str]].ok(command)

    @staticmethod
    def translate_pipeline_run(
        params: FlextMeltanoModels.PipelineRunParams,
    ) -> FlextResult[tuple[list[str], list[str]]]:
        """Convert PipelineRunParams to tap and target CLI commands.

        Args:
            params: Validated PipelineRunParams model

        Returns:
            FlextResult containing tuple of (tap_command, target_command)

        """
        # Build tap command
        tap_command: list[str] = [params.tap_name]

        if params.tap_config:
            tap_command.extend(["--config", params.tap_config])

        if params.catalog_file:
            tap_command.extend(["--catalog", params.catalog_file])

        if params.state_file:
            tap_command.extend(["--state", params.state_file])

        # Build target command
        target_command: list[str] = [params.target_name]

        if params.target_config:
            target_command.extend(["--config", params.target_config])

        return FlextResult[tuple[list[str], list[str]]].ok((
            tap_command,
            target_command,
        ))

    @staticmethod
    def translate_dbt_run(
        params: FlextMeltanoModels.DbtRunParams,
    ) -> FlextResult[list[str]]:
        """Convert DbtRunParams to DBT CLI command.

        Args:
            params: Validated DbtRunParams model

        Returns:
            FlextResult containing list of DBT CLI command arguments

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

        if params.vars:
            command.extend(["--vars", params.vars])

        return FlextResult[list[str]].ok(command)

    @staticmethod
    def execute_singer_command(
        command: list[str],
        input_data: str | None = None,
        timeout: int = 300,
    ) -> FlextResult[dict[str, object]]:
        """Execute Singer SDK command and capture output.

        Args:
            command: CLI command as list of arguments
            input_data: Optional input data for stdin (for targets)
            timeout: Command timeout in seconds

        Returns:
            FlextResult containing execution results with stdout/stderr

        """
        # Use FlextUtilities.run_external_command for standardized subprocess execution
        process_input = input_data.encode() if input_data else None

        # Execute command with FlextUtilities (includes comprehensive error handling)
        result = FlextUtilities.run_external_command(
            cmd=command,
            capture_output=True,
            check=False,  # Don't raise exception on non-zero exit
            timeout=timeout,
            command_input=process_input,
            text=True,  # Get string output automatically
        )

        # Handle execution failure
        if result.is_failure:
            return FlextResult[dict[str, object]].fail(result.error)

        # Extract completed process
        completed_process = result.value

        # Check for non-zero exit code
        if completed_process.returncode != 0:
            error_msg = completed_process.stderr or "Unknown error"
            return FlextResult[dict[str, object]].fail(
                f"Command failed with code {completed_process.returncode}: {error_msg}"
            )

        # Prepare output data with decoded strings
        output_data: dict[str, object] = {
            "stdout": completed_process.stdout or "",
            "stderr": completed_process.stderr or "",
            "returncode": completed_process.returncode,
            "command": " ".join(command),
        }

        return FlextResult[dict[str, object]].ok(output_data)

    @staticmethod
    def validate_file_path(file_path: str | None) -> FlextResult[Path | None]:
        """Validate file path exists if provided.

        Args:
            file_path: Optional file path to validate

        Returns:
            FlextResult containing Path object or None if not provided

        """
        if not file_path:
            return FlextResult[Path | None].ok(None)

        path = Path(file_path)
        if not path.exists():
            return FlextResult[Path | None].fail(f"File not found: {file_path}")

        if not path.is_file():
            return FlextResult[Path | None].fail(f"Not a file: {file_path}")

        return FlextResult[Path | None].ok(path)


__all__ = ["SingerCliTranslator"]
