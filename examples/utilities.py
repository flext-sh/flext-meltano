"""Example utilities for flext-meltano.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoUtilities


class ExamplesFlextMeltanoUtilities(FlextMeltanoUtilities):
    """Examples utilities facade extending flext-meltano utilities."""

    class Meltano(FlextMeltanoUtilities.Meltano):
        """Meltano domain utilities for examples."""

        class Examples:
            """Examples-only utility namespace."""


u = ExamplesFlextMeltanoUtilities

__all__: list[str] = ["ExamplesFlextMeltanoUtilities", "u"]
