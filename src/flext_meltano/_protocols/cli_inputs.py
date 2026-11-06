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
    class PipelineCreateInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        pipeline_name: str
        config_json: str | None

    @runtime_checkable
    class PipelineRunInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        pipeline_name: str
        args: Sequence[str]

    @runtime_checkable
    class PipelineNameInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        pipeline_name: str

    @runtime_checkable
    class PipelineListInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class PluginListInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        plugin_type: str | None

    @runtime_checkable
    class PluginInfoInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        plugin_type: str
        plugin_name: str

    @runtime_checkable
    class PluginInstallInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        plugin_name: str

    @runtime_checkable
    class StatusShowInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class StatusHealthInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class DbtInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        subcommand: str
        args: Sequence[str]

    @runtime_checkable
    class TapInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        operation: str | None
        args: Sequence[str]

    @runtime_checkable
    class TargetInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        operation: str | None
        args: Sequence[str]

    @runtime_checkable
    class VersionInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""


__all__: list[str] = [
    "FlextMeltanoProtocolsCliInputs",
]
