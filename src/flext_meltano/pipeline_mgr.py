"""FLEXT Meltano pipeline manager - handlers for pipeline CLI commands."""

from __future__ import annotations

import os
import signal
from contextlib import suppress
from pathlib import Path

from flext_cli import cli as flext_cli
from flext_meltano import (
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    e,
    m,
    p,
    r,
    t,
    u,
)
from flext_meltano.services.executor import FlextMeltanoExecutor


class FlextMeltanoPipelineManager(FlextMeltanoServiceBase):
    """Pipeline manager for FLEXT Meltano CLI."""

    _cli: p.Meltano.PipelineCli = u.PrivateAttr()

    def __init__(
        self,
        cli: p.Meltano.PipelineCli | None = None,
        settings: p.Settings | None = None,
    ) -> None:
        """Initialize the pipeline manager with an optional CLI reference."""
        resolved_settings = (
            settings if settings is not None else type(self).fetch_fresh_settings()
        )
        super().__init__(
            runtime_settings=resolved_settings,
            service_name="FlextMeltanoPipelineManager",
        )
        self._cli = cli

    @classmethod
    def fetch_fresh_settings(cls) -> FlextMeltanoSettings:
        """Build one fresh settings snapshot for pipeline command handling."""
        process_environment = u.resolve_process_environment()
        configured_root = process_environment.get(
            c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV,
        )
        if configured_root is None:
            with FlextMeltanoSettings.singleton_disabled():
                return FlextMeltanoSettings()
        return FlextMeltanoSettings.model_validate({
            c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV: configured_root,
        })

    def _pipelines_root(self) -> Path:
        return self.settings.pipelines_dir

    def _pipeline_dir(self, pipeline_name: str) -> Path:
        return self._pipelines_root() / pipeline_name

    def _config_path(self, pipeline_name: str) -> Path:
        return Path(
            self._pipeline_dir(pipeline_name),
            c.Meltano.CLI_DEFAULT_PIPELINE_CONFIG_FILE,
        )

    def _pid_path(self, pipeline_name: str) -> Path:
        return Path(
            self._pipeline_dir(pipeline_name),
            c.Meltano.CLI_DEFAULT_PIPELINE_PID_FILE,
        )

    @staticmethod
    def _normalize_pipeline_name(pipeline_name: str) -> p.Result[str]:
        normalized_name = pipeline_name.strip()
        if not normalized_name:
            return e.fail_validation("pipeline name", result_type=r[str])
        return r[str].ok(normalized_name)

    def _load_pipeline_config(self, pipeline_name: str) -> p.Result[t.JsonMapping]:
        config_result = flext_cli.read_json_file(self._config_path(pipeline_name))
        if config_result.failure:
            return r[t.JsonMapping].fail(
                config_result.error or "Pipeline configuration could not be read",
            )
        try:
            config_mapping = m.Meltano.ConfigMappingPayload.model_validate({
                "values": config_result.value,
            })
        except ValueError as exc:
            return e.fail_validation(
                "pipeline configuration JSON",
                error=exc,
                result_type=r[t.JsonMapping],
            )
        return r[t.JsonMapping].ok(config_mapping.values)

    def _pipeline_command(
        self,
        pipeline_name: str,
        args: t.StrSequence | None = None,
    ) -> p.Result[t.StrSequence]:
        config_result = self._load_pipeline_config(pipeline_name)
        if config_result.failure:
            return r[t.StrSequence].fail(
                config_result.error or "Pipeline execution not configured",
            )
        command_value = config_result.value.get("command")
        if not isinstance(command_value, t.SEQUENCE_PAIR_TYPES):
            return r[t.StrSequence].fail("Pipeline execution not configured")
        command = m.Meltano.StringListValue.model_validate({
            "items": command_value,
        }).items
        return r[t.StrSequence].ok([
            *command,
            *(list(args) if args is not None else []),
        ])

    def _read_pid(self, pipeline_name: str) -> p.Result[int]:
        pid_result = flext_cli.read_text_file(self._pid_path(pipeline_name))
        if pid_result.failure:
            return r[int].fail(pid_result.error or "Unable to read pipeline pid")
        try:
            pid_value = int(pid_result.value.strip())
        except ValueError as exc:
            return e.fail_validation("pipeline pid", error=exc, result_type=r[int])
        return r[int].ok(pid_value)

    @staticmethod
    def _process_running(pid_value: int) -> bool:
        try:
            os.kill(pid_value, 0)
        except OSError:
            return False
        return True

    def create_pipeline(
        self,
        pipeline_name: str,
        config_payload: t.JsonMapping | None,
    ) -> p.Result[str]:
        """Create and persist a named pipeline configuration."""
        name_result = self._normalize_pipeline_name(pipeline_name)
        if name_result.failure:
            return r[str].fail(name_result.error or "Pipeline name is invalid")
        if config_payload is None:
            return r[str].fail("Pipeline creation not configured")
        try:
            config_mapping = m.Meltano.ConfigMappingPayload.model_validate({
                "values": config_payload,
            })
        except ValueError as exc:
            return e.fail_validation(
                "pipeline configuration JSON",
                error=exc,
                result_type=r[str],
            )
        ensure_result = flext_cli.ensure_dir(self._pipeline_dir(name_result.value))
        if ensure_result.failure:
            return r[str].fail(
                ensure_result.error or "Unable to create pipeline directory",
            )
        write_result = flext_cli.write_json_file(
            self._config_path(name_result.value),
            config_mapping.values,
        )
        if write_result.failure:
            return r[str].fail(
                write_result.error or "Unable to persist pipeline configuration",
            )
        return r[str].ok(name_result.value)

    def execute_pipeline(
        self,
        pipeline_name: str,
        args: t.StrSequence | None = None,
    ) -> p.Result[str]:
        """Execute a named pipeline using the persisted command definition."""
        name_result = self._normalize_pipeline_name(pipeline_name)
        if name_result.failure:
            return r[str].fail(name_result.error or "Pipeline name is invalid")
        command_result = self._pipeline_command(name_result.value, args)
        if command_result.failure:
            return r[str].fail(
                command_result.error or "Pipeline execution not configured",
            )
        execution_result = FlextMeltanoExecutor(
            settings=self.settings,
        ).execute_meltano_command(command_result.value)
        if execution_result.failure:
            return r[str].fail(execution_result.error or "Pipeline execution failed")
        if not execution_result.value.success:
            return r[str].fail(
                execution_result.value.error
                or execution_result.value.output
                or "Pipeline execution failed",
            )
        return r[str].ok(execution_result.value.output)

    def list_pipelines(self) -> p.Result[t.StrSequence]:
        """List all persisted pipeline names."""
        return flext_cli.list_directory_names(self._pipelines_root())

    def fetch_pipeline_status(self, pipeline_name: str) -> p.Result[str]:
        """Return the current status of a named pipeline."""
        name_result = self._normalize_pipeline_name(pipeline_name)
        if name_result.failure:
            return r[str].fail(name_result.error or "Pipeline name is invalid")
        pid_path = self._pid_path(name_result.value)
        if not pid_path.exists():
            return r[str].ok("stopped")
        pid_result = self._read_pid(name_result.value)
        if pid_result.failure:
            return r[str].fail(pid_result.error or "Unable to inspect pipeline status")
        if self._process_running(pid_result.value):
            return r[str].ok("running")
        _ = flext_cli.delete_path(pid_path)
        return r[str].ok("stopped")

    def stop_pipeline(self, pipeline_name: str) -> p.Result[str]:
        """Stop a named pipeline and remove its persisted pid file."""
        name_result = self._normalize_pipeline_name(pipeline_name)
        if name_result.failure:
            return r[str].fail(name_result.error or "Pipeline name is invalid")
        pid_path = self._pid_path(name_result.value)
        if not pid_path.exists():
            return r[str].ok("stopped")
        pid_result = self._read_pid(name_result.value)
        if pid_result.success and self._process_running(pid_result.value):
            with suppress(OSError):
                os.kill(pid_result.value, signal.SIGTERM)
        delete_result = flext_cli.delete_path(pid_path)
        if delete_result.failure and pid_path.exists():
            return r[str].fail(delete_result.error or "Unable to delete pipeline pid")
        return r[str].ok("stopped")

    def delete_pipeline(self, pipeline_name: str) -> p.Result[str]:
        """Delete a named pipeline and its persisted artifacts."""
        name_result = self._normalize_pipeline_name(pipeline_name)
        if name_result.failure:
            return r[str].fail(name_result.error or "Pipeline name is invalid")
        pipeline_dir = self._pipeline_dir(name_result.value)
        if not pipeline_dir.exists():
            return r[str].ok(name_result.value)
        delete_result = flext_cli.delete_path(pipeline_dir)
        if delete_result.failure:
            return r[str].fail(delete_result.error or "Unable to delete pipeline")
        return r[str].ok(name_result.value)

    def handle_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle pipeline command using composition."""
        if not args or u.Meltano.is_help_request(args):
            if self._cli is not None:
                self._cli.show_pipeline_help()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP)
        subcommand = args[0]
        subcommand_args = args[1:]
        return self._dispatch_pipeline(subcommand, subcommand_args)

    def _create_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Create a new pipeline."""
        if not args:
            return r[str].fail(
                "Pipeline creation requires pipeline name and JSON configuration",
            )
        pipeline_name = args[0]
        config_payload: t.JsonMapping | None = None
        if len(args) >= c.Meltano.CLI_DEFAULT_MIN_ARGS_WITH_CONFIG:
            loaded_config_result = u.Cli.json_loads(args[1])
            if loaded_config_result.failure:
                return r[str].fail(
                    loaded_config_result.error
                    or "pipeline configuration JSON could not be parsed",
                )
            try:
                config_payload = m.Meltano.ConfigMappingPayload.model_validate({
                    "values": loaded_config_result.value,
                }).values
            except ValueError as exc:
                return e.fail_validation(
                    "pipeline configuration JSON",
                    error=exc,
                    result_type=r[str],
                )
        return self.create_pipeline(pipeline_name, config_payload)

    def _delete_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Delete a pipeline."""
        if not args:
            return r[str].fail("Pipeline delete requires pipeline name")
        return self.delete_pipeline(args[0])

    def _dispatch_pipeline(
        self,
        subcommand: str,
        args: t.StrSequence,
    ) -> p.Result[str]:
        """Dispatch one pipeline subcommand to the matching handler."""
        match subcommand:
            case c.Meltano.PipelineCommand.CREATE:
                return self._create_pipeline(args)
            case c.Meltano.PipelineCommand.RUN:
                return self._run_pipeline(args)
            case c.Meltano.PipelineCommand.LIST:
                return self._list_pipelines()
            case c.Meltano.PipelineCommand.STATUS:
                return self._fetch_pipeline_status(args)
            case c.Meltano.PipelineCommand.STOP:
                return self._stop_pipeline(args)
            case c.Meltano.PipelineCommand.DELETE:
                return self._delete_pipeline(args)
            case _:
                return r[str].fail(f"Unknown pipeline command: {subcommand}")

    def _fetch_pipeline_status(self, args: t.StrSequence) -> p.Result[str]:
        """Fetch one pipeline status."""
        if not args:
            return r[str].fail("Pipeline status requires pipeline name")
        return self.fetch_pipeline_status(args[0])

    def _list_pipelines(self) -> p.Result[str]:
        """List pipelines as one CLI-renderable string."""
        return self.list_pipelines().map(
            lambda pipelines: ", ".join(pipelines) or "none",
        )

    def _run_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Run a persisted pipeline."""
        if not args:
            return r[str].fail("Pipeline execution requires pipeline name")
        pipeline_name = args[0]
        command_args = args[1:] if len(args) > 1 else None
        return self.execute_pipeline(pipeline_name, command_args)

    def _stop_pipeline(self, args: t.StrSequence) -> p.Result[str]:
        """Stop a running pipeline."""
        if not args:
            return r[str].fail("Pipeline stop requires pipeline name")
        return self.stop_pipeline(args[0])


__all__: list[str] = ["FlextMeltanoPipelineManager"]
