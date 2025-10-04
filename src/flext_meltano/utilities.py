"""FLEXT Meltano Utilities - Domain-specific Meltano utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

import yaml
from flext_core import (
    FlextConstants,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

# Use specific module imports to avoid circular dependencies
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.file_managers import FlextMeltanoFileManagers


class FlextMeltanoUtilities(FlextUtilities):
    """DOMAIN-SPECIFIC Meltano utilities - ONLY what cannot be generalized to flext-core.

    Inherits from FlextUtilities to avoid duplication and ensure consistency.
    """

    @classmethod
    def create_meltano_config_dict(
        cls,
        project_id: str,
        project_name: str = "",
    ) -> FlextResult[FlextTypes.Dict]:
        """Create MELTANO-SPECIFIC configuration dictionary - DOMAIN-SPECIFIC ONLY."""
        logger = FlextLogger(__name__)
        try:
            # Delegate to FlextUtilities for text processing
            safe_project_id = FlextUtilities.TextProcessor.safe_string(
                project_id, project_id
            )
            safe_project_name = FlextUtilities.TextProcessor.safe_string(
                project_name, project_name
            )

            # DOMAIN-SPECIFIC: Meltano configuration structure
            config_dict: FlextTypes.Dict = {
                "version": 1,
                "project_id": safe_project_id,
                "project_name": safe_project_name,
                "environments": [
                    {"name": "env"}
                    for env in FlextMeltanoConstants.METADATA_DEFAULT_ENVIRONMENTS
                ],
                "plugins": {
                    "extractors": [],
                    "loaders": [],
                    "transformers": [],
                    "orchestrators": [],
                },
                "metadata": {
                    "created_by": FlextMeltanoConstants.METADATA_CREATED_BY,
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),  # NO DUPLICATION
                    "flext_version": FlextMeltanoConstants.FLEXT_MELTANO_VERSION,
                },
            }
            return FlextResult[FlextTypes.Dict].ok(data=config_dict)
        except Exception as e:  # pragma: no cover
            error_msg = f"Failed to create Meltano config dict: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextTypes.Dict].fail(error_msg)

    @classmethod
    def write_meltano_yml(
        cls,
        config: FlextTypes.Dict,
        target_path: Path,
    ) -> FlextResult[bool]:
        """Write MELTANO-SPECIFIC YAML configuration using monadic resource management.

        Uses FlextResult.with_resource() for automatic file handle management
        and composable error handling with proper resource cleanup.
        DOMAIN-SPECIFIC: YAML writing (cannot be generalized to flext-core).

        Args:
            config: Configuration dictionary to write.
            target_path: Path where to write the YAML file.

        Returns:
            FlextResult indicating write operation success.

        """
        # MONADIC RESOURCE MANAGEMENT: Automatic file handle cleanup
        # with_resource expects operation(value, resource) -> FlextResult[U]

        def write_operation(
            _unused_value: object,  # Required by with_resource signature
            file_handle: TextIO,
            /,
        ) -> FlextResult[bool]:
            return cls._write_yaml_content(file_handle, config)

        # Cleanup function should be Callable[[TResource], None] | None
        def cleanup_file_handle(file_handle: TextIO) -> None:
            try:
                if hasattr(file_handle, "close"):
                    file_handle.close()
            except Exception as e:
                FlextLogger(__name__).warning(f"Error closing file handle: {e}")

        def resource_factory() -> TextIO:
            result: FlextResult[TextIO] = cls._open_yaml_file_for_writing(target_path)
            if result.is_failure:
                error_msg = f"Failed to open file: {result.error}"
                raise RuntimeError(error_msg)
            return result.value

        return (
            FlextResult[bool]
            .ok(data=True)
            .with_resource(
                resource_factory,
                write_operation,
                cleanup_file_handle,
            )
            .with_context(
                lambda error: f"Writing {FlextMeltanoConstants.MELTANO_PROJECT_FILE}: {error}"
            )
        )

    @classmethod
    def _open_yaml_file_for_writing(cls, target_path: Path) -> FlextResult[TextIO]:
        """Open YAML file for writing with validation.

        Args:
            target_path: Path to open for writing.

        Returns:
            FlextResult containing file handle or error.

        """
        try:
            # Validate parent directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)

            file_handle = target_path.open(
                "w", encoding=FlextConstants.Mixins.DEFAULT_ENCODING
            )
            return FlextResult[TextIO].ok(data=file_handle)
        except Exception as e:
            return FlextResult[TextIO].fail(f"Failed to open file for writing: {e}")

    @classmethod
    def _write_yaml_content(
        cls, file_handle: TextIO, config: FlextTypes.Dict
    ) -> FlextResult[bool]:
        """Write YAML content to file handle.

        Args:
            file_handle: Open file handle for writing.
            config: Configuration dictionary to write.

        Returns:
            FlextResult indicating write success.

        """
        try:
            # TYPE SAFETY: Ensure file_handle is writable and config is properly typed
            if not hasattr(file_handle, "write"):
                return FlextResult[bool].fail(
                    "Invalid file handle: missing write method"
                )

            # MONADIC PATTERN: Safe YAML conversion with proper type casting
            yaml_data: FlextTypes.Dict = dict(config)  # Type-safe conversion

            # DOMAIN-SPECIFIC: YAML writing with Meltano formatting preferences
            yaml.dump(yaml_data, file_handle, default_flow_style=False, indent=2)
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to write YAML content: {e}")

    @classmethod
    def _close_file_handle(cls, file_handle: TextIO) -> FlextResult[None]:
        """Close file handle safely.

        Args:
            file_handle: File handle to close.

        Returns:
            FlextResult indicating close operation result.

        """
        try:
            if hasattr(file_handle, "close"):
                file_handle.close()
            return FlextResult.ok(data=None)
        except Exception as e:
            # Log but don't fail on close errors
            FlextLogger(__name__).warning(f"Error closing file handle: {e}")
            return FlextResult.ok(data=None)

    # NOTE: create_temp_directory moved to FlextMeltanoFileManagers (proper domain responsibility)

    @classmethod
    def create_plugin_config_dict(
        cls,
        name: str,
        plugin_type: str = "extractor",
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> FlextResult[FlextTypes.Dict]:
        """Create MELTANO-SPECIFIC plugin config using FlextUtilities foundation."""
        try:
            # Delegate to FlextUtilities for ALL text processing
            safe_name = FlextUtilities.TextProcessor.safe_string(name, name)
            safe_namespace = FlextUtilities.TextProcessor.safe_string(
                namespace, namespace
            )

            # DOMAIN-SPECIFIC: Meltano plugin-specific defaults
            safe_pip_url = FlextUtilities.TextProcessor.safe_string(pip_url, pip_url)
            safe_executable = FlextUtilities.TextProcessor.safe_string(
                executable, executable
            )

            config_dict: FlextTypes.Dict = {
                "name": safe_name,
                "namespace": safe_namespace,
                "pip_url": safe_pip_url,
                "executable": safe_executable,
                "type": plugin_type or "extractor",
                "settings": {},
                "config": {},
                "metadata": {
                    "created_by": FlextMeltanoConstants.METADATA_CREATED_BY,
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),  # NO DUPLICATION
                },
            }
            return FlextResult[FlextTypes.Dict].ok(data=config_dict)
        except Exception as e:  # pragma: no cover
            error_msg = f"Failed to create plugin config: {e}"
            FlextLogger(__name__).exception(error_msg)
            return FlextResult[FlextTypes.Dict].fail(error_msg)

    @classmethod
    def load_yaml_config(cls, path: Path) -> FlextResult[FlextTypes.Dict]:
        """Load YAML config using monadic composition with resource management.

        Uses FlextResult monadic patterns to chain file loading, validation,
        and type conversion with automatic error propagation and resource cleanup.
        ZERO DUPLICATION: Delegates to FlextMeltanoFileManagers as SOURCE OF TRUTH.

        Args:
            path: Path to YAML configuration file.

        Returns:
            FlextResult containing loaded configuration dictionary.

        """

        # MONADIC COMPOSITION: Chain file operations with automatic error handling
        def convert_to_dict(
            config_dict: object,
        ) -> FlextTypes.Dict:
            """Type-safe conversion from ConfigDict to FlextTypes.Dict."""
            # ConfigDict is compatible with dict["str", "JsonValue"] but MyPy needs explicit conversion
            return dict(config_dict) if isinstance(config_dict, dict) else {}

        return (
            FlextResult[Path]
            .ok(path)
            .flat_map(cls._validate_yaml_path)
            .flat_map(FlextMeltanoFileManagers.load_yaml_config)
            .map(convert_to_dict)  # Type-safe conversion to FlextTypes.Dict
            .with_context(
                lambda error: f"Loading YAML config from {path}: {error}"
            )  # Add error context
        )

    @classmethod
    def _validate_yaml_path(cls, path: Path) -> FlextResult[Path]:
        """Validate YAML file path before loading.

        Args:
            path: Path to validate.

        Returns:
            FlextResult containing validated path or error.

        """
        if not path.exists():
            return FlextResult.fail(f"YAML config file not found: {path}")
        if not path.is_file():
            return FlextResult.fail(f"Path is not a file: {path}")
        if path.suffix.lower() not in {
            FlextConstants.Platform.EXT_YML,
            FlextConstants.Platform.EXT_YAML,
        }:
            return FlextResult.fail(f"File is not a YAML file: {path}")

        return FlextResult.ok(data=path)

    def directory_exists(self, path: Path) -> FlextResult[bool]:
        """Check if directory exists."""
        try:
            return FlextResult.ok(path.exists() and path.is_dir())
        except (OSError, ValueError) as e:
            return FlextResult.fail(f"Failed to check directory existence: {e}")

    def validate_project_structure(self, project_path: Path) -> FlextResult[bool]:
        """Validate Meltano project structure."""
        try:
            if not project_path.exists():
                return FlextResult.fail(f"Project path does not exist: {project_path}")

            meltano_yml = project_path / "meltano.yml"
            if not meltano_yml.exists():
                return FlextResult.fail(f"Meltano config file not found: {meltano_yml}")

            return FlextResult.ok(True)
        except (OSError, ValueError) as e:
            return FlextResult.fail(f"Failed to validate project structure: {e}")

    def create_project_file(self, file_path: Path, content: str) -> FlextResult[Path]:
        """Create a project file with content."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return FlextResult.ok(file_path)
        except (OSError, ValueError) as e:
            return FlextResult.fail(f"Failed to create project file: {e}")

    def load_yaml_file(self, file_path: Path) -> FlextResult[FlextTypes.Dict]:
        """Load YAML file."""
        return self.load_yaml_config(file_path)

    def save_yaml_file(
        self, file_path: Path, content: FlextTypes.Dict
    ) -> FlextResult[Path]:
        """Save content to YAML file."""
        try:
            self.write_meltano_yml(file_path, content)
            return FlextResult.ok(file_path)
        except (OSError, ValueError, yaml.YAMLError) as e:
            return FlextResult.fail(f"Failed to save YAML file: {e}")


__all__ = ["FlextMeltanoUtilities"]
