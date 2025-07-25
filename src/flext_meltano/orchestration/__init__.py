"""FLEXT Meltano Orchestration - Consolidated Implementation.

This module consolidates ALL orchestration functionality across the FLEXT ecosystem,
eliminating duplication from individual flext-tap-*, flext-target-*, and flext-dbt-* projects.

Key consolidations:
- Target orchestrators from flext-target-oracle-wms, flext-target-ldap, etc.
- Tap orchestrators from flext-tap-oracle-*, flext-tap-ldap, etc.
- DBT orchestrators from flext-dbt-oracle-wms, flext-dbt-ldap, etc.
- Project-specific orchestrators like gruponos
"""

from __future__ import annotations

# Project-specific orchestrators
from . import gruponos

# Consolidated orchestrators
from .dbt import (
    FlextDbtConfig,
    FlextDbtOrchestrator,
    FlextLDAPDbtOrchestrator,
    FlextOracleDbtOrchestrator,
    FlextOracleWMSDbtOrchestrator,
    create_dbt_orchestrator,
)
from .taps import (
    FlextLDAPTapOrchestrator,
    FlextOracleTapOrchestrator,
    FlextTapConfig,
    FlextTapOrchestrator,
    create_tap_orchestrator,
)
from .targets import (
    FlextLDAPTargetOrchestrator,
    FlextOracleTargetOrchestrator,
    FlextTargetConfig,
    FlextTargetOrchestrator,
    create_target_orchestrator,
)

__all__ = [
    "FlextDbtConfig",
    "FlextDbtOrchestrator",
    "FlextLDAPDbtOrchestrator",
    # LDAP orchestrators
    "FlextLDAPTapOrchestrator",
    "FlextLDAPTargetOrchestrator",
    "FlextOracleDbtOrchestrator",
    # Oracle orchestrators
    "FlextOracleTapOrchestrator",
    "FlextOracleTargetOrchestrator",
    "FlextOracleWMSDbtOrchestrator",
    # Base configuration classes
    "FlextTapConfig",
    # Base orchestrator classes
    "FlextTapOrchestrator",
    "FlextTargetConfig",
    "FlextTargetOrchestrator",
    "create_dbt_orchestrator",
    # Factory functions
    "create_tap_orchestrator",
    "create_target_orchestrator",
    # Project-specific
    "gruponos",
]
