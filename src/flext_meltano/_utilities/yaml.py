"""FLEXT Meltano Utilities - YAML file operations.

Pure helpers for YAML loading, saving, validation, and writing.
Services delegate to these helpers — never import from services/.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TextIO

from flext_cli import FlextCliUtilities, r, u as cli_u

from flext_core import FlextLogger
from flext_meltano import c, m, t


class FlextMeltanoUtilitiesYaml:
    """YAML loading, validation, and writing utilities for Meltano configs.

    All methods are pure helpers with no service-layer dependencies.
    """

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

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
        try:
            content = FlextCliUtilities.Cli.yaml_dump_str(config)
            file_handle.write(content)
            return r[bool].ok(value=True)
        except (ValueError, TypeError, AttributeError):
            return r[bool].fail(
                "Failed to write YAML content: non-serializable value",
            )

    # ------------------------------------------------------------------
    # Raw YAML I/O (SOURCE OF TRUTH for all YAML operations)
    # ------------------------------------------------------------------

    @classmethod
    def load_raw_yaml(cls, file_path: Path) -> r[t.Meltano.FileConfigDict]:
        """Load and validate a YAML file, returning normalized config dict.

        This is the canonical YAML loading implementation. Services delegate here.
        """
        try:
            if not cli_u.is_string_non_empty(str(file_path)):
                return r[t.Meltano.FileConfigDict].fail(
                    f"Failed to load YAML config: Invalid YAML file path: {file_path}",
                )
            if not file_path.exists():
                return r[t.Meltano.FileConfigDict].fail(
                    f"Failed to load YAML config: YAML file not found: {file_path}",
                )
            load_result = FlextCliUtilities.Cli.yaml_safe_load(file_path)
            if load_result.is_failure:
                return r[t.Meltano.FileConfigDict].fail(
                    f"Failed to load YAML config: {load_result.error}",
                )
            config_data = load_result.value
            raw_validated = m.Meltano.ConfigMappingPayload.model_validate({
                "values": config_data,
            }).values
            validated = _normalize_file_config(raw_validated)
            return r[t.Meltano.FileConfigDict].ok(validated)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:
            return r[t.Meltano.FileConfigDict].fail(f"Failed to load YAML config: {e}")

    @classmethod
    def save_raw_yaml(
        cls, config: t.Meltano.FileConfigDict, file_path: Path
    ) -> r[bool]:
        """Save config dict to a YAML file.

        This is the canonical YAML saving implementation. Services delegate here.
        """
        dump_result = FlextCliUtilities.Cli.yaml_dump(
            file_path, config, sort_keys=False, indent=2
        )
        if dump_result.is_failure:
            return r[bool].fail(
                f"Failed to save YAML config: {dump_result.error}",
            )
        return r[bool].ok(True)

    @classmethod
    def validate_yaml_syntax(cls, file_path: Path) -> r[bool]:
        """Validate YAML file syntax and existence."""
        if not cli_u.is_string_non_empty(str(file_path)):
            return r[bool].fail(f"Invalid YAML file path: {file_path}")
        if not file_path.exists():
            return r[bool].fail(f"YAML file not found: {file_path}")
        load_result = FlextCliUtilities.Cli.yaml_safe_load(file_path)
        if load_result.is_failure:
            return r[bool].fail(
                f"Invalid YAML syntax: {load_result.error}",
            )
        return r[bool].ok(value=True)

    # ------------------------------------------------------------------
    # Higher-level convenience (still pure, no service dependencies)
    # ------------------------------------------------------------------

    @classmethod
    def load_yaml_config(cls, path: Path) -> r[t.Meltano.MeltanoConfigDict]:
        """Load YAML config with path validation and type normalization."""

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
            cls.load_raw_yaml
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
        """Write Meltano YAML configuration with resource management."""

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
                return cls._write_yaml_content(resource, config)
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


def _normalize_file_config(
    raw: Mapping[
        str,
        t.Scalar | Sequence[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
    ],
) -> t.ContainerMapping:
    """Normalize raw config values into ContainerMapping."""
    normalized: t.MutableContainerMapping = {}
    for key, value in raw.items():
        if value is None or cli_u.is_scalar(value):
            normalized[key] = value
            continue
        if isinstance(value, list):
            normalized[key] = [item for item in value if item is not None]
            continue
        if isinstance(value, Mapping):
            nested: t.MutableConfigurationMapping = {}
            for nested_key, nested_value in value.items():
                if cli_u.is_scalar(nested_value):
                    nested[str(nested_key)] = nested_value
            normalized[key] = nested
    return normalized


__all__ = ["FlextMeltanoUtilitiesYaml"]
