"""FLEXT Meltano LDAP Tap - Consolidated Singer tap implementation.

This module provides the consolidated LDAP server tap implementation
for the FLEXT ecosystem, eliminating code duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from flext_meltano.common.config import FlextMeltanoLDAPConnectionConfig


class TapLDAPConfig(FlextMeltanoLDAPConnectionConfig):
    """LDAP tap configuration using consolidated connection config."""

    def __init__(self, **kwargs: object) -> None:
        """Initialize LDAP tap configuration.

        Args:
            **kwargs: Configuration parameters

        """
        super().__init__(**kwargs)
        # Additional tap-specific configuration
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)


class FlextTapLDAP:
    """Consolidated LDAP tap implementation."""

    name = "tap-ldap"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize LDAP tap.

        Args:
            config: Tap configuration

        """
        self.config = config or {}

    @classmethod
    def cli(cls) -> None:
        """CLI entry point."""


__version__ = "0.8.0-consolidated"

__all__ = [
    "FlextTapLDAP",
    "TapLDAPConfig",
    "__version__",
]
