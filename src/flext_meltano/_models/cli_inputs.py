"""FLEXT Meltano models - CLI input models for flext_cli.cli model-driven commands."""

from __future__ import annotations

from typing import Annotated

from flext_cli import m, t, u


class FlextMeltanoModelsCliInputs:
    """CLI input models consumed by the canonical flext_cli.cli router."""

    class PipelineCreateInput(m.BaseModel):
        """Create a persisted pipeline from a name and optional JSON config."""

        pipeline_name: Annotated[
            str, u.Field(description="Name of the pipeline to create")
        ]
        config_json: Annotated[
            str | None,
            u.Field(
                default=None, description="Pipeline configuration as a JSON string"
            ),
        ] = None

    class PipelineRunInput(m.BaseModel):
        """Run a persisted pipeline with optional extra arguments."""

        pipeline_name: Annotated[
            str, u.Field(description="Name of the pipeline to run")
        ]
        # mro-wkii.17 (codex): keep the runtime annotation resolvable so the
        # model-driven CLI preserves the optional immutable sequence default.
        args: Annotated[
            t.StrSequence,
            u.Field(
                default_factory=tuple,
                description="Extra arguments forwarded to the pipeline command",
            ),
        ]

    class PipelineNameInput(m.BaseModel):
        """Reference one persisted pipeline by name."""

        pipeline_name: Annotated[str, u.Field(description="Name of the pipeline")]

    class PipelineListInput(m.BaseModel):
        """List all persisted pipelines."""

    class PluginListInput(m.BaseModel):
        """List discovered plugins, optionally filtered by type."""

        plugin_type: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Optional plugin type filter (e.g. tap, target)",
            ),
        ] = None

    class PluginInfoInput(m.BaseModel):
        """Fetch information about one plugin."""

        plugin_type: Annotated[
            str, u.Field(description="Plugin type (e.g. tap, target)")
        ]
        plugin_name: Annotated[str, u.Field(description="Plugin name")]

    class PluginInstallInput(m.BaseModel):
        """Placeholder for plugin installation (not supported)."""

        plugin_name: Annotated[str, u.Field(description="Plugin name to install")]

    class StatusShowInput(m.BaseModel):
        """Show Meltano runtime status."""

    class StatusHealthInput(m.BaseModel):
        """Check Meltano service health."""

    class DbtInput(m.BaseModel):
        """Dispatch one DBT subcommand with optional arguments."""

        subcommand: Annotated[
            str, u.Field(description="DBT subcommand (run, test, compile, docs)")
        ]
        args: Annotated[
            t.StrSequence,
            u.Field(
                default_factory=tuple, description="Extra arguments forwarded to DBT"
            ),
        ]

    class TapInput(m.BaseModel):
        """Dispatch one tap operation with optional arguments."""

        operation: Annotated[
            str | None, u.Field(default=None, description="Tap operation name")
        ] = None
        args: Annotated[
            t.StrSequence,
            u.Field(
                default_factory=tuple,
                description="Extra arguments forwarded to the tap operation",
            ),
        ]

    class TargetInput(m.BaseModel):
        """Dispatch one target operation with optional arguments."""

        operation: Annotated[
            str | None, u.Field(default=None, description="Target operation name")
        ] = None
        args: Annotated[
            t.StrSequence,
            u.Field(
                default_factory=tuple,
                description="Extra arguments forwarded to the target operation",
            ),
        ]

    class VersionInput(m.BaseModel):
        """Show the FLEXT Meltano version."""


__all__: list[str] = ["FlextMeltanoModelsCliInputs"]
