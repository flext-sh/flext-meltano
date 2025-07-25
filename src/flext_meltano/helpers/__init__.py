"""FLEXT Meltano helpers - APENAS helpers isolados."""

from __future__ import annotations

# APENAS helpers que NÃO importam flext_core
from flext_meltano.helpers.cli import flext_meltano_run_command
from flext_meltano.helpers.execution import flext_meltano_execute_job

__all__ = [
    "flext_meltano_execute_job",
    "flext_meltano_run_command",
]
