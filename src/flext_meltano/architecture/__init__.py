"""Architecture standardization and verification for FLEXT Meltano consolidation.

This module provides tools to ensure Singer/Meltano/DBT are properly consolidated
in flext-meltano according to the architectural directive:
"Singer, Meltano e DBT tem que estar em flext-meltano, acabae com essa confusão arrumando isso"

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

from flext_meltano.architecture.standardizer import FlextSingerArchitectureStandardizer
from flext_meltano.architecture.verifier import FlextMeltanoConsolidationVerifier

__all__ = [
    "FlextMeltanoConsolidationVerifier",
    "FlextSingerArchitectureStandardizer",
]
