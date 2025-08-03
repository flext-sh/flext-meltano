#!/usr/bin/env python3
"""FLEXT Meltano Simplified Imports Demo - Migration Guide and Import Patterns.

**Purpose**: Demonstrate simplified import patterns and deprecation warnings
**Scope**: New architecture migration guidance and streamlined import usage
**Target Audience**: Developers migrating to new FLEXT Meltano architecture
**Dependencies**: FLEXT Meltano library with deprecation warning system

## Overview

This example demonstrates how to use the new simplified imports and deprecation
warnings to guide migration to the new architecture patterns.
"""

from __future__ import annotations

import contextlib
import warnings

from flext_meltano import FlextMeltanoBridge

# ===== ✅ IMPORTS RECOMENDADOS (Nova Arquitetura) =====
# Imports simplificados - SEM warnings

# ===== ⚠️ DEMOS DE WARNINGS DE DEPRECIAÇÃO =====


# Configura warnings para aparecer sempre
warnings.simplefilter("always")


# Este import emitirá warning
with contextlib.suppress(Exception):
    pass


with contextlib.suppress(Exception):
    pass


with contextlib.suppress(Exception):
    pass

# ===== 🎯 EXEMPLO PRÁTICO DE USO =====

# Usando bibliotecas consolidadas em flext-meltano

# Exemplo: Bridge para integração Go
bridge = FlextMeltanoBridge(project_root="/home/marlonsc/flext")
version_info = bridge.get_version()

# ===== 📖 GUIA DE MIGRAÇÃO =====


migration_examples = [
    (
        "❌ OLD",
        "from flext_meltano.application.services.project_service import ProjectApplicationService",
    ),
    ("✅ NEW", "from flext_meltano import ProjectService"),
    ("", ""),
    (
        "❌ OLD",
        "from flext_meltano.domain.entities.project import MeltanoProject",
    ),
    ("✅ NEW", "from flext_meltano import MeltanoProject"),
    ("", ""),
    (
        "❌ OLD",
        "from flext_meltano.application.services.state_service import MeltanoStateService",
    ),
    ("✅ NEW", "from flext_meltano import StateService"),
]

for label, _example in migration_examples:
    if not label:
        pass
