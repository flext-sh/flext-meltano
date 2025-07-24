"""FlextMeltano EDK Extension Manager.

Extension lifecycle management following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.edk.extension import FlextMeltanoExtension

if TYPE_CHECKING:
    from pathlib import Path

    from flext_core import FlextContainer

    from flext_meltano.config.settings import FlextMeltanoSettings


class FlextMeltanoExtensionManager:
    """Meltano EDK extension lifecycle manager.

    Application service for managing extension installation, configuration,
    and lifecycle following Clean Architecture patterns.
    """

    def __init__(
        self,
        settings: FlextMeltanoSettings,
        container: FlextContainer,
    ) -> None:
        """Initialize extension manager.

        Args:
            settings: Platform settings
            container: Dependency injection container

        """
        self._settings = settings
        self._container = container
        self._extensions: dict[str, FlextMeltanoExtension] = {}

    def create_extension(
        self,
        name: str,
        extension_type: str,
        extension_dir: Path,
        description: str | None = None,
        executable: str | None = None,
    ) -> FlextResult[FlextMeltanoExtension]:
        """Create new extension.

        Args:
            name: Extension name
            extension_type: Type of extension
            extension_dir: Extension directory
            description: Optional description
            executable: Optional executable command

        Returns:
            FlextResult containing created extension or error

        """
        try:
            # Validate extension type
            if extension_type not in FlextMeltanoConstants.EDK_EXTENSION_TYPES:
                return FlextResult.fail(f"Invalid extension type: {extension_type}")

            # Check if extension already exists
            if name in self._extensions:
                return FlextResult.fail(f"Extension '{name}' already exists")

            # Create extension directory if needed
            extension_dir.mkdir(parents=True, exist_ok=True)

            # Create extension instance
            extension = FlextMeltanoExtension(
                name=name,
                extension_type=extension_type,
                extension_dir=extension_dir,
                description=description,
                executable=executable,
            )

            # Register extension
            self._extensions[name] = extension

            return FlextResult.ok(extension)

        except Exception as e:
            return FlextResult.fail(f"Failed to create extension: {e}")

    def install_extension(
        self,
        name: str,
        force_reinstall: bool = False,
    ) -> FlextResult[None]:
        """Install extension and its dependencies.

        Args:
            name: Extension name
            force_reinstall: Force reinstallation if already installed

        Returns:
            FlextResult indicating success or failure

        """
        try:
            extension = self._get_extension(name)
            if not extension:
                return FlextResult.fail(f"Extension '{name}' not found")

            # Check if already installed
            if extension.is_installed and not force_reinstall:
                return FlextResult.fail(
                    f"Extension '{name}' already installed. "
                    "Use force_reinstall=True to reinstall.",
                )

            # Validate extension before installation
            validation_result = extension.validate_configuration()
            if not validation_result.is_success:
                return FlextResult.fail(
                    f"Extension validation failed: {validation_result.error}",
                )

            # Install extension
            install_result = extension.install()
            if not install_result.is_success:
                return install_result

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Extension installation failed: {e}")

    def uninstall_extension(self, name: str) -> FlextResult[None]:
        """Uninstall extension.

        Args:
            name: Extension name

        Returns:
            FlextResult indicating success or failure

        """
        try:
            extension = self._get_extension(name)
            if not extension:
                return FlextResult.fail(f"Extension '{name}' not found")

            # Deactivate if active
            if extension.is_active:
                deactivate_result = extension.deactivate()
                if not deactivate_result.is_success:
                    return deactivate_result

            # Mark as uninstalled
            extension.is_installed = False

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Extension uninstallation failed: {e}")

    def activate_extension(self, name: str) -> FlextResult[None]:
        """Activate extension.

        Args:
            name: Extension name

        Returns:
            FlextResult indicating success or failure

        """
        try:
            extension = self._get_extension(name)
            if not extension:
                return FlextResult.fail(f"Extension '{name}' not found")

            return extension.activate()

        except Exception as e:
            return FlextResult.fail(f"Extension activation failed: {e}")

    def deactivate_extension(self, name: str) -> FlextResult[None]:
        """Deactivate extension.

        Args:
            name: Extension name

        Returns:
            FlextResult indicating success or failure

        """
        try:
            extension = self._get_extension(name)
            if not extension:
                return FlextResult.fail(f"Extension '{name}' not found")

            return extension.deactivate()

        except Exception as e:
            return FlextResult.fail(f"Extension deactivation failed: {e}")

    def list_extensions(
        self,
        extension_type: str | None = None,
        installed_only: bool = False,
        active_only: bool = False,
    ) -> FlextResult[list[dict[str, Any]]]:
        """List registered extensions.

        Args:
            extension_type: Filter by extension type
            installed_only: Show only installed extensions
            active_only: Show only active extensions

        Returns:
            FlextResult with list of extensions

        """
        try:
            extensions_data = []

            for extension in self._extensions.values():
                # Apply filters
                if extension_type and extension.extension_type != extension_type:
                    continue
                if installed_only and not extension.is_installed:
                    continue
                if active_only and not extension.is_active:
                    continue

                metadata_result = extension.get_metadata()
                if metadata_result.is_success and metadata_result.data is not None:
                    extensions_data.append(metadata_result.data)

            return FlextResult.ok(extensions_data)

        except Exception as e:
            return FlextResult.fail(f"Failed to list extensions: {e}")

    def get_extension_status(self, name: str) -> FlextResult[dict[str, Any]]:
        """Get comprehensive extension status.

        Args:
            name: Extension name

        Returns:
            FlextResult with extension status

        """
        try:
            extension = self._get_extension(name)
            if not extension:
                return FlextResult.fail(f"Extension '{name}' not found")

            # Get basic metadata
            metadata_result = extension.get_metadata()
            if not metadata_result.is_success:
                return metadata_result

            status_data = metadata_result.data or {}

            # Add validation results
            validation_result = extension.validate_configuration()
            status_data["validation"] = (
                validation_result.data
                if validation_result.is_success
                else {"error": validation_result.error}
            )

            return FlextResult.ok(status_data)

        except Exception as e:
            return FlextResult.fail(f"Failed to get extension status: {e}")

    def update_extension_settings(
        self,
        name: str,
        settings: dict[str, Any],
    ) -> FlextResult[None]:
        """Update extension settings.

        Args:
            name: Extension name
            settings: New settings

        Returns:
            FlextResult indicating success or failure

        """
        try:
            extension = self._get_extension(name)
            if not extension:
                return FlextResult.fail(f"Extension '{name}' not found")

            return extension.update_settings(settings)

        except Exception as e:
            return FlextResult.fail(f"Failed to update extension settings: {e}")

    def generate_meltano_config(
        self,
        extension_names: list[str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Generate Meltano configuration for extensions.

        Args:
            extension_names: Specific extensions to include (all if None)

        Returns:
            FlextResult with Meltano configuration

        """
        try:
            meltano_config: dict[str, Any] = {
                "plugins": {
                    "extractors": [],
                    "loaders": [],
                    "transformers": [],
                    "orchestrators": [],
                    "file_bundles": [],
                    "utilities": [],
                },
            }

            extensions_to_process = (
                [
                    self._extensions[name]
                    for name in extension_names
                    if name in self._extensions
                ]
                if extension_names
                else list(self._extensions.values())
            )

            for extension in extensions_to_process:
                if not extension.is_active:
                    continue

                config_result = extension.generate_config()
                if config_result.is_success:
                    extension_config = config_result.data

                    # Map extension types to Meltano plugin categories
                    if extension.extension_type == "tap":
                        meltano_config["plugins"]["extractors"].append(extension_config)
                    elif extension.extension_type == "target":
                        meltano_config["plugins"]["loaders"].append(extension_config)
                    elif extension.extension_type == "transform":
                        meltano_config["plugins"]["transformers"].append(
                            extension_config,
                        )
                    elif extension.extension_type == "orchestrate":
                        meltano_config["plugins"]["orchestrators"].append(
                            extension_config,
                        )
                    elif extension.extension_type == "file":
                        meltano_config["plugins"]["file_bundles"].append(
                            extension_config,
                        )
                    elif extension.extension_type == "utility":
                        meltano_config["plugins"]["utilities"].append(extension_config)

            return FlextResult.ok(meltano_config)

        except Exception as e:
            return FlextResult.fail(f"Failed to generate Meltano config: {e}")

    def discover_extensions(
        self, search_path: Path,
    ) -> FlextResult[list[dict[str, Any]]]:
        """Discover extensions in given path.

        Args:
            search_path: Path to search for extensions

        Returns:
            FlextResult with discovered extensions

        """
        try:
            discovered_extensions = []

            if not search_path.exists():
                return FlextResult.fail(f"Search path not found: {search_path}")

            # Search for extension directories
            for item in search_path.iterdir():
                if item.is_dir():
                    # Check for extension markers
                    if self._is_extension_directory(item):
                        extension_info = self._analyze_extension_directory(item)
                        if extension_info:
                            discovered_extensions.append(extension_info)

            return FlextResult.ok(discovered_extensions)

        except Exception as e:
            return FlextResult.fail(f"Extension discovery failed: {e}")

    def _get_extension(self, name: str) -> FlextMeltanoExtension | None:
        """Get extension by name.

        Args:
            name: Extension name

        Returns:
            Extension instance or None if not found

        """
        return self._extensions.get(name)

    def _is_extension_directory(self, directory: Path) -> bool:
        """Check if directory contains a Meltano extension.

        Args:
            directory: Directory to check

        Returns:
            True if directory contains extension, False otherwise

        """
        # Check for common extension files
        extension_markers = [
            "setup.py",
            "pyproject.toml",
            "requirements.txt",
            "meltano.yml",
            "extension.py",
        ]

        return any((directory / marker).exists() for marker in extension_markers)

    def _analyze_extension_directory(self, directory: Path) -> dict[str, Any] | None:
        """Analyze extension directory to extract metadata.

        Args:
            directory: Extension directory

        Returns:
            Extension metadata or None if analysis fails

        """
        try:
            metadata: dict[str, Any] = {
                "name": directory.name,
                "directory": str(directory),
                "type": "unknown",
                "files": [],
            }

            # Analyze files
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    metadata["files"].append(str(file_path.relative_to(directory)))

            # Try to determine extension type from name or structure
            name_lower = directory.name.lower()
            if name_lower.startswith("tap-"):
                metadata["type"] = "tap"
            elif name_lower.startswith("target-"):
                metadata["type"] = "target"
            elif "transform" in name_lower:
                metadata["type"] = "transform"

            return metadata

        except Exception:
            return None
