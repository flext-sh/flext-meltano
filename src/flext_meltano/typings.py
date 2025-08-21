"""Centralized TypeVars used across flext_meltano at runtime.

Define Meltano-specific TypeVars and extend flext_core typings following
the same pattern as flext-core's typings.py module.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TypeVar

# Re-export core types
from flext_core.typings import (
    E,
    F,
    FlextTypes as CoreFlextTypes,
    P,
    R,
    T,
    TConfig,
    TData,
    TResult,
    TValue,
    U,
    V,
)

# =============================================================================
# MELTANO-SPECIFIC TYPE VARIABLES
# =============================================================================

# Meltano domain types
TMeltanoConfig = TypeVar("TMeltanoConfig")
TMeltanoPlugin = TypeVar("TMeltanoPlugin")
TMeltanoTap = TypeVar("TMeltanoTap")
TMeltanoTarget = TypeVar("TMeltanoTarget")
TMeltanoDbt = TypeVar("TMeltanoDbt")

# Singer protocol types
TSingerTap = TypeVar("TSingerTap")
TSingerTarget = TypeVar("TSingerTarget")
TSingerStream = TypeVar("TSingerStream")
TSingerRecord = TypeVar("TSingerRecord")
TSingerSchema = TypeVar("TSingerSchema")
TSingerCatalog = TypeVar("TSingerCatalog")

# DBT types
TDbtProject = TypeVar("TDbtProject")
TDbtModel = TypeVar("TDbtModel")
TDbtRun = TypeVar("TDbtRun")
TDbtTest = TypeVar("TDbtTest")

# Execution types
TExecutionResult = TypeVar("TExecutionResult")
TExecutionContext = TypeVar("TExecutionContext")
TPipelineConfig = TypeVar("TPipelineConfig")

# =============================================================================
# MELTANO TYPE ALIASES
# =============================================================================

# Path-related aliases
ProjectPath = Path
MeltanoYmlPath = Path
DbtProjectPath = Path
PluginPath = Path

# Configuration aliases
MeltanoConfigDict = Mapping[str, object]
PluginConfigDict = Mapping[str, object]
SingerConfigDict = Mapping[str, object]
DbtConfigDict = Mapping[str, object]

# Data aliases
SingerRecordDict = Mapping[str, object]
SingerSchemaDict = Mapping[str, object]
MeltanoStateDict = Mapping[str, object]

# Collection aliases
PluginList = Sequence[object]
StreamList = Sequence[object]
RecordList = Sequence[Mapping[str, object]]


class FlextMeltanoTypes(CoreFlextTypes):
    """Meltano-specific types extending core FlextTypes."""

    # Meltano domain types
    MeltanoConfig = TMeltanoConfig
    MeltanoPlugin = TMeltanoPlugin
    MeltanoTap = TMeltanoTap
    MeltanoTarget = TMeltanoTarget
    MeltanoDbt = TMeltanoDbt

    # Singer types
    SingerTap = TSingerTap
    SingerTarget = TSingerTarget
    SingerStream = TSingerStream
    SingerRecord = TSingerRecord
    SingerSchema = TSingerSchema
    SingerCatalog = TSingerCatalog

    # DBT types
    DbtProject = TDbtProject
    DbtModel = TDbtModel
    DbtRun = TDbtRun
    DbtTest = TDbtTest

    # Execution types
    ExecutionResult = TExecutionResult
    ExecutionContext = TExecutionContext
    PipelineConfig = TPipelineConfig


# Legacy alias for backward compatibility
FlextTypes = FlextMeltanoTypes


__all__ = [
    "DbtConfigDict",
    "DbtProjectPath",
    # Core re-exports
    "E",
    "F",
    # Classes
    "FlextMeltanoTypes",
    "FlextTypes",
    "MeltanoConfigDict",
    "MeltanoStateDict",
    "MeltanoYmlPath",
    "P",
    "PluginConfigDict",
    "PluginList",
    "PluginPath",
    # Type aliases
    "ProjectPath",
    "R",
    "RecordList",
    "SingerConfigDict",
    "SingerRecordDict",
    "SingerSchemaDict",
    "StreamList",
    "T",
    "TConfig",
    "TData",
    "TDbtModel",
    "TDbtProject",
    "TDbtRun",
    "TDbtTest",
    "TExecutionContext",
    "TExecutionResult",
    # Meltano TypeVars
    "TMeltanoConfig",
    "TMeltanoDbt",
    "TMeltanoPlugin",
    "TMeltanoTap",
    "TMeltanoTarget",
    "TPipelineConfig",
    "TResult",
    "TSingerCatalog",
    "TSingerRecord",
    "TSingerSchema",
    "TSingerStream",
    "TSingerTap",
    "TSingerTarget",
    "TValue",
    "U",
    "V",
]
