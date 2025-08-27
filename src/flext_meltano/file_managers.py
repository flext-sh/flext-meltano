"""FLEXT Meltano File Management - Interface Segregation Implementation.

**Interface Segregation Principle**: Separate file management concerns
**Single Responsibility**: Each manager handles one type of file operation
**SOLID Compliance**: Focused interfaces for specific file management needs

File management utilities extracted from utilities.py for better separation of concerns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import yaml
from flext_core import (
    FlextResult,
    get_logger,
)

# Type definitions for file management operations
ConfigDict = dict[str, object]
PathDict = dict[str, str]

logger = get_logger(__name__)

# =============================================================================
# MAIN FILE MANAGERS CLASS - Following Flext[Area][Module] pattern
# =============================================================================


class FlextMeltanoFileManagers:
    """Single main file managers class for all file management operations (Flext[Area][Module] pattern).

    Architectural Compliance:
    - All file management operations organized under single class
    - Nested classes implement specific manager types
    - Aliases for backward compatibility
    - Type-safe operations with ConfigDict and PathDict

    SOLID Principles:
    - Single Responsibility: All file management in one place
    - Open/Closed: Extensible through inheritance
    - Interface Segregation: Specialized nested classes
    """

    # =================================================================
    # NESTED MANAGER CLASSES - Actual implementations
    # =================================================================

    class YamlFileManager:
        """Single responsibility: YAML file operations only."""

        @staticmethod
        def save_yaml_config(config: ConfigDict, file_path: Path) -> FlextResult[bool]:
            """Salva configuração YAML em arquivo.

            Args:
            config: Configuração para salvar
            file_path: Caminho do arquivo

            Returns:
            FlextResult indicando sucesso/falha

            """
            try:
                with file_path.open("w", encoding="utf-8") as f:
                    yaml.dump(config, f)
                return FlextResult[bool].ok(data=True)
            except Exception as e:
                return FlextResult.fail(f"Failed to save YAML config: {e}")

        @staticmethod
        def load_yaml_config(file_path: Path) -> FlextResult[ConfigDict]:
            """Carrega configuração YAML de arquivo.

            Args:
                file_path: Caminho do arquivo

            Returns:
                FlextResult com configuração carregada

            """
            try:
                if not file_path.exists():
                    return FlextResult.fail(f"Config file not found: {file_path}")

                with file_path.open("r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)

                # Return the config as-is to preserve nested structure
                return FlextResult[ConfigDict].ok(config or {})
            except Exception as e:
                return FlextResult.fail(f"Failed to load YAML config: {e}")

        @staticmethod
        def validate_yaml_file(file_path: Path) -> FlextResult[bool]:
            """Valida se arquivo YAML é válido.

            Args:
                file_path: Caminho do arquivo YAML

            Returns:
                FlextResult indicando se o arquivo é válido

            """
            try:
                if not file_path.exists():
                    return FlextResult.fail(f"YAML file not found: {file_path}")

                with file_path.open("r", encoding="utf-8") as f:
                    yaml.safe_load(f)

                return FlextResult[bool].ok(data=True)
            except yaml.YAMLError as e:
                return FlextResult.fail(f"Invalid YAML file: {e}")
            except Exception as e:
                return FlextResult.fail(f"Failed to validate YAML: {e}")

    class ProjectStructureManager:
        """Single responsibility: Project structure setup and management only."""

        @staticmethod
        def setup_project_structure(
            project_root: Path, project_name: str
        ) -> FlextResult[PathDict]:
            """Configura estrutura completa de projeto Meltano + DBT.

            Args:
                project_root: Diretório raiz do projeto
                project_name: Nome do projeto

            Returns:
                FlextResult com informações dos diretórios criados

            """
            try:
                # Criar diretórios necessários
                project_root.mkdir(exist_ok=True)

                # Estrutura Meltano
                meltano_dirs = {
                    "extract": project_root / "extract",
                    "load": project_root / "load",
                    "transform": project_root / "transform",
                    "analyze": project_root / "analyze",
                    "models": project_root / "transform" / "models",
                    "tests": project_root / "transform" / "tests",
                    "data": project_root / "transform" / "data",
                }

                created_dirs = {}
                for name, dir_path in meltano_dirs.items():
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_dirs[name] = str(dir_path)

                # Create meltano.yml using basic config structure
                meltano_config: ConfigDict = {
                    "version": 1,
                    "project_id": project_name,
                    "project_name": project_name,
                }
                meltano_yml = project_root / "meltano.yml"

                # Create dbt_project.yml using basic config structure
                dbt_config: ConfigDict = {
                    "name": f"{project_name}_dbt",
                    "version": "1.0.0",
                }
                dbt_yml = project_root / "transform" / "dbt_project.yml"

                # Save configs using YAML manager static methods directly
                # Try to save configs, but don't fail structure creation if save fails
                try:
                    FlextMeltanoFileManagers.YamlFileManager.save_yaml_config(
                        meltano_config, meltano_yml
                    )
                    FlextMeltanoFileManagers.YamlFileManager.save_yaml_config(
                        dbt_config, dbt_yml
                    )
                except Exception as e:
                    logger.debug(
                        f"Config save warning: {e}"
                    )  # Non-critical for structure setup

                result_info = {
                    "project_root": str(project_root),
                    "meltano_yml": str(meltano_yml),
                    "dbt_yml": str(dbt_yml),
                    **created_dirs,
                }

                return FlextResult[PathDict].ok(result_info)

            except Exception as e:
                return FlextResult.fail(f"Failed to setup project structure: {e}")

        @staticmethod
        def create_directory_structure(
            base_path: Path, directories: list[str]
        ) -> FlextResult[dict[str, str]]:
            """Cria estrutura de diretórios personalizada.

            Args:
                base_path: Caminho base
                directories: Lista de diretórios para criar

            Returns:
                FlextResult com paths dos diretórios criados

            """
            try:
                base_path.mkdir(parents=True, exist_ok=True)
                created_paths = {}

                for directory in directories:
                    dir_path = base_path / directory
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_paths[directory] = str(dir_path)

                return FlextResult[dict[str, str]].ok(created_paths)
            except Exception as e:
                return FlextResult.fail(f"Failed to create directory structure: {e}")

        @staticmethod
        def validate_project_structure(
            project_root: Path, required_files: list[str] | None = None
        ) -> FlextResult[dict[str, bool]]:
            """Valida estrutura de projeto Meltano.

            Args:
                project_root: Diretório raiz do projeto
                required_files: Lista de arquivos obrigatórios (opcional)

            Returns:
                FlextResult com status de validação

            """
            try:
                if not project_root.exists():
                    return FlextResult.fail(f"Project root not found: {project_root}")

                # Default required files for Meltano project
                if required_files is None:
                    required_files = ["meltano.yml"]

                validation_results = {}
                for file_name in required_files:
                    file_path = project_root / file_name
                    validation_results[file_name] = file_path.exists()

                # Check if all required files exist
                all_files_exist = all(validation_results.values())
                validation_results["project_valid"] = all_files_exist

                return FlextResult[dict[str, bool]].ok(validation_results)
            except Exception as e:
                return FlextResult.fail(f"Failed to validate project structure: {e}")

    class TempDirectoryManager:
        """Single responsibility: Temporary directory management only."""

        @staticmethod
        def create_temp_directory(prefix: str = "flext_meltano_") -> Path:
            """Create temporary directory with default prefix.

            Args:
                prefix: Prefix for temporary directory

            Returns:
                Path of created directory

            """
            return Path(tempfile.mkdtemp(prefix=prefix))

        @staticmethod
        def create_temp_directory_with_result(
            prefix: str = "flext_meltano_",
        ) -> FlextResult[Path]:
            """Create temporary directory with FlextResult wrapping.

            Args:
                prefix: Prefix for temporary directory

            Returns:
                FlextResult containing Path of created directory

            """
            try:
                temp_path = Path(tempfile.mkdtemp(prefix=prefix))
                return FlextResult[Path].ok(temp_path)
            except Exception as e:
                return FlextResult.fail(f"Failed to create temporary directory: {e}")

        @staticmethod
        def cleanup_temp_directory(temp_path: Path) -> FlextResult[bool]:
            """Clean up temporary directory and its contents.

            Args:
                temp_path: Path to temporary directory

            Returns:
                FlextResult indicating success/failure

            """
            try:
                if temp_path.exists() and temp_path.is_dir():
                    shutil.rmtree(temp_path)
                return FlextResult[bool].ok(data=True)
            except Exception as e:
                return FlextResult.fail(f"Failed to cleanup temporary directory: {e}")


# =============================================================================
# MODULE-LEVEL ALIASES FOR BACKWARD COMPATIBILITY
# =============================================================================


class FlextTempDirectoryManager:
    """Legacy alias for FlextMeltanoFileManagers.TempDirectoryManager.

    DEPRECATED: Use FlextMeltanoFileManagers.TempDirectoryManager instead.
    """

    # Delegate to internal class
    create_temp_directory = (
        FlextMeltanoFileManagers.TempDirectoryManager.create_temp_directory
    )
    create_temp_directory_with_result = (
        FlextMeltanoFileManagers.TempDirectoryManager.create_temp_directory_with_result
    )
    cleanup_temp_directory = (
        FlextMeltanoFileManagers.TempDirectoryManager.cleanup_temp_directory
    )


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoFileManagers",
    "FlextTempDirectoryManager",
]
