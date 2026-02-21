"""FLEXT Meltano File Management - Enterprise ELT file operations.

This module provides file management utilities for Meltano ELT operations
following FLEXT architectural patterns with proper error handling.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import yaml
from flext_core import (
    FlextLogger,
    FlextResult as r,
    u,
)

from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes as t

m = FlextMeltanoModels

logger = FlextLogger(__name__)


class FlextMeltanoFileManagers:
    """DOMAIN-SPECIFIC Meltano file managers using flext-core as SOURCE OF TRUTH.

    Contains ONLY Meltano-specific file operations that cannot be generalized to flext-core.
    ALL general file operations MUST use u (FlextUtilities) directly.

    ZERO DUPLICATION PRINCIPLE:
    - u (FlextUtilities) is SOURCE OF TRUTH for general file operations
    - Contains ONLY Meltano-specific operations (YAML configs, project structure)
    - Uses tempfile standard library with u (FlextUtilities) validation
    """

    @classmethod
    def create_temp_directory(cls, prefix: str = "flext_meltano_") -> r[Path]:
        """Create temporary directory using DSL patterns.

        DSL: Uses u.try_ for unified error handling.

        Returns:
        FlextResult containing the created temporary directory path.

        """
        logger = FlextLogger(__name__)

        # DSL: Use u.try_ for unified error handling
        def _create() -> r[Path]:
            # Use direct tempfile.mkdtemp for temporary directory creation
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
            logger.info("Created temporary directory: %s", temp_dir)
            return r[Path].ok(temp_dir)

        result = u.try_(
            _create,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
            default=None,
        )
        if result is None:
            error_msg = "Failed to create temp directory"
            logger.error(error_msg)
            return r[Path].fail(error_msg)
        return result

    @classmethod
    def save_yaml_config(
        cls,
        config: t.MeltanoCore.FileConfigDict,
        file_path: Path,
    ) -> r[bool]:
        """Save YAML config using DSL patterns.

        DSL: Uses u.try_ for unified error handling.

        Returns:
        FlextResult indicating success or failure of the save operation.

        """

        # DSL: Use u.try_ for unified error handling
        def _save() -> r[bool]:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # Write YAML with proper encoding
            with file_path.open("w", encoding=c.Utilities.DEFAULT_ENCODING) as f:
                yaml.dump(
                    config,
                    f,
                    indent=2,
                    default_flow_style=False,
                    sort_keys=False,
                )
            return r[bool].ok(value=True)

        result = u.try_(
            _save,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
            default=None,
        )
        if result is None:
            return r[bool].fail("Failed to save YAML config")
        return result

    @classmethod
    def load_yaml_config(cls, file_path: Path) -> r[t.MeltanoCore.FileConfigDict]:
        """Load YAML config using DSL patterns + direct YAML.

        ZERO DUPLICATION: Uses u.Guards.is_string_non_empty for validation.
        DSL: Uses u.try_ for unified error handling.

        Returns:
        r containing the loaded YAML configuration.

        """

        # DSL: Use u.try_ for unified error handling
        def _load() -> r[t.MeltanoCore.FileConfigDict]:
            # Basic path validation using flext-core utilities
            if not u.Guards.is_string_non_empty(str(file_path)):
                return r[t.MeltanoCore.FileConfigDict].fail(
                    f"Invalid YAML file path: {file_path}",
                )

            if not file_path.exists():
                return r[t.MeltanoCore.FileConfigDict].fail(
                    f"YAML file not found: {file_path}",
                )

            with file_path.open("r", encoding=c.Utilities.DEFAULT_ENCODING) as f:
                config_data: object = yaml.safe_load(f)

            # DSL: Use u.when for conditional handling
            if config_data is None:
                return r[t.MeltanoCore.FileConfigDict].ok({})

            validated_config = m.Meltano.ConfigMappingPayload.model_validate(
                {"values": config_data},
            ).values
            return r[t.MeltanoCore.FileConfigDict].ok(validated_config)

        result = u.try_(
            _load,
            catch=(
                yaml.YAMLError,
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
            ),
            default=None,
        )
        # Type narrowing: result is object | None
        if result is None:
            return r[t.MeltanoCore.FileConfigDict].fail("Failed to load YAML config")
        return result

    @classmethod
    def validate_yaml_file(cls, file_path: Path) -> r[bool]:
        """Validate YAML using DSL patterns + direct YAML parsing.

        ZERO DUPLICATION: Uses u.Guards.is_string_non_empty for validation.
        DSL: Uses u.try_ for unified error handling.

        Returns:
        r indicating whether the YAML file is valid.

        """

        # DSL: Use u.try_ for unified error handling
        def _validate() -> r[bool]:
            # Basic path validation using flext-core utilities
            if not u.Guards.is_string_non_empty(str(file_path)):
                return r[bool].fail(f"Invalid YAML file path: {file_path}")

            if not file_path.exists():
                return r[bool].fail(f"YAML file not found: {file_path}")

            with file_path.open("r", encoding=c.Utilities.DEFAULT_ENCODING) as f:
                yaml.safe_load(f)  # This will raise an exception if invalid YAML

            return r[bool].ok(value=True)

        # DSL: Handle YAML-specific errors separately
        try:
            return _validate()
        except yaml.YAMLError as e:
            return r[bool].fail(f"Invalid YAML syntax: {e}")
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Failed to validate YAML: {e}")

    @classmethod
    def create_directory_structure(
        cls,
        base_path: Path,
        directories: list[str],
    ) -> r[dict[str, str]]:
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

            return r[dict[str, str]].ok(created_paths)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, str]].fail(
                f"Failed to create directories: {e}",
            )

    @classmethod
    def setup_project_structure(
        cls,
        project_root: Path,
        _project_name: str,
    ) -> r[t.MeltanoCore.PathDict]:
        """Setup Meltano project structure using direct implementation.

        Returns:
        r containing the project structure information.

        """
        try:
            # Define Meltano directory structure
            directories = [
                "extract",
                "load",
                "transform",
                "analyze",
                "transform/models",
                "transform/tests",
                "transform/data",
            ]

            # Create directory structure
            created_paths: dict[str, Path | str] = {}
            for directory in directories:
                dir_path = project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = dir_path

            # Create essential config files
            configs = {
                c.Meltano.Paths.MELTANO_PROJECT_FILE: {
                    "version": 1,
                    "project_id": "project_name",
                    "project_name": "project_name",
                    "plugins": {
                        "extractors": [],
                        "loaders": [],
                        "transformers": [],
                    },
                },
                "transform/dbt_project.yml": {
                    "name": "project_name",
                    "version": "1.0.0",
                    "profile": "project_name",
                    "model-paths": ["models"],
                    "test-paths": ["tests"],
                },
            }

            for filename, config_data in configs.items():
                config_path = project_root / filename
                validated_config = m.Meltano.ConfigMappingPayload.model_validate(
                    {"values": config_data},
                ).values
                save_result = cls.save_yaml_config(
                    validated_config,
                    config_path,
                )
                if save_result.is_success:
                    created_paths[filename.replace("/", "_")] = str(config_path)

            # Add project root
            created_paths["project_root"] = project_root
            return r[t.MeltanoCore.PathDict].ok(created_paths)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.MeltanoCore.PathDict].fail(
                f"Failed to setup project structure: {e}",
            )

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
    def validate_project_structure(cls, project_root: Path) -> r[bool]:
        """Validate Meltano project structure.

        Returns:
        FlextResult indicating whether the project structure is valid.

        """
        try:
            # Check if path exists and is directory
            if not project_root.exists():
                return r[bool].fail(f"Project path does not exist: {project_root}")

            if not project_root.is_dir():
                return r[bool].fail(f"Project path is not a directory: {project_root}")

            # Check for required pipeline files
            pipeline_config = project_root / "pipeline.yml"
            if not pipeline_config.exists():
                return r[bool].fail(f"pipeline.yml not found in {project_root}")

            return r[bool].ok(value=True)
        except (ValueError, TypeError, OSError) as e:
            return r[bool].fail(f"Failed to validate project structure: {e}")


__all__ = ["FlextMeltanoFileManagers"]
