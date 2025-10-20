"""Meltano Integration for FLEXT Ecosystem.

This module provides deep integration with meltano-sdk for project management,
plugin operations, and pipeline orchestration with FLEXT ecosystem patterns
and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.meltano.project import FlextMeltanoProjectManager
from flext_meltano.meltano.service import FlextMeltanoMeltanoService

__all__ = [
    "FlextMeltanoMeltanoService",
    "FlextMeltanoProjectManager",
]
