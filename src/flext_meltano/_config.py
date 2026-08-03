"""FlextMeltanoConfig — frozen config singleton for flext-meltano (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Meltano:`` key and
are exposed through the open ``config.Meltano`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Meltano.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliConfig, m


class _MeltanoNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = m.ConfigDict(extra="allow", frozen=True)


class FlextMeltanoConfig(FlextCliConfig):
    """Meltano config auto-loaded model-less from ``config/*.yaml``."""

    Meltano: _MeltanoNamespace = _MeltanoNamespace()


config: FlextMeltanoConfig = FlextMeltanoConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_meltano import config``."""

__all__: list[str] = ["FlextMeltanoConfig", "config"]
