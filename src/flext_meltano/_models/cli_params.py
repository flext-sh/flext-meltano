"""FLEXT Meltano models - CLI parameter models."""

from __future__ import annotations

from typing import Annotated

from flext_cli import m, u


class FlextMeltanoModelsCliParams:
    """CLI parameter models for pipeline operations."""

    class CliDataSourceParams(m.Entity):
        """Generic parameters for data source operations."""

        source_name: Annotated[
            str,
            u.Field(description="Name of the data source"),
        ]
        config_file: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Path to source configuration file",
            ),
        ] = None
        catalog_file: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Path to catalog file for schema discovery",
            ),
        ] = None
        state_file: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Path to state file for incremental sync",
            ),
        ] = None
        discover: Annotated[
            bool,
            u.Field(
                default=False,
                description="Run in discovery mode to output schema",
            ),
        ] = False

    class CliDataSinkParams(m.Entity):
        """Generic parameters for data sink operations."""

        sink_name: Annotated[str, u.Field(description="Name of the data sink")]
        config_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to sink configuration file"),
        ] = None
        input_file: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Path to input data file (default: stdin)",
            ),
        ] = None

    class CliPipelineParams(m.Entity):
        """Generic parameters for pipeline operations."""

        source_name: Annotated[
            str,
            u.Field(description="Name of the data source"),
        ]
        sink_name: Annotated[str, u.Field(description="Name of the data sink")]
        source_config: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Path to source configuration file",
            ),
        ] = None
        sink_config: Annotated[
            str | None,
            u.Field(default=None, description="Path to sink configuration file"),
        ] = None
        catalog_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to catalog file"),
        ] = None
        state_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to state file"),
        ] = None
        state_output_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to write final state"),
        ] = None

    class CliTransformationParams(m.Entity):
        """Generic parameters for transformation operations."""

        project_dir: Annotated[
            str,
            u.Field(description="Transformation project directory"),
        ]
        models: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Specific models to run (space-separated)",
            ),
        ] = None
        select: Annotated[
            str | None,
            u.Field(default=None, description="Selection syntax for models"),
        ] = None
        exclude: Annotated[
            str | None,
            u.Field(default=None, description="Exclusion syntax for models"),
        ] = None
        full_refresh: Annotated[
            bool,
            u.Field(default=False, description="Run with full refresh"),
        ] = False

    class PipelineRunParams(m.Entity):
        """Parameters for pipeline run operations."""

        tap_name: Annotated[str, u.Field(description="Name of the tap to run")]
        target_name: Annotated[str, u.Field(description="Name of the target to run")]
        catalog_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to catalog file"),
        ] = None
        state_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to state file"),
        ] = None
        state_output_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to write final state"),
        ] = None
        tap_config: Annotated[
            str | None,
            u.Field(default=None, description="Path to tap configuration file"),
        ] = None
        target_config: Annotated[
            str | None,
            u.Field(default=None, description="Path to target configuration file"),
        ] = None
        full_refresh: Annotated[
            bool,
            u.Field(default=False, description="Run with full refresh"),
        ] = False
