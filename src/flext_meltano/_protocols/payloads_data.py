# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/payloads_data
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_meltano import t


class FlextMeltanoProtocolsPayloadsData:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ConfigMappingPayload(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        values: t.JsonMapping

    @runtime_checkable
    class PathPayload(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        value: Path


__all__: list[str] = [
    "FlextMeltanoProtocolsPayloadsData",
]
