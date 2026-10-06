# Copyright (c) 2025 FLEXT Team. All rights reserved.
from __future__ import annotations

from flext_meltano import m


class _MeltanoNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = m.ConfigDict(extra="allow", frozen=True)
