"""Simple test for FLEXT Meltano application services - MyPy compliant."""
from __future__ import annotations

import sys
from unittest.mock import MagicMock

# Mock missing dependencies to avoid import errors
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# Import from simplified API - must be after mocking
# ruff: noqa: E402
from flext_meltano import (
    JobService,
    PluginService,
    ProjectService,
    StateService,
)


class TestServiceInitialization:
    """Test basic service initialization - works with current stub implementations."""

    def test_project_service_initialization(self) -> None:
        """Test that ProjectService can be imported and has basic structure."""
        # ProjectService (ProjectApplicationService) requires dependencies in constructor
        assert ProjectService is not None
        assert hasattr(ProjectService, "__init__")

    def test_state_service_initialization(self) -> None:
        """Test that StateService can be imported and initialized."""
        service = StateService()
        assert service is not None
        assert hasattr(service, "validate_invariants")
        assert service.validate_invariants() is True

    def test_job_service_initialization(self) -> None:
        """Test that JobService can be imported and initialized."""
        service = JobService()
        assert service is not None
        assert hasattr(service, "validate_invariants")
        assert service.validate_invariants() is True

    def test_plugin_service_initialization(self) -> None:
        """Test that PluginService can be imported and initialized."""
        service = PluginService()
        assert service is not None
        assert hasattr(service, "validate_invariants")
        assert service.validate_invariants() is True


class TestServiceTypes:
    """Test service type compatibility."""

    def test_all_services_are_callable(self) -> None:
        """Test that all service classes are callable."""
        assert callable(ProjectService)
        assert callable(StateService)
        assert callable(JobService)
        assert callable(PluginService)

    def test_service_imports(self) -> None:
        """Test that services can be imported from the root module."""
        from flext_meltano import (
            JobService as JobSvc,
            PluginService as PluginSvc,
            ProjectService as ProjectSvc,
            StateService as StateSvc,
        )

        assert JobSvc is JobService
        assert PluginSvc is PluginService
        assert ProjectSvc is ProjectService
        assert StateSvc is StateService
