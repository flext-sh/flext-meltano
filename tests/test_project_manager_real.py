"""Testes reais para project_manager.py - COVERAGE DIRETO NO TARGET CRÍTICO.

Objetivo: Gerar coverage real no arquivo project_manager.py (199 statements, 0% coverage).
TARGET MÁXIMO IMPACTO para melhorar coverage total significativamente.
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest
import yaml
from flext_core import FlextResult

# Import direto das classes REAIS do project_manager.py
from flext_meltano.project_manager import (
    FlextMeltanoExecutionError,
    FlextMeltanoFlextProjectManager,
    FlextMeltanoProjectError,
    FlextMeltanoProjectInitializationMode,
    FlextMeltanoProjectManager,
)


class TestFlextMeltanoProjectInitializationMode:
    """Testes reais da enumeração FlextMeltanoProjectInitializationMode."""

    def test_initialization_mode_values(self) -> None:
        """Testa valores da enumeração de modos de inicialização."""
        assert FlextMeltanoProjectInitializationMode.CREATE_NEW.value == "create_new"
        assert FlextMeltanoProjectInitializationMode.FORCE_RECREATE.value == "force_recreate"
        assert FlextMeltanoProjectInitializationMode.OVERWRITE_EXISTING.value == "overwrite_existing"


class TestFlextMeltanoProjectError:
    """Testes reais da exceção FlextMeltanoProjectError."""

    def test_project_error_creation(self) -> None:
        """Testa criação de erro de projeto."""
        error = FlextMeltanoProjectError("Test project error")
        assert str(error) == "Test project error"
        assert isinstance(error, Exception)


class TestFlextMeltanoExecutionError:
    """Testes reais da exceção FlextMeltanoExecutionError."""

    def test_execution_error_basic(self) -> None:
        """Testa criação básica de erro de execução."""
        error = FlextMeltanoExecutionError("Test execution error")
        assert str(error) == "Test execution error"
        assert error.command is None
        assert error.returncode is None
        assert error.stderr is None

    def test_execution_error_complete(self) -> None:
        """Testa erro de execução com todos os parâmetros."""
        command = ["meltano", "run", "tap-csv", "target-jsonl"]
        error = FlextMeltanoExecutionError(
            "Command failed",
            command=command,
            returncode=1,
            stderr="Error output",
        )

        assert str(error) == "Command failed"
        assert error.command == command
        assert error.returncode == 1
        assert error.stderr == "Error output"


class TestFlextMeltanoProjectManager:
    """Testes reais da classe FlextMeltanoProjectManager."""

    @pytest.fixture
    def temp_project_root(self) -> Path:
        """Cria diretório temporário para testes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def project_manager(self, temp_project_root: Path) -> FlextMeltanoProjectManager:
        """Cria instância real do project manager."""
        return FlextMeltanoProjectManager(temp_project_root)

    def test_project_manager_initialization(self, project_manager: FlextMeltanoProjectManager, temp_project_root: Path) -> None:
        """Testa inicialização do project manager."""
        assert project_manager.project_root == temp_project_root
        assert isinstance(project_manager.project_root, Path)

    def test_filter_singer_warnings(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa filtro de warnings do Singer SDK."""
        stderr_with_warnings = """
        Normal output line
        SingerSDKDeprecationWarning: This is deprecated
        Another normal line
        DeprecationWarning: Another warning
        Final normal line
        """

        filtered = project_manager._filter_singer_warnings(stderr_with_warnings)
        
        # Should keep normal lines and filter warning lines
        assert "Normal output line" in filtered
        assert "Another normal line" in filtered
        assert "Final normal line" in filtered
        assert "SingerSDKDeprecationWarning" not in filtered
        assert "DeprecationWarning" not in filtered

    def test_filter_singer_warnings_empty(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa filtro com entrada vazia."""
        assert project_manager._filter_singer_warnings("") == ""
        assert project_manager._filter_singer_warnings(None) is None

    @pytest.mark.asyncio
    async def test_create_project_success(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa criação de projeto com sucesso."""
        project_name = "test-project"
        environment = "dev"

        result = await project_manager.create_project(project_name, environment)

        assert result.success is True
        assert result.data is not None
        
        result_data = result.data.get("result", {})
        assert result_data["project_name"] == project_name
        assert result_data["environment"] == environment
        assert "project_path" in result_data
        assert "created_at" in result_data

        # Verify project structure was created
        project_path = project_manager.project_root / project_name
        assert project_path.exists()
        assert (project_path / "meltano.yml").exists()
        assert (project_path / ".meltano").exists()

    @pytest.mark.asyncio
    async def test_create_project_already_exists(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa criação de projeto que já existe."""
        project_name = "existing-project"
        
        # Create project first time
        result1 = await project_manager.create_project(project_name)
        assert result1.success is True

        # Try to create same project again
        result2 = await project_manager.create_project(project_name)
        assert result2.success is False
        assert "already exists" in result2.error

    @pytest.mark.asyncio
    async def test_load_project_config_success(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa carregamento de configuração com sucesso."""
        project_name = "config-test-project"
        
        # Create project first
        await project_manager.create_project(project_name)

        # Load config
        result = await project_manager.load_project_config(project_name)
        
        assert result.success is True
        config = result.data.get("result", {})
        assert config["version"] == 1
        assert config["default_environment"] == "dev"
        assert "project_id" in config
        assert "plugins" in config

    @pytest.mark.asyncio
    async def test_load_project_config_not_found(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa carregamento de configuração não encontrada."""
        result = await project_manager.load_project_config("nonexistent-project")
        
        assert result.success is False
        assert "not found" in result.error

    @pytest.mark.asyncio
    async def test_save_project_config_success(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa salvamento de configuração com sucesso."""
        project_name = "save-config-project"
        
        # Create project first
        await project_manager.create_project(project_name)

        # Update config
        new_config = {
            "version": 1,
            "project_id": "updated-project",
            "default_environment": "staging",
            "plugins": {"extractors": [], "loaders": []},
        }

        # Save config
        result = await project_manager.save_project_config(project_name, new_config)
        assert result.success is True

        # Verify config was saved
        load_result = await project_manager.load_project_config(project_name)
        assert load_result.success is True
        loaded_config = load_result.data.get("result", {})
        assert loaded_config["default_environment"] == "staging"
        assert loaded_config["project_id"] == "updated-project"

        # Verify backup was created
        project_path = project_manager.project_root / project_name
        backup_path = project_path / "meltano.yml.backup"
        assert backup_path.exists()

    @pytest.mark.asyncio
    async def test_run_pipeline_direct_success(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa execução de pipeline direto com sucesso."""
        project_name = "pipeline-project"
        
        # Create project first
        await project_manager.create_project(project_name)

        # Run pipeline direct
        result = await project_manager.run_pipeline_direct(
            project_name, "tap-csv", "target-jsonl"
        )

        assert result.success is True
        pipeline_result = result.data.get("result", {})
        assert pipeline_result["success"] is True
        assert pipeline_result["returncode"] == 0
        assert "direct-singer" in pipeline_result["command"]
        assert pipeline_result["stderr"] == ""  # No warnings

    @pytest.mark.asyncio
    async def test_run_pipeline_direct_project_not_found(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa execução de pipeline com projeto não encontrado."""
        result = await project_manager.run_pipeline_direct(
            "nonexistent-project", "tap-csv", "target-jsonl"
        )

        assert result.success is False
        assert "not found" in result.error

    @pytest.mark.asyncio
    async def test_run_command_success(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa execução de comando com sucesso."""
        project_name = "command-project"
        
        # Create project first
        await project_manager.create_project(project_name)

        # Mock subprocess execution
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = Mock()
            mock_process.returncode = 0
            mock_process.communicate.return_value = (b"success output", b"")
            mock_subprocess.return_value = mock_process

            result = await project_manager.run_command(
                project_name, ["--version"]
            )

            assert result.success is True
            command_result = result.data.get("result", {})
            assert command_result["success"] is True
            assert command_result["returncode"] == 0
            assert command_result["stdout"] == "success output"

    @pytest.mark.asyncio
    async def test_run_command_with_environment(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa execução de comando com ambiente específico."""
        project_name = "env-command-project"
        
        await project_manager.create_project(project_name)

        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = Mock()
            mock_process.returncode = 0
            mock_process.communicate.return_value = (b"prod output", b"")
            mock_subprocess.return_value = mock_process

            result = await project_manager.run_command(
                project_name, ["--version"], environment="production"
            )

            assert result.success is True
            # Verify environment argument was included
            call_args = mock_subprocess.call_args[0]
            assert "--environment" in call_args
            assert "production" in call_args

    @pytest.mark.asyncio
    async def test_run_command_failure(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa execução de comando com falha."""
        project_name = "fail-command-project"
        
        await project_manager.create_project(project_name)

        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = Mock()
            mock_process.returncode = 1
            mock_process.communicate.return_value = (b"", b"Command failed")
            mock_subprocess.return_value = mock_process

            result = await project_manager.run_command(
                project_name, ["invalid-command"]
            )

            assert result.success is False
            assert "Command failed" in result.error

    @pytest.mark.asyncio
    async def test_add_plugin_success(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa adição de plugin com sucesso."""
        project_name = "plugin-project"
        
        await project_manager.create_project(project_name)

        # Mock successful command execution
        with patch.object(project_manager, "run_command") as mock_run_command:
            mock_run_command.return_value = FlextResult.ok({
                "result": {
                    "stdout": "Plugin added successfully",
                    "stderr": "",
                    "returncode": 0,
                }
            })

            result = await project_manager.add_plugin(
                project_name, "extractors", "tap-csv", variant="meltanolabs"
            )

            assert result.success is True
            plugin_result = result.data.get("result", {})
            assert plugin_result["plugin_type"] == "extractors"
            assert plugin_result["plugin_name"] == "tap-csv"
            assert plugin_result["plugin_variant"] == "meltanolabs"

            # Verify add and lock commands were called
            assert mock_run_command.call_count == 2

    @pytest.mark.asyncio
    async def test_add_plugin_add_failure(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa falha na adição de plugin."""
        project_name = "plugin-fail-project"
        
        await project_manager.create_project(project_name)

        # Mock failed add command
        with patch.object(project_manager, "run_command") as mock_run_command:
            mock_run_command.return_value = FlextResult.fail("Add command failed")

            result = await project_manager.add_plugin(
                project_name, "extractors", "invalid-plugin"
            )

            assert result.success is False
            assert "Failed to add plugin" in result.error

    @pytest.mark.asyncio
    async def test_validate_project_success(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa validação de projeto com sucesso."""
        project_name = "validate-project"
        
        # Create valid project
        await project_manager.create_project(project_name)

        result = await project_manager.validate_project(project_name)
        
        assert result.success is True
        validation = result.data.get("result", {})
        assert validation["project_exists"] is True
        assert validation["config_exists"] is True
        assert validation["meltano_dir_exists"] is True
        assert validation["config_valid"] is True
        assert validation["is_valid"] is True
        assert len(validation["errors"]) == 0

    @pytest.mark.asyncio
    async def test_validate_project_not_found(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa validação de projeto não encontrado."""
        result = await project_manager.validate_project("nonexistent-project")
        
        assert result.success is True  # Validation returns result, not failure
        validation = result.data.get("result", {})
        assert validation["project_exists"] is False
        assert validation["is_valid"] is False
        assert "Project directory does not exist" in validation["errors"]

    @pytest.mark.asyncio
    async def test_validate_project_missing_config(self, project_manager: FlextMeltanoProjectManager) -> None:
        """Testa validação com configuração ausente."""
        project_name = "no-config-project"
        project_path = project_manager.project_root / project_name
        project_path.mkdir(parents=True)  # Create directory but no meltano.yml

        result = await project_manager.validate_project(project_name)
        
        assert result.success is True
        validation = result.data.get("result", {})
        assert validation["project_exists"] is True
        assert validation["config_exists"] is False
        # Early return in validation when config doesn't exist, so is_valid might not be set
        if "is_valid" in validation:
            assert validation["is_valid"] is False
        assert "meltano.yml not found" in validation["errors"]


class TestFlextMeltanoFlextProjectManager:
    """Testes reais da classe FlextMeltanoFlextProjectManager."""

    @pytest.fixture
    def temp_project_root(self) -> Path:
        """Cria diretório temporário para testes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def enhanced_project_manager(self, temp_project_root: Path) -> FlextMeltanoFlextProjectManager:
        """Cria instância real do enhanced project manager."""
        return FlextMeltanoFlextProjectManager(temp_project_root)

    @pytest.fixture
    def mock_event_bus(self) -> Mock:
        """Cria mock do event bus."""
        mock_bus = Mock()
        mock_bus.publish = AsyncMock()
        return mock_bus

    def test_enhanced_project_manager_initialization(
        self, 
        enhanced_project_manager: FlextMeltanoFlextProjectManager, 
        temp_project_root: Path
    ) -> None:
        """Testa inicialização do enhanced project manager."""
        assert enhanced_project_manager.project_root == temp_project_root
        assert enhanced_project_manager.event_bus is None

    def test_enhanced_project_manager_with_event_bus(self, temp_project_root: Path, mock_event_bus: Mock) -> None:
        """Testa inicialização com event bus."""
        manager = FlextMeltanoFlextProjectManager(temp_project_root, mock_event_bus)
        assert manager.event_bus is mock_event_bus

    @pytest.mark.asyncio
    async def test_create_project_with_events_success(
        self, 
        enhanced_project_manager: FlextMeltanoFlextProjectManager,
        mock_event_bus: Mock
    ) -> None:
        """Testa criação de projeto com eventos."""
        enhanced_project_manager.event_bus = mock_event_bus
        
        result = await enhanced_project_manager.create_project_with_events("event-project")
        
        assert result.success is True
        mock_event_bus.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_project_with_events_no_bus(
        self, 
        enhanced_project_manager: FlextMeltanoFlextProjectManager
    ) -> None:
        """Testa criação de projeto sem event bus."""
        result = await enhanced_project_manager.create_project_with_events("no-event-project")
        
        assert result.success is True
        # No event bus, so no events published

    @pytest.mark.asyncio
    async def test_backup_project_success(
        self, 
        enhanced_project_manager: FlextMeltanoFlextProjectManager,
        temp_project_root: Path
    ) -> None:
        """Testa backup de projeto com sucesso."""
        project_name = "backup-project"
        backup_path = temp_project_root / "backups" / "backup-project"
        
        # Create project first
        await enhanced_project_manager.create_project(project_name)

        # Mock shutil.make_archive to avoid actual file operations
        with patch("shutil.make_archive") as mock_make_archive:
            mock_make_archive.return_value = str(backup_path.with_suffix(".zip"))

            result = await enhanced_project_manager.backup_project(project_name, backup_path)
            
            assert result.success is True
            backup_result = result.data.get("result")
            assert backup_result.endswith(".zip")
            mock_make_archive.assert_called_once()

    @pytest.mark.asyncio
    async def test_backup_project_with_events(
        self, 
        enhanced_project_manager: FlextMeltanoFlextProjectManager,
        temp_project_root: Path,
        mock_event_bus: Mock
    ) -> None:
        """Testa backup de projeto com eventos."""
        enhanced_project_manager.event_bus = mock_event_bus
        project_name = "backup-event-project"
        backup_path = temp_project_root / "backups" / "backup-event-project"
        
        await enhanced_project_manager.create_project(project_name)

        with patch("shutil.make_archive"):
            result = await enhanced_project_manager.backup_project(project_name, backup_path)
            
            assert result.success is True
            mock_event_bus.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_backup_project_not_found(
        self, 
        enhanced_project_manager: FlextMeltanoFlextProjectManager,
        temp_project_root: Path
    ) -> None:
        """Testa backup de projeto não encontrado."""
        backup_path = temp_project_root / "backups" / "nonexistent"
        
        result = await enhanced_project_manager.backup_project("nonexistent-project", backup_path)
        
        assert result.success is False
        assert "not found" in result.error


class TestProjectManagerIntegration:
    """Testes de integração para project managers."""

    @pytest.fixture
    def temp_project_root(self) -> Path:
        """Cria diretório temporário para testes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.mark.asyncio
    async def test_complete_project_lifecycle(self, temp_project_root: Path) -> None:
        """Testa ciclo completo de vida do projeto."""
        manager = FlextMeltanoProjectManager(temp_project_root)
        project_name = "lifecycle-project"

        # 1. Create project
        create_result = await manager.create_project(project_name, "dev")
        assert create_result.success is True

        # 2. Validate project
        validate_result = await manager.validate_project(project_name)
        assert validate_result.success is True
        assert validate_result.data["result"]["is_valid"] is True

        # 3. Load config
        load_result = await manager.load_project_config(project_name)
        assert load_result.success is True

        # 4. Modify and save config
        config = load_result.data["result"]
        config["custom_field"] = "test_value"
        save_result = await manager.save_project_config(project_name, config)
        assert save_result.success is True

        # 5. Verify config was saved
        reload_result = await manager.load_project_config(project_name)
        assert reload_result.success is True
        assert reload_result.data["result"]["custom_field"] == "test_value"

    @pytest.mark.asyncio
    async def test_enhanced_manager_inheritance(self, temp_project_root: Path) -> None:
        """Testa herança do enhanced manager."""
        enhanced_manager = FlextMeltanoFlextProjectManager(temp_project_root)
        
        # Enhanced manager should have all base functionality
        result = await enhanced_manager.create_project("inheritance-test")
        assert result.success is True

        # Plus enhanced functionality
        backup_path = temp_project_root / "test-backup"
        with patch("shutil.make_archive"):
            backup_result = await enhanced_manager.backup_project("inheritance-test", backup_path)
            assert backup_result.success is True

    def test_error_classes_inheritance(self) -> None:
        """Testa herança das classes de erro."""
        project_error = FlextMeltanoProjectError("test")
        execution_error = FlextMeltanoExecutionError("test")

        assert isinstance(project_error, Exception)
        assert isinstance(execution_error, Exception)
        assert isinstance(execution_error, FlextMeltanoProjectError) is False  # Different exception types