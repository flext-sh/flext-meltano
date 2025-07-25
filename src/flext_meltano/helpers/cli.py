"""FLEXT Meltano CLI Helpers - ELIMINAR DUPLICAÇÃO.

REDIRECIONAMENTO PARA EXECUTION - sem duplicação de código.
BIBLIOTECA ISOLADA - não importa flext_core.
"""

from __future__ import annotations

# ELIMINAR DUPLICAÇÃO - importar do execution.py
from flext_meltano.helpers.execution import (
    FlextMeltanoResult,
    flext_meltano_run_command,
)

# Aliases for compatibility
flext_run_meltano_command = flext_meltano_run_command

__all__ = [
    "FlextMeltanoResult",
    "flext_meltano_run_command",
    "flext_run_meltano_command",
]
