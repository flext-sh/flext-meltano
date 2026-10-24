"""FLEXT Meltano Protocols - Base executor and dbt project protocols.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import p

from flext_meltano import t

if TYPE_CHECKING:
    from flext_meltano import m


class FlextMeltanoProtocolsBase:
    """Base executor and dbt project protocol definitions."""

    @runtime_checkable
    class MeltanoExecutor(Protocol):
        """Protocol for Meltano command execution."""

        def execute_meltano_command(
            self,
            command: t.StrSequence,
            timeout: int = ...,
            _cwd: Path | None = None,
        ) -> p.Result[m.Meltano.CommandExecutionResult]:
            """Execute a Meltano runtime command."""
            ...

        def fetch_project_plugins(
            self,
            plugin_type: str | None = None,
            _cwd: Path | None = None,
        ) -> p.Result[t.SequenceOf[t.StrMapping]]:
            """Return project-scoped plugin definitions."""
            ...

        def execute_dbt_command(
            self,
            dbt_command: str,
            args: t.StrSequence | None = None,
        ) -> p.Result[m.Meltano.CommandExecutionResult]:
            """Execute a DBT command."""
            ...

    @runtime_checkable
    class DbtConnectionProfile(Protocol):
        """Canonical dbt connection profile surface.

        Consumer DBT projects expose a typed model (``m.<Ns>.DbtConnectionProfile``)
        satisfying this protocol rather than passing raw dictionaries.
        """

        @property
        def type(self) -> str:
            """DBT adapter type."""
            ...

        @property
        def project(self) -> str:
            """DBT project name."""
            ...

        def model_dump(self, *, mode: str = ...) -> t.JsonMapping:
            """Serialize the profile to a JSON-safe mapping."""
            ...


__all__: list[str] = ["FlextMeltanoProtocolsBase"]
