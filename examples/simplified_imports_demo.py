#!/usr/bin/env python3
"""Demo de imports simplificados do flext-meltano.

Este exemplo demonstra como usar os novos imports simplificados e os warnings
de depreciação para orientar a migração para a nova arquitetura.
"""

from __future__ import annotations

import contextlib
import warnings
from pathlib import Path

# ===== ✅ IMPORTS RECOMENDADOS (Nova Arquitetura) =====
# Imports simplificados - SEM warnings
from flext_meltano import (
    MeltanoProject,
)

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


# Criar um projeto Meltano com a nova arquitetura

with contextlib.suppress(Exception):
    project = MeltanoProject(
        name="demo-project",
        directory=Path("/tmp/demo"),
        config_path=Path("/tmp/demo/meltano.yml"),
        description="Demo project",
    )

# ===== 📖 GUIA DE MIGRAÇÃO =====


migration_examples = [
    ("❌ OLD", "from flext_meltano.application.services.project_service import ProjectApplicationService"),
    ("✅ NEW", "from flext_meltano import ProjectService"),
    ("", ""),
    ("❌ OLD", "from flext_meltano.domain.entities.project import MeltanoProject"),
    ("✅ NEW", "from flext_meltano import MeltanoProject"),
    ("", ""),
    ("❌ OLD", "from flext_meltano.application.services.state_service import MeltanoStateService"),
    ("✅ NEW", "from flext_meltano import StateService"),
]

for label, _example in migration_examples:
    if not label:
        pass
