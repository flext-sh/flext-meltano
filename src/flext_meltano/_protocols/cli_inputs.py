# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/cli_inputs
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols


class FlextMeltanoProtocolsCliInputs:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class PipelineCreateInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def pipeline_name(self) -> str:
            """Name of the pipeline to create."""
            ...

        @property
        def config_json(self) -> str | None:
            """Pipeline configuration as a JSON string."""
            ...

    @runtime_checkable
    class PipelineRunInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def pipeline_name(self) -> str:
            """Name of the pipeline to run."""
            ...

        @property
        def args(self) -> Sequence[str]:
            """Extra arguments forwarded to the pipeline command."""
            ...

    @runtime_checkable
    class PipelineNameInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def pipeline_name(self) -> str:
            """Name of the pipeline."""
            ...

    @runtime_checkable
    class PipelineListInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class PluginListInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def plugin_type(self) -> str | None:
            """Optional plugin type filter (e.g. tap, target)."""
            ...

    @runtime_checkable
    class PluginInfoInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def plugin_type(self) -> str:
            """Plugin type (e.g. tap, target)."""
            ...

        @property
        def plugin_name(self) -> str:
            """Plugin name."""
            ...

    @runtime_checkable
    class PluginInstallInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def plugin_name(self) -> str:
            """Plugin name to install."""
            ...

    @runtime_checkable
    class StatusShowInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class StatusHealthInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class DbtInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def subcommand(self) -> str:
            """DBT subcommand (run, test, compile, docs)."""
            ...

        @property
        def args(self) -> Sequence[str]:
            """Extra arguments forwarded to DBT."""
            ...

    @runtime_checkable
    class TapInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def operation(self) -> str | None:
            """Tap operation name."""
            ...

        @property
        def args(self) -> Sequence[str]:
            """Extra arguments forwarded to the tap operation."""
            ...

    @runtime_checkable
    class TargetInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def operation(self) -> str | None:
            """Target operation name."""
            ...

        @property
        def args(self) -> Sequence[str]:
            """Extra arguments forwarded to the target operation."""
            ...

    @runtime_checkable
    class VersionInput(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""


__all__: list[str] = [
    "FlextMeltanoProtocolsCliInputs",
]
