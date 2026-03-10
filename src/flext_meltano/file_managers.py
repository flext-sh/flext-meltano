"""FLEXT Meltano File Management - Enterprise ELT file operations.

This module provides file management utilities for Meltano ELT operations
following FLEXT architectural patterns with proper error handling.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Mapping
from pathlib import Path

import yaml
from flext_core import FlextLogger, r

from flext_meltano import c, m, t, u


class FlextMeltanoFileManagers:
    """DOMAIN-SPECIFIC Meltano file managers using flext-core as SOURCE OF TRUTH.

    Contains ONLY Meltano-specific file operations that cannot be generalized to flext-core.
    ALL general file operations MUST use u (FlextUtilities) directly.

    ZERO DUPLICATION PRINCIPLE:
    - u (FlextUtilities) is SOURCE OF TRUTH for general file operations
    - Contains ONLY Meltano-specific operations (YAML configs, project structure)
    - Uses tempfile standard library with u (FlextUtilities) validation
    """

    logger = FlextLogger(__name__)

    @classmethod
    def cleanup_temp_directory(cls, temp_path: Path) -> r[bool]:
        """Cleanup temporary directory using direct implementation.

        Returns:
        r indicating success or failure of the cleanup operation.

        """
        try:
            if temp_path.exists() and temp_path.is_dir():
                shutil.rmtree(temp_path)
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Failed to cleanup temp directory: {e}")

    @classmethod
    def create_directory_structure(
        cls, base_path: Path, directories: list[str]
    ) -> r[Mapping[str, str]]:
        """Create directory structure using direct pathlib implementation.

        Returns:
        r containing the created directory structure information.

        """
        try:
            created_paths: dict[str, str] = {}
            for directory in directories:
                dir_path = base_path / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = str(dir_path)
            return r[Mapping[str, str]].ok(created_paths)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Mapping[str, str]].fail(f"Failed to create directories: {e}")

    @classmethod
    def create_temp_directory(cls, prefix: str = "flext_meltano_") -> r[Path]:
        """Create temporary directory using DSL patterns.

        DSL: Uses u.try_ for unified error handling.

        Returns:
        FlextResult containing the created temporary directory path.

        """

        def _create() -> Path:
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
            FlextMeltanoFileManagers.logger.info(
                "Created temporary directory: %s", temp_dir
            )
            return temp_dir

        return u.try_(
            _create,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to create temp directory: {e}")

    @classmethod
    def load_yaml_config(cls, file_path: Path) -> r[t.Meltano.FileConfigDict]:
        """Load YAML config using DSL patterns + direct YAML.

        ZERO DUPLICATION: Uses u.Guards.is_string_non_empty for validation.
        DSL: Uses u.try_ for unified error handling.

        Returns:
        r containing the loaded YAML configuration.

        """

        def _load() -> t.Meltano.FileConfigDict:
            if not u.Guards.is_string_non_empty(str(file_path)):
                msg = f"Invalid YAML file path: {file_path}"
                raise ValueError(
                    msg,
                )
            if not file_path.exists():
                msg = f"YAML file not found: {file_path}"
                raise FileNotFoundError(
                    msg,
                )
            with file_path.open("r", encoding=c.Utilities.DEFAULT_ENCODING) as f:
                config_data: t.ContainerValue = yaml.safe_load(f)
            if config_data is None:
                return {}
            return m.Meltano.ConfigMappingPayload.model_validate({
                "values": config_data
            }).values

        return u.try_(
            _load,
            catch=(
                yaml.YAMLError,
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
            ),
        ).map_error(lambda e: f"Failed to load YAML config: {e}")

    @classmethod
    def save_yaml_config(
        cls, config: t.Meltano.FileConfigDict, file_path: Path
    ) -> r[bool]:
        """Save YAML config using DSL patterns.

        DSL: Uses u.try_ for unified error handling.

        Returns:
        FlextResult indicating success or failure of the save operation.

        """

        def _save() -> bool:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open("w", encoding=c.Utilities.DEFAULT_ENCODING) as f:
                yaml.dump(
                    config, f, indent=2, default_flow_style=False, sort_keys=False
                )
            return True

        return u.try_(
            _save,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to save YAML config: {e}")

    @classmethod
    def setup_project_structure(
        cls, project_root: Path, _project_name: str
    ) -> r[t.Meltano.PathDict]:
        """Setup Meltano project structure using direct implementation.

        Returns:
        r containing the project structure information.

        """
        try:
            directories = [
                "extract",
                "load",
                "transform",
                "analyze",
                "transform/models",
                "transform/tests",
                "transform/data",
            ]
            created_paths: dict[str, Path | str] = {}
            for directory in directories:
                dir_path = project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = dir_path
            meltano_config: t.Meltano.FileConfigDict = {
                "version": 1,
                "project_id": "project_name",
                "project_name": "project_name",
                "plugins": {
                    "extractors": list[str](),
                    "loaders": list[str](),
                    "transformers": list[str](),
                },
            }
            dbt_project_config: t.Meltano.FileConfigDict = {
                "name": "project_name",
                "version": "1.0.0",
                "profile": "project_name",
                "model-paths": ["models"],
                "test-paths": ["tests"],
            }
            configs: dict[str, t.Meltano.FileConfigDict] = {
                c.Meltano.Paths.MELTANO_PROJECT_FILE: meltano_config,
                "transform/dbt_project.yml": dbt_project_config,
            }
            for filename, config_data in configs.items():
                config_path = project_root / filename
                validated_config = m.Meltano.ConfigMappingPayload.model_validate({
                    "values": config_data
                }).values
                save_result = cls.save_yaml_config(validated_config, config_path)
                if save_result.is_success:
                    created_paths[filename.replace("/", "_")] = str(config_path)
            created_paths["project_root"] = project_root
            return r[t.Meltano.PathDict].ok(created_paths)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.PathDict].fail(f"Failed to setup project structure: {e}")

    @classmethod
    def validate_project_structure(cls, project_root: Path) -> r[bool]:
        """Validate Meltano project structure.

        Returns:
        FlextResult indicating whether the project structure is valid.

        """
        try:
            if not project_root.exists():
                return r[bool].fail(f"Project path does not exist: {project_root}")
            if not project_root.is_dir():
                return r[bool].fail(f"Project path is not a directory: {project_root}")
            pipeline_config = project_root / "pipeline.yml"
            if not pipeline_config.exists():
                return r[bool].fail(f"pipeline.yml not found in {project_root}")
            return r[bool].ok(value=True)
        except (ValueError, TypeError, OSError) as e:
            return r[bool].fail(f"Failed to validate project structure: {e}")

    @classmethod
    def validate_yaml_file(cls, file_path: Path) -> r[bool]:
        """Validate YAML using DSL patterns + direct YAML parsing.

        ZERO DUPLICATION: Uses u.Guards.is_string_non_empty for validation.
        DSL: Uses u.try_ for unified error handling.

        Returns:
        r indicating whether the YAML file is valid.

        """

        def _validate() -> r[bool]:
            if not u.Guards.is_string_non_empty(str(file_path)):
                return r[bool].fail(f"Invalid YAML file path: {file_path}")
            if not file_path.exists():
                return r[bool].fail(f"YAML file not found: {file_path}")
            with file_path.open("r", encoding=c.Utilities.DEFAULT_ENCODING) as f:
                yaml.safe_load(f)
            return r[bool].ok(value=True)

        try:
            return _validate()
        except yaml.YAMLError as e:
            return r[bool].fail(f"Invalid YAML syntax: {e}")
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Failed to validate YAML: {e}")


__all__ = ["FlextMeltanoFileManagers"]
