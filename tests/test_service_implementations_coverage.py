"""Test coverage for service_implementations module - backward compatibility validation.

This module provides focused tests for the deprecated service_implementations
module to ensure complete coverage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_meltano.service_implementations import (
    FlextMeltanoDbtService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
)
from flext_meltano.services import FlextMeltanoService


class TestServiceImplementationsCoverage:
    """Test coverage for deprecated service implementations."""

    def test_legacy_service_creation(self) -> None:
        """Test legacy service creation functions work correctly."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Test tap service creation
            tap_service = FlextMeltanoTapService("test-tap")
            assert isinstance(tap_service, FlextMeltanoService)

            # Test target service creation
            target_service = FlextMeltanoTargetService("test-target")
            assert isinstance(target_service, FlextMeltanoService)

            # Test dbt service creation
            dbt_service = FlextMeltanoDbtService("test-dbt")
            assert isinstance(dbt_service, FlextMeltanoService)

    def test_legacy_service_with_kwargs(self) -> None:
        """Test legacy service creation with additional kwargs."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Test creation with additional parameters
            service = FlextMeltanoTapService("test-tap", extra_param="value")
            assert isinstance(service, FlextMeltanoService)
