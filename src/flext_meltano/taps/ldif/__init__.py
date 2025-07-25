"""FLEXT Meltano LDIF Tap - Consolidated Singer tap implementation.

This module provides the consolidated LDIF file tap implementation
for the FLEXT ecosystem, eliminating code duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.common.config import FlextMeltanoConnectionConfig
from flext_meltano.common.validation import validate_file_path


class TapLDIFConfig(FlextMeltanoConnectionConfig):
    """LDIF tap configuration."""

    def __init__(self, ldif_path: str | None = None, **kwargs) -> None:
        """Initialize LDIF tap configuration.

        Args:
            ldif_path: Path to LDIF file
            **kwargs: Configuration parameters

        """
        super().__init__(**kwargs)
        self.ldif_path = validate_file_path(ldif_path) if ldif_path else None
        # Additional tap-specific configuration
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)


class TapLDIF:
    """Consolidated LDIF tap implementation."""

    name = "tap-ldif"

    def __init__(self, config=None, **kwargs) -> None:
        """Initialize LDIF tap.

        Args:
            config: Tap configuration
            **kwargs: Additional parameters

        """
        self.config = config or {}

    @classmethod
    def cli(cls) -> None:
        """CLI entry point."""


__version__ = "0.8.0-consolidated"

__all__ = [
    "TapLDIF",
    "TapLDIFConfig",
    "__version__",
]
