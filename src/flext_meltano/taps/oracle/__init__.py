"""FLEXT Meltano Oracle Tap - Consolidated Singer implementation.

This module provides the consolidated Oracle database tap implementation
for the FLEXT ecosystem, eliminating code duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any


# Basic configuration class for now
class TapOracleConfig:
    """Basic Oracle tap configuration."""

    def __init__(self, **kwargs: object) -> None:
        """Initialize Oracle tap configuration.

        Args:
            **kwargs: Configuration parameters

        """
        for key, value in kwargs.items():
            setattr(self, key, value)


# Basic tap class for now
class TapOracle:
    """Basic Oracle tap implementation."""

    name = "tap-oracle"

    def __init__(self, config: dict[str, Any] | None = None, **kwargs: object) -> None:
        """Initialize Oracle tap.

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
    "TapOracle",
    "TapOracleConfig",
    "__version__",
]
