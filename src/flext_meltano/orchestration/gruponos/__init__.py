"""GrupoNOS Meltano Orchestration - Consolidated Implementation.

This module consolidates all GrupoNOS-specific Meltano orchestration functionality
from gruponos-meltano-native into the centralized flext-meltano library.

All configuration, orchestration, and pipeline management for GrupoNOS implementations
should use this consolidated module.
"""

from __future__ import annotations

# Configuration
from .config import (
    GruponosMeltanoAlertConfig,
    GruponosMeltanoJobConfig,
    GruponosMeltanoOracleConnectionConfig,
    GruponosMeltanoSettings,
    GruponosMeltanoTargetOracleConfig,
    GruponosMeltanoWMSSourceConfig,
    create_gruponos_meltano_settings,
)

# Orchestration
from .orchestrator import (
    GruponosMeltanoOrchestrator,
    GruponosMeltanoPipelineResult,
    GruponosMeltanoPipelineRunner,
    create_gruponos_meltano_orchestrator,
    create_gruponos_meltano_pipeline_runner,
)

__all__ = [
    # Configuration
    "GruponosMeltanoAlertConfig",
    "GruponosMeltanoJobConfig",
    "GruponosMeltanoOracleConnectionConfig",
    # Orchestration
    "GruponosMeltanoOrchestrator",
    "GruponosMeltanoPipelineResult",
    "GruponosMeltanoPipelineRunner",
    "GruponosMeltanoSettings",
    "GruponosMeltanoTargetOracleConfig",
    "GruponosMeltanoWMSSourceConfig",
    "create_gruponos_meltano_orchestrator",
    "create_gruponos_meltano_pipeline_runner",
    "create_gruponos_meltano_settings",
]
