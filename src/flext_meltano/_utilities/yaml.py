"""FLEXT Meltano Utilities - YAML file operations."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import TextIO

import yaml
from flext_cli import FlextCliUtilities, r
from flext_core import FlextLogger

from flext_meltano import FlextMeltanoFileManagers, c, m, t


class FlextMeltanoUtilitiesYaml:
    """YAML loading, validation, and writing utilities for Meltano configs."""

    @classmethod
    def _close_file_handle(cls, file_handle: TextIO) -> r[None]:
        """Close file handle safely."""
        try:
            file_handle.close()
            return r[None].ok(None)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as err:
            _ = FlextLogger(__name__).warning(f"Error closing file handle: {err}")
            return r[None].ok(None)

    @classmethod
    def _open_yaml_file_for_writing(cls, target_path: Path) -> r[TextIO]:
        """Open YAML file for writing with validation."""

        def open_file() -> TextIO:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            return target_path.open("w", encoding=c.DEFAULT_ENCODING)

        return FlextCliUtilities.try_(
            open_file,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to open file for writing: {e}")

    @classmethod
    def _validate_yaml_path(cls, path: Path) -> r[Path]:
        """Validate YAML file path before loading."""
        if not path.exists():
            return r[Path].fail(f"File does not exist: {path}")
        if not path.is_file():
            return r[Path].fail(f"Path is not a file: {path}")
        suffix = FlextCliUtilities.normalize(path.suffix, case="lower")
        if suffix not in {".yml", ".yaml"}:
            return r[Path].fail(f"File is not a YAML file: {path}")
        return r[Path].ok(path)

    @classmethod
    def _write_yaml_content(
        cls,
        file_handle: TextIO,
        config: t.Meltano.MeltanoConfigDict,
    ) -> r[bool]:
        """Write YAML content to file handle."""
        if getattr(file_handle, "write", None) is None:
            return r[bool].fail("Invalid file handle: missing write method")
        try:
            yaml.dump(
                config,
                file_handle,
                Dumper=yaml.Dumper,
                default_flow_style=False,
                indent=2,
                allow_unicode=True,
            )
            return r[bool].ok(value=True)
        except (yaml.YAMLError, ValueError, TypeError, AttributeError):
            return r[bool].fail(
                "Failed to write YAML content: non-serializable t.NormalizedValue",
            )

    @classmethod
    def load_yaml_config(cls, path: Path) -> r[t.Meltano.MeltanoConfigDict]:
        """Load YAML config using monadic composition with resource management.

        Delegates to FlextMeltanoFileManagers as SOURCE OF TRUTH.

        Args:
        path: Path to YAML configuration file.

        Returns:
        r containing loaded configuration dictionary.

        """

        def convert_to_dict(
            config_dict: t.Meltano.FileConfigDict,
        ) -> t.Meltano.MeltanoConfigDict:
            normalized_values = m.Meltano.ConfigMappingPayload.model_validate({
                "values": config_dict,
            }).values
            converted: t.MutableContainerMapping = {}
            for key, value in normalized_values.items():
                if value is None:
                    continue
                if isinstance(value, Mapping):
                    converted[str(key)] = {
                        str(map_key): map_value
                        for map_key, map_value in value.items()
                        if map_value is not None
                    }
                elif isinstance(value, list):
                    converted[str(key)] = [item for item in value if item is not None]
                else:
                    converted[str(key)] = value
            return converted

        validated_path: r[Path] = r[Path].ok(path).flat_map(cls._validate_yaml_path)
        loaded: r[t.Meltano.MeltanoConfigDict] = validated_path.flat_map(
            FlextMeltanoFileManagers.load_yaml_config
        )
        result = loaded.map(convert_to_dict)
        return (
            result
            if result.is_success
            else r[t.Meltano.MeltanoConfigDict].fail(
                result.error or f"Loading YAML config from {path} failed",
            )
        )

    @classmethod
    def load_yaml_file(cls, file_path: Path) -> r[t.Meltano.MeltanoConfigDict]:
        """Load YAML file."""
        return cls.load_yaml_config(file_path)

    @classmethod
    def save_yaml_file(
        cls,
        file_path: Path,
        content: t.Meltano.MeltanoConfigDict,
    ) -> r[Path]:
        """Save content to YAML file."""
        result = cls.write_meltano_yml(content, file_path)
        return (
            r[Path].ok(file_path)
            if result.is_success
            else r[Path].fail(result.error or "Failed to save YAML file")
        )

    @classmethod
    def write_meltano_yml(
        cls,
        config: t.Meltano.MeltanoConfigDict,
        target_path: Path,
    ) -> r[bool]:
        """Write MELTANO-SPECIFIC YAML configuration using monadic resource management."""

        def write_operation(_unused_value: None, file_handle: TextIO, /) -> r[bool]:
            return cls._write_yaml_content(file_handle, config)

        def cleanup_file_handle(file_handle: TextIO) -> None:
            try:
                file_handle.close()
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
            ) as err:
                _ = FlextLogger(__name__).warning(
                    f"Error closing file handle: {err}",
                )

        try:
            open_result = cls._open_yaml_file_for_writing(target_path)
            if open_result.is_failure:
                filename = c.Meltano.Paths.MELTANO_PROJECT_FILE
                return r[bool].fail(f"Writing {filename}: {open_result.error}")
            resource = open_result.value
            try:
                return write_operation(None, resource)
            finally:
                cleanup_file_handle(resource)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as err:
            filename = c.Meltano.Paths.MELTANO_PROJECT_FILE
            return r[bool].fail(f"Writing {filename}: {err}")
