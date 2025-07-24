"""Flext-Meltano Domain Entities - NEW SEMANTIC ARCHITECTURE.

🚨 DEPRECATION WARNING: Importing from this path is deprecated.

❌ OLD: from flext_meltano.domain.entities import MeltanoProject
✅ NEW: from flext_meltano import MeltanoProject

❌ OLD: from flext_meltano.domain.entities.project import MeltanoProject
✅ NEW: from flext_meltano import MeltanoProject

Built on flext-core foundation patterns for maximum clarity and maintainability.
"""

from __future__ import annotations

import warnings
from typing import Any

# Domain entities
from flext_meltano.domain.entities.environment_type import (
    FlextMeltanoEnvironmentType,
)
from flext_meltano.domain.entities.job import FlextMeltanoJob
from flext_meltano.domain.entities.job_status import FlextMeltanoJobStatus
from flext_meltano.domain.entities.plugin import FlextMeltanoPlugin
from flext_meltano.domain.entities.plugin_type import FlextMeltanoPluginType
from flext_meltano.domain.entities.project import FlextMeltanoProject
from flext_meltano.domain.entities.state import FlextMeltanoState

# 🚨 ARCHITECTURAL COMPLIANCE: Import from local DI container
from flext_meltano.infrastructure.di_container import (
    AbstractEntity,
    DomainEntity,
)


def _entity_deprecation_warning(entity_name: str) -> None:
    """Emite warning de depreciação para imports de entidades."""
    warnings.warn(
        f"🚨 DEPRECATED: Importing {entity_name} from 'flext_meltano.domain.entities' is deprecated.\n"
        f"✅ Use: from flext_meltano import {entity_name}\n"
        f"📖 This path will be removed in version 0.8.0.\n"
        f"📚 Migration guide: https://docs.flext.dev/migration/meltano",
        DeprecationWarning,
        stacklevel=3,
    )


def __getattr__(name: str) -> Any:
    """Handle imports com warnings de depreciação."""
    entity_mapping = {
        "MeltanoProject": FlextMeltanoProject,
        "MeltanoState": FlextMeltanoState,
        "MeltanoJob": FlextMeltanoJob,
        "MeltanoPlugin": FlextMeltanoPlugin,
        "FlextMeltanoProject": FlextMeltanoProject,
        "FlextMeltanoState": FlextMeltanoState,
        "FlextMeltanoJob": FlextMeltanoJob,
        "FlextMeltanoPlugin": FlextMeltanoPlugin,
        "EnvironmentType": FlextMeltanoEnvironmentType,
        "FlextMeltanoEnvironmentType": FlextMeltanoEnvironmentType,
        "JobStatus": FlextMeltanoJobStatus,
        "FlextMeltanoJobStatus": FlextMeltanoJobStatus,
        "PluginType": FlextMeltanoPluginType,
        "FlextMeltanoPluginType": FlextMeltanoPluginType,
    }

    if name in entity_mapping:
        _entity_deprecation_warning(name)
        return entity_mapping[name]

    if name in {"AbstractEntity", "DomainEntity"}:
        # Foundation patterns não emitem warning
        if name == "AbstractEntity":
            return AbstractEntity
        if name == "DomainEntity":
            return DomainEntity

    msg = f"module 'flext_meltano.domain.entities' has no attribute '{name}'"
    raise AttributeError(msg)


__all__ = [
    "AbstractEntity",
    "DomainEntity",
    "EnvironmentType",  # Backward compatibility
    "FlextMeltanoEnvironmentType",
    "FlextMeltanoJob",
    "FlextMeltanoJobStatus",
    "FlextMeltanoPlugin",
    "FlextMeltanoPluginType",
    "FlextMeltanoProject",
    "FlextMeltanoState",
    "JobStatus",  # Backward compatibility
    "MeltanoJob",  # Backward compatibility
    "MeltanoPlugin",  # Backward compatibility
    "MeltanoProject",  # Backward compatibility
    "MeltanoState",  # Backward compatibility
    "PluginType",  # Backward compatibility
]
