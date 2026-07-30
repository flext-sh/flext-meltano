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
        config: Annotated[
            t.FlatContainerMapping,
            Field(description="Pipeline config"),
        ] = Field(default_factory=dict, description="Pipeline config")

    class ExecutePipelinePayload(m.ArbitraryTypesModel):
        """Payload for execute_pipeline operation."""

        pipeline_id: Annotated[str, Field(description="Pipeline identifier")]
        config: Annotated[
            t.FlatContainerMapping,
            Field(description="Execution config"),
        ] = Field(default_factory=dict, description="Execution config")

    class InstallPluginPayload(m.ArbitraryTypesModel):
        """Payload for install_plugin operation."""

        plugin_type: Annotated[t.NonEmptyStr, Field(description="Plugin type")]
        plugin_name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
        config: Annotated[
            t.FlatContainerMapping,
            Field(description="Plugin config"),
        ] = Field(default_factory=dict, description="Plugin config")

    class ListPluginsPayload(m.ArbitraryTypesModel):
        """Payload for list_plugins operation."""

        plugin_type: Annotated[
            str | None, Field(default=None, description="Filter by plugin type")
        ] = None

    class ConfigureEnvironmentPayload(m.ArbitraryTypesModel):
        """Payload for configure_environment operation."""

        environment_name: Annotated[str, Field(description="Environment name")]
        config: Annotated[
            t.FlatContainerMapping,
            Field(description="Environment config"),
        ] = Field(default_factory=dict, description="Environment config")

    class RunDbtModelsPayload(m.ArbitraryTypesModel):
        """Payload for run/test dbt models operation."""

        models: Annotated[
            t.StrSequence | None, Field(default=None, description="Models to run")
        ] = None
        config: Annotated[
            t.FlatContainerMapping | None,
            Field(default=None, description="Execution config"),
        ] = None

    class RunEltPipelinePayload(m.ArbitraryTypesModel):
        """Payload for run_elt_pipeline operation."""

        tap_name: Annotated[t.NonEmptyStr, Field(description="Singer tap name")]
        target_name: Annotated[str, Field(description="Singer target name")]
        dbt_models: Annotated[
            t.StrSequence | None, Field(default=None, description="DBT models to run")
        ] = None
        config: Annotated[
            t.FlatContainerMapping | None,
            Field(default=None, description="Pipeline config"),
        ] = None
