"""Singer Target Abstractions — base service for Singer target entry points.

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

from typing import override

from flext_meltano import FlextMeltanoServiceBase, p, r, settings, t


class FlextMeltanoTargetAbstractions(FlextMeltanoServiceBase):
    """Base service for Singer target entry points."""

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute sink abstraction operations (implements Service).

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        return r[t.JsonMapping].ok(settings.model_dump(mode="json"))


__all__: list[str] = ["FlextMeltanoTargetAbstractions"]
