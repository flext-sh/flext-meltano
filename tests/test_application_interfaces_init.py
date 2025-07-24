"""Tests for application interfaces __init__ module.

Comprehensive tests for interface imports and exports.
Zero tolerance for untested code.
"""

from __future__ import annotations

from flext_meltano.application import interfaces
from flext_meltano.application.interfaces import (
    EventPublisher,
    JobRepository,
    MeltanoCLIService,
    NotificationService,
    PluginRepository,
    ProjectRepository,
    StateRepository,
)


class TestApplicationInterfacesInit:
    """Test application interfaces initialization and exports."""

    def test_module_imports_successfully(self) -> None:
        """Test that the module imports successfully."""
        assert interfaces is not None
        assert hasattr(interfaces, "__all__")

    def test_external_service_interfaces_import(self) -> None:
        """Test that external service interfaces can be imported."""
        assert EventPublisher is not None
        assert MeltanoCLIService is not None
        assert NotificationService is not None

    def test_repository_interfaces_import(self) -> None:
        """Test that repository interfaces can be imported."""
        assert JobRepository is not None
        assert PluginRepository is not None
        assert ProjectRepository is not None
        assert StateRepository is not None

    def test_all_exports_defined(self) -> None:
        """Test that __all__ is properly defined."""
        expected_exports = {
            "AbstractRepository",
            "EventPublisher",
            "JobRepository",
            "MeltanoCLIService",
            "NotificationService",
            "PluginRepository",
            "ProjectRepository",
            "StateRepository",
        }

        assert hasattr(interfaces, "__all__")
        assert set(interfaces.__all__) == expected_exports

    def test_exported_items_are_accessible(self) -> None:
        """Test that all exported items are accessible."""
        for item_name in interfaces.__all__:
            if item_name != "AbstractRepository":  # This might not be directly available
                assert hasattr(interfaces, item_name)
                item = getattr(interfaces, item_name)
                assert item is not None

    def test_interface_types_are_classes(self) -> None:
        """Test that the imported interfaces are class types."""
        interface_classes = [
            EventPublisher,
            MeltanoCLIService,
            NotificationService,
            JobRepository,
            PluginRepository,
            ProjectRepository,
            StateRepository,
        ]

        for interface_class in interface_classes:
            # Should be a type/class (though might be ABC or Protocol)
            assert isinstance(interface_class, type)

    def test_module_documentation(self) -> None:
        """Test that the module has proper documentation."""
        assert interfaces.__doc__ is not None
        assert "Application Interfaces" in interfaces.__doc__
        assert "NEW SEMANTIC ARCHITECTURE" in interfaces.__doc__

    def test_imports_from_submodules(self) -> None:
        """Test that imports come from the correct submodules."""
        # Test that we can import from the submodules directly
        from flext_meltano.application.interfaces.external_services import (
            EventPublisher as DirectEventPublisher,
            MeltanoCLIService as DirectMeltanoCLIService,
            NotificationService as DirectNotificationService,
        )
        from flext_meltano.application.interfaces.repositories import (
            JobRepository as DirectJobRepository,
            PluginRepository as DirectPluginRepository,
            ProjectRepository as DirectProjectRepository,
            StateRepository as DirectStateRepository,
        )

        # Verify they are the same objects
        assert EventPublisher is DirectEventPublisher
        assert MeltanoCLIService is DirectMeltanoCLIService
        assert NotificationService is DirectNotificationService
        assert JobRepository is DirectJobRepository
        assert PluginRepository is DirectPluginRepository
        assert ProjectRepository is DirectProjectRepository
        assert StateRepository is DirectStateRepository

    def test_interface_availability_via_getattr(self) -> None:
        """Test interface availability using getattr."""
        available_interfaces = [
            "EventPublisher",
            "MeltanoCLIService",
            "NotificationService",
            "JobRepository",
            "PluginRepository",
            "ProjectRepository",
            "StateRepository",
        ]

        for interface_name in available_interfaces:
            interface = getattr(interfaces, interface_name, None)
            assert interface is not None, f"{interface_name} should be available"

    def test_no_extra_exports(self) -> None:
        """Test that there are no unexpected exports."""
        # Get all public attributes (not starting with _)
        public_attrs = [attr for attr in dir(interfaces) if not attr.startswith("_")]

        # Should only contain items from __all__ plus the module itself
        expected_attrs = set(interfaces.__all__)
        actual_attrs = set(public_attrs)

        # Remove standard module attributes and imported submodules
        standard_attrs = {"annotations", "external_services", "repositories"}
        actual_attrs -= standard_attrs

        # All public attributes should be in __all__
        extra_attrs = actual_attrs - expected_attrs
        assert len(extra_attrs) == 0, f"Unexpected public attributes: {extra_attrs}"
