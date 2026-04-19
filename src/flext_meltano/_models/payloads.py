"""FLEXT Meltano models - API operation payload models."""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsPayloads:
    """API payload models for pipeline operations."""

    class CreatePipelinePayload(m.ArbitraryTypesModel):
        """Payload for create_pipeline operation."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        tap_name: Annotated[t.NonEmptyStr, u.Field(description="Singer tap name")]
        target_name: Annotated[str, u.Field(description="Singer target name")]
        settings: Annotated[
            Mapping[str, t.Container],
            u.Field(description="Pipeline settings"),
        ] = u.Field(default_factory=dict)

    class ExecutePipelinePayload(m.ArbitraryTypesModel):
        """Payload for execute_pipeline operation."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        pipeline_id: Annotated[str, u.Field(description="Pipeline identifier")]
        settings: Annotated[
            Mapping[str, t.Container],
            u.Field(description="Execution settings"),
        ] = u.Field(default_factory=dict)

    class InstallPluginPayload(m.ArbitraryTypesModel):
        """Payload for install_plugin operation."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        plugin_type: Annotated[t.NonEmptyStr, u.Field(description="Plugin type")]
        plugin_name: Annotated[t.NonEmptyStr, u.Field(description="Plugin name")]
        settings: Annotated[
            Mapping[str, t.Container],
            u.Field(description="Plugin settings"),
        ] = u.Field(default_factory=dict)

    class ListPluginsPayload(m.ArbitraryTypesModel):
        """Payload for list_plugins operation."""

        plugin_type: Annotated[
            str | None, u.Field(default=None, description="Filter by plugin type")
        ] = None

    class ConfigureEnvironmentPayload(m.ArbitraryTypesModel):
        """Payload for configure_environment operation."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        environment_name: Annotated[str, u.Field(description="Environment name")]
        settings: Annotated[
            Mapping[str, t.Container],
            u.Field(description="Environment settings"),
        ] = u.Field(default_factory=dict)

    class RunDbtModelsPayload(m.ArbitraryTypesModel):
        """Payload for run/test dbt models operation."""

        models: Annotated[
            t.StrSequence | None, u.Field(default=None, description="Models to run")
        ] = None
        settings: Annotated[
            Mapping[str, t.Container] | None,
            u.Field(default=None, description="Execution settings"),
        ] = None

    class RunEltPipelinePayload(m.ArbitraryTypesModel):
        """Payload for run_elt_pipeline operation."""

        tap_name: Annotated[t.NonEmptyStr, u.Field(description="Singer tap name")]
        target_name: Annotated[str, u.Field(description="Singer target name")]
        dbt_models: Annotated[
            t.StrSequence | None, u.Field(default=None, description="DBT models to run")
        ] = None
        settings: Annotated[
            Mapping[str, t.Container] | None,
            u.Field(default=None, description="Pipeline settings"),
        ] = None
