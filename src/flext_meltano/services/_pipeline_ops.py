"""FLEXT Meltano Pipeline Operations - Path resolution, CRUD, and lifecycle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from pathlib import Path

from flext_cli import cli

from flext_meltano import p, r
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.services._executor_base import FlextMeltanoExecutorBase
from flext_meltano.typings import FlextMeltanoTypes as t
from flext_meltano.utilities import FlextMeltanoUtilities as u


class FlextMeltanoPipelinePaths:
    """Shared path resolution for pipeline directories and files."""

    _PIPELINES_ROOT_ENV = c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV
    _PIPELINE_CONFIG_FILE = c.Meltano.CLI_DEFAULT_PIPELINE_CONFIG_FILE
    _PIPELINE_PID_FILE = c.Meltano.CLI_DEFAULT_PIPELINE_PID_FILE

    @staticmethod
    def pipelines_root_dir() -> Path:
        """Resolve pipelines root from current environment state."""
        configured_root = os.environ.get(
            FlextMeltanoPipelinePaths._PIPELINES_ROOT_ENV,
        )
        normalized_root = u.to_str(configured_root).strip()
        if u.chk(normalized_root, empty=False):
            return Path(normalized_root).expanduser().resolve()
        return (Path.cwd() / ".flext-meltano" / "pipelines").resolve()

    @staticmethod
    def pipeline_dir(pipeline_name: str) -> Path:
        return FlextMeltanoPipelinePaths.pipelines_root_dir() / pipeline_name

    @staticmethod
    def pipeline_config_path(pipeline_name: str) -> Path:
        return (
            FlextMeltanoPipelinePaths.pipeline_dir(pipeline_name)
            / FlextMeltanoPipelinePaths._PIPELINE_CONFIG_FILE
        )

    @staticmethod
    def pipeline_pid_path(pipeline_name: str) -> Path:
        return (
            FlextMeltanoPipelinePaths.pipeline_dir(pipeline_name)
            / FlextMeltanoPipelinePaths._PIPELINE_PID_FILE
        )


class FlextMeltanoPipelineCrudOperations(FlextMeltanoPipelinePaths):
    """Static CRUD operations for pipelines - create, execute, list."""

    @staticmethod
    def create_pipeline(
        pipeline_name: str,
        settings: t.RecursiveContainerMapping | None,
    ) -> p.Result[str]:
        """Create a new Meltano pipeline with the given configuration."""
        if not pipeline_name.strip():
            return r[str].fail("Pipeline creation requires a non-empty pipeline name")
        if settings is None:
            return r[str].fail("Pipeline creation not configured")
        pipeline_dir = FlextMeltanoPipelinePaths.pipeline_dir(pipeline_name)
        if pipeline_dir.exists():
            return r[str].fail(f"Pipeline '{pipeline_name}' already exists")
        try:
            pipeline_dir.mkdir(parents=True, exist_ok=False)
            config_path = FlextMeltanoPipelinePaths.pipeline_config_path(
                pipeline_name,
            )
            validated = m.Meltano.ConfigMappingPayload.model_validate({
                "values": settings,
            })
            u.write_file(
                config_path,
                validated.model_dump_json(indent=2),
            )
        except OSError as exc:
            return r[str].fail(f"Failed to create pipeline '{pipeline_name}': {exc}")
        return r[str].ok(str(pipeline_dir))

    @staticmethod
    def execute_pipeline(
        pipeline_name: str,
        command_args: t.StrSequence | None = None,
    ) -> p.Result[str]:
        """Execute a Meltano pipeline."""
        pipeline_dir = FlextMeltanoPipelinePaths.pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[str].fail(f"Pipeline '{pipeline_name}' not found")
        configured_command: t.StrSequence | None = None
        config_path = FlextMeltanoPipelinePaths.pipeline_config_path(pipeline_name)
        if config_path.exists():
            config_mapping_result = cli.read_json_model(
                config_path, m.Meltano.ConfigMappingPayload
            )
            if config_mapping_result.failure:
                return r[str].fail(
                    f"Failed to read pipeline '{pipeline_name}' configuration: {config_mapping_result.error}",
                )
            config_mapping = config_mapping_result.value
            validated_payload = config_mapping.values
            command_value = validated_payload.get("command")
            if isinstance(command_value, list):
                configured_command = m.Meltano.StringListValue.model_validate({
                    "items": command_value,
                }).items
        meltano_args = command_args or configured_command
        if not meltano_args:
            return r[str].fail("Pipeline execution not configured")
        run_result: p.Result[m.Meltano.CommandExecutionResult] = (
            FlextMeltanoExecutorBase().execute_meltano_command(
                list(meltano_args),
                _cwd=pipeline_dir,
            )
        )
        if run_result.failure:
            error_msg = run_result.error or "Unknown error"
            return r[str].fail(
                f"Failed to execute Meltano runtime command: {error_msg}"
            )
        completed: m.Meltano.CommandExecutionResult = run_result.value
        if completed.exit_code != 0:
            command_error = u.Meltano.command_failure_message(
                completed,
                default=f"Meltano command failed with exit code {completed.exit_code}",
            )
            return r[str].fail(command_error)
        logger = u.fetch_logger(__name__)
        output = u.to_str(completed.output).strip()
        if u.chk(output, empty=False):
            logger.info(output)
        return r[str].ok(output or "executed")

    @staticmethod
    def list_pipelines() -> p.Result[t.StrSequence]:
        """List all available Meltano pipelines."""
        pipelines_root = FlextMeltanoPipelinePaths.pipelines_root_dir()
        if not pipelines_root.exists():
            return r[t.StrSequence].ok([])
        if not pipelines_root.is_dir():
            return r[t.StrSequence].fail(
                f"Pipelines root path is not a directory: {pipelines_root}",
            )
        try:
            pipeline_names = sorted(
                entry.name for entry in pipelines_root.iterdir() if entry.is_dir()
            )
        except OSError as exc:
            return r[t.StrSequence].fail(f"Failed to list pipelines: {exc}")
        return r[t.StrSequence].ok(pipeline_names)
