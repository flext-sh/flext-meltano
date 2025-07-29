"""FLEXT Meltano Taps - Consolidated Singer Tap implementations.

This module provides consolidated Singer tap implementations for the FLEXT ecosystem.
All tap implementations follow FLEXT Core patterns and Singer SDK standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# LDAP tap implementation
from flext_meltano.taps.ldap import (
    FlextTapLDAP,
    TapLDAP,
    TapLDAPConfig,
)

# LDIF tap implementation
from flext_meltano.taps.ldif import (
    FlextTapLDIF,
    TapLDIF,
    TapLDIFConfig,
)

# Oracle tap implementation
from flext_meltano.taps.oracle import (
    FlextTapOracle,
    TapOracle,
    TapOracleConfig,
)

__all__ = [
    # LDAP
    "FlextTapLDAP",
    # LDIF
    "FlextTapLDIF",
    # Oracle
    "FlextTapOracle",
    "TapLDAP",
    "TapLDAPConfig",
    "TapLDIF",
    "TapLDIFConfig",
    "TapOracle",
    "TapOracleConfig",
]
