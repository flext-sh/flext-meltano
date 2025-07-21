"""Test FLEXT Meltano Anti-Corruption Layer - 64 lines of code, 0% coverage.

ZERO TOLERANCE for fake code, mockups, or library fallbacks.
Comprehensive tests for ALL anti-corruption layer classes and functionality.
"""

from __future__ import annotations

import sys
from abc import ABC
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Mock missing dependencies to avoid import errors - must be before local imports
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# ruff: noqa: E402 - Module mocking must happen before imports
from flext_meltano.anti_corruption_layer import (
    MeltanoAdapter,
    MeltanoAntiCorruptionLayer,
    SimpleMeltanoAdapter,
)


class TestMeltanoAdapter:
    """Test MeltanoAdapter abstract base class."""

    def test_meltano_adapter_is_abstract(self) -> None:
        """Test that MeltanoAdapter is an abstract base class."""
        assert issubclass(MeltanoAdapter, ABC)

        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            MeltanoAdapter()

    def test_meltano_adapter_has_required_methods(self) -> None:
        """Test that MeltanoAdapter defines required abstract methods."""
        required_methods = [
            "run_pipeline",
            "install_plugin",
            "list_plugins",
            "get_plugin_config",
        ]

        for method_name in required_methods:
            assert hasattr(MeltanoAdapter, method_name)
            method = getattr(MeltanoAdapter, method_name)
            assert getattr(method, "__isabstractmethod__", False), (
                f"{method_name} should be abstract"
            )


class TestMeltanoAntiCorruptionLayer:
    """Test MeltanoAntiCorruptionLayer - comprehensive coverage."""

    @pytest.fixture
    def mock_adapter(self) -> AsyncMock:
        """Create a mock adapter for testing."""
        return AsyncMock(spec=MeltanoAdapter)

    @pytest.fixture
    def acl(self, mock_adapter: AsyncMock) -> MeltanoAntiCorruptionLayer:
        """Create an anti-corruption layer instance."""
        return MeltanoAntiCorruptionLayer(mock_adapter)

    def test_acl_initialization(self, mock_adapter: AsyncMock) -> None:
        """Test MeltanoAntiCorruptionLayer initialization."""
        acl = MeltanoAntiCorruptionLayer(mock_adapter)

        assert acl.adapter == mock_adapter

    @pytest.mark.asyncio
    async def test_execute_pipeline_success(
        self,
        acl: MeltanoAntiCorruptionLayer,
        mock_adapter: AsyncMock,
    ) -> None:
        """Test successful pipeline execution."""
        from flext_core import ServiceResult

        # Mock adapter to return success
        mock_result_data = {
            "status": "completed",
            "output": "Pipeline executed",
            "duration": 120,
            "metadata": {"env": "dev"},
        }
        mock_adapter.run_pipeline.return_value = ServiceResult.ok(mock_result_data)

        config = {"database_url": "postgres://test", "batch_size": 1000}
        result = await acl.execute_pipeline("test-pipeline", "dev", config)

        assert result.is_success is True
        assert result.data["status"] == "completed"
        assert result.data["output"] == "Pipeline executed"
        assert result.data["duration"] == 120
        assert result.data["metadata"] == {"env": "dev"}

        # Verify adapter was called with translated config
        mock_adapter.run_pipeline.assert_called_once_with(
            pipeline_name="test-pipeline",
            environment="dev",
            configuration={"database-url": "postgres://test", "batch-size": 1000},
        )

    @pytest.mark.asyncio
    async def test_execute_pipeline_with_defaults(
        self,
        acl: MeltanoAntiCorruptionLayer,
        mock_adapter: AsyncMock,
    ) -> None:
        """Test pipeline execution with default parameters."""
        from flext_core import ServiceResult

        mock_adapter.run_pipeline.return_value = ServiceResult.ok(
            {"status": "completed", "output": "Success"},
        )

        result = await acl.execute_pipeline("simple-pipeline")

        assert result.is_success is True

        # Should use default environment and empty config
        mock_adapter.run_pipeline.assert_called_once_with(
            pipeline_name="simple-pipeline",
            environment="dev",
            configuration={},
        )

    @pytest.mark.asyncio
    async def test_execute_pipeline_adapter_failure(
        self,
        acl: MeltanoAntiCorruptionLayer,
        mock_adapter: AsyncMock,
    ) -> None:
        """Test pipeline execution when adapter fails."""
        from flext_core import ServiceResult

        mock_adapter.run_pipeline.return_value = ServiceResult.fail("Adapter error")

        result = await acl.execute_pipeline("failing-pipeline")

        assert result.is_success is False
        assert result.error == "Adapter error"

    @pytest.mark.asyncio
    async def test_execute_pipeline_exception_handling(
        self,
        acl: MeltanoAntiCorruptionLayer,
        mock_adapter: AsyncMock,
    ) -> None:
        """Test pipeline execution exception handling."""
        mock_adapter.run_pipeline.side_effect = RuntimeError("Connection failed")

        result = await acl.execute_pipeline("error-pipeline")

        assert result.is_success is False
        assert "Failed to execute pipeline: Connection failed" in result.error

    @pytest.mark.asyncio
    async def test_manage_plugin_install_success(
        self,
        acl: MeltanoAntiCorruptionLayer,
        mock_adapter: AsyncMock,
    ) -> None:
        """Test successful plugin installation."""
        from flext_core import ServiceResult

        mock_result_data = {
            "plugin_type": "extractor",
            "plugin_name": "tap-csv",
            "status": "installed",
        }
        mock_adapter.install_plugin.return_value = ServiceResult.ok(mock_result_data)

        result = await acl.manage_plugin(
            action="install",
            plugin_type="extractor",
            plugin_name="tap-csv",
            variant="meltanolabs",
        )

        assert result.is_success is True
        assert result.data["plugin_name"] == "tap-csv"
        assert result.data["status"] == "installed"

        mock_adapter.install_plugin.assert_called_once_with(
            plugin_type="extractor",
            plugin_name="tap-csv",
            variant="meltanolabs",
        )

    @pytest.mark.asyncio
    async def test_manage_plugin_install_with_no_variant(
        self,
        acl: MeltanoAntiCorruptionLayer,
        mock_adapter: AsyncMock,
    ) -> None:
        """Test plugin installation without variant."""
        from flext_core import ServiceResult

        mock_adapter.install_plugin.return_value = ServiceResult.ok(
            {"status": "installed"},
        )

        result = await acl.manage_plugin(
            action="install",
            plugin_type="loader",
            plugin_name="target-postgres",
        )

        assert result.is_success is True

        mock_adapter.install_plugin.assert_called_once_with(
            plugin_type="loader",
            plugin_name="target-postgres",
            variant=None,
        )

    @pytest.mark.asyncio
    async def test_manage_plugin_list_success(
        self,
        acl: Any,
        mock_adapter: Any,
    ) -> None:
        """Test successful plugin listing."""
        from flext_core import ServiceResult

        mock_result_data = [
            {"name": "tap-csv", "type": "extractor"},
            {"name": "target-postgres", "type": "loader"},
        ]
        mock_adapter.list_plugins.return_value = ServiceResult.ok(mock_result_data)

        result = await acl.manage_plugin(
            action="list",
            plugin_type="extractor",
            plugin_name="dummy",
        )

        assert result.is_success is True
        assert len(result.data) == 2

        mock_adapter.list_plugins.assert_called_once_with(plugin_type="extractor")

    @pytest.mark.asyncio
    async def test_manage_plugin_config_success(
        self,
        acl: Any,
        mock_adapter: Any,
    ) -> None:
        """Test successful plugin config retrieval."""
        from flext_core import ServiceResult

        mock_result_data = {
            "plugin_name": "tap-csv",
            "settings": {"file_path": "required"},
        }
        mock_adapter.get_plugin_config.return_value = ServiceResult.ok(mock_result_data)

        result = await acl.manage_plugin(
            action="config",
            plugin_type="extractor",
            plugin_name="tap-csv",
        )

        assert result.is_success is True
        assert result.data["plugin_name"] == "tap-csv"

        mock_adapter.get_plugin_config.assert_called_once_with(plugin_name="tap-csv")

    @pytest.mark.asyncio
    async def test_manage_plugin_unknown_action(
        self,
        acl: Any,
        mock_adapter: Any,
    ) -> None:
        """Test plugin management with unknown action."""
        result = await acl.manage_plugin(
            action="unknown",
            plugin_type="extractor",
            plugin_name="tap-csv",
        )

        assert result.is_success is False
        assert "Unknown plugin action: unknown" in result.error

        # No adapter methods should be called
        mock_adapter.install_plugin.assert_not_called()
        mock_adapter.list_plugins.assert_not_called()
        mock_adapter.get_plugin_config.assert_not_called()

    @pytest.mark.asyncio
    async def test_manage_plugin_exception_handling(
        self,
        acl: Any,
        mock_adapter: Any,
    ) -> None:
        """Test plugin management exception handling."""
        mock_adapter.install_plugin.side_effect = ValueError("Invalid plugin")

        result = await acl.manage_plugin(
            action="install",
            plugin_type="extractor",
            plugin_name="invalid-plugin",
        )

        assert result.is_success is False
        assert "Failed to manage plugin: Invalid plugin" in result.error

    def test_translate_config(self, acl: Any) -> None:
        """Test configuration translation from domain to Meltano."""
        domain_config = {
            "database_url": "postgres://localhost:5432/db",
            "batch_size": 1000,
            "enable_logging": True,
            "api_key": "secret123",
        }

        meltano_config = acl._translate_config(domain_config)

        expected = {
            "database-url": "postgres://localhost:5432/db",
            "batch-size": 1000,
            "enable-logging": True,
            "api-key": "secret123",
        }

        assert meltano_config == expected

    def test_translate_config_empty(self, acl: Any) -> None:
        """Test configuration translation with empty config."""
        result = acl._translate_config({})
        assert result == {}

    def test_translate_result(self, acl: Any) -> None:
        """Test result translation from Meltano to domain."""
        meltano_result = {
            "status": "completed",
            "output": "Pipeline executed successfully",
            "duration": 150,
            "metadata": {"records": 1000, "errors": 0},
            "extra_field": "should_be_ignored",
        }

        domain_result = acl._translate_result(meltano_result)

        expected = {
            "status": "completed",
            "output": "Pipeline executed successfully",
            "duration": 150,
            "metadata": {"records": 1000, "errors": 0},
        }

        assert domain_result == expected

    def test_translate_result_with_missing_fields(self, acl: Any) -> None:
        """Test result translation with missing fields."""
        meltano_result = {"status": "completed"}

        domain_result = acl._translate_result(meltano_result)

        expected = {
            "status": "completed",
            "output": "",
            "duration": 0,
            "metadata": {},
        }

        assert domain_result == expected

    def test_translate_result_empty(self, acl: Any) -> None:
        """Test result translation with empty result."""
        domain_result = acl._translate_result({})

        expected = {
            "status": "unknown",
            "output": "",
            "duration": 0,
            "metadata": {},
        }

        assert domain_result == expected


class TestSimpleMeltanoAdapter:
    """Test SimpleMeltanoAdapter implementation - comprehensive coverage."""

    @pytest.fixture
    def adapter(self) -> SimpleMeltanoAdapter:
        """Create a SimpleMeltanoAdapter instance."""
        return SimpleMeltanoAdapter()

    def test_adapter_implements_interface(self, adapter: SimpleMeltanoAdapter) -> None:
        """Test that SimpleMeltanoAdapter implements MeltanoAdapter."""
        assert isinstance(adapter, MeltanoAdapter)

    @pytest.mark.asyncio
    async def test_run_pipeline_success(self, adapter: SimpleMeltanoAdapter) -> None:
        """Test successful pipeline execution."""
        result = await adapter.run_pipeline(
            pipeline_name="test-pipeline",
            environment="production",
            configuration={"setting1": "value1", "setting2": 42},
        )

        assert result.is_success is True
        assert result.data["status"] == "completed"
        assert "test-pipeline" in result.data["output"]
        assert result.data["duration"] == 100

        metadata = result.data["metadata"]
        assert metadata["environment"] == "production"
        assert metadata["configuration"]["setting1"] == "value1"
        assert metadata["configuration"]["setting2"] == 42

    @pytest.mark.asyncio
    async def test_run_pipeline_with_defaults(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test pipeline execution with default parameters."""
        result = await adapter.run_pipeline("simple-pipeline")

        assert result.is_success is True
        assert result.data["status"] == "completed"
        assert "simple-pipeline" in result.data["output"]

        metadata = result.data["metadata"]
        assert metadata["environment"] == "dev"
        assert metadata["configuration"] == {}

    @pytest.mark.asyncio
    async def test_run_pipeline_error_handling(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test pipeline execution error handling."""
        # Mock asyncio.sleep to raise an exception
        with patch("asyncio.sleep", side_effect=RuntimeError("Sleep failed")):
            result = await adapter.run_pipeline("error-pipeline")

            assert result.is_success is False
            assert "Failed to run pipeline: Sleep failed" in result.error

    @pytest.mark.asyncio
    async def test_install_plugin_success(self, adapter: SimpleMeltanoAdapter) -> None:
        """Test successful plugin installation."""
        result = await adapter.install_plugin(
            plugin_type="extractor",
            plugin_name="tap-csv",
            variant="meltanolabs",
        )

        assert result.is_success is True
        assert result.data["plugin_type"] == "extractor"
        assert result.data["plugin_name"] == "tap-csv"
        assert result.data["variant"] == "meltanolabs"
        assert result.data["status"] == "installed"

    @pytest.mark.asyncio
    async def test_install_plugin_no_variant(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test plugin installation without variant."""
        result = await adapter.install_plugin(
            plugin_type="loader",
            plugin_name="target-postgres",
        )

        assert result.is_success is True
        assert result.data["plugin_type"] == "loader"
        assert result.data["plugin_name"] == "target-postgres"
        assert result.data["variant"] == "original"
        assert result.data["status"] == "installed"

    @pytest.mark.asyncio
    async def test_install_plugin_error_handling(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test plugin installation error handling."""
        # Mock asyncio.sleep to raise an exception
        with patch("asyncio.sleep", side_effect=OSError("File system error")):
            result = await adapter.install_plugin("extractor", "broken-plugin")

            assert result.is_success is False
            assert "Failed to install plugin: File system error" in result.error

    @pytest.mark.asyncio
    async def test_list_plugins_all(self, adapter: SimpleMeltanoAdapter) -> None:
        """Test listing all plugins."""
        result = await adapter.list_plugins()

        assert result.is_success is True
        plugins = result.data
        assert len(plugins) == 2

        # Check tap-csv plugin
        tap_csv = next(p for p in plugins if p["name"] == "tap-csv")
        assert tap_csv["type"] == "extractor"
        assert tap_csv["variant"] == "original"
        assert tap_csv["status"] == "available"

        # Check target-postgres plugin
        target_postgres = next(p for p in plugins if p["name"] == "target-postgres")
        assert target_postgres["type"] == "loader"
        assert target_postgres["variant"] == "original"
        assert target_postgres["status"] == "available"

    @pytest.mark.asyncio
    async def test_list_plugins_filtered_by_type(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test listing plugins filtered by type."""
        # Test extractor filter
        result = await adapter.list_plugins(plugin_type="extractor")

        assert result.is_success is True
        plugins = result.data
        assert len(plugins) == 1
        assert plugins[0]["name"] == "tap-csv"
        assert plugins[0]["type"] == "extractor"

        # Test loader filter
        result = await adapter.list_plugins(plugin_type="loader")

        assert result.is_success is True
        plugins = result.data
        assert len(plugins) == 1
        assert plugins[0]["name"] == "target-postgres"
        assert plugins[0]["type"] == "loader"

    @pytest.mark.asyncio
    async def test_list_plugins_no_matches(self, adapter: SimpleMeltanoAdapter) -> None:
        """Test listing plugins with no matches."""
        result = await adapter.list_plugins(plugin_type="orchestrator")

        assert result.is_success is True
        assert result.data == []

    @pytest.mark.asyncio
    async def test_list_plugins_error_handling(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test plugin listing error handling."""
        # Mock ServiceResult.ok to raise an exception during result creation
        with patch(
            "flext_meltano.anti_corruption_layer.ServiceResult.ok",
            side_effect=TypeError("Result creation failed"),
        ):
            result = await adapter.list_plugins(plugin_type="extractor")

            assert result.is_success is False
            assert "Failed to list plugins: Result creation failed" in result.error

    @pytest.mark.asyncio
    async def test_get_plugin_config_success(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test successful plugin config retrieval."""
        result = await adapter.get_plugin_config("tap-csv")

        assert result.is_success is True
        config = result.data
        assert config["plugin_name"] == "tap-csv"

        settings = config["settings"]
        assert settings["api_key"] == "required"
        assert settings["base_url"] == "optional"

        commands = config["commands"]
        assert commands["test"] == "Check connection"
        assert commands["discover"] == "Discover schema"

    @pytest.mark.asyncio
    async def test_get_plugin_config_different_plugin(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test plugin config retrieval for different plugin."""
        result = await adapter.get_plugin_config("target-postgres")

        assert result.is_success is True
        config = result.data
        assert config["plugin_name"] == "target-postgres"

        # Should still have the same structure
        assert "settings" in config
        assert "commands" in config

    @pytest.mark.asyncio
    async def test_get_plugin_config_error_handling(
        self,
        adapter: SimpleMeltanoAdapter,
    ) -> None:
        """Test plugin config retrieval error handling."""
        # Mock ServiceResult.ok to raise an exception
        with patch(
            "flext_meltano.anti_corruption_layer.ServiceResult.ok",
            side_effect=ValueError("Config error"),
        ):
            result = await adapter.get_plugin_config("broken-plugin")

            assert result.is_success is False
            assert "Failed to get plugin config: Config error" in result.error


class TestIntegrationWorkflow:
    """Test complete integration workflow scenarios."""

    @pytest.mark.asyncio
    async def test_complete_acl_workflow(self) -> None:
        """Test complete workflow from adapter to ACL execution."""
        # Step 1: Create adapter and ACL
        adapter = SimpleMeltanoAdapter()
        acl = MeltanoAntiCorruptionLayer(adapter)

        # Step 2: Execute pipeline
        pipeline_result = await acl.execute_pipeline(
            pipeline_id="integration-test",
            environment="staging",
            config={"source_path": "/data/source", "batch_size": 500},
        )

        assert pipeline_result.is_success is True
        assert pipeline_result.data["status"] == "completed"
        assert "integration-test" in pipeline_result.data["output"]

        # Step 3: Install plugin
        install_result = await acl.manage_plugin(
            action="install",
            plugin_type="extractor",
            plugin_name="tap-integration",
            variant="latest",
        )

        assert install_result.is_success is True
        assert install_result.data["status"] == "installed"

        # Step 4: List plugins
        list_result = await acl.manage_plugin(
            action="list",
            plugin_type="extractor",
            plugin_name="dummy",
        )

        assert list_result.is_success is True
        extractors = list_result.data
        assert len(extractors) == 1
        assert extractors[0]["type"] == "extractor"

        # Step 5: Get config
        config_result = await acl.manage_plugin(
            action="config",
            plugin_type="extractor",
            plugin_name="tap-integration",
        )

        assert config_result.is_success is True
        assert config_result.data["plugin_name"] == "tap-integration"

    @pytest.mark.asyncio
    async def test_error_propagation_workflow(self) -> None:
        """Test error propagation through the anti-corruption layer."""
        # Create a mock adapter that fails
        failing_adapter = AsyncMock(spec=MeltanoAdapter)
        failing_adapter.run_pipeline.side_effect = RuntimeError("Adapter failure")

        acl = MeltanoAntiCorruptionLayer(failing_adapter)

        # Test that errors are properly handled and propagated
        result = await acl.execute_pipeline("failing-pipeline")

        assert result.is_success is False
        assert "Failed to execute pipeline: Adapter failure" in result.error

    @pytest.mark.asyncio
    async def test_config_translation_workflow(self) -> None:
        """Test configuration translation in a complete workflow."""
        adapter = SimpleMeltanoAdapter()
        acl = MeltanoAntiCorruptionLayer(adapter)

        # Complex domain configuration
        domain_config = {
            "database_url": "postgresql://user:pass@host:5432/db",
            "api_timeout": 30,
            "enable_ssl": True,
            "batch_size": 1000,
            "log_level": "info",
        }

        result = await acl.execute_pipeline(
            pipeline_id="config-test",
            environment="test",
            config=domain_config,
        )

        assert result.is_success is True

        # Verify that the result contains translated domain concepts
        assert result.data["status"] == "completed"
        assert result.data["output"] != ""
        assert result.data["duration"] == 100
        assert isinstance(result.data["metadata"], dict)
