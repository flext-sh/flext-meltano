"""FLEXT Meltano Pipeline Operations - Path resolution, CRUD, and lifecycle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from pathlib import Path

from flext_core import FlextLogger, r
from flext_infra import FlextInfraUtilitiesSubprocess

from flext_meltano import c, m, t


class _PipelinePaths:
    """Shared path resolution for pipeline directories and files."""

    _PIPELINES_ROOT_ENV = c.Meltano.CliDefaults.PIPELINES_ROOT_ENV
    _PIPELINE_CONFIG_FILE = c.Meltano.CliDefaults.PIPELINE_CONFIG_FILE
    _PIPELINE_PID_FILE = c.Meltano.CliDefaults.PIPELINE_PID_FILE

    @staticmethod
    def _pipelines_root_dir() -> Path:
        configured_root = os.environ.get(
            _PipelinePaths._PIPELINES_ROOT_ENV,
        )
        if configured_root and configured_root.strip():
            return Path(configured_root).expanduser().resolve()
        return (Path.cwd() / ".flext-meltano" / "pipelines").resolve()

    @staticmethod
    def _pipeline_dir(pipeline_name: str) -> Path:
        return _PipelinePaths._pipelines_root_dir() / pipeline_name

    @staticmethod
    def _pipeline_config_path(pipeline_name: str) -> Path:
        return (
            _PipelinePaths._pipeline_dir(pipeline_name)
            / _PipelinePaths._PIPELINE_CONFIG_FILE
        )

    @staticmethod
    def _pipeline_pid_path(pipeline_name: str) -> Path:
        return (
            _PipelinePaths._pipeline_dir(pipeline_name)
            / _PipelinePaths._PIPELINE_PID_FILE
        )


class _PipelineCrudOperations(_PipelinePaths):
    """Static CRUD operations for pipelines - create, execute, list."""

    @staticmethod
    def create_pipeline(
        pipeline_name: str,
        config: Mapping[
            str,
            t.Scalar | Sequence[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
        ]
        | None,
    ) -> r[str]:
        """Create a new Meltano pipeline with the given configuration."""
        if not pipeline_name.strip():
            return r[str].fail("Pipeline creation requires a non-empty pipeline name")
        if config is None:
            return r[str].fail("Pipeline creation not configured")
        pipeline_dir = _PipelinePaths._pipeline_dir(pipeline_name)
        if pipeline_dir.exists():
            return r[str].fail(f"Pipeline '{pipeline_name}' already exists")
        try:
            pipeline_dir.mkdir(parents=True, exist_ok=False)
            config_path = _PipelinePaths._pipeline_config_path(pipeline_name)
            validated = m.Meltano.ConfigMappingPayload.model_validate({
                "values": dict(config),
            })
            config_path.write_text(
                validated.model_dump_json(indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            return r[str].fail(f"Failed to create pipeline '{pipeline_name}': {exc}")
        return r[str].ok(str(pipeline_dir))

    @staticmethod
    def execute_pipeline(
        pipeline_name: str,
        command_args: t.StrSequence | None = None,
    ) -> r[str]:
        """Execute a Meltano pipeline."""
        pipeline_dir = _PipelinePaths._pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[str].fail(f"Pipeline '{pipeline_name}' not found")
        configured_command: t.StrSequence | None = None
        config_path = _PipelinePaths._pipeline_config_path(pipeline_name)
        if config_path.exists():
            try:
                config_mapping = m.Meltano.ConfigMappingPayload.model_validate_json(
                    config_path.read_text(encoding="utf-8"),
                )
            except (ValueError, OSError) as exc:
                return r[str].fail(
                    f"Failed to read pipeline '{pipeline_name}' configuration: {exc}",
                )
            validated_payload = config_mapping.values
            command_value = validated_payload.get("command")
            if isinstance(command_value, list):
                configured_command = m.Meltano.StringListValue.model_validate({
                    "items": command_value,
                }).items
        meltano_args = command_args or configured_command
        if not meltano_args:
            return r[str].fail("Pipeline execution not configured")
        command = ["meltano", *meltano_args]
        runner = FlextInfraUtilitiesSubprocess()
        run_result = runner.run_raw(command, cwd=pipeline_dir)
        if run_result.is_failure:
            error_msg = run_result.error or "Unknown error"
            if "FileNotFoundError" in error_msg or "not found" in error_msg.lower():
                return r[str].fail("Meltano CLI executable not found")
            return r[str].fail(f"Failed to execute Meltano CLI command: {error_msg}")
        completed = run_result.value
        if completed.exit_code != 0:
            command_error = completed.stderr.strip() or completed.stdout.strip()
            if not command_error:
                command_error = (
                    f"Meltano command failed with exit code {completed.exit_code}"
                )
            return r[str].fail(command_error)
        logger = FlextLogger(__name__)
        if completed.stdout.strip():
            logger.info(completed.stdout.strip())
        return r[str].ok(completed.stdout.strip() or "executed")

    @staticmethod
    def list_pipelines() -> r[t.StrSequence]:
        """List all available Meltano pipelines."""
        pipelines_root = _PipelinePaths._pipelines_root_dir()
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
