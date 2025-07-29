"""Comprehensive tests for FlextMeltano helpers module - Real implementations only.

Tests all helper functionality including typed configurations, Singer utilities,
and validation with actual flext-core integration.
"""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from flext_meltano.helpers import (
    FlextMeltanoConfigValidator,
    FlextMeltanoResult,
    FlextMeltanoSingerUtils,
    FlextMeltanoTypedConfig,
    create_flext_meltano_config_validator,
    create_flext_meltano_typed_dict,
    detect_plugin_type,
    normalize_plugin_name,
    validate_meltano_project_structure,
)

# =============================================================================
# FIXTURES - Real test data and configurations
# =============================================================================


@pytest.fixture
def sample_meltano_config():
    """Sample Meltano configuration for testing."""
    return {
        "version": 1,
        "default_environment": "dev",
        "project_id": "test-flext-meltano",
        "send_anonymous_usage_stats": False,
        "environments": [{"name": "dev"}, {"name": "prod"}],
        "plugins": {
            "extractors": [
                {
                    "name": "tap-postgres",
                    "namespace": "tap_postgres",
                    "executable": "tap-postgres",
                    "config": {
                        "host": "localhost",
                        "port": 5432,
                        "user": "postgres",
                        "database": "analytics",
                        "schema": "public",
                    },
                    "select": ["users.*", "orders.*"],
                    "metadata": {"replication_method": "INCREMENTAL"},
                },
            ],
            "loaders": [
                {
                    "name": "target-jsonl",
                    "namespace": "target_jsonl",
                    "executable": "target-jsonl",
                    "config": {
                        "destination_path": "./output",
                        "file_naming_scheme": "{stream_name}.jsonl",
                    },
                    "schema": {"users": {"id": "integer", "name": "string"}},
                },
            ],
            "transformers": [
                {
                    "name": "dbt-postgres",
                    "namespace": "dbt",
                    "executable": "dbt",
                    "config": {"project_dir": "./dbt"},
                    "vars": {"start_date": "2024-01-01"},
                },
            ],
        },
        "tap-postgres": {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "database": "analytics",
        },
        "target-jsonl": {"destination_path": "./output"},
    }


@pytest.fixture
def sample_singer_catalog():
    """Sample Singer catalog for testing."""
    return {
        "streams": [
            {
                "tap_stream_id": "users",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "created_at": {"type": "string", "format": "date-time"},
                    },
                },
                "metadata": [
                    {
                        "breadcrumb": [],
                        "metadata": {
                            "replication-method": "INCREMENTAL",
                            "replication-key": "id",
                        },
                    },
                ],
            },
            {
                "tap_stream_id": "orders",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "amount": {"type": "number"},
                        "status": {"type": "string"},
                    },
                },
            },
        ],
    }


@pytest.fixture
def sample_singer_output():
    """Sample Singer tap output for testing."""
    messages = [
        {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 1, "name": "Alice Johnson", "email": "alice@test.com"},
            "time_extracted": "2024-01-15T10:30:00Z",
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 2, "name": "Bob Smith", "email": "bob@test.com"},
            "time_extracted": "2024-01-15T10:31:00Z",
        },
        {
            "type": "STATE",
            "value": {
                "bookmarks": {
                    "users": {"replication_key": "id", "replication_key_value": 2},
                },
            },
        },
    ]
    return "\n".join(json.dumps(msg) for msg in messages)


# =============================================================================
# TESTS FOR TYPED CONFIGURATION
# =============================================================================


class TestFlextMeltanoTypedConfig:
    """Test typed configuration functionality with flext-core integration."""

    def test_typed_config_initialization(self) -> None:
        """Test typed config initializes correctly."""
        config = FlextMeltanoTypedConfig()

        # Should have flext-core functionality
        assert hasattr(config, "flext_safe_get")
        assert hasattr(config, "flext_safe_get_nested")

        # Should have Meltano-specific functionality
        assert hasattr(config, "_meltano_schemas")
        assert hasattr(config, "_plugin_cache")

        # Should have loaded schemas
        schemas = config.get_meltano_schemas()
        assert "tap_postgres" in schemas
        assert "tap_mysql" in schemas
        assert "target_jsonl" in schemas

    def test_typed_config_with_data(self, sample_meltano_config) -> None:
        """Test typed config with initial data."""
        config = FlextMeltanoTypedConfig(sample_meltano_config)

        # Test flext-core safe operations
        version_result = config.flext_safe_get(["version"], 0)
        assert version_result.is_success
        assert version_result.data == 1

        project_id_result = config.flext_safe_get(["project_id"], "")
        assert project_id_result.is_success
        assert project_id_result.data == "test-flext-meltano"

    def test_get_tap_config_success(self, sample_meltano_config) -> None:
        """Test getting tap configuration successfully."""
        config = FlextMeltanoTypedConfig(sample_meltano_config)

        result = config.flext_meltano_get_tap_config(
            "tap-postgres", required_fields=["host", "database"],
        )

        assert result.is_success
        tap_config = result.data
        assert tap_config["host"] == "localhost"
        assert tap_config["port"] == 5432
        assert tap_config["database"] == "analytics"

    def test_get_tap_config_missing(self) -> None:
        """Test getting missing tap configuration."""
        config = FlextMeltanoTypedConfig({})

        result = config.flext_meltano_get_tap_config("nonexistent-tap")

        assert not result.is_success
        assert "not found" in result.error

    def test_get_tap_config_missing_required_field(self, sample_meltano_config) -> None:
        """Test getting tap config with missing required field."""
        # Remove required field
        del sample_meltano_config["tap-postgres"]["host"]
        config = FlextMeltanoTypedConfig(sample_meltano_config)

        result = config.flext_meltano_get_tap_config(
            "tap-postgres", required_fields=["host", "database"],
        )

        assert not result.is_success
        assert "host" in result.error

    def test_get_target_config_success(self, sample_meltano_config) -> None:
        """Test getting target configuration successfully."""
        config = FlextMeltanoTypedConfig(sample_meltano_config)

        result = config.flext_meltano_get_target_config(
            "target-jsonl", required_fields=["destination_path"],
        )

        assert result.is_success
        target_config = result.data
        assert target_config["destination_path"] == "./output"

    def test_get_target_config_missing(self) -> None:
        """Test getting missing target configuration."""
        config = FlextMeltanoTypedConfig({})

        result = config.flext_meltano_get_target_config("nonexistent-target")

        assert not result.is_success
        assert "not found" in result.error

    def test_get_project_info(self, sample_meltano_config) -> None:
        """Test extracting project information."""
        config = FlextMeltanoTypedConfig(sample_meltano_config)

        result = config.flext_meltano_get_project_info()

        assert result.is_success
        info = result.data
        assert info["project_id"] == "test-flext-meltano"
        assert info["version"] == 1
        assert info["send_anonymous_usage_stats"] is False
        assert len(info["environments"]) == 2

    def test_get_project_info_with_defaults(self) -> None:
        """Test extracting project info with default values."""
        config = FlextMeltanoTypedConfig({})

        result = config.flext_meltano_get_project_info()

        assert result.is_success
        info = result.data
        assert info["project_id"] == "flext-meltano-project"  # Default
        assert info["version"] == 1  # Default
        assert isinstance(info["environments"], list)

    def test_validate_singer_catalog_success(self, sample_singer_catalog) -> None:
        """Test validating valid Singer catalog."""
        config = FlextMeltanoTypedConfig(sample_singer_catalog)

        result = config.flext_meltano_validate_singer_catalog()

        assert result.is_success
        assert result.data is True

    def test_validate_singer_catalog_missing_streams(self) -> None:
        """Test validating Singer catalog without streams."""
        config = FlextMeltanoTypedConfig({"version": 1})

        result = config.flext_meltano_validate_singer_catalog()

        assert not result.is_success
        assert "streams" in result.error

    def test_validate_singer_catalog_invalid_stream(self) -> None:
        """Test validating Singer catalog with invalid stream."""
        invalid_catalog = {
            "streams": [
                {"tap_stream_id": "users"},  # Missing schema
                "invalid_stream",  # Not a dict
            ],
        }
        config = FlextMeltanoTypedConfig(invalid_catalog)

        result = config.flext_meltano_validate_singer_catalog()

        assert not result.is_success
        assert "missing required field" in result.error or "must be a dictionary" in result.error

    def test_extract_plugin_configs(self, sample_meltano_config) -> None:
        """Test extracting all plugin configurations."""
        config = FlextMeltanoTypedConfig(sample_meltano_config)

        result = config.flext_meltano_extract_plugin_configs()

        assert result.is_success
        configs = result.data

        # Check taps
        assert "tap-postgres" in configs["taps"]
        tap_config = configs["taps"]["tap-postgres"]
        assert tap_config["executable"] == "tap-postgres"
        assert "config" in tap_config

        # Check targets
        assert "target-jsonl" in configs["targets"]
        target_config = configs["targets"]["target-jsonl"]
        assert target_config["executable"] == "target-jsonl"

        # Check transformers
        assert "dbt-postgres" in configs["transformers"]
        transformer_config = configs["transformers"]["dbt-postgres"]
        assert transformer_config["executable"] == "dbt"

    def test_extract_plugin_configs_empty(self) -> None:
        """Test extracting plugin configs from empty configuration."""
        config = FlextMeltanoTypedConfig({})

        result = config.flext_meltano_extract_plugin_configs()

        assert not result.is_success
        assert "No plugins configuration found" in result.error

    def test_validate_against_schema_success(self) -> None:
        """Test schema validation success."""
        config = FlextMeltanoTypedConfig()

        test_config = {"host": "localhost", "port": 5432, "user": "postgres"}
        schema = config.get_meltano_schemas()["tap_postgres"]

        result = config.validate_against_schema(test_config, schema)

        assert result.is_success
        assert result.data == test_config

    def test_validate_against_schema_missing_required(self) -> None:
        """Test schema validation with missing required field."""
        config = FlextMeltanoTypedConfig()

        test_config = {"host": "localhost"}  # Missing port, user
        schema = config.get_meltano_schemas()["tap_postgres"]

        result = config.validate_against_schema(test_config, schema)

        assert not result.is_success
        assert "Required field" in result.error

    def test_validate_against_schema_constraint_violation(self) -> None:
        """Test schema validation with constraint violation."""
        config = FlextMeltanoTypedConfig()

        test_config = {
            "host": "localhost",
            "port": 99999,  # Exceeds max port
            "user": "postgres",
            "database": "test",
        }
        schema = config.get_meltano_schemas()["tap_postgres"]

        result = config.validate_against_schema(test_config, schema)

        assert not result.is_success
        assert "port" in result.error


# =============================================================================
# TESTS FOR CONFIGURATION VALIDATOR
# =============================================================================


class TestFlextMeltanoConfigValidator:
    """Test configuration validator functionality."""

    def test_validator_initialization(self) -> None:
        """Test validator initializes correctly."""
        validator = FlextMeltanoConfigValidator()

        assert hasattr(validator, "_config_helper")
        assert hasattr(validator, "_schemas")
        assert len(validator._schemas) > 0

    def test_validate_postgres_config_success(self) -> None:
        """Test validating valid PostgreSQL configuration."""
        validator = FlextMeltanoConfigValidator()

        valid_config = {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "database": "analytics",
            "password": "secret",
            "schema": "public",
        }

        result = validator.flext_meltano_validate_tap_postgres_config(valid_config)

        assert result.is_success
        assert result.data == valid_config

    def test_validate_postgres_config_missing_required(self) -> None:
        """Test validating PostgreSQL config with missing required fields."""
        validator = FlextMeltanoConfigValidator()

        invalid_config = {
            "host": "localhost",
            # Missing port, user, database
            "password": "secret",
        }

        result = validator.flext_meltano_validate_tap_postgres_config(invalid_config)

        assert not result.is_success
        assert "Required field" in result.error

    def test_validate_mysql_config_success(self) -> None:
        """Test validating valid MySQL configuration."""
        validator = FlextMeltanoConfigValidator()

        valid_config = {
            "host": "mysql-server",
            "port": 3306,
            "user": "root",
            "database": "production",
            "password": "mysql_secret",
        }

        result = validator.flext_meltano_validate_tap_mysql_config(valid_config)

        assert result.is_success

    def test_validate_oracle_config_success(self) -> None:
        """Test validating valid Oracle configuration."""
        validator = FlextMeltanoConfigValidator()

        valid_config = {
            "host": "oracle-server",
            "port": 1521,
            "user": "system",
            "password": "oracle_password",
            "sid": "xe",
        }

        result = validator.flext_meltano_validate_tap_oracle_config(valid_config)

        assert result.is_success

    def test_validate_target_jsonl_config_success(self) -> None:
        """Test validating valid JSONL target configuration."""
        validator = FlextMeltanoConfigValidator()

        valid_config = {
            "destination_path": "/data/exports",
            "file_naming_scheme": "{stream_name}_{date}.jsonl",
            "overwrite_behavior": "replace_file",
        }

        result = validator.flext_meltano_validate_target_jsonl_config(valid_config)

        assert result.is_success

    def test_validate_target_csv_config_success(self) -> None:
        """Test validating valid CSV target configuration."""
        validator = FlextMeltanoConfigValidator()

        valid_config = {
            "destination_path": "/exports",
            "file_naming_scheme": "{stream_name}.csv",
            "delimiter": "|",
            "quotechar": "'",
        }

        result = validator.flext_meltano_validate_target_csv_config(valid_config)

        assert result.is_success

    def test_validate_any_config_success(self) -> None:
        """Test validating any configuration with known schema."""
        validator = FlextMeltanoConfigValidator()

        config = {"host": "localhost", "port": 5432, "user": "postgres", "database": "test"}

        result = validator.flext_meltano_validate_any_config(config, "tap_postgres")

        assert result.is_success

    def test_validate_any_config_unknown_schema(self) -> None:
        """Test validating config with unknown schema."""
        validator = FlextMeltanoConfigValidator()

        result = validator.flext_meltano_validate_any_config({}, "unknown_schema")

        assert not result.is_success
        assert "Unknown configuration schema" in result.error


# =============================================================================
# TESTS FOR SINGER UTILITIES
# =============================================================================


class TestFlextMeltanoSingerUtils:
    """Test Singer SDK utilities functionality."""

    def test_singer_utils_initialization(self) -> None:
        """Test Singer utils initializes correctly."""
        utils = FlextMeltanoSingerUtils()

        assert hasattr(utils, "logger")
        assert utils.logger is not None

    def test_create_singer_record_success(self) -> None:
        """Test creating valid Singer RECORD message."""
        utils = FlextMeltanoSingerUtils()

        result = utils.flext_meltano_create_singer_record(
            "users",
            {"id": 1, "name": "Alice", "email": "alice@test.com"},
            "2024-01-15T10:30:00Z",
        )

        assert result.is_success
        message = result.data
        assert message["type"] == "RECORD"
        assert message["stream"] == "users"
        assert message["record"]["id"] == 1
        assert message["time_extracted"] == "2024-01-15T10:30:00Z"

    def test_create_singer_record_invalid_stream(self) -> None:
        """Test creating Singer record with invalid stream name."""
        utils = FlextMeltanoSingerUtils()

        result = utils.flext_meltano_create_singer_record("", {"id": 1})

        assert not result.is_success
        assert "Invalid stream name" in result.error

    def test_create_singer_record_invalid_data(self) -> None:
        """Test creating Singer record with invalid data."""
        utils = FlextMeltanoSingerUtils()

        result = utils.flext_meltano_create_singer_record("users", "not_a_dict")

        assert not result.is_success
        assert "must be a dictionary" in result.error

    def test_create_singer_schema(self) -> None:
        """Test creating Singer SCHEMA message."""
        schema = {
            "type": "object",
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }

        message = FlextMeltanoSingerUtils.create_singer_schema(
            "users", schema, ["id"],
        )

        assert message["type"] == "SCHEMA"
        assert message["stream"] == "users"
        assert message["schema"] == schema
        assert message["key_properties"] == ["id"]

    def test_create_singer_state(self) -> None:
        """Test creating Singer STATE message."""
        state_data = {"bookmarks": {"users": {"replication_key_value": 100}}}

        message = FlextMeltanoSingerUtils.create_singer_state(state_data)

        assert message["type"] == "STATE"
        assert message["value"] == state_data

    def test_extract_records_from_singer_output(self, sample_singer_output) -> None:
        """Test extracting records from Singer output."""
        result = FlextMeltanoSingerUtils.extract_records_from_singer_output(
            sample_singer_output,
        )

        assert result.is_success
        records = result.data
        assert len(records) == 2
        assert records[0]["name"] == "Alice Johnson"
        assert records[1]["name"] == "Bob Smith"

    def test_extract_records_invalid_json(self) -> None:
        """Test extracting records from invalid JSON output."""
        invalid_output = '{"type": "RECORD"}\ninvalid json line\n{"type": "RECORD"}'

        result = FlextMeltanoSingerUtils.extract_records_from_singer_output(
            invalid_output,
        )

        assert not result.is_success
        assert "Invalid JSON" in result.error

    def test_validate_singer_message_record(self) -> None:
        """Test validating Singer RECORD message."""
        message = {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 1, "name": "Alice"},
        }

        result = FlextMeltanoSingerUtils.validate_singer_message(message)

        assert result.is_success
        assert result.data is True

    def test_validate_singer_message_schema(self) -> None:
        """Test validating Singer SCHEMA message."""
        message = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {"type": "object"},
        }

        result = FlextMeltanoSingerUtils.validate_singer_message(message)

        assert result.is_success

    def test_validate_singer_message_state(self) -> None:
        """Test validating Singer STATE message."""
        message = {"type": "STATE", "value": {"bookmark": "test"}}

        result = FlextMeltanoSingerUtils.validate_singer_message(message)

        assert result.is_success

    def test_validate_singer_message_invalid_format(self) -> None:
        """Test validating invalid Singer message format."""
        # Not a dictionary
        result = FlextMeltanoSingerUtils.validate_singer_message("not_a_dict")
        assert not result.is_success

        # Missing type field
        result = FlextMeltanoSingerUtils.validate_singer_message({"stream": "test"})
        assert not result.is_success

        # Unknown type
        result = FlextMeltanoSingerUtils.validate_singer_message({"type": "UNKNOWN"})
        assert not result.is_success

    def test_validate_singer_message_missing_fields(self) -> None:
        """Test validating Singer message with missing required fields."""
        # RECORD missing stream
        message = {"type": "RECORD", "record": {"id": 1}}
        result = FlextMeltanoSingerUtils.validate_singer_message(message)
        assert not result.is_success

        # SCHEMA missing schema
        message = {"type": "SCHEMA", "stream": "test"}
        result = FlextMeltanoSingerUtils.validate_singer_message(message)
        assert not result.is_success

        # STATE missing value
        message = {"type": "STATE"}
        result = FlextMeltanoSingerUtils.validate_singer_message(message)
        assert not result.is_success


# =============================================================================
# TESTS FOR UTILITY FUNCTIONS
# =============================================================================


class TestUtilityFunctions:
    """Test standalone utility functions."""

    def test_create_typed_dict_factory(self) -> None:
        """Test factory function for creating typed dictionary."""
        config = create_flext_meltano_typed_dict({"test": "value"})

        assert isinstance(config, FlextMeltanoTypedConfig)
        result = config.flext_safe_get(["test"], "")
        assert result.is_success
        assert result.data == "value"

    def test_create_config_validator_factory(self) -> None:
        """Test factory function for creating config validator."""
        validator = create_flext_meltano_config_validator()

        assert isinstance(validator, FlextMeltanoConfigValidator)

    def test_normalize_plugin_name(self) -> None:
        """Test plugin name normalization."""
        test_cases = [
            ("tap-postgres", "postgres"),
            ("target-jsonl", "jsonl"),
            ("tap_mysql", "mysql"),
            ("TARGET-CSV", "csv"),
            ("Tap-Oracle", "oracle"),
        ]

        for input_name, expected in test_cases:
            result = normalize_plugin_name(input_name)
            assert result == expected

    def test_detect_plugin_type(self) -> None:
        """Test plugin type detection."""
        test_cases = [
            ("tap-postgres", "postgres"),
            ("tap-postgresql", "postgres"),
            ("tap-mysql", "mysql"),
            ("tap-mariadb", "mysql"),
            ("tap-oracle", "oracle"),
            ("target-csv", "csv"),
            ("target-jsonl", "jsonl"),
            ("target-parquet", "parquet"),
            ("tap-unknown-source", "unknown-source"),
        ]

        for plugin_name, expected_type in test_cases:
            result = detect_plugin_type(plugin_name)
            assert result == expected_type

    def test_validate_meltano_project_structure_valid(self) -> None:
        """Test validating valid Meltano project structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create valid meltano.yml
            meltano_yml = project_path / "meltano.yml"
            config = {"version": 1, "project_id": "test"}
            with meltano_yml.open("w") as f:
                yaml.safe_dump(config, f)

            result = validate_meltano_project_structure(project_path)

            assert result.is_success
            assert result.data is True

    def test_validate_meltano_project_structure_missing_directory(self) -> None:
        """Test validating non-existent project directory."""
        result = validate_meltano_project_structure("/nonexistent/path")

        assert not result.is_success
        assert "does not exist" in result.error

    def test_validate_meltano_project_structure_missing_yml(self) -> None:
        """Test validating project without meltano.yml."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_meltano_project_structure(temp_dir)

            assert not result.is_success
            assert "meltano.yml" in result.error

    def test_validate_meltano_project_structure_invalid_yml(self) -> None:
        """Test validating project with invalid YAML."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            meltano_yml = project_path / "meltano.yml"

            # Create invalid YAML
            meltano_yml.write_text("invalid: yaml: content:")

            result = validate_meltano_project_structure(project_path)

            assert not result.is_success
            assert "Error reading meltano.yml" in result.error

    def test_validate_meltano_project_structure_invalid_config(self) -> None:
        """Test validating project with invalid configuration structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            meltano_yml = project_path / "meltano.yml"

            # Create YAML with missing required fields
            with meltano_yml.open("w") as f:
                yaml.safe_dump({"invalid": "config"}, f)

            result = validate_meltano_project_structure(project_path)

            assert not result.is_success


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestHelpersIntegration:
    """Integration tests for helpers module components."""

    def test_full_configuration_validation_flow(self, sample_meltano_config) -> None:
        """Test complete configuration validation workflow."""
        # Create typed config from sample
        config = create_flext_meltano_typed_dict(sample_meltano_config)

        # Extract tap configuration
        tap_result = config.flext_meltano_get_tap_config("tap-postgres")
        assert tap_result.is_success

        # Validate with validator
        validator = create_flext_meltano_config_validator()
        validation_result = validator.flext_meltano_validate_tap_postgres_config(
            tap_result.data,
        )
        assert validation_result.is_success

        # Extract and validate target config
        target_result = config.flext_meltano_get_target_config("target-jsonl")
        assert target_result.is_success

        target_validation = validator.flext_meltano_validate_target_jsonl_config(
            target_result.data,
        )
        assert target_validation.is_success

    def test_singer_processing_with_validation(self, sample_singer_output) -> None:
        """Test Singer message processing with validation."""
        utils = FlextMeltanoSingerUtils()

        # Extract records from output
        records_result = utils.extract_records_from_singer_output(sample_singer_output)
        assert records_result.is_success

        records = records_result.data
        assert len(records) == 2

        # Create and validate new messages from records
        for i, record in enumerate(records, 1):
            # Create new RECORD message
            record_result = utils.flext_meltano_create_singer_record(
                "users", record, f"2024-01-15T10:3{i}:00Z",
            )
            assert record_result.is_success

            # Validate the created message
            validation = utils.validate_singer_message(record_result.data)
            assert validation.is_success

    def test_project_structure_and_config_integration(self, sample_meltano_config) -> None:
        """Test project structure validation with config extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create meltano.yml with sample config
            meltano_yml = project_path / "meltano.yml"
            with meltano_yml.open("w") as f:
                yaml.safe_dump(sample_meltano_config, f)

            # Validate project structure
            structure_result = validate_meltano_project_structure(project_path)
            assert structure_result.is_success

            # Load and process the configuration
            config = create_flext_meltano_typed_dict(sample_meltano_config)

            # Extract project info
            info_result = config.flext_meltano_get_project_info()
            assert info_result.is_success

            # Extract plugin configs
            plugins_result = config.flext_meltano_extract_plugin_configs()
            assert plugins_result.is_success

            plugins = plugins_result.data
            assert len(plugins["taps"]) > 0
            assert len(plugins["targets"]) > 0
            assert len(plugins["transformers"]) > 0

    def test_error_handling_and_recovery(self) -> None:
        """Test error handling across helper components."""
        # Test with invalid configurations
        config = create_flext_meltano_typed_dict({})
        validator = create_flext_meltano_config_validator()
        utils = FlextMeltanoSingerUtils()

        # All operations should fail gracefully
        tap_result = config.flext_meltano_get_tap_config("nonexistent")
        assert not tap_result.is_success

        validation_result = validator.flext_meltano_validate_tap_postgres_config({})
        assert not validation_result.is_success

        record_result = utils.flext_meltano_create_singer_record("", {})
        assert not record_result.is_success

        # All should return FlextMeltanoResult with proper error messages
        for result in [tap_result, validation_result, record_result]:
            assert isinstance(result, FlextMeltanoResult)
            assert not result.is_success
            assert result.error
            assert isinstance(result.error, str)

    def test_type_safety_and_constraints(self) -> None:
        """Test type safety and constraint validation."""
        validator = create_flext_meltano_config_validator()

        # Test constraint violations
        invalid_configs = [
            # Port too high
            {"host": "localhost", "port": 99999, "user": "postgres", "database": "test"},
            # Empty required string
            {"host": "", "port": 5432, "user": "postgres", "database": "test"},
            # Wrong type for port
            {"host": "localhost", "port": "not_a_number", "user": "postgres", "database": "test"},
        ]

        for invalid_config in invalid_configs:
            result = validator.flext_meltano_validate_tap_postgres_config(invalid_config)
            assert not result.is_success
            assert result.error  # Should have descriptive error message
