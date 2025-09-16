"""Test coverage for unified service implementations - FLEXT compliant architecture.

This module tests the unified FlextMeltanoService architecture that eliminates
wrapper classes in favor of direct service_type parameters.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.services import FlextMeltanoService


class TestUnifiedServiceImplementations:
    """Test coverage for unified service implementations (FLEXT compliant)."""

    def test_unified_service_creation(self) -> None:
        """Test unified service creation with service_type parameter."""
        # Test tap service creation using unified service
        tap_service = FlextMeltanoService(service_type="tap", tap_name="test-tap")
        assert isinstance(tap_service, FlextMeltanoService)
        assert tap_service._service_type == "tap"
        assert getattr(tap_service, "tap_name", None) == "test-tap"

        # Test target service creation using unified service
        target_service = FlextMeltanoService(
            service_type="target", target_name="test-target"
        )
        assert isinstance(target_service, FlextMeltanoService)
        assert target_service._service_type == "target"
        assert getattr(target_service, "target_name", None) == "test-target"

        # Test dbt service creation using unified service
        dbt_service = FlextMeltanoService(service_type="dbt", project_name="test-dbt")
        assert isinstance(dbt_service, FlextMeltanoService)
        assert dbt_service._service_type == "dbt"
        assert getattr(dbt_service, "project_name", None) == "test-dbt"

    def test_unified_service_with_kwargs(self) -> None:
        """Test unified service creation with additional kwargs."""
        # Test creation with additional parameters (stored as instance attributes)
        service = FlextMeltanoService(service_type="tap", tap_name="test-tap")
        assert isinstance(service, FlextMeltanoService)
        assert service._service_type == "tap"
        assert getattr(service, "tap_name", None) == "test-tap"
