"""FLEXT Meltano Protocols - Base protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from flext_meltano import FlextMeltanoProtocolsServices


class FlextMeltanoProtocolsBase:
    """Base and Stream protocol definitions."""

    class SingerCli(Protocol):
        def show_tap_help(self) -> None: ...

        def show_target_help(self) -> None: ...

    class DbtCli(Protocol):
        def show_dbt_help(self) -> None: ...

    class PluginCli(Protocol):
        def show_plugin_help(self) -> None: ...

    class StatusCli(Protocol):
        def show_status_help(self) -> None: ...

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
