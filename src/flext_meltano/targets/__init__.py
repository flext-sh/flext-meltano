"""FLEXT Meltano Targets - Consolidated Singer Target implementations.

This module provides consolidated Singer target implementations for the FLEXT ecosystem.
All target implementations follow FLEXT Core patterns and Singer SDK standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# LDAP target implementation
from flext_meltano.targets.ldap import (
    FlextLDAPTarget,
    FlextLDAPTargetConfig,
    TargetLDAP,
    TargetLDAPConfig,
)

# LDIF target implementation
from flext_meltano.targets.ldif import (
    FlextLDIFTarget,
    FlextLDIFTargetConfig,
    TargetLDIF,
    TargetLDIFConfig,
)

# Oracle target implementation
from flext_meltano.targets.oracle import (
    FlextOracleTarget,
    FlextOracleTargetConfig,
    LoadMethod,
)

__all__ = [
    # LDAP
    "FlextLDAPTarget",
    "FlextLDAPTargetConfig",
    # LDIF
    "FlextLDIFTarget",
    "FlextLDIFTargetConfig",
    # Oracle
    "FlextOracleTarget",
    "FlextOracleTargetConfig",
    "LoadMethod",
    "TargetLDAP",
    "TargetLDAPConfig",
    "TargetLDIF",
    "TargetLDIFConfig",
]
