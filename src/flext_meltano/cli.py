"""FLEXT Meltano CLI public facade."""

from __future__ import annotations

import sys
from typing import ClassVar

from flext_cli import cli
from flext_meltano import FlextMeltano, c, e, m, p, r, t, u
from flext_meltano.pipeline_mgr import FlextMeltanoPipelineManager


class FlextMeltanoCli:
    """Model-driven CLI facade for FLEXT Meltano operations."""

    app_name: ClassVar[str] = "flext-meltano"
    app_help: ClassVar[str] = "FLEXT Meltano operations"

    def __init__(self) -> None:
        """Initialize the CLI with service and pipeline manager facades."""
        self._service = FlextMeltano.fetch_global()
        self._pipeline_mgr = FlextMeltanoPipelineManager()
        self._app = cli.create_app_with_common_params(
            name=self.app_name,
            help_text=self.app_help,
        )
        self._register_commands()

    def run(self, args: t.StrSequence | None = None) -> p.Result[bool]:
        """Run the CLI with the given arguments."""
        return cli.execute_app(self._app, prog_name=self.app_name, args=args)

    def _register_commands(self) -> None:
        self._register_version_command()
        self._register_status_commands()
        self._register_tap_command()
        self._register_target_command()
        self._register_dbt_command()
        self._register_plugin_commands()
        self._register_pipeline_commands()

    def _register_version_command(self) -> None:
        cli.register_result_command(
            self._app,
            name=c.Meltano.Command.VERSION,
            help_text="Show the FLEXT Meltano version",
            model_cls=m.Meltano.VersionInput,
            handler=self._handle_version,
        )

    def _handle_version(self, _model: p.Meltano.VersionInput) -> p.Result[str]:
        return self._service.fetch_version()

    def _register_status_commands(self) -> None:
        status_group = cli.create_group(
            name=c.Meltano.Command.STATUS,
            help_text="Meltano status operations",
        )
        cli.register_result_command(
            status_group,
            name="show",
            help_text="Show Meltano runtime status",
            model_cls=m.Meltano.StatusShowInput,
            handler=self._handle_status_show,
        )
        cli.register_result_command(
            status_group,
            name=c.Meltano.ExecutorCommand.HEALTH,
            help_text="Check Meltano service health",
            model_cls=m.Meltano.StatusHealthInput,
            handler=self._handle_status_health,
        )
        cli.add_group(self._app, name=c.Meltano.Command.STATUS, group=status_group)

    def _handle_status_show(self, _model: p.Meltano.StatusShowInput) -> p.Result[str]:
        return self._service.run_cli([]).flat_map(
            lambda payload: u.Cli.json_dumps(
                t.json_dict_adapter().validate_python(payload),
            )
        )

    def _handle_status_health(
        self,
        _model: p.Meltano.StatusHealthInput,
    ) -> p.Result[str]:
        return self._service.health().flat_map(
            lambda payload: u.Cli.json_dumps(
                t.json_dict_adapter().validate_python(payload),
            )
        )

    def _register_tap_command(self) -> None:
        cli.register_result_command(
            self._app,
            name=c.Meltano.Command.TAP,
            help_text="Tap operations",
            model_cls=m.Meltano.TapInput,
            handler=self._handle_tap,
        )

    def _handle_tap(self, model: p.Meltano.TapInput) -> p.Result[str]:
        if model.operation is None or u.Meltano.is_help_request([model.operation]):
            return r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        return r[str].fail(f"Tap operation '{model.operation}' is not supported")

    def _register_target_command(self) -> None:
        cli.register_result_command(
            self._app,
            name=c.Meltano.Command.TARGET,
            help_text="Target operations",
            model_cls=m.Meltano.TargetInput,
            handler=self._handle_target,
        )

    def _handle_target(self, model: p.Meltano.TargetInput) -> p.Result[str]:
        if model.operation is None or u.Meltano.is_help_request([model.operation]):
            return r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        return r[str].fail(f"Target operation '{model.operation}' is not supported")

    def _register_dbt_command(self) -> None:
        cli.register_result_command(
            self._app,
            name=c.Meltano.Command.DBT,
            help_text="Run DBT subcommands",
            model_cls=m.Meltano.DbtInput,
            handler=self._handle_dbt,
        )

    def _handle_dbt(self, model: p.Meltano.DbtInput) -> p.Result[str]:
        if u.Meltano.is_help_request([model.subcommand]):
            return r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        result = self._service.execute_dbt_command(model.subcommand, model.args)
        if result.failure:
            return r[str].fail(result.error or "DBT command failed")
        if not result.value.success:
            return r[str].fail(result.value.error or result.value.output)
        return r[str].ok(result.value.output)

    def _register_plugin_commands(self) -> None:
        plugin_group = cli.create_group(
            name=c.Meltano.Command.PLUGIN,
            help_text="Meltano plugin operations",
        )
        cli.register_result_command(
            plugin_group,
            name=c.Meltano.ExecutorCommand.LIST,
            help_text="List discovered plugins",
            model_cls=m.Meltano.PluginListInput,
            handler=self._handle_plugin_list,
        )
        cli.register_result_command(
            plugin_group,
            name=c.Meltano.ExecutorCommand.INFO,
            help_text="Fetch information about a plugin",
            model_cls=m.Meltano.PluginInfoInput,
            handler=self._handle_plugin_info,
        )
        cli.register_result_command(
            plugin_group,
            name=c.Meltano.ExecutorCommand.INSTALL,
            help_text="Install a plugin",
            model_cls=m.Meltano.PluginInstallInput,
            handler=self._handle_plugin_install,
        )
        cli.add_group(
            self._app,
            name=c.Meltano.Command.PLUGIN,
            group=plugin_group,
        )

    def _handle_plugin_list(
        self,
        model: p.Meltano.PluginListInput,
    ) -> p.Result[str]:
        plugin_type = (
            u.Meltano.normalize_plugin_group(model.plugin_type)
            if model.plugin_type is not None
            else None
        )
        return (
            self._service
            .discover_plugins()
            .map(
                lambda plugins: [
                    t.json_dict_adapter().validate_python(plugin)
                    for plugin in plugins
                    if plugin_type is None or plugin.get("type") == plugin_type
                ]
            )
            .flat_map(
                lambda payload: u.Cli.json_dumps(
                    list(t.Cli.JSON_LIST_ADAPTER.validate_python(payload))
                )
            )
        )

    def _handle_plugin_info(
        self,
        model: p.Meltano.PluginInfoInput,
    ) -> p.Result[str]:
        plugin_type = u.Meltano.normalize_plugin_group(model.plugin_type)
        if plugin_type is None:
            return r[str].fail("Plugin info requires a valid plugin type")
        return self._service.fetch_plugin_info(
            model.plugin_name,
            plugin_type,
        ).flat_map(
            lambda payload: u.Cli.json_dumps(
                t.json_dict_adapter().validate_python(payload),
            )
        )

    def _handle_plugin_install(
        self,
        _model: p.Meltano.PluginInstallInput,
    ) -> p.Result[str]:
        return r[str].fail("Plugin install is not supported by this CLI")

    def _register_pipeline_commands(self) -> None:
        pipeline_group = cli.create_group(
            name=c.Meltano.Command.PIPELINE,
            help_text="Pipeline operations",
        )
        cli.register_result_command(
            pipeline_group,
            name=c.Meltano.PipelineCommand.CREATE,
            help_text="Create a persisted pipeline",
            model_cls=m.Meltano.PipelineCreateInput,
            handler=self._handle_pipeline_create,
        )
        cli.register_result_command(
            pipeline_group,
            name=c.Meltano.PipelineCommand.RUN,
            help_text="Run a persisted pipeline",
            model_cls=m.Meltano.PipelineRunInput,
            handler=self._handle_pipeline_run,
        )
        cli.register_result_command(
            pipeline_group,
            name=c.Meltano.PipelineCommand.LIST,
            help_text="List persisted pipelines",
            model_cls=m.Meltano.PipelineListInput,
            handler=self._handle_pipeline_list,
        )
        cli.register_result_command(
            pipeline_group,
            name=c.Meltano.PipelineCommand.STATUS,
            help_text="Show pipeline status",
            model_cls=m.Meltano.PipelineNameInput,
            handler=self._handle_pipeline_status,
        )
        cli.register_result_command(
            pipeline_group,
            name=c.Meltano.PipelineCommand.STOP,
            help_text="Stop a running pipeline",
            model_cls=m.Meltano.PipelineNameInput,
            handler=self._handle_pipeline_stop,
        )
        cli.register_result_command(
            pipeline_group,
            name=c.Meltano.PipelineCommand.DELETE,
            help_text="Delete a persisted pipeline",
            model_cls=m.Meltano.PipelineNameInput,
            handler=self._handle_pipeline_delete,
        )
        cli.add_group(
            self._app,
            name=c.Meltano.Command.PIPELINE,
            group=pipeline_group,
        )

    def _handle_pipeline_create(
        self,
        model: p.Meltano.PipelineCreateInput,
    ) -> p.Result[str]:
        config_payload: t.JsonMapping | None = None
        if model.config_json is not None:
            loaded_config_result = u.Cli.json_loads(model.config_json)
            if loaded_config_result.failure:
                return r[str].fail(
                    loaded_config_result.error
                    or "Pipeline configuration JSON could not be parsed"
                )
            try:
                config_payload = m.Meltano.ConfigMappingPayload.model_validate({
                    "values": loaded_config_result.value
                }).values
            except ValueError as exc:
                return e.fail_validation(
                    "pipeline configuration JSON",
                    error=exc,
                    result_type=r[str],
                )
        return self._pipeline_mgr.create_pipeline(model.pipeline_name, config_payload)

    def _handle_pipeline_run(self, model: p.Meltano.PipelineRunInput) -> p.Result[str]:
        command_args = model.args or None
        return self._pipeline_mgr.execute_pipeline(model.pipeline_name, command_args)

    def _handle_pipeline_list(
        self,
        _model: p.Meltano.PipelineListInput,
    ) -> p.Result[str]:
        return self._pipeline_mgr.list_pipelines().map(
            lambda pipelines: ", ".join(pipelines) or "none"
        )

    def _handle_pipeline_status(
        self,
        model: p.Meltano.PipelineNameInput,
    ) -> p.Result[str]:
        return self._pipeline_mgr.fetch_pipeline_status(model.pipeline_name)

    def _handle_pipeline_stop(
        self,
        model: p.Meltano.PipelineNameInput,
    ) -> p.Result[str]:
        return self._pipeline_mgr.stop_pipeline(model.pipeline_name)

    def _handle_pipeline_delete(
        self,
        model: p.Meltano.PipelineNameInput,
    ) -> p.Result[str]:
        return self._pipeline_mgr.delete_pipeline(model.pipeline_name)


def main() -> int:
    """Run the FLEXT Meltano CLI main entry point."""
    result = FlextMeltanoCli().run(sys.argv[1:])
    return 0 if result.success else 1


__all__: list[str] = ["FlextMeltanoCli", "main"]
