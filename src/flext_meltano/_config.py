"""FlextMeltanoConfig — frozen config singleton for flext-meltano (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Meltano:`` key and
are exposed through the open ``config.Meltano`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Meltano.<domain>[<key>...]``.


Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_cli import FlextCliConfig

from flext_core import FlextSettings
from flext_meltano import m


class FlextMeltanoConfig(FlextSettings, FlextCliConfig):
    """Meltano config auto-loaded model-less from ``config/*.yaml``."""

    # Why: the two bases each declare the singleton slot with their own class
    # as the value type. The concrete subclass is assignable to both, which
    # resolves the mypy MRO conflict, but pyright checks variable overrides
    # invariantly against each base separately and no single type satisfies
    # both declarations; the family-wide diamond (FlextSettings, FlextCliConfig)
    # is the upstream owner shape, so the unsatisfiable invariant check is
    # admitted explicitly on this one line.
    _instance: ClassVar[FlextMeltanoConfig | None] = None  # pyright: ignore[reportIncompatibleVariableOverride]

    Meltano: Annotated[
        m.Meltano.MeltanoNamespace,
        m.Field(
            description="Open namespace exposing ``config/*.yaml`` under ``Meltano``.",
        ),
    ] = m.Meltano.MeltanoNamespace()


config: FlextMeltanoConfig = FlextMeltanoConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_meltano import config``."""

__all__: list[str] = ["FlextMeltanoConfig", "config"]
