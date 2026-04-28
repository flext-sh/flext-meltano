"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)

from flext_cli import t


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions."""

    type ValidatorInput = t.JsonValue | t.JsonPayload | None

    type OptionalScalarMap = Mapping[str, t.Scalar | None]
