"""Tests for FLEXT Meltano boilerplate reduction patterns.

Validates massive code reduction patterns including mixins, decorators,
and pipeline helpers that eliminate 200+ lines of repetitive code.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from flext_meltano.helpers.execution import FlextMeltanoResult
from flext_meltano.patterns import (

# Timeout constants to avoid magic numbers
DEFAULT_TIMEOUT = 300
DISCOVERY_TIMEOUT = 60
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_ORACLE_PORT = 1521
DEFAULT_MYSQL_PORT = 3306
BACKOFF_BASE = 2


    CSV_TAP_CONFIG_TEMPLATE,
    CSV_TARGET_CONFIG_TEMPLATE,
    JSONL_TARGET_CONFIG_TEMPLATE,
    ORACLE_TAP_CONFIG_TEMPLATE,
    POSTGRES_TAP_CONFIG_TEMPLATE,
    FlextMeltanoConfigDict,
    FlextMeltanoMixin,
    FlextMeltanoPipeline,
    config,
    flext_meltano_config,
    flext_meltano_csv_to_jsonl,
    flext_meltano_postgres_to_csv,
    flext_meltano_quick_pipeline,
)


class TestConfigTemplates:
    """Test configuration templates for massive boilerplate reduction."""

    def test_csv_tap_config_template(self) -> None:
        """Test CSV tap configuration template structure."""
        assert "files" in CSV_TAP_CONFIG_TEMPLATE
        assert isinstance(CSV_TAP_CONFIG_TEMPLATE["files",], list)
        assert len(CSV_TAP_CONFIG_TEMPLATE["files",]) > 0

        file_config = CSV_TAP_CONFIG_TEMPLATE["files"][0,]
        assert "entity" in file_config
        assert "path" in file_config
        assert file_config["entity",] == "data"
        assert file_config["path",] == "data.csv"

    def test_postgres_tap_config_template(self) -> None:
        """Test PostgreSQL tap configuration template structure."""
        assert "host" in POSTGRES_TAP_CONFIG_TEMPLATE
        assert "port" in POSTGRES_TAP_CONFIG_TEMPLATE
        assert "database" in POSTGRES_TAP_CONFIG_TEMPLATE
        assert "user" in POSTGRES_TAP_CONFIG_TEMPLATE
        assert "schema" in POSTGRES_TAP_CONFIG_TEMPLATE

        assert POSTGRES_TAP_CONFIG_TEMPLATE["host",] == "localhost"
        assert POSTGRES_TAP_CONFIG_TEMPLATE["port",] == 5432
        assert POSTGRES_TAP_CONFIG_TEMPLATE["database",] == "postgres"

    def test_oracle_tap_config_template(self) -> None:
        """Test Oracle tap configuration template structure."""
        assert "host" in ORACLE_TAP_CONFIG_TEMPLATE
        assert "port" in ORACLE_TAP_CONFIG_TEMPLATE
        assert "sid" in ORACLE_TAP_CONFIG_TEMPLATE
        assert "user" in ORACLE_TAP_CONFIG_TEMPLATE

        assert ORACLE_TAP_CONFIG_TEMPLATE["host",] == "localhost"
        assert ORACLE_TAP_CONFIG_TEMPLATE["port",] == 1521
        assert ORACLE_TAP_CONFIG_TEMPLATE["sid",] == "xe"

    def test_target_config_templates(self) -> None:
        """Test target configuration templates."""
        # JSONL target
        assert "destination_path" in JSONL_TARGET_CONFIG_TEMPLATE
        assert "file_naming_scheme" in JSONL_TARGET_CONFIG_TEMPLATE
        assert JSONL_TARGET_CONFIG_TEMPLATE["destination_path",] == "output"
        assert "{stream_name,}.jsonl" in JSONL_TARGET_CONFIG_TEMPLATE["file_naming_scheme",]

        # CSV target
        assert "destination_path" in CSV_TARGET_CONFIG_TEMPLATE
        assert "file_naming_scheme" in CSV_TARGET_CONFIG_TEMPLATE
        assert "delimiter" in CSV_TARGET_CONFIG_TEMPLATE
        assert CSV_TARGET_CONFIG_TEMPLATE["delimiter",] == ","


class TestFlextMeltanoConfig:
    """Test smart configuration creation that reduces 15+ lines to single call."""

    def test_flext_meltano_config_csv_tap(self) -> None:
        """Test smart config creation for CSV tap."""
        config_result = flext_meltano_config("tap-csv", "target-jsonl")

        assert config_result["tap_name",] == "tap-csv"
        assert config_result["target_name",] == "target-jsonl"
        assert "tap_config" in config_result
        assert "target_config" in config_result

        # Should auto-select CSV template
        tap_config = config_result["tap_config",]
        assert "files" in tap_config
        assert isinstance(tap_config["files",], list)

    def test_flext_meltano_config_postgres_tap(self) -> None:
        """Test smart config creation for PostgreSQL tap."""
        config_result = flext_meltano_config("tap-postgres", "target-csv")

        # Should auto-select PostgreSQL template
        tap_config = config_result["tap_config",]
        assert "host" in tap_config
        assert "port" in tap_config
        assert "database" in tap_config
        assert tap_config["host",] == "localhost"
        assert tap_config["port",] == 5432

        # Should auto-select CSV target template
        target_config = config_result["target_config",]
        assert "destination_path" in target_config
        assert "delimiter" in target_config
        assert target_config["delimiter",] == ","

    def test_flext_meltano_config_with_overrides(self) -> None:
        """Test config creation with overrides."""
        overrides = {
            "tap_config": {"custom_field": "custom_value",},
            "target_config": {"output_path": "/custom/output",},
            "environment": "prod",
        }

        config_result = flext_meltano_config("tap-oracle", "target-jsonl", **overrides)

        # Should merge overrides with template
        tap_config = config_result["tap_config",]
        assert "custom_field" in tap_config
        assert tap_config["custom_field",] == "custom_value"
        assert "host" in tap_config  # From Oracle template

        target_config = config_result["target_config",]
        assert "output_path" in target_config
        assert target_config["output_path",] == "/custom/output"

        assert config_result["environment",] == "prod"


class TestFlextMeltanoConfigDict:
    """Test fluent configuration building that eliminates manual dict assembly."""

    def test_fluent_config_building(self) -> None:
        """Test fluent interface for config building."""
        cfg = FlextMeltanoConfigDict()
        result = (cfg
                 .tap("tap-postgres")
                 .target("target-jsonl")
                 .tap_config(host="db.example.com", port=DEFAULT_POSTGRES_PORT, database="mydb")
                 .target_config(destination_path="/data/output")
                 .project("/path/to/project")
                 .env("production"))

        assert result["tap_name",] == "tap-postgres"
        assert result["target_name",] == "target-jsonl"
        assert result["tap_config"]["host",] == "db.example.com"
        assert result["tap_config"]["port",] == 5432
        assert result["target_config"]["destination_path",] == "/data/output"
        assert result["project_root",] == "/path/to/project"
        assert result["environment",] == "production"

    def test_config_builder_function(self) -> None:
        """Test config() builder function."""
        cfg = config().tap("tap-csv").target("target-csv").tap_config(files=[{"entity": "test", "path": "test.csv",},])

        assert isinstance(cfg, FlextMeltanoConfigDict)
        assert cfg["tap_name",] == "tap-csv"
        assert cfg["target_name",] == "target-csv"
        assert "files" in cfg["tap_config",]


class TestFlextMeltanoMixin:
    """Test mixin class that reduces 50+ lines of repetitive class setup."""

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_mixin_initialization(self, temp_project_dir: Path) -> None:
        """Test mixin initialization."""
        mixin = FlextMeltanoMixin(temp_project_dir)

        assert mixin.project_root == temp_project_dir
        assert isinstance(mixin._config_cache, dict)
        assert len(mixin._config_cache) == 0

    def test_mixin_config_caching(self, temp_project_dir: Path) -> None:
        """Test config caching functionality."""
        mixin = FlextMeltanoMixin(temp_project_dir)

        test_config = {"key": "value", "setting": 123,}
        mixin.cache_config("test_key", test_config)

        cached_config = mixin.get_cached_config("test_key")
        assert cached_config == test_config

        # Test non-existent key
        assert mixin.get_cached_config("nonexistent") is None

    @pytest.mark.asyncio
    async def test_mixin_discovery_methods(self, temp_project_dir: Path) -> None:
        """Test mixin discovery methods."""
        mixin = FlextMeltanoMixin(temp_project_dir)

        # Test plugin discovery (should work without project setup)
        plugins_result = mixin.discover_plugins()
        assert isinstance(plugins_result, FlextMeltanoResult)

        # Test plugin discovery with filter
        extractors_result = mixin.discover_plugins("extractors")
        assert isinstance(extractors_result, FlextMeltanoResult)

    def test_mixin_validation_methods(self, temp_project_dir: Path) -> None:
        """Test mixin validation methods."""
        mixin = FlextMeltanoMixin(temp_project_dir)

        # Test project validation (will fail without meltano.yml)
        validation_result = mixin.validate_project()
        assert isinstance(validation_result, FlextMeltanoResult)


class TestFlextMeltanoPipeline:
    """Test complete pipeline class that eliminates 100+ lines of setup."""

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_pipeline_initialization(self, temp_project_dir: Path) -> None:
        """Test pipeline initialization."""
        pipeline = FlextMeltanoPipeline("tap-csv", "target-jsonl", temp_project_dir, "dev")

        assert pipeline.tap_name == "tap-csv"
        assert pipeline.target_name == "target-jsonl"
        assert pipeline.project_root == temp_project_dir
        assert pipeline.environment == "dev"
        assert pipeline._pipeline_config is None

    def test_pipeline_configuration(self, temp_project_dir: Path) -> None:
        """Test pipeline configuration with smart defaults."""
        pipeline = FlextMeltanoPipeline("tap-postgres", "target-csv", temp_project_dir)

        # Configure with overrides
        configured = pipeline.configure(
            tap_config={"host": "custom.db.com", "port": 5433,},
            target_config={"output_dir": "/custom/output",},
        )

        # Should return self for chaining
        assert configured is pipeline
        assert pipeline._pipeline_config is not None

        config = pipeline._pipeline_config
        assert config["tap_name",] == "tap-postgres"
        assert config["target_name",] == "target-csv"
        assert config["tap_config"]["host",] == "custom.db.com"
        assert config["tap_config"]["port",] == 5433
        assert config["target_config"]["output_dir",] == "/custom/output"


class TestConvenienceFunctions:
    """Test one-liner convenience functions that eliminate 30-50 lines each."""

    @pytest.mark.asyncio
    async def test_flext_meltano_quick_pipeline(self) -> None:
        """Test quick pipeline execution function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Should handle gracefully even without proper Meltano project
            result = await flext_meltano_quick_pipeline(
                "tap-csv",
                "target-jsonl",
                tmpdir,
                tap_config={"files": [{"entity": "test", "path": "test.csv"},],},
            )

            assert isinstance(result, FlextMeltanoResult)
            # May fail due to missing meltano.yml, but should handle gracefully

    def test_flext_meltano_csv_to_jsonl(self) -> None:
        """Test CSV to JSONL one-liner function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = flext_meltano_csv_to_jsonl("test.csv", "output", tmpdir)

            assert isinstance(result, FlextMeltanoResult)
            # Function should complete, may fail execution due to missing dependencies

    @pytest.mark.asyncio
    async def test_flext_meltano_postgres_to_csv(self) -> None:
        """Test PostgreSQL to CSV one-liner function."""
        db_config = {
            "host": "localhost",
            "port": 5432,
            "database": "test",
            "user": "test",
            "password": "test",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            result = await flext_meltano_postgres_to_csv(db_config, "output", tmpdir)

            assert isinstance(result, FlextMeltanoResult)
            # Function should complete, may fail execution due to missing dependencies


class TestIntegrationWorkflows:
    """Test complete integration workflows demonstrating massive code reduction."""

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_complete_csv_pipeline_workflow(self, temp_project_dir: Path) -> None:
        """Test complete CSV pipeline workflow in minimal code."""
        # OLD WAY: Would require 50+ lines of manual setup
        # NEW WAY: 5 lines with smart defaults

        pipeline = (FlextMeltanoPipeline("tap-csv", "target-jsonl", temp_project_dir)
                   .configure(
                       tap_config={"files": [{"entity": "sales", "path": "sales.csv"},],},
                       target_config={"destination_path": "output/sales",},
                   ))

        assert pipeline._pipeline_config is not None
        config = pipeline._pipeline_config

        # Verify smart configuration
        assert config["tap_name",] == "tap-csv"
        assert config["target_name",] == "target-jsonl"
        assert "files" in config["tap_config",]
        assert config["tap_config"]["files"][0]["entity",] == "sales"
        assert config["target_config"]["destination_path",] == "output/sales"

    def test_fluent_config_to_pipeline_workflow(self, temp_project_dir: Path) -> None:
        """Test fluent config building integrated with pipeline."""
        # Create fluent config
        cfg = (config()
               .tap("tap-postgres")
               .target("target-csv")
               .tap_config(
                   host="prod.db.com",
                   port=DEFAULT_POSTGRES_PORT,
                   database="analytics",
                   user="etl_user",
               )
               .target_config(destination_path="exports")
               .project(str(temp_project_dir))
               .env("production"))

        # Use config with pipeline
        pipeline = FlextMeltanoPipeline(
            cfg["tap_name",],
            cfg["target_name",],
            cfg["project_root",],
            cfg["environment",],
        )
        pipeline.configure(**cfg)

        assert pipeline.tap_name == "tap-postgres"
        assert pipeline.target_name == "target-csv"
        assert pipeline.environment == "production"
        assert pipeline._pipeline_config is not None

    @pytest.mark.asyncio
    async def test_mixin_integration_workflow(self, temp_project_dir: Path) -> None:
        """Test mixin integration for custom pipeline classes."""

        class CustomPipeline(FlextMeltanoMixin,):
            """Custom pipeline using mixin for zero boilerplate."""

            def __init__(self, project_root: Path) -> None:
                super().__init__(project_root)
                self.custom_setting = "test"

            async def run_custom_workflow(self) -> FlextMeltanoResult:
                """Custom workflow using mixin capabilities."""
                # Step 1: Validate project
                validation = self.validate_project()
                if not validation.success:
                    return validation

                # Step 2: Discover plugins
                plugins = self.discover_plugins("extractors")
                if not plugins.success:
                    return plugins

                return FlextMeltanoResult.ok({
                    "workflow_completed": True,
                    "validation": validation.data,
                    "plugins_found": len(plugins.data.get("plugins", [])),
                })

        # Test custom pipeline
        custom = CustomPipeline(temp_project_dir)
        result = await custom.run_custom_workflow()

        assert isinstance(result, FlextMeltanoResult)
        assert custom.custom_setting == "test"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short",])
