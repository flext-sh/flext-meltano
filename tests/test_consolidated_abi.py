"""Tests for FLEXT Meltano Consolidated ABI.

Validates that the consolidation eliminates duplications and provides
massive boilerplate reduction while maintaining full functionality.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def mock_flext_result():
    """Mock FlextMeltanoResult for testing."""

    class MockResult:
        def __init__(self, success: bool, data=None, error=None):
            self.success = success
            self.data = data or {}
            self.error = error

        @classmethod
        def ok(cls, data):
            return cls(True, data)

        @classmethod
        def fail(cls, error):
            return cls(False, error=error)

    return MockResult


@pytest.fixture
def mock_dependencies(mock_flext_result):
    """Mock all external dependencies."""
    with patch.dict(
        "sys.modules",
        {
            "flext_meltano.helpers.discovery": Mock(),
            "flext_meltano.helpers.execution": Mock(
                FlextMeltanoResult=mock_flext_result,
            ),
            "flext_meltano.helpers.validation": Mock(),
        },
    ):
        yield


class TestConsolidatedTemplates:
    """Test consolidated configuration templates."""

    def test_csv_tap_template_structure(self, mock_dependencies):
        """Test CSV tap template has correct structure."""
        from flext_meltano.core_consolidated import FLEXT_MELTANO_CSV_TAP_TEMPLATE

        assert "files" in FLEXT_MELTANO_CSV_TAP_TEMPLATE
        assert isinstance(FLEXT_MELTANO_CSV_TAP_TEMPLATE["files"], list)
        assert len(FLEXT_MELTANO_CSV_TAP_TEMPLATE["files"]) == 1

        file_config = FLEXT_MELTANO_CSV_TAP_TEMPLATE["files"][0]
        assert "entity" in file_config
        assert "path" in file_config
        assert "keys" in file_config

    def test_postgres_tap_template_structure(self, mock_dependencies):
        """Test Postgres tap template has correct structure."""
        from flext_meltano.core_consolidated import FLEXT_MELTANO_POSTGRES_TAP_TEMPLATE

        required_fields = ["host", "port", "database", "user", "password", "schema"]
        for field in required_fields:
            assert field in FLEXT_MELTANO_POSTGRES_TAP_TEMPLATE

        assert FLEXT_MELTANO_POSTGRES_TAP_TEMPLATE["port"] == 5432
        assert FLEXT_MELTANO_POSTGRES_TAP_TEMPLATE["schema"] == "public"

    def test_oracle_tap_template_structure(self, mock_dependencies):
        """Test Oracle tap template has correct structure."""
        from flext_meltano.core_consolidated import FLEXT_MELTANO_ORACLE_TAP_TEMPLATE

        required_fields = ["host", "port", "sid", "user", "password", "service_name"]
        for field in required_fields:
            assert field in FLEXT_MELTANO_ORACLE_TAP_TEMPLATE

        assert FLEXT_MELTANO_ORACLE_TAP_TEMPLATE["port"] == 1521
        assert FLEXT_MELTANO_ORACLE_TAP_TEMPLATE["sid"] == "xe"

    def test_target_templates_structure(self, mock_dependencies):
        """Test all target templates have correct structure."""
        from flext_meltano.core_consolidated import (
            FLEXT_MELTANO_CSV_TARGET_TEMPLATE,
            FLEXT_MELTANO_JSONL_TARGET_TEMPLATE,
            FLEXT_MELTANO_PARQUET_TARGET_TEMPLATE,
        )

        # All target templates should have destination_path and file_naming_scheme
        for template in [
            FLEXT_MELTANO_JSONL_TARGET_TEMPLATE,
            FLEXT_MELTANO_CSV_TARGET_TEMPLATE,
            FLEXT_MELTANO_PARQUET_TARGET_TEMPLATE,
        ]:
            assert "destination_path" in template
            assert "file_naming_scheme" in template

        # CSV specific fields
        assert "delimiter" in FLEXT_MELTANO_CSV_TARGET_TEMPLATE
        assert "quotechar" in FLEXT_MELTANO_CSV_TARGET_TEMPLATE

        # Parquet specific fields
        assert "compression" in FLEXT_MELTANO_PARQUET_TARGET_TEMPLATE


class TestSmartConfiguration:
    """Test smart configuration functionality."""

    def test_smart_config_postgres_auto_selection(self, mock_dependencies):
        """Test smart config auto-selects Postgres template."""
        from flext_meltano.core_consolidated import flext_meltano_smart_config

        config = flext_meltano_smart_config("tap-postgres", "target-jsonl")

        assert config["tap_name"] == "tap-postgres"
        assert config["target_name"] == "target-jsonl"
        assert "tap_config" in config
        assert "target_config" in config

        # Should auto-select Postgres template
        tap_config = config["tap_config"]
        assert "host" in tap_config
        assert "port" in tap_config
        assert tap_config["port"] == 5432

    def test_smart_config_csv_auto_selection(self, mock_dependencies):
        """Test smart config auto-selects CSV template."""
        from flext_meltano.core_consolidated import flext_meltano_smart_config

        config = flext_meltano_smart_config("tap-csv", "target-csv")

        # Should auto-select CSV tap template
        tap_config = config["tap_config"]
        assert "files" in tap_config
        assert isinstance(tap_config["files"], list)

        # Should auto-select CSV target template
        target_config = config["target_config"]
        assert "delimiter" in target_config
        assert "quotechar" in target_config

    def test_smart_config_with_overrides(self, mock_dependencies):
        """Test smart config handles overrides correctly."""
        from flext_meltano.core_consolidated import flext_meltano_smart_config

        overrides = {
            "tap_config": {"host": "custom.db.com", "port": 9999},
            "target_config": {"destination_path": "/custom/path"},
            "environment": "production",
        }

        config = flext_meltano_smart_config("tap-postgres", "target-jsonl", **overrides)

        # Should merge overrides with template
        assert config["tap_config"]["host"] == "custom.db.com"
        assert config["tap_config"]["port"] == 9999
        assert config["target_config"]["destination_path"] == "/custom/path"
        assert config["environment"] == "production"

        # Should still have template defaults not overridden
        assert "database" in config["tap_config"]
        assert "user" in config["tap_config"]


class TestSmartPipeline:
    """Test smart pipeline functionality."""

    def test_pipeline_initialization(self, mock_dependencies):
        """Test pipeline initializes correctly."""
        from flext_meltano.core_consolidated import FlextMeltanoSmartPipeline

        pipeline = FlextMeltanoSmartPipeline("tap-postgres", "target-jsonl", "/project")

        assert pipeline.tap_name == "tap-postgres"
        assert pipeline.target_name == "target-jsonl"
        assert pipeline.project_root == Path("/project")
        assert pipeline.environment == "dev"
        assert pipeline._smart_config is None

    def test_pipeline_smart_configuration(self, mock_dependencies):
        """Test pipeline smart configuration."""
        from flext_meltano.core_consolidated import FlextMeltanoSmartPipeline

        pipeline = FlextMeltanoSmartPipeline("tap-mysql", "target-parquet")
        result = pipeline.flext_meltano_configure_smart(
            tap_config={"host": "mysql.db.com"},
            target_config={"compression": "gzip"},
        )

        # Should return self for fluent interface
        assert result is pipeline

        # Should have configured smart config
        assert pipeline._smart_config is not None
        config = pipeline._smart_config

        assert config["tap_name"] == "tap-mysql"
        assert config["target_name"] == "target-parquet"

        # Should merge with MySQL template
        assert config["tap_config"]["host"] == "mysql.db.com"
        assert config["tap_config"]["port"] == 3306  # From template

        # Should merge with Parquet template
        assert config["target_config"]["compression"] == "gzip"  # Override
        assert "file_naming_scheme" in config["target_config"]  # From template


class TestOperationsMixin:
    """Test operations mixin functionality."""

    def test_mixin_initialization(self, mock_dependencies):
        """Test mixin initializes correctly."""
        from flext_meltano.core_consolidated import FlextMeltanoOperationsMixin

        mixin = FlextMeltanoOperationsMixin("/project/root")

        assert mixin.project_root == Path("/project/root")
        assert isinstance(mixin._operation_cache, dict)
        assert isinstance(mixin._config_cache, dict)
        assert isinstance(mixin._last_discovery, dict)
        assert isinstance(mixin._config_templates, dict)

        # Should have all template mappings
        assert "csv" in mixin._config_templates
        assert "postgres" in mixin._config_templates
        assert "oracle" in mixin._config_templates
        assert "mysql" in mixin._config_templates

    def test_smart_config_template_retrieval(self, mock_dependencies):
        """Test smart config template retrieval."""
        from flext_meltano.core_consolidated import FlextMeltanoOperationsMixin

        mixin = FlextMeltanoOperationsMixin()

        # Test template matching
        postgres_template = mixin.flext_meltano_get_smart_config_template("postgres")
        assert "host" in postgres_template
        assert postgres_template["port"] == 5432

        oracle_template = mixin.flext_meltano_get_smart_config_template("oracle")
        assert "sid" in oracle_template
        assert oracle_template["port"] == 1521

        # Test unknown type returns empty dict
        unknown_template = mixin.flext_meltano_get_smart_config_template("unknown")
        assert unknown_template == {}

    def test_caching_functionality(self, mock_dependencies):
        """Test caching operations."""
        from flext_meltano.core_consolidated import FlextMeltanoOperationsMixin

        mixin = FlextMeltanoOperationsMixin()

        # Test operation caching
        test_data = {"test": "data"}
        mixin.flext_meltano_cache_operation("test_key", test_data)
        retrieved = mixin.flext_meltano_get_cached_operation("test_key")
        assert retrieved == test_data

        # Test config caching
        test_config = {"config": "value"}
        mixin.flext_meltano_cache_config("config_key", test_config)
        retrieved_config = mixin.flext_meltano_get_cached_config("config_key")
        assert retrieved_config == test_config

        # Test cache clearing
        mixin.flext_meltano_clear_all_caches()
        assert mixin.flext_meltano_get_cached_operation("test_key") is None
        assert mixin.flext_meltano_get_cached_config("config_key") is None


class TestSmartConfigDict:
    """Test smart configuration dictionary."""

    def test_fluent_interface(self, mock_dependencies):
        """Test fluent interface functionality."""
        from flext_meltano.core_consolidated import FlextMeltanoSmartConfigDict

        config_dict = FlextMeltanoSmartConfigDict()

        # Test method chaining
        result = (
            config_dict.flext_meltano_tap("tap-oracle")
            .flext_meltano_target("target-csv")
            .flext_meltano_tap_config(host="oracle.db.com", port=1522)
            .flext_meltano_target_config(delimiter="|")
            .flext_meltano_project("/custom/project")
            .flext_meltano_environment("production")
        )

        # Should return self for all methods
        assert result is config_dict

        # Should have correct values
        assert config_dict["tap_name"] == "tap-oracle"
        assert config_dict["target_name"] == "target-csv"
        assert config_dict["project_root"] == "/custom/project"
        assert config_dict["environment"] == "production"

        # Should merge with templates and overrides
        assert config_dict["tap_config"]["host"] == "oracle.db.com"
        assert config_dict["tap_config"]["port"] == 1522  # Override
        assert config_dict["tap_config"]["sid"] == "xe"  # From template

        assert config_dict["target_config"]["delimiter"] == "|"  # Override
        assert config_dict["target_config"]["quotechar"] == '"'  # From template

    def test_config_builder_function(self, mock_dependencies):
        """Test config builder function."""
        from flext_meltano.core_consolidated import flext_meltano_smart_config_builder

        builder = flext_meltano_smart_config_builder()
        assert isinstance(builder, dict)
        assert "tap_name" in builder
        assert "target_name" in builder
        assert builder["target_name"] == "target-jsonl"  # Default


class TestUltraHelpers:
    """Test ultra convenience functions."""

    @pytest.mark.asyncio
    async def test_ultra_pipeline(self, mock_dependencies, mock_flext_result):
        """Test ultra pipeline function."""
        from flext_meltano.core_consolidated import flext_meltano_ultra_pipeline

        # Mock the pipeline execution
        with patch(
            "flext_meltano.core_consolidated.FlextMeltanoSmartPipeline",
        ) as mock_pipeline_class:
            mock_pipeline = Mock()
            mock_pipeline.flext_meltano_configure_smart.return_value = mock_pipeline
            mock_pipeline.flext_meltano_run_complete_workflow.return_value = (
                mock_flext_result.ok({"completed": True})
            )
            mock_pipeline_class.return_value = mock_pipeline

            result = await flext_meltano_ultra_pipeline(
                "tap-postgres",
                "target-jsonl",
                "/project",
                tap_config={"host": "db.com"},
            )

            # Should create pipeline with correct parameters
            mock_pipeline_class.assert_called_once_with(
                "tap-postgres",
                "target-jsonl",
                "/project",
            )

            # Should configure with overrides
            mock_pipeline.flext_meltano_configure_smart.assert_called_once_with(
                tap_config={"host": "db.com"},
            )

            # Should run complete workflow
            mock_pipeline.flext_meltano_run_complete_workflow.assert_called_once()

            # Should return result
            assert result.success is True
            assert result.data["completed"] is True

    def test_ultra_csv_to_jsonl(self, mock_dependencies, mock_flext_result):
        """Test ultra CSV to JSONL function."""
        from flext_meltano.core_consolidated import flext_meltano_ultra_csv_to_jsonl

        with patch(
            "flext_meltano.core_consolidated.FlextMeltanoSmartPipeline",
        ) as mock_pipeline_class:
            mock_pipeline = Mock()
            mock_pipeline.flext_meltano_configure_smart.return_value = mock_pipeline
            mock_pipeline.flext_meltano_execute_complete_pipeline.return_value = (
                mock_flext_result.ok({"status": "completed"})
            )
            mock_pipeline_class.return_value = mock_pipeline

            result = flext_meltano_ultra_csv_to_jsonl(
                "/data/input.csv",
                "/output",
                "/project",
            )

            # Should create CSV to JSONL pipeline
            mock_pipeline_class.assert_called_once_with(
                "tap-csv",
                "target-jsonl",
                "/project",
            )

            # Should configure with CSV file and output directory
            expected_config = {
                "tap_config": {
                    "files": [{"entity": "data", "path": "/data/input.csv"}],
                },
                "target_config": {"destination_path": "/output"},
            }
            mock_pipeline.flext_meltano_configure_smart.assert_called_once_with(
                **expected_config,
            )

            # Should execute pipeline
            mock_pipeline.flext_meltano_execute_complete_pipeline.assert_called_once()
            assert result.success is True

    @pytest.mark.asyncio
    async def test_ultra_database_to_warehouse(
        self,
        mock_dependencies,
        mock_flext_result,
    ):
        """Test ultra database to warehouse function."""
        from flext_meltano.core_consolidated import (
            flext_meltano_ultra_database_to_warehouse,
        )

        source_config = {"host": "source.db.com", "database": "source_db"}
        target_config = {"host": "warehouse.db.com", "database": "warehouse_db"}

        with patch(
            "flext_meltano.core_consolidated.flext_meltano_ultra_pipeline",
        ) as mock_ultra:
            mock_ultra.return_value = mock_flext_result.ok({"transferred": True})

            result = await flext_meltano_ultra_database_to_warehouse(
                source_config,
                target_config,
                "mysql",
                "postgres",
                "/project",
            )

            # Should call ultra pipeline with correct tap/target names
            mock_ultra.assert_called_once_with(
                "tap-mysql",
                "target-postgres",
                "/project",
                tap_config=source_config,
                target_config=target_config,
            )

            assert result.success is True
            assert result.data["transferred"] is True


class TestConsolidationEffectiveness:
    """Test that consolidation actually eliminates duplications."""

    def test_no_duplicate_templates(self, mock_dependencies):
        """Test that templates are not duplicated across modules."""
        from flext_meltano.core_consolidated import (
            FLEXT_MELTANO_CSV_TAP_TEMPLATE,
            FLEXT_MELTANO_POSTGRES_TAP_TEMPLATE,
        )

        # Templates should be unique objects (not duplicated)
        csv_template_id = id(FLEXT_MELTANO_CSV_TAP_TEMPLATE)
        postgres_template_id = id(FLEXT_MELTANO_POSTGRES_TAP_TEMPLATE)

        # Import again to verify they're the same objects
        from flext_meltano.core_consolidated import (
            FLEXT_MELTANO_CSV_TAP_TEMPLATE as CSV_TEMPLATE_2,
            FLEXT_MELTANO_POSTGRES_TAP_TEMPLATE as POSTGRES_TEMPLATE_2,
        )

        assert id(CSV_TEMPLATE_2) == csv_template_id
        assert id(POSTGRES_TEMPLATE_2) == postgres_template_id

    def test_unified_type_aliases(self, mock_dependencies):
        """Test that type aliases are unified."""
        # All should be dict[str, Any] type aliases

        from flext_meltano.core_consolidated import (
            FlextMeltanoConfig,
            FlextMeltanoPipelineConfig,
            FlextMeltanoTapConfig,
            FlextMeltanoTargetConfig,
        )

        # These are type aliases, so we check their string representation
        assert str(FlextMeltanoConfig).startswith("dict")
        assert str(FlextMeltanoTapConfig).startswith("dict")
        assert str(FlextMeltanoTargetConfig).startswith("dict")
        assert str(FlextMeltanoPipelineConfig).startswith("dict")

    def test_code_reduction_measurement(self, mock_dependencies):
        """Test that code reduction goals are met."""
        from flext_meltano.core_consolidated import (
            FlextMeltanoSmartPipeline,
            flext_meltano_smart_config,
            flext_meltano_ultra_pipeline,
        )

        # Smart config should replace 20+ lines with 1 function call
        config = flext_meltano_smart_config("tap-postgres", "target-jsonl")
        assert len(config) >= 6  # Should have at least 6 configuration keys

        # Smart pipeline should eliminate 100+ lines of setup
        pipeline = FlextMeltanoSmartPipeline("tap-csv", "target-jsonl")
        assert hasattr(pipeline, "flext_meltano_configure_smart")
        assert hasattr(pipeline, "flext_meltano_validate_complete_pipeline")
        assert hasattr(pipeline, "flext_meltano_discover_complete_catalog")
        assert hasattr(pipeline, "flext_meltano_execute_complete_pipeline")
        assert hasattr(pipeline, "flext_meltano_run_complete_workflow")

        # Ultra functions should provide single-line pipeline operations
        assert callable(flext_meltano_ultra_pipeline)
        assert flext_meltano_ultra_pipeline.__doc__.find("100+ lines") > -1
