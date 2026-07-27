"""FLEXT Meltano Protocols - Base protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_meltano._protocols.services import FlextMeltanoProtocolsServices


class FlextMeltanoProtocolsBase:
    """Base and Stream protocol definitions."""

    @runtime_checkable
    class PipelineCli(Protocol):
        def show_pipeline_help(self) -> None: ...

    @runtime_checkable
    class SingerCli(Protocol):
        def show_tap_help(self) -> None: ...

        def show_target_help(self) -> None: ...

    @runtime_checkable
    class DbtCli(Protocol):
        def show_dbt_help(self) -> None: ...

    @runtime_checkable
    class PluginCli(Protocol):
        def show_plugin_help(self) -> None: ...

    @runtime_checkable
    class StatusCli(Protocol):
        def show_status_help(self) -> None: ...

    @runtime_checkable
    class CommandRouterCli(Protocol):
        @property
        def pipeline_manager(self) -> FlextMeltanoProtocolsServices.CLIManager: ...

        @property
        def singer_manager(self) -> FlextMeltanoProtocolsServices.SingerManager: ...

        @property
        def dbt_manager(self) -> FlextMeltanoProtocolsServices.CLIManager: ...

        @property
        def plugin_manager(self) -> FlextMeltanoProtocolsServices.CLIManager: ...

        @property
        def status_manager(self) -> FlextMeltanoProtocolsServices.StatusManager: ...

        def show_banner(self) -> None: ...
