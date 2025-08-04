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


# ===== ✅ IMPORTS RECOMENDADOS (Nova Arquitetura) =====
# Imports simplificados - SEM warnings
from flext_meltano import (
    FlextMeltanoConfig,
    create_executor,
    create_flext_meltano_bridge,
    flext_meltano_execute_job,
)

# ===== ⚠️ DEMOS DE WARNINGS DE DEPRECIAÇÃO =====


# Configura warnings para aparecer sempre
warnings.simplefilter("always")


# Este import emitirá warning
with contextlib.suppress(Exception):
    # Simulate old import patterns that would emit warnings
    print("Warning: Using deprecated import pattern (example only)")


with contextlib.suppress(Exception):
    # Simulate old service import
    print("Warning: Deprecated service import (example only)")


with contextlib.suppress(Exception):
    # Simulate old entity import
    print("Warning: Deprecated entity import (example only)")

# ===== 🎯 EXEMPLO PRÁTICO DE USO =====

# Usando bibliotecas consolidadas em flext-meltano

def functional_example() -> dict:
    """Demonstrates new simplified API vs old complex imports."""
    try:
        # ✅ NEW: Simple configuration
        config = FlextMeltanoConfig(project_root="./demo_project")

        # ✅ NEW: One-line executor creation
        executor_result = create_executor(config)
        if executor_result.is_success:
            executor = executor_result.data
            print(f"✅ Executor created successfully: {type(executor).__name__}")

        # ✅ NEW: Simple bridge creation
        bridge = create_flext_meltano_bridge()
        health_result = bridge.validate_bridge_health()
        bridge_version = bridge.get_bridge_version()

        # ✅ NEW: One-line job execution
        job_result = flext_meltano_execute_job("tap-csv", "target-csv")

        return {
            "new_api_functional": True,
            "executor_created": executor_result.is_success,
            "bridge_healthy": health_result.is_success,
            "bridge_version": bridge_version,
            "job_executed": job_result.success,  # Using legacy .success pattern
            "status": "simplified_imports_successful"
        }

    except Exception as e:
        return {
            "new_api_functional": False,
            "error": str(e),
            "status": "simplified_imports_failed"
        }

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

def main() -> None:
    """Execute the simplified imports demonstration."""
    print("🔄 FLEXT Meltano Simplified Imports Demo")
    print("=" * 50)

    # Run functional example
    print("\n✅ Testing NEW Simplified API:")
    result = functional_example()

    print(f"   Status: {result['status']}")
    if result.get('new_api_functional'):
        print(f"   Executor: {'✅' if result.get('executor_created') else '❌'}")
        print(f"   Bridge: {'✅' if result.get('bridge_healthy') else '❌'}")
        print(f"   Job Execution: {'✅' if result.get('job_executed') else '❌'}")

    # Show migration examples
    print("\n📖 Migration Guide Examples:")
    for label, example in migration_examples:
        if label:
            print(f"   {label}: {example}")
        else:
            print()

    print("\n✅ Simplified imports demo completed!")


if __name__ == "__main__":
    main()
