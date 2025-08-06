"""DBT Package Management for FLEXT Ecosystem.

Provides centralized DBT package management, model registry, and in-memory
execution capabilities for the FLEXT ecosystem, enabling reusable DBT
components across flext-dbt-* projects.

Key Components:
    - FlextDbtPackageManager: Package registration and dependency resolution
    - FlextDbtModelRegistry: Reusable models catalog and compilation
    - FlextDbtInMemoryExecutor: DuckDB-based in-memory execution
    - FlextDbtPackage: Package metadata and versioning

Integration:
    - Built on flext-core foundation patterns
    - Integrates with flext-dbt-ldap, flext-dbt-oracle, flext-dbt-oracle-wms
    - Provides zero-database testing capabilities

Author: FLEXT Development Team
Version: 1.0.0
License: MIT
"""

from __future__ import annotations

from flext_meltano.dbt_packages.executor import (
    FlextDbtInMemoryExecutor,
    create_in_memory_executor,
)
from flext_meltano.dbt_packages.manager import (
    FlextDbtPackage,
    FlextDbtPackageManager,
    create_package_manager,
)
from flext_meltano.dbt_packages.registry import (
    FlextDbtModel,
    FlextDbtModelRegistry,
    create_model_registry,
)

__all__ = [
    "FlextDbtInMemoryExecutor",
    "FlextDbtModel",
    "FlextDbtModelRegistry",
    "FlextDbtPackage",
    "FlextDbtPackageManager",
    "create_in_memory_executor",
    "create_model_registry",
    "create_package_manager",
]
