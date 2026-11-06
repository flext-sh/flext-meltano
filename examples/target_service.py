"""Minimal Singer target on the flext-meltano target base - REAL usage.

The service declares its sink factory and defines no method: the base drains
Singer messages from stdin, creates one sink per stream through ``sink_factory``
and flushes them at STATE boundaries.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, ClassVar

from examples import ExamplesFlextMeltanoTargetSink, m, p, t
from flext_meltano import FlextMeltanoTargetServiceBase


class ExamplesFlextMeltanoTargetService(FlextMeltanoTargetServiceBase):
    """Example target: per-stream in-memory sinks built by the declared factory."""

    target_name: Annotated[
        t.NonEmptyStr,
        m.Field(description="Canonical Singer target identifier."),
    ] = "target-example"

    sink_factory: ClassVar[p.Meltano.SinkFactory] = ExamplesFlextMeltanoTargetSink


__all__: list[str] = ["ExamplesFlextMeltanoTargetService"]
