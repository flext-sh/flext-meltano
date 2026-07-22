"""FLEXT Meltano Adapters - SOLID-compliant adapter classes following FLEXT patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_meltano import FlextMeltanoServiceBase, p, r, settings, t


class FlextMeltanoAdapter(FlextMeltanoServiceBase):
    """Base adapter namespace class for focused integrations."""

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute adapter service returning current settings."""
        return r[t.JsonMapping].ok(settings.model_dump(mode="json"))


__all__: list[str] = ["FlextMeltanoAdapter"]
