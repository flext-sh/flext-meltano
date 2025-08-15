"""Compatibility shim: re-export config from models.

Historicamente, `FlextMeltanoConfig` vivia aqui. Após consolidação, sua
definição canônica está em `flext_meltano.models`. Este módulo apenas
reexporta para manter compatibilidade.
"""

from __future__ import annotations

from .models import FlextMeltanoConfig

__all__ = ["FlextMeltanoConfig"]
