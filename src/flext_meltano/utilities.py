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
    FlextExceptions,
    FlextLogger,
    FlextResult,
    FlextUtilities,
    u,
)

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.file_managers import FlextMeltanoFileManagers

# Import aliases for simplified usage
r = FlextResult
e = FlextExceptions
c_base = FlextConstants
c = FlextMeltanoConstants


class FlextMeltanoUtilities(FlextUtilities):
    """DOMAIN-SPECIFIC Meltano utilities - ONLY what cannot be generalized to flext-core.

    Inherits from FlextUtilities to avoid duplication and ensure consistency.
    """

    @classmethod
    def create_meltano_config_dict(  # noqa: PLR0913, PLR0917
        cls,
        project_id: str,
        project_name: str = "",
        version: str | None = None,
        default_environment: str | None = None,
        plugins: dict[str, object] | None = None,
        environments: dict[str, object] | None = None,
    ) -> r[dict[str, object]]:
        """Create MELTANO-SPECIFIC configuration dictionary - DOMAIN-SPECIFIC ONLY."""
        logger = FlextLogger(__name__)
        try:
            # Delegate to u for text processing - use TextProcessor for validation
            safe_project_id = u.TextProcessor.safe_string(project_id)
            safe_project_name = (
                u.TextProcessor.safe_string(project_name)
                if project_name
                else safe_project_id
            )

            # DOMAIN-SPECIFIC: Meltano configuration structure
            config_dict: dict[str, object] = {
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
                env_result = u.process(
                    c.Metadata.DEFAULT_ENVIRONMENTS,
                    lambda env: {"name": env},
                )
                config_dict["environments"] = (
                    env_result.value if env_result.is_success else []
                )

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
                "created_by": c.Metadata.CREATED_BY,
                "created_at": u.Generators.generate_iso_timestamp(),
                "flext_version": c.FLEXT_MELTANO_VERSION,
            }
            return r[dict[str, object]].ok(config_dict)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:  # pragma: no cover
            error_msg = f"Failed to create Meltano config dict[str, object]: {e}"
            logger.exception(error_msg)
            return r[dict[str, object]].fail(error_msg)

    @classmethod
    def write_meltano_yml(
        cls,
        config: dict[str, object],
        target_path: Path,
    ) -> r[bool]:
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
        # with_resource expects operation(value, resource) -> r[U]

        def write_operation(
            _unused_value: object,  # Required by with_resource signature
            file_handle: TextIO,
            /,
        ) -> r[bool]:
            return cls._write_yaml_content(file_handle, config)

        # Cleanup function should be Callable[[TResource], None] | None
        def cleanup_file_handle(file_handle: TextIO) -> None:
            try:
                if hasattr(file_handle, "close"):
                    file_handle.close()
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextLogger(__name__).warning(f"Error closing file handle: {e}")

        def resource_factory() -> TextIO:
            result: r[TextIO] = cls._open_yaml_file_for_writing(target_path)
            if result.is_failure:
                error_msg = f"Failed to open file: {result.error}"
                raise RuntimeError(error_msg)
            return result.value

        try:
            resource = resource_factory()
            try:
                return write_operation(None, resource)
            finally:
                cleanup_file_handle(resource)
        except Exception as e:
            return r[bool].fail(f"Writing {c.Paths.MELTANO_PROJECT_FILE}: {e}")

    @classmethod
    def _open_yaml_file_for_writing(cls, target_path: Path) -> r[TextIO]:
        """Open YAML file for writing with validation.

        Args:
        target_path: Path to open for writing.

        Returns:
        FlextResult containing file handle or error.

        """
        try:
            # Validate parent directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)

            file_handle = target_path.open("w", encoding=c_base.Mixins.DEFAULT_ENCODING)
            return r[TextIO].ok(file_handle)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[TextIO].fail(f"Failed to open file for writing: {e}")

    @classmethod
    def _write_yaml_content(
        cls, file_handle: TextIO, config: dict[str, object]
    ) -> r[bool]:
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
                return r[bool].fail("Invalid file handle: missing write method")

            # MONADIC PATTERN: Safe YAML conversion with proper type casting
            yaml_data: dict[str, object] = dict[str, object](
                config
            )  # Type-safe conversion

            # DOMAIN-SPECIFIC: YAML writing with Meltano formatting preferences
            yaml.dump(yaml_data, file_handle, default_flow_style=False, indent=2)
            return r[bool].ok(True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Failed to write YAML content: {e}")

    @classmethod
    def _close_file_handle(cls, file_handle: TextIO) -> r[None]:
        """Close file handle safely.

        Args:
        file_handle: File handle to close.

        Returns:
        FlextResult indicating close operation result.

        """
        try:
            if hasattr(file_handle, "close"):
                file_handle.close()
            return r.ok(None)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            # Log but don't fail on close errors
            FlextLogger(__name__).warning(f"Error closing file handle: {e}")
            return r.ok(None)

    # Note: create_temp_directory moved to FlextMeltanoFileManagers (proper domain responsibility)

    @classmethod
    def create_plugin_config_dict(
        cls,
        name: str,
        plugin_type: str = "extractor",
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> r[dict[str, object]]:
        """Create MELTANO-SPECIFIC plugin config using u foundation."""
        try:
            # Delegate to u for ALL text processing - use TextProcessor for validation
            safe_name = u.TextProcessor.safe_string(name)
            safe_namespace = u.TextProcessor.safe_string(namespace) if namespace else ""
            safe_pip_url = u.TextProcessor.safe_string(pip_url) if pip_url else ""
            safe_executable = (
                u.TextProcessor.safe_string(executable) if executable else ""
            )

            config_dict: dict[str, object] = {
                "name": safe_name,
                "namespace": safe_namespace,
                "pip_url": safe_pip_url,
                "executable": safe_executable,
                "type": plugin_type or "extractor",
                "settings": {},
                "config": {},
                "metadata": {
                    "created_by": c.Metadata.CREATED_BY,
                    "created_at": u.Generators.generate_iso_timestamp(),
                },
            }
            return r[dict[str, object]].ok(config_dict)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:  # pragma: no cover
            error_msg = f"Failed to create plugin config: {e}"
            FlextLogger(__name__).exception(error_msg)
            return r[dict[str, object]].fail(error_msg)

    @classmethod
    def load_yaml_config(cls, path: Path) -> r[dict[str, object]]:
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
        ) -> dict[str, object]:
            """Type-safe conversion from ConfigDict to dict[str, object]."""
            # ConfigDict is compatible with dict["str", "JsonValue"] but MyPy needs explicit conversion
            return u.ensure(config_dict, dict, default={})

        result = (
            r[Path]
            .ok(path)
            .flat_map(cls._validate_yaml_path)
            .flat_map(FlextMeltanoFileManagers.load_yaml_config)
            .map(convert_to_dict)  # Type-safe conversion to dict[str, object]
        )
        if result.is_failure:
            return r[dict[str, object]].fail(
                f"Loading YAML config from {path}: {result.error}"
            )
        return result

    @classmethod
    def _validate_yaml_path(cls, path: Path) -> r[Path]:
        """Validate YAML file path before loading.

        Args:
        path: Path to validate.

        Returns:
        FlextResult containing validated path or error.

        """
        if not path.exists():
            return r.fail(f"YAML config file not found: {path}")
        if not path.is_file():
            return r.fail(f"Path is not a file: {path}")
        suffix_lower = u.normalize(path.suffix, case="lower")
        if suffix_lower not in {".yml", ".yaml"}:
            return r.fail(f"File is not a YAML file: {path}")

        return r.ok(path)

    @staticmethod
    def directory_exists(path: Path) -> r[bool]:
        """Check if directory exists."""
        try:
            return r.ok(path.exists() and path.is_dir())
        except (OSError, ValueError) as e:
            return r.fail(f"Failed to check directory existence: {e}")

    @staticmethod
    def validate_project_structure(project_path: Path) -> r[bool]:
        """Validate Meltano project structure."""
        try:
            if not project_path.exists():
                return r.fail(f"Project path does not exist: {project_path}")

            meltano_yml = project_path / "meltano.yml"
            if not meltano_yml.exists():
                return r.fail(f"Meltano config file not found: {meltano_yml}")

            return r.ok(True)
        except (OSError, ValueError) as e:
            return r.fail(f"Failed to validate project structure: {e}")

    @staticmethod
    def create_project_file(
        file_path: Path, content: str | dict[str, object]
    ) -> r[Path]:
        """Create a project file with content."""
        content_guard = u.guard(content, (str, dict), return_value=True)
        if content_guard is None:
            return r.fail("Invalid content type: must be string or dict")

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content_guard, dict):
                yaml_content = yaml.dump(
                    content_guard, default_flow_style=False, indent=2
                )
                file_path.write_text(yaml_content, encoding="utf-8")
            else:
                file_path.write_text(content_guard, encoding="utf-8")
            return r.ok(file_path)
        except (OSError, ValueError, yaml.YAMLError) as e:
            return r.fail(f"Failed to create project file: {e}")

    @classmethod
    def load_yaml_file(cls, file_path: Path) -> r[dict[str, object]]:
        """Load YAML file."""
        return cls.load_yaml_config(file_path)

    @classmethod
    def save_yaml_file(cls, file_path: Path, content: dict[str, object]) -> r[Path]:
        """Save content to YAML file."""
        try:
            cls.write_meltano_yml(content, file_path)
            return r.ok(file_path)
        except (OSError, ValueError, yaml.YAMLError) as e:
            return r.fail(f"Failed to save YAML file: {e}")


__all__ = ["FlextMeltanoUtilities"]
