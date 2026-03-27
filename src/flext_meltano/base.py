"""Shared service foundation for flext-meltano components.

Centralizes access to configuration singleton while maintaining inheritance
aligned with `FlextService` from flext-core, avoiding duplication of initialization
across library services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC
from typing import override

from flext_core import FlextSettings, s

from flext_meltano import FlextMeltanoSettings, t


class FlextMeltanoServiceBase(s[t.Meltano.MeltanoConfigDict], ABC):
    """Base class for flext-meltano services with typed configuration access.

    Note: This is an abstract base class. Subclasses must implement the
    `execute` method from FlextService.
    """

    @property
    @override
    def settings(self) -> FlextMeltanoSettings:
        """Return the typed Meltano settings namespace."""
        return FlextSettings.get_global().get_namespace(
            "meltano",
            FlextMeltanoSettings,
        )


__all__ = ["FlextMeltanoServiceBase"]
