"""FlextMeltano EDK Extension Integration.

Meltano EDK extension management following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult
from pydantic import BaseModel, Field, model_validator

from flext_meltano.constants import FlextMeltanoConstants

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoExtension(BaseModel):
    """Meltano EDK extension representation.

    Domain entity for Meltano extensions following Clean Architecture
    patterns with business rules and validation.
    """

    # Core identification
    name: str = Field(
        ...,
        description="Extension name",
        min_length=1,
        max_length=100,
    )
    extension_type: str = Field(
        ...,
        description="Extension type (tap, target, transform, etc.)",
    )

    # Extension metadata
    description: str | None = Field(
        default=None,
        description="Extension description",
        max_length=500,
    )
    version: str = Field(
        default="1.0.0",
        description="Extension version",
    )
    python_version: str = Field(
        default=FlextMeltanoConstants.EDK_PYTHON_VERSION,
        description="Required Python version",
    )

    # File system paths
    extension_dir: Path = Field(
        ...,
        description="Extension root directory",
    )
    config_file: Path | None = Field(
        default=None,
        description="Extension configuration file",
    )
    requirements_file: Path | None = Field(
        default=None,
        description="Python requirements file",
    )

    # Runtime configuration
    executable: str | None = Field(
        default=None,
        description="Extension executable command",
    )
    settings: dict[str, Any] = Field(
        default_factory=dict,
        description="Extension settings",
    )

    # Installation status
    is_installed: bool = Field(
        default=False,
        description="Whether extension is installed",
    )
    is_active: bool = Field(
        default=False,
        description="Whether extension is active",
    )

    class Config:
        """Pydantic model configuration."""

        frozen = False
        validate_assignment = True
        extra = "forbid"

    @model_validator(mode="after")
    def validate_extension_structure(self) -> FlextMeltanoExtension:
        """Validate extension structure and configuration.

        Returns:
            Validated extension instance

        Raises:
            ValueError: If validation fails

        """
        # Validate extension name
        if not FlextMeltanoConstants.is_valid_plugin_name(self.name):
            msg = f"Invalid extension name: {self.name}"
            raise ValueError(msg)

        # Validate extension type
        if self.extension_type not in FlextMeltanoConstants.EDK_EXTENSION_TYPES:
            msg = f"Invalid extension type: {self.extension_type}"
            raise ValueError(msg)

        # Validate extension directory
        if not self.extension_dir.exists():
            msg = f"Extension directory not found: {self.extension_dir}"
            raise ValueError(msg)

        return self

    def install(self) -> FlextResult[None]:
        """Install extension dependencies.

        Business rule: Extension must have valid structure before installation.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if self.is_installed:
                return FlextResult.fail("Extension already installed")

            # Install Python dependencies if requirements file exists
            if self.requirements_file and self.requirements_file.exists():
                install_result = self._install_requirements()
                if not install_result.is_success:
                    return install_result

            self.is_installed = True
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Extension installation failed: {e}")

    def activate(self) -> FlextResult[None]:
        """Activate extension.

        Business rule: Extension must be installed before activation.

        Returns:
            FlextResult indicating success or failure

        """
        if not self.is_installed:
            return FlextResult.fail("Cannot activate uninstalled extension")

        self.is_active = True
        return FlextResult.ok(None)

    def deactivate(self) -> FlextResult[None]:
        """Deactivate extension.

        Returns:
            FlextResult indicating success or failure

        """
        self.is_active = False
        return FlextResult.ok(None)

    def validate_configuration(self) -> FlextResult[dict[str, Any]]:
        """Validate extension configuration and structure.

        Returns:
            FlextResult with validation results

        """
        try:
            validation_results: dict[str, Any] = {
                "extension_valid": True,
                "directory_exists": self.extension_dir.exists(),
                "config_valid": True,
                "requirements_valid": True,
                "executable_valid": True,
                "issues": [],
            }

            # Check configuration file if specified
            if self.config_file and not self.config_file.exists():
                validation_results["config_valid"] = False
                validation_results["extension_valid"] = False
                validation_results["issues"].append(
                    f"Configuration file not found: {self.config_file}",
                )

            # Check requirements file if specified
            if self.requirements_file and not self.requirements_file.exists():
                validation_results["requirements_valid"] = False
                validation_results["extension_valid"] = False
                validation_results["issues"].append(
                    f"Requirements file not found: {self.requirements_file}",
                )

            # Validate executable
            if self.executable and not self._validate_executable():
                validation_results["executable_valid"] = False
                validation_results["extension_valid"] = False
                validation_results["issues"].append(
                    f"Invalid or missing executable: {self.executable}",
                )

            return FlextResult.ok(validation_results)

        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    def get_metadata(self) -> FlextResult[dict[str, Any]]:
        """Get comprehensive extension metadata.

        Returns:
            FlextResult with extension metadata

        """
        try:
            metadata = {
                "name": self.name,
                "type": self.extension_type,
                "version": self.version,
                "description": self.description,
                "python_version": self.python_version,
                "directory": str(self.extension_dir),
                "executable": self.executable,
                "is_installed": self.is_installed,
                "is_active": self.is_active,
                "settings": self.settings,
                "files": {
                    "config_file": str(self.config_file) if self.config_file else None,
                    "requirements_file": (
                        str(self.requirements_file) if self.requirements_file else None
                    ),
                },
            }

            return FlextResult.ok(metadata)

        except Exception as e:
            return FlextResult.fail(f"Failed to get metadata: {e}")

    def update_settings(
        self,
        new_settings: dict[str, Any],
    ) -> FlextResult[None]:
        """Update extension settings.

        Args:
            new_settings: New settings to apply

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Merge with existing settings (type already guaranteed by annotation)
            self.settings.update(new_settings)
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to update settings: {e}")

    def generate_config(self) -> FlextResult[dict[str, Any]]:
        """Generate extension configuration for Meltano.

        Returns:
            FlextResult with Meltano configuration

        """
        try:
            config = {
                "name": self.name,
                "type": self.extension_type,
                "version": self.version,
                "description": self.description,
                "python_version": self.python_version,
                "settings": self.settings,
            }

            if self.executable:
                config["executable"] = self.executable

            return FlextResult.ok(config)

        except Exception as e:
            return FlextResult.fail(f"Failed to generate config: {e}")

    def _install_requirements(self) -> FlextResult[None]:
        """Install Python requirements.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            import subprocess

            # Install requirements using pip
            result = subprocess.run(
                [
                    "pip",
                    "install",
                    "-r",
                    str(self.requirements_file),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )

            if result.returncode != 0:
                return FlextResult.fail(
                    f"Requirements installation failed: {result.stderr}",
                )

            return FlextResult.ok(None)

        except subprocess.TimeoutExpired:
            return FlextResult.fail("Requirements installation timed out")
        except Exception as e:
            return FlextResult.fail(f"Requirements installation error: {e}")

    def _validate_executable(self) -> bool:
        """Validate extension executable.

        Returns:
            True if executable is valid, False otherwise

        """
        try:
            if not self.executable:
                return True  # No executable specified is valid

            import shutil

            # Check if executable exists in PATH
            return shutil.which(self.executable) is not None

        except Exception:
            return False

    def to_dict(self) -> dict[str, Any]:
        """Convert extension to dictionary representation.

        Returns:
            Dictionary representation of the extension

        """
        return {
            "name": self.name,
            "extension_type": self.extension_type,
            "description": self.description,
            "version": self.version,
            "python_version": self.python_version,
            "extension_dir": str(self.extension_dir),
            "config_file": str(self.config_file) if self.config_file else None,
            "requirements_file": (
                str(self.requirements_file) if self.requirements_file else None
            ),
            "executable": self.executable,
            "settings": self.settings,
            "is_installed": self.is_installed,
            "is_active": self.is_active,
        }
