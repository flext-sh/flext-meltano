"""External Service Interfaces - NEW SEMANTIC ARCHITECTURE.

Interfaces for external services and integrations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Protocol

from flext_meltano.infrastructure.di_container import get_service_result

if TYPE_CHECKING:
    from flext_core import ServiceResult

# 🚨 ARCHITECTURAL COMPLIANCE: Import via módulo raiz





class MeltanoCLIService(Protocol):
    """Interface for Meltano CLI operations."""

    @abstractmethod
    async def init_project(self, name: str, directory: str) -> ServiceResult[Any]:
        """Initialize a new Meltano project."""

    @abstractmethod
    async def install_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        project_dir: str,
        variant: str | None = None,
    ) -> ServiceResult[Any]:
        """Install a Meltano plugin."""

    @abstractmethod
    async def run_job(
        self,
        job_name: str,
        project_dir: str,
        environment: str | None = None,
    ) -> ServiceResult[Any]:
        """Run a Meltano job."""

    @abstractmethod
    async def discover_plugins(
        self,
        plugin_type: str | None = None,
    ) -> ServiceResult[Any]:
        """Discover available plugins."""

    @abstractmethod
    async def get_plugin_config(
        self,
        plugin_name: str,
        project_dir: str,
    ) -> ServiceResult[Any]:
        """Get plugin configuration."""


class EventPublisher(Protocol):
    """Interface for publishing domain events."""

    @abstractmethod
    async def publish(self, event: dict[str, Any]) -> ServiceResult[Any]:
        """Publish a domain event."""

    @abstractmethod
    async def publish_batch(self, events: list[dict[str, Any]]) -> ServiceResult[Any]:
        """Publish multiple events as a batch."""


class NotificationService(Protocol):
    """Interface for sending notifications."""

    @abstractmethod
    async def send_job_started(
        self,
        job_id: str,
        job_name: str,
        project_name: str,
    ) -> ServiceResult[Any]:
        """Send job started notification."""

    @abstractmethod
    async def send_job_completed(
        self,
        job_id: str,
        job_name: str,
        project_name: str,
        success: bool,
        duration_seconds: float,
    ) -> ServiceResult[Any]:
        """Send job completed notification."""

    @abstractmethod
    async def send_plugin_installed(
        self,
        plugin_name: str,
        plugin_type: str,
        project_name: str,
    ) -> ServiceResult[Any]:
        """Send plugin installed notification."""


class FileSystemService(ABC):
    """Abstract base class for file system operations."""

    @abstractmethod
    async def create_directory(self, path: str) -> ServiceResult[Any]:
        """Create a directory."""

    @abstractmethod
    async def write_file(self, path: str, content: str) -> ServiceResult[Any]:
        """Write content to a file."""

    @abstractmethod
    async def read_file(self, path: str) -> ServiceResult[Any]:
        """Read content from a file."""

    @abstractmethod
    async def file_exists(self, path: str) -> bool:
        """Check if file exists."""

    @abstractmethod
    async def directory_exists(self, path: str) -> bool:
        """Check if directory exists."""


class ConfigurationService(Protocol):
    """Interface for configuration management."""

    @abstractmethod
    async def load_meltano_config(self, project_dir: str) -> ServiceResult[Any]:
        """Load meltano.yml configuration."""

    @abstractmethod
    async def save_meltano_config(
        self,
        project_dir: str,
        config: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Save meltano.yml configuration."""

    @abstractmethod
    async def validate_config(self, config: dict[str, Any]) -> ServiceResult[Any]:
        """Validate Meltano configuration."""

    @abstractmethod
    async def merge_config(
        self,
        base_config: dict[str, Any],
        override_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Merge configuration objects."""
