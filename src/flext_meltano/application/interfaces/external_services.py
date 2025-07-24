"""External Service Interfaces - NEW SEMANTIC ARCHITECTURE.

Interfaces for external services and integrations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from flext_core import FlextResult

# 🚨 ARCHITECTURAL COMPLIANCE: Import via módulo raiz


class FlextMeltanoMeltanoCLIService(Protocol):
    """Interface for Meltano CLI operations."""

    @abstractmethod
    async def init_project(self, name: str, directory: str) -> FlextResult[Any]:
        """Initialize a new Meltano project."""

    @abstractmethod
    async def install_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        project_dir: str,
        variant: str | None = None,
    ) -> FlextResult[Any]:
        """Install a Meltano plugin."""

    @abstractmethod
    async def run_job(
        self,
        job_name: str,
        project_dir: str,
        environment: str | None = None,
    ) -> FlextResult[Any]:
        """Run a Meltano job."""

    @abstractmethod
    async def discover_plugins(
        self,
        plugin_type: str | None = None,
    ) -> FlextResult[Any]:
        """Discover available plugins."""

    @abstractmethod
    async def get_plugin_config(
        self,
        plugin_name: str,
        project_dir: str,
    ) -> FlextResult[Any]:
        """Get plugin configuration."""


class FlextMeltanoEventPublisher(Protocol):
    """Interface for publishing domain events."""

    @abstractmethod
    async def publish(self, event: dict[str, Any]) -> FlextResult[Any]:
        """Publish a domain event."""

    @abstractmethod
    async def publish_batch(self, events: list[dict[str, Any]]) -> FlextResult[Any]:
        """Publish multiple events as a batch."""


class FlextMeltanoNotificationService(Protocol):
    """Interface for sending notifications."""

    @abstractmethod
    async def send_job_started(
        self,
        job_id: str,
        job_name: str,
        project_name: str,
    ) -> FlextResult[Any]:
        """Send job started notification."""

    @abstractmethod
    async def send_job_completed(
        self,
        job_id: str,
        job_name: str,
        project_name: str,
        success: bool,
        duration_seconds: float,
    ) -> FlextResult[Any]:
        """Send job completed notification."""

    @abstractmethod
    async def send_plugin_installed(
        self,
        plugin_name: str,
        plugin_type: str,
        project_name: str,
    ) -> FlextResult[Any]:
        """Send plugin installed notification."""


class FlextMeltanoFileSystemService(ABC):
    """Abstract base class for file system operations."""

    @abstractmethod
    async def create_directory(self, path: str) -> FlextResult[Any]:
        """Create a directory."""

    @abstractmethod
    async def write_file(self, path: str, content: str) -> FlextResult[Any]:
        """Write content to a file."""

    @abstractmethod
    async def read_file(self, path: str) -> FlextResult[Any]:
        """Read content from a file."""

    @abstractmethod
    async def file_exists(self, path: str) -> bool:
        """Check if file exists."""

    @abstractmethod
    async def directory_exists(self, path: str) -> bool:
        """Check if directory exists."""


class FlextMeltanoConfigurationService(Protocol):
    """Interface for configuration management."""

    @abstractmethod
    async def load_meltano_config(self, project_dir: str) -> FlextResult[Any]:
        """Load meltano.yml configuration."""

    @abstractmethod
    async def save_meltano_config(
        self,
        project_dir: str,
        config: dict[str, Any],
    ) -> FlextResult[Any]:
        """Save meltano.yml configuration."""

    @abstractmethod
    async def validate_config(self, config: dict[str, Any]) -> FlextResult[Any]:
        """Validate Meltano configuration."""

    @abstractmethod
    async def merge_config(
        self,
        base_config: dict[str, Any],
        override_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Merge configuration objects."""


# Create aliases for the expected interface names
MeltanoCLIService = FlextMeltanoMeltanoCLIService
EventPublisher = FlextMeltanoEventPublisher
NotificationService = FlextMeltanoNotificationService
