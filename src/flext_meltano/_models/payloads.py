"""FLEXT Meltano models - API operation payload models."""

from __future__ import annotations

from typing import Annotated

from flext_cli import m
from pydantic import Field

from flext_meltano import t


class FlextMeltanoModelsPayloads:
    """API payload models for pipeline operations."""

    class CreatePipelinePayload(m.ArbitraryTypesModel):
        """Payload for create_pipeline operation."""

        tap_name: Annotated[t.NonEmptyStr, Field(description="Singer tap name")]
        target_name: Annotated[str, Field(description="Singer target name")]
        settings: Annotated[
            t.ContainerMapping,
            Field(description="Pipeline settings"),
        ] = Field(default_factory=dict, description="Pipeline settings")

    class ExecutePipelinePayload(m.ArbitraryTypesModel):
        """Payload for execute_pipeline operation."""

        pipeline_id: Annotated[str, Field(description="Pipeline identifier")]
        settings: Annotated[
            t.ContainerMapping,
            Field(description="Execution settings"),
        ] = Field(default_factory=dict, description="Execution settings")

    class InstallPluginPayload(m.ArbitraryTypesModel):
        """Payload for install_plugin operation."""

        plugin_type: Annotated[t.NonEmptyStr, Field(description="Plugin type")]
        plugin_name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
        settings: Annotated[
            t.ContainerMapping,
            Field(description="Plugin settings"),
        ] = Field(default_factory=dict, description="Plugin settings")

    class ListPluginsPayload(m.ArbitraryTypesModel):
        """Payload for list_plugins operation."""

        plugin_type: Annotated[
            str | None, Field(default=None, description="Filter by plugin type")
        ] = None

    class ConfigureEnvironmentPayload(m.ArbitraryTypesModel):
        """Payload for configure_environment operation."""

        environment_name: Annotated[str, Field(description="Environment name")]
        settings: Annotated[
            t.ContainerMapping,
            Field(description="Environment settings"),
        ] = Field(default_factory=dict, description="Environment settings")

    class RunDbtModelsPayload(m.ArbitraryTypesModel):
        """Payload for run/test dbt models operation."""

        models: Annotated[
            t.StrSequence | None, Field(default=None, description="Models to run")
        ] = None
        settings: Annotated[
            t.ContainerMapping | None,
            Field(default=None, description="Execution settings"),
        ] = None

    class RunEltPipelinePayload(m.ArbitraryTypesModel):
        """Payload for run_elt_pipeline operation."""

        tap_name: Annotated[t.NonEmptyStr, Field(description="Singer tap name")]
        target_name: Annotated[str, Field(description="Singer target name")]
        dbt_models: Annotated[
            t.StrSequence | None, Field(default=None, description="DBT models to run")
        ] = None
        settings: Annotated[
            t.ContainerMapping | None,
            Field(default=None, description="Pipeline settings"),
        ] = None
