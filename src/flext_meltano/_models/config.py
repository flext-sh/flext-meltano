"""FLEXT Meltano models - Config namespace models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_cli import m


class FlextMeltanoModelsConfig:
    """Config namespace models for model-less ``config/*.yaml`` exposure."""

    class MeltanoNamespace(m.FrozenModel):
        """Open, frozen namespace exposing every ``config/*.yaml`` domain."""

        model_config = m.ConfigDict(extra="allow", frozen=True)


__all__: list[str] = ["FlextMeltanoModelsConfig"]
