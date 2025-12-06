"""Test models extending flext_meltano.models for test-specific functionality.

This module provides test-specific model classes that extend the production
models from src/flext_meltano/models.py. All test models use real inheritance
to expose the full hierarchy and avoid duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.models import FlextMeltanoModels


class TestsModels(FlextMeltanoModels):
    """Test-specific models extending FlextMeltanoModels.

    Provides test-specific model classes that extend production models
    with test-specific functionality. Uses real inheritance to expose
    the full hierarchy without duplication.
    """

    # Test-specific models can be added here as nested classes
    # All parent models are accessible via inheritance


# Standardized short name for use in tests (same pattern as flext-core)
m = TestsModels

__all__ = ["TestsModels", "m"]
