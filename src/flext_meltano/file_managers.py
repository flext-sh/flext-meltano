"""FLEXT Meltano File Managers - DOMAIN-SPECIFIC file operations using flext-core as SOURCE OF TRUTH.

This module provides ONLY Meltano-specific file operations that cannot be generalized.
ALL general file operations MUST use FlextUtilities from flext-core directly.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import shutil
import tempfile
from pathlib import Path

import yaml
from flext_core import FlextLogger, FlextResult, FlextTypes, FlextUtilities

from flext_meltano.constants import FlextMeltanoConstants  # SOURCE OF TRUTH

# Type aliases (MyPy compatible)
ConfigDict = dict[
    str,
    str
    | int
    | FlextTypes.Core.StringList
    | dict[str, str | FlextTypes.Core.StringList],
]
PathDict = dict[str, Path | str]

logger = FlextLogger(__name__)


class FlextMeltanoFileManagers:
    """DOMAIN-SPECIFIC Meltano file managers using flext-core as SOURCE OF TRUTH.

    Contains ONLY Meltano-specific file operations that cannot be generalized to flext-core.
    ALL general file operations MUST use FlextUtilities from flext-core directly.

    ZERO DUPLICATION PRINCIPLE:
    - FlextUtilities.Files is SOURCE OF TRUTH for general file operations
    - Contains ONLY Meltano-specific operations (YAML configs, project structure)
    - Uses tempfile standard library with FlextUtilities validation
    """

    @classmethod
    def create_temp_directory(
        cls, prefix: str = "flext_meltano_", *, meltano_structure: bool = False
    ) -> FlextResult[Path]:
        """Create temporary directory with optional Meltano structure.

        CONSOLIDATED: Single method for temp directory creation with optional Meltano-specific structure.
        ZERO DUPLICATION: Uses tempfile standard library + FlextUtilities validation.
        """
        try:
            # Use Python tempfile standard library for temp directory creation
            temp_dir_str = tempfile.mkdtemp(prefix=prefix)
            temp_dir = Path(temp_dir_str)

            # Delegate to FlextUtilities.EnvironmentUtils for path validation - NO DUPLICATION
            if not FlextUtilities.EnvironmentUtils.is_valid_path(str(temp_dir)):
                return FlextResult[Path].fail(
                    f"Invalid temp directory path: {temp_dir}"
                )

            # Add MELTANO-SPECIFIC directory structure if requested (DOMAIN-SPECIFIC)
            if meltano_structure:
                meltano_dirs = [".meltano", "extract", "load", "transform"]
                for dir_name in meltano_dirs:
                    (temp_dir / dir_name).mkdir(exist_ok=True)

            logger.info(
                "Created temp directory",
                extra={"path": str(temp_dir), "meltano_structure": meltano_structure},
            )
            return FlextResult[Path].ok(temp_dir)
        except Exception as e:
            error_msg = f"Failed to create temp directory: {e}"
            logger.exception(error_msg)
            return FlextResult[Path].fail(error_msg)

    @classmethod
    def save_yaml_config(cls, config: ConfigDict, file_path: Path) -> FlextResult[bool]:
        """Save YAML config using direct implementation."""
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # Write YAML with proper encoding
            with file_path.open("w", encoding="utf-8") as f:
                yaml.dump(
                    config, f, indent=2, default_flow_style=False, sort_keys=False
                )
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to save YAML config: {e}")

    @classmethod
    def load_yaml_config(cls, file_path: Path) -> FlextResult[ConfigDict]:
        """Load YAML config using FlextUtilities.Files validation + direct YAML.

        ZERO DUPLICATION: Uses FlextUtilities.Files.is_valid_path for validation.
        """
        try:
            # Delegate path validation to FlextUtilities.EnvironmentUtils - NO DUPLICATION
            if not FlextUtilities.EnvironmentUtils.is_valid_path(str(file_path)):
                return FlextResult[ConfigDict].fail(
                    f"Invalid YAML file path: {file_path}"
                )

            if not file_path.exists():
                return FlextResult[ConfigDict].fail(f"YAML file not found: {file_path}")

            with file_path.open("r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            if config_data is None:
                return FlextResult[ConfigDict].ok({})

            if not isinstance(config_data, dict):
                return FlextResult[ConfigDict].fail("YAML content is not a dictionary")

            return FlextResult[ConfigDict].ok(config_data)
        except Exception as e:
            return FlextResult[ConfigDict].fail(f"Failed to load YAML config: {e}")

    @classmethod
    def validate_yaml_file(cls, file_path: Path) -> FlextResult[bool]:
        """Validate YAML using FlextUtilities.Files + direct YAML parsing.

        ZERO DUPLICATION: Uses FlextUtilities.Files.is_valid_path for validation.
        """
        try:
            # Delegate path validation to FlextUtilities.EnvironmentUtils - NO DUPLICATION
            if not FlextUtilities.EnvironmentUtils.is_valid_path(str(file_path)):
                return FlextResult[bool].fail(f"Invalid YAML file path: {file_path}")

            if not file_path.exists():
                return FlextResult[bool].fail(f"YAML file not found: {file_path}")

            with file_path.open("r", encoding="utf-8") as f:
                yaml.safe_load(f)  # This will raise an exception if invalid YAML

            return FlextResult[bool].ok(data=True)
        except yaml.YAMLError as e:
            return FlextResult[bool].fail(f"Invalid YAML syntax: {e}")
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to validate YAML: {e}")

    @classmethod
    def create_directory_structure(
        cls, base_path: Path, directories: FlextTypes.Core.StringList
    ) -> FlextResult[FlextTypes.Core.Headers]:
        """Create directory structure using direct pathlib implementation."""
        try:
            created_paths: FlextTypes.Core.Headers = {}

            for directory in directories:
                dir_path = base_path / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = str(dir_path)

            return FlextResult[FlextTypes.Core.Headers].ok(created_paths)
        except Exception as e:
            return FlextResult[FlextTypes.Core.Headers].fail(
                f"Failed to create directories: {e}"
            )

    @classmethod
    def setup_project_structure(
        cls, project_root: Path, project_name: str
    ) -> FlextResult[PathDict]:
        """Setup Meltano project structure using direct implementation."""
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
            configs: dict[str, ConfigDict] = {
                FlextMeltanoConstants.Meltano.PROJECT_FILE: {
                    "version": 1,
                    "project_id": project_name,
                    "project_name": project_name,
                    "plugins": {
                        "extractors": [],
                        "loaders": [],
                        "transformers": [],
                    },
                },
                "transform/dbt_project.yml": {
                    "name": project_name,
                    "version": "1.0.0",
                    "profile": project_name,
                    "model-paths": ["models"],
                    "test-paths": ["tests"],
                },
            }

            for filename, config_data in configs.items():
                config_path = project_root / filename
                save_result = cls.save_yaml_config(config_data, config_path)
                if save_result.success:
                    created_paths[filename.replace("/", "_")] = str(config_path)

            # Add project root
            created_paths["project_root"] = project_root
            return FlextResult[PathDict].ok(created_paths)
        except Exception as e:
            return FlextResult[PathDict].fail(f"Failed to setup project structure: {e}")

    @classmethod
    def cleanup_temp_directory(cls, temp_path: Path) -> FlextResult[bool]:
        """Cleanup temporary directory using direct implementation."""
        try:
            if temp_path.exists() and temp_path.is_dir():
                shutil.rmtree(temp_path)
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to cleanup temp directory: {e}")

    @classmethod
    def validate_project_structure(cls, project_root: Path) -> FlextResult[bool]:
        """Validate Meltano project structure using FlextUtilities.Files validation.

        ZERO DUPLICATION: Uses FlextUtilities.Files.is_valid_path for path validation.
        """
        try:
            # Delegate to FlextUtilities.EnvironmentUtils for path validation - NO DUPLICATION
            if not FlextUtilities.EnvironmentUtils.is_valid_path(str(project_root)):
                return FlextResult[bool].fail(
                    f"Invalid project root path: {project_root}"
                )

            if not project_root.exists():
                return FlextResult[bool].fail(
                    f"Project root does not exist: {project_root}"
                )

            # DOMAIN-SPECIFIC: Meltano project requirements
            required_files = [FlextMeltanoConstants.Meltano.PROJECT_FILE]
            required_dirs = ["extract", "load", "transform", "analyze"]

            for filename in required_files:
                file_path = project_root / filename
                if not file_path.exists():
                    return FlextResult[bool].fail(f"Missing required file: {filename}")

            for dirname in required_dirs:
                dir_path = project_root / dirname
                if not dir_path.is_dir():
                    return FlextResult[bool].fail(
                        f"Missing required directory: {dirname}"
                    )

            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to validate project structure: {e}")


__all__ = ["FlextMeltanoFileManagers"]
