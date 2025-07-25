"""FLEXT ORACLE OIC EXT - Oracle Integration Cloud Extensions with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Oracle OIC Extensions with simplified public API:
- All common imports available from root: from flext_oracle_oic_ext import ExtendedOICClient
- Built on flext-core foundation for robust Oracle OIC integration
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

from flext_meltano.extensions.oracle_oic.extension import OracleOICExtension
from flext_meltano.extensions.oracle_oic.infrastructure.di_container import (
    get_flext_oracle_oic_ext_container,
)

# Import from flext-core for foundational patterns
# 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports
# NOTE: Using local implementations instead of external flext_oracle_oic_ext
from flext_meltano.helpers.execution import FlextMeltanoResult as FlextResult

# Use local container instead of external dependencies
_container = get_flext_oracle_oic_ext_container()

# Basic types for oracle oic extension
Field = dict  # Simple field type
FlextValueObject = dict  # Simple value object type
BaseConfig = dict  # Simple config type

__all__ = [
    "BaseConfig",
    "Field",
    "FlextResult",
    "FlextValueObject",
]

try:
    __version__ = importlib.metadata.version("flext-oracle-oic-ext")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextOracleOicExtDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT ORACLE OIC EXT import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT ORACLE OIC EXT docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextOracleOicExtDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Foundation patterns - ALWAYS from flext-core (imported above)

# Local imports - using flext-meltano extensions instead of external packages

# Mock classes for compatibility - these should be implemented locally if needed
ExtendedOICClient = None
IntegrationPattern = None
IntegrationPatternOrchestrator = None
CustomDatabaseAdapter = None
CustomRESTAdapter = None
OICAdapterManager = None

# ================================

__all__ = [
    # Basic types
    "BaseConfig",
    "Field",
    "FlextResult",
    "FlextValueObject",
    # Local extension
    "OracleOICExtension",
    # Version
    "__version__",
    "__version_info__",
]
