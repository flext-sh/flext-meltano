"""FLEXT Meltano - Biblioteca ISOLADA para Singer/Meltano/DBT.

BIBLIOTECA VERDADEIRAMENTE ISOLADA:
- ZERO dependências flext_*
- Interface mínima via helpers
- Subprocess direto para Meltano CLI
- Máximo 10 arquivos essenciais

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

# Helper ISOLADO (sem flext_core)
from flext_meltano.helpers.execution import (
    FlextMeltanoResult,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)

# Bridge para Go integration (se disponível)
from flext_meltano.simple_bridge import FlextMeltanoBridge

# Singer SDK essentials (apenas re-exports)
try:
    from singer_sdk import Stream, Tap, Target
    from singer_sdk.sinks import Sink, SQLSink
    from singer_sdk.typing import PropertiesList, Property
    SINGER_AVAILABLE = True
except ImportError:
    Stream = Tap = Target = Sink = SQLSink = PropertiesList = Property = None  # type: ignore[assignment,misc]
    SINGER_AVAILABLE = False

# Meltano essentials (apenas se disponível)
try:
    from meltano.core.project import Project as MeltanoProject
    MeltanoPluginType = None  # PluginType import removed due to type issues
    MELTANO_AVAILABLE = True
except ImportError:
    MeltanoProject = MeltanoPluginType = None  # type: ignore[assignment,misc]
    MELTANO_AVAILABLE = False

# DBT essentials (apenas se disponível)
try:
    # Import without problematic type annotations
    import dbt.contracts.results
    DbtRunResult = getattr(dbt.contracts.results, "RunResult", None)
    DBT_AVAILABLE = DbtRunResult is not None
except ImportError:
    DbtRunResult = None  # type: ignore[assignment,misc]
    DBT_AVAILABLE = False

__version__ = "1.0.0-isolated"

# Interface pública MINIMALISTA - APENAS TESTADO
__all__ = [
    # Availability flags
    "DBT_AVAILABLE",
    "MELTANO_AVAILABLE",
    "SINGER_AVAILABLE",
    # Bridge integration
    "DbtRunResult",
    "FlextMeltanoBridge",
    # Core helpers (ISOLADOS)
    "FlextMeltanoResult",
    "MeltanoPluginType",
    "MeltanoProject",
    "PropertiesList",
    "Property",
    "SQLSink",
    # Essential re-exports (apenas se disponíveis)
    "Sink",
    "Stream",
    "Tap",
    "Target",
    # Version info
    "__version__",
    # Helper functions
    "flext_meltano_execute_job",
    "flext_meltano_run_command",
]
