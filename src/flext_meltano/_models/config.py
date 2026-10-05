"""FLEXT Meltano models - Config namespace models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m


class FlextMeltanoModelsConfig:
    """Config namespace models for model-less ``config/*.yaml`` exposure."""

    class MeltanoNamespace(m.BaseModel):
        """Open, frozen namespace exposing every ``config/*.yaml`` domain."""

        model_config = m.ConfigDict(extra="allow", frozen=True)
