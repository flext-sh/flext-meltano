"""Example protocols for flext-meltano.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoProtocols


class ExamplesFlextMeltanoProtocols(FlextMeltanoProtocols):
    """Examples protocols facade extending flext-meltano protocols."""

    class Meltano(FlextMeltanoProtocols.Meltano):
        """Meltano domain protocols for examples."""

        class Examples:
            """Examples-only protocol namespace."""


p = ExamplesFlextMeltanoProtocols

__all__: list[str] = ["ExamplesFlextMeltanoProtocols", "p"]
