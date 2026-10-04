"""FLEXT Meltano models - API operation payload models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated

from flext_cli import m

from flext_meltano import t


class FlextMeltanoModelsPayloads:
    """API payload models for pipeline operations."""

    class FrozenConfigPayload(m.ArbitraryTypesModel):
        """Payload base owning a read-only flat operation config mapping."""

        config: Annotated[
            t.FlatContainerMapping, m.Field(description="Operation config"),
        ] = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Operation config",
        )

        @m.field_validator("config", mode="after")
        @classmethod
        def freeze_config(cls, value: t.FlatContainerMapping) -> t.FlatContainerMapping:
            """Expose the operation configuration as read-only.

            Returns:
                The resulting ``t.FlatContainerMapping``.
            """
            return MappingProxyType(dict(value))

    class CreatePipelinePayload(FrozenConfigPayload):
        """Payload for create_pipeline operation."""

        tap_name: Annotated[t.NonEmptyStr, m.Field(description="Singer tap name")]
        target_name: Annotated[str, m.Field(description="Singer target name")]

    class ExecutePipelinePayload(FrozenConfigPayload):
        """Payload for execute_pipeline operation."""

        pipeline_id: Annotated[str, m.Field(description="Pipeline identifier")]

    class InstallPluginPayload(FrozenConfigPayload):
        """Payload for install_plugin operation."""

        plugin_type: Annotated[t.NonEmptyStr, m.Field(description="Plugin type")]
        plugin_name: Annotated[t.NonEmptyStr, m.Field(description="Plugin name")]

    class ListPluginsPayload(m.ArbitraryTypesModel):
        """Payload for list_plugins operation."""

        plugin_type: Annotated[
            str | None, m.Field(default=None, description="Filter by plugin type"),
        ] = None

    class ConfigureEnvironmentPayload(FrozenConfigPayload):
        """Payload for configure_environment operation."""

        environment_name: Annotated[str, m.Field(description="Environment name")]

    class RunDbtModelsPayload(m.ArbitraryTypesModel):
        """Payload for run/test dbt models operation."""

        models: Annotated[
            t.StrSequence | None, m.Field(default=None, description="Models to run"),
        ] = None
        config: Annotated[
            t.FlatContainerMapping | None,
            m.Field(default=None, description="Execution config"),
        ] = None

    class RunEltPipelinePayload(m.ArbitraryTypesModel):
        """Payload for run_elt_pipeline operation."""

        tap_name: Annotated[t.NonEmptyStr, m.Field(description="Singer tap name")]
        target_name: Annotated[str, m.Field(description="Singer target name")]
        dbt_models: Annotated[
            t.StrSequence | None
            , m.Field(default=None, description="DBT models to run"),
        ] = None
        config: Annotated[
            t.FlatContainerMapping | None,
            m.Field(default=None, description="Pipeline config"),
        ] = None
