"""Singer SDK Integration.

Clean Singer SDK integration using flext-core patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult

# Singer SDK imports with clean error handling
try:
    from singer_sdk import Stream, Tap, Target
    from singer_sdk.authenticators import OAuthAuthenticator
    from singer_sdk.sinks import BatchSink, Sink, SQLSink
    from singer_sdk.testing import get_tap_test_class
    from singer_sdk.typing import PropertiesList, Property, StringType

    SINGER_AVAILABLE = True
except ImportError:
    Stream = Tap = Target = Sink = SQLSink = PropertiesList = Property = (
        get_tap_test_class
    ) = OAuthAuthenticator = BatchSink = StringType = None
    SINGER_AVAILABLE = False

if TYPE_CHECKING and SINGER_AVAILABLE:
    pass


class FlextSingerService:
    """Singer SDK service using flext-core patterns."""

    def __init__(self, project_root: str = ".") -> None:
        """Initialize Singer service."""
        self.project_root = project_root

    def create_tap(
        self, tap_class: type[Tap], config: dict[str, Any],
    ) -> FlextResult[Tap]:
        """Create tap instance.

        Args:
            tap_class: Tap class to instantiate
            config: Tap configuration

        Returns:
            FlextResult containing tap instance

        """
        if not SINGER_AVAILABLE:
            return FlextResult.fail("Singer SDK not available")

        try:
            tap_instance = tap_class(config=config)
            return FlextResult.ok(tap_instance)
        except Exception as e:
            return FlextResult.fail(f"Failed to create tap: {e}")

    def create_target(
        self, target_class: type[Target], config: dict[str, Any],
    ) -> FlextResult[Target]:
        """Create target instance.

        Args:
            target_class: Target class to instantiate
            config: Target configuration

        Returns:
            FlextResult containing target instance

        """
        if not SINGER_AVAILABLE:
            return FlextResult.fail("Singer SDK not available")

        try:
            target_instance = target_class(config=config)
            return FlextResult.ok(target_instance)
        except Exception as e:
            return FlextResult.fail(f"Failed to create target: {e}")

    def discover_catalog(self, tap: Tap) -> FlextResult[dict[str, Any]]:
        """Discover catalog from tap.

        Args:
            tap: Tap instance

        Returns:
            FlextResult containing catalog

        """
        if not SINGER_AVAILABLE:
            return FlextResult.fail("Singer SDK not available")

        try:
            catalog = tap.catalog_dict
            return FlextResult.ok(catalog)
        except Exception as e:
            return FlextResult.fail(f"Failed to discover catalog: {e}")

    def test_connection(self, tap: Tap) -> FlextResult[bool]:
        """Test tap connection.

        Args:
            tap: Tap instance

        Returns:
            FlextResult containing connection status

        """
        if not SINGER_AVAILABLE:
            return FlextResult.fail("Singer SDK not available")

        try:
            tap.test_connection()
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Connection test failed: {e}")


def get_singer_service(project_root: str = ".") -> FlextSingerService:
    """Get Singer service instance.

    Args:
        project_root: Project root directory

    Returns:
        Singer service instance

    """
    return FlextSingerService(project_root)


__all__ = [
    # Availability
    "SINGER_AVAILABLE",
    "BatchSink",
    # Service
    "FlextSingerService",
    "OAuthAuthenticator",
    "PropertiesList",
    "Property",
    "SQLSink",
    "Sink",
    # Singer SDK exports
    "Stream",
    "StringType",
    "Tap",
    "Target",
    "get_singer_service",
    "get_tap_test_class",
]
