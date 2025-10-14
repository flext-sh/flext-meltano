"""FLEXT Meltano Utilities - Domain-specific Meltano utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

import yaml
from flext_core import FlextCore

# Use specific module imports to avoid circular dependencies
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.file_managers import FlextMeltanoFileManagers


class FlextMeltanoUtilities(FlextCore.Utilities):
    """DOMAIN-SPECIFIC Meltano utilities - ONLY what cannot be generalized to flext-core.

    Inherits from FlextCore.Utilities to avoid duplication and ensure consistency.
    """

    @classmethod
    def create_meltano_config_dict(
        cls,
        project_id: str,
        project_name: str = "",
        version: str | None = None,
        default_environment: str | None = None,
        plugins: FlextCore.Types.Dict | None = None,
        environments: FlextCore.Types.Dict | None = None,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Create MELTANO-SPECIFIC configuration dictionary - DOMAIN-SPECIFIC ONLY."""
        logger = FlextCore.Logger(__name__)
        try:
            # Delegate to FlextCore.Utilities for text processing
            safe_project_id = FlextCore.Utilities.TextProcessor.safe_string(
                project_id, project_id
            )
            safe_project_name = FlextCore.Utilities.TextProcessor.safe_string(
                project_name, project_name
            )

            # DOMAIN-SPECIFIC: Meltano configuration structure
            config_dict: FlextCore.Types.Dict = {
                "version": version or 1,
                "project_id": safe_project_id,
                "project_name": safe_project_name or safe_project_id,
            }

            # Add default_environment if provided
            if default_environment:
                config_dict["default_environment"] = default_environment

            # Add environments if provided, otherwise use defaults
            if environments:
                config_dict["environments"] = environments
            else:
                config_dict["environments"] = [
                    {"name": env}
                    for env in FlextMeltanoConstants.Meltano.METADATA_DEFAULT_ENVIRONMENTS
                ]

            # Add plugins if provided, otherwise use defaults
            if plugins:
                config_dict["plugins"] = plugins
            else:
                config_dict["plugins"] = {
                    "extractors": [],
                    "loaders": [],
                    "transformers": [],
                    "orchestrators": [],
                }

            # Add metadata
            config_dict["metadata"] = {
                "created_by": FlextMeltanoConstants.Meltano.METADATA_CREATED_BY,
                "created_at": FlextCore.Utilities.Generators.generate_iso_timestamp(),  # NO DUPLICATION
                "flext_version": FlextMeltanoConstants.Meltano.FLEXT_MELTANO_VERSION,
            }
            return FlextCore.Result[FlextCore.Types.Dict].ok(data=config_dict)
        except Exception as e:  # pragma: no cover
            error_msg = f"Failed to create Meltano config dict[str, object]: {e}"
            logger.exception(error_msg)
            return FlextCore.Result[FlextCore.Types.Dict].fail(error_msg)

    @classmethod
    def write_meltano_yml(
        cls,
        config: FlextCore.Types.Dict,
        target_path: Path,
    ) -> FlextCore.Result[bool]:
        """Write MELTANO-SPECIFIC YAML configuration using monadic resource management.

        Uses FlextCore.Result.with_resource() for automatic file handle management
        and composable error handling with proper resource cleanup.
        DOMAIN-SPECIFIC: YAML writing (cannot be generalized to flext-core).

        Args:
            config: Configuration dictionary to write.
            target_path: Path where to write the YAML file.

        Returns:
            FlextCore.Result indicating write operation success.

        """
        # MONADIC RESOURCE MANAGEMENT: Automatic file handle cleanup
        # with_resource expects operation(value, resource) -> FlextCore.Result[U]

        def write_operation(
            _unused_value: object,  # Required by with_resource signature
            file_handle: TextIO,
            /,
        ) -> FlextCore.Result[bool]:
            return cls._write_yaml_content(file_handle, config)

        # Cleanup function should be Callable[[TResource], None] | None
        def cleanup_file_handle(file_handle: TextIO) -> None:
            try:
                if hasattr(file_handle, "close"):
                    file_handle.close()
            except Exception as e:
                FlextCore.Logger(__name__).warning(f"Error closing file handle: {e}")

        def resource_factory() -> TextIO:
            result: FlextCore.Result[TextIO] = cls._open_yaml_file_for_writing(
                target_path
            )
            if result.is_failure:
                error_msg = f"Failed to open file: {result.error}"
                raise RuntimeError(error_msg)
            return result.value

        return (
            FlextCore.Result[bool]
            .ok(data=True)
            .with_resource(
                resource_factory,
                write_operation,
                cleanup_file_handle,
            )
            .with_context(
                lambda error: f"Writing {FlextMeltanoConstants.Meltano.MELTANO_PROJECT_FILE}: {error}"
            )
        )

    @classmethod
    def _open_yaml_file_for_writing(cls, target_path: Path) -> FlextCore.Result[TextIO]:
        """Open YAML file for writing with validation.

        Args:
            target_path: Path to open for writing.

        Returns:
            FlextCore.Result containing file handle or error.

        """
        try:
            # Validate parent directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)

            file_handle = target_path.open(
                "w", encoding=FlextCore.Constants.Mixins.DEFAULT_ENCODING
            )
            return FlextCore.Result[TextIO].ok(data=file_handle)
        except Exception as e:
            return FlextCore.Result[TextIO].fail(
                f"Failed to open file for writing: {e}"
            )

    @classmethod
    def _write_yaml_content(
        cls, file_handle: TextIO, config: FlextCore.Types.Dict
    ) -> FlextCore.Result[bool]:
        """Write YAML content to file handle.

        Args:
            file_handle: Open file handle for writing.
            config: Configuration dictionary to write.

        Returns:
            FlextCore.Result indicating write success.

        """
        try:
            # TYPE SAFETY: Ensure file_handle is writable and config is properly typed
            if not hasattr(file_handle, "write"):
                return FlextCore.Result[bool].fail(
                    "Invalid file handle: missing write method"
                )

            # MONADIC PATTERN: Safe YAML conversion with proper type casting
            yaml_data: FlextCore.Types.Dict = dict[str, object](
                config
            )  # Type-safe conversion

            # DOMAIN-SPECIFIC: YAML writing with Meltano formatting preferences
            yaml.dump(yaml_data, file_handle, default_flow_style=False, indent=2)
            return FlextCore.Result[bool].ok(data=True)
        except Exception as e:
            return FlextCore.Result[bool].fail(f"Failed to write YAML content: {e}")

    @classmethod
    def _close_file_handle(cls, file_handle: TextIO) -> FlextCore.Result[None]:
        """Close file handle safely.

        Args:
            file_handle: File handle to close.

        Returns:
            FlextCore.Result indicating close operation result.

        """
        try:
            if hasattr(file_handle, "close"):
                file_handle.close()
            return FlextCore.Result.ok(data=None)
        except Exception as e:
            # Log but don't fail on close errors
            FlextCore.Logger(__name__).warning(f"Error closing file handle: {e}")
            return FlextCore.Result.ok(data=None)

    # NOTE: create_temp_directory moved to FlextMeltanoFileManagers (proper domain responsibility)

    @classmethod
    def create_plugin_config_dict(
        cls,
        name: str,
        plugin_type: str = "extractor",
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Create MELTANO-SPECIFIC plugin config using FlextCore.Utilities foundation."""
        try:
            # Delegate to FlextCore.Utilities for ALL text processing
            safe_name = FlextCore.Utilities.TextProcessor.safe_string(name, name)
            safe_namespace = FlextCore.Utilities.TextProcessor.safe_string(
                namespace, namespace
            )

            # DOMAIN-SPECIFIC: Meltano plugin-specific defaults
            safe_pip_url = FlextCore.Utilities.TextProcessor.safe_string(
                pip_url, pip_url
            )
            safe_executable = FlextCore.Utilities.TextProcessor.safe_string(
                executable, executable
            )

            config_dict: FlextCore.Types.Dict = {
                "name": safe_name,
                "namespace": safe_namespace,
                "pip_url": safe_pip_url,
                "executable": safe_executable,
                "type": plugin_type or "extractor",
                "settings": {},
                "config": {},
                "metadata": {
                    "created_by": FlextMeltanoConstants.Meltano.METADATA_CREATED_BY,
                    "created_at": FlextCore.Utilities.Generators.generate_iso_timestamp(),  # NO DUPLICATION
                },
            }
            return FlextCore.Result[FlextCore.Types.Dict].ok(data=config_dict)
        except Exception as e:  # pragma: no cover
            error_msg = f"Failed to create plugin config: {e}"
            FlextCore.Logger(__name__).exception(error_msg)
            return FlextCore.Result[FlextCore.Types.Dict].fail(error_msg)

    @classmethod
    def load_yaml_config(cls, path: Path) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Load YAML config using monadic composition with resource management.

        Uses FlextCore.Result monadic patterns to chain file loading, validation,
        and type conversion with automatic error propagation and resource cleanup.
        ZERO DUPLICATION: Delegates to FlextMeltanoFileManagers as SOURCE OF TRUTH.

        Args:
            path: Path to YAML configuration file.

        Returns:
            FlextCore.Result containing loaded configuration dictionary.

        """

        # MONADIC COMPOSITION: Chain file operations with automatic error handling
        def convert_to_dict(
            config_dict: object,
        ) -> FlextCore.Types.Dict:
            """Type-safe conversion from ConfigDict to FlextCore.Types.Dict."""
            # ConfigDict is compatible with dict["str", "JsonValue"] but MyPy needs explicit conversion
            return (
                dict[str, object](config_dict) if isinstance(config_dict, dict) else {}
            )

        return (
            FlextCore.Result[Path]
            .ok(path)
            .flat_map(cls._validate_yaml_path)
            .flat_map(FlextMeltanoFileManagers.load_yaml_config)
            .map(convert_to_dict)  # Type-safe conversion to FlextCore.Types.Dict
            .with_context(
                lambda error: f"Loading YAML config from {path}: {error}"
            )  # Add error context
        )

    @classmethod
    def _validate_yaml_path(cls, path: Path) -> FlextCore.Result[Path]:
        """Validate YAML file path before loading.

        Args:
            path: Path to validate.

        Returns:
            FlextCore.Result containing validated path or error.

        """
        if not path.exists():
            return FlextCore.Result.fail(f"YAML config file not found: {path}")
        if not path.is_file():
            return FlextCore.Result.fail(f"Path is not a file: {path}")
        if path.suffix.lower() not in {
            FlextCore.Constants.Platform.EXT_YML,
            FlextCore.Constants.Platform.EXT_YAML,
        }:
            return FlextCore.Result.fail(f"File is not a YAML file: {path}")

        return FlextCore.Result.ok(data=path)

    def directory_exists(self, path: Path) -> FlextCore.Result[bool]:
        """Check if directory exists."""
        try:
            return FlextCore.Result.ok(path.exists() and path.is_dir())
        except (OSError, ValueError) as e:
            return FlextCore.Result.fail(f"Failed to check directory existence: {e}")

    def validate_project_structure(self, project_path: Path) -> FlextCore.Result[bool]:
        """Validate Meltano project structure."""
        try:
            if not project_path.exists():
                return FlextCore.Result.fail(
                    f"Project path does not exist: {project_path}"
                )

            meltano_yml = project_path / "meltano.yml"
            if not meltano_yml.exists():
                return FlextCore.Result.fail(
                    f"Meltano config file not found: {meltano_yml}"
                )

            return FlextCore.Result.ok(True)
        except (OSError, ValueError) as e:
            return FlextCore.Result.fail(f"Failed to validate project structure: {e}")

    def create_project_file(
        self, file_path: Path, content: str | FlextCore.Types.Dict
    ) -> FlextCore.Result[Path]:
        """Create a project file with content."""
        if not isinstance(content, (str, dict)):
            return FlextCore.Result.fail("Invalid content type: must be string or dict")

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, dict):
                yaml_content = yaml.dump(content, default_flow_style=False, indent=2)
                file_path.write_text(yaml_content, encoding="utf-8")
            else:
                file_path.write_text(content, encoding="utf-8")
            return FlextCore.Result.ok(file_path)
        except (OSError, ValueError, yaml.YAMLError) as e:
            return FlextCore.Result.fail(f"Failed to create project file: {e}")

    def load_yaml_file(self, file_path: Path) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Load YAML file."""
        return self.load_yaml_config(file_path)

    def save_yaml_file(
        self, file_path: Path, content: FlextCore.Types.Dict
    ) -> FlextCore.Result[Path]:
        """Save content to YAML file."""
        try:
            self.write_meltano_yml(content, file_path)
            return FlextCore.Result.ok(file_path)
        except (OSError, ValueError, yaml.YAMLError) as e:
            return FlextCore.Result.fail(f"Failed to save YAML file: {e}")


__all__ = ["FlextMeltanoUtilities"]
