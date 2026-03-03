"""FLEXT Meltano Test Configuration - Enterprise testing standards.

This module provides pytest fixtures and configuration for testing flext-meltano
using real Meltano projects and flext-core patterns with enterprise testing standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any, Protocol

import pytest
import yaml

from flext_meltano import t
from tests.helpers.docker_test_manager import FlextTestsDocker


class CliRunnerProtocol(Protocol):
    """Protocol for CLI runner interface."""

    def invoke(
        self,
        *args: t.JsonValue,
        **kwargs: t.JsonValue,
    ) -> t.JsonValue:
        """Invoke CLI command."""


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "DEBUG"
    os.environ["MELTANO_ENVIRONMENT"] = "test"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)
    os.environ.pop("MELTANO_ENVIRONMENT", None)


# Meltano project fixtures
@pytest.fixture
def test_meltano_project_dir() -> Generator[Path]:
    """Temporary Meltano project directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir) / "test_meltano_project"
        project_dir.mkdir()
        yield project_dir


@pytest.fixture
def meltano_yml_config() -> dict[str, t.JsonValue]:
    """Sample pipeline.yml configuration for testing."""
    return {
        "version": 1,
        "default_environment": "test",
        "project_id": "test-project",
        "environments": [
            {
                "name": "test",
                "config": {
                    "plugins": {
                        "extractors": [
                            {
                                "name": "tap-csv",
                                "variant": "meltanolabs",
                                "pip_url": "pipelinewise-tap-csv",
                            },
                        ],
                        "loaders": [
                            {
                                "name": "target-csv",
                                "variant": "meltanolabs",
                                "pip_url": "pipelinewise-target-csv",
                            },
                        ],
                    },
                },
            },
        ],
        "plugins": {
            "extractors": [
                {
                    "name": "tap-csv",
                    "variant": "meltanolabs",
                    "pip_url": "pipelinewise-tap-csv",
                    "config": {
                        "files": [
                            {
                                "entity": "test_data",
                                "path": "test_data.csv",
                                "keys": ["id"],
                            },
                        ],
                    },
                },
            ],
            "loaders": [
                {
                    "name": "target-csv",
                    "variant": "meltanolabs",
                    "pip_url": "pipelinewise-target-csv",
                    "config": {
                        "destination_path": "output",
                    },
                },
            ],
        },
    }


@pytest.fixture
def meltano_project(
    test_meltano_project_dir: Path,
    meltano_yml_config: dict[str, t.JsonValue],
) -> dict[str, Any]:
    """Meltano project for testing."""
    # Create pipeline.yml

    meltano_yml = test_meltano_project_dir / "pipeline.yml"
    with meltano_yml.open("w", encoding="utf-8") as f:
        yaml.dump(meltano_yml_config, f)

    # Return simple dict[str, Any] instead of missing MeltanoProject class
    return {
        "name": "test-project",
        "directory": test_meltano_project_dir,
        "config_path": test_meltano_project_dir / "pipeline.yml",
        "description": "Test project for flext-meltano",
        "version": "1",
        "config": meltano_yml_config,
    }


# Plugin fixtures
@pytest.fixture
def tap_csv_config() -> dict[str, t.JsonValue]:
    """Tap CSV configuration for testing."""
    return {
        "files": [
            {
                "entity": "test_entity",
                "path": "test_data.csv",
                "keys": ["id"],
                "encoding": "utf-8",
            },
        ],
    }


@pytest.fixture
def target_csv_config() -> dict[str, t.JsonValue]:
    """Target CSV configuration for testing."""
    return {
        "destination_path": "output",
        "file_format": "csv",
        "delimiter": ",",
    }


@pytest.fixture
def sample_csv_data() -> str:
    """Sample CSV data for testing."""
    return """id,name,email,created_at
1,John Doe,john@example.com,2023-01-01
2,Jane Smith,jane@example.com,2023-01-02
3,Bob Johnson,bob@example.com,2023-01-03"""


# Meltano CLI fixtures
class MockCliRunner:
    """Mock CLI runner."""

    @staticmethod
    def invoke(
        *args: object,
        **kwargs: object,
    ) -> object:
        """Mock invoke method."""
        return type("Result", (), {"exit_code": 0, "output": ""})()


@pytest.fixture
def meltano_cli_runner() -> MockCliRunner:
    """Meltano CLI runner for testing using flext-cli patterns."""
    return MockCliRunner()


@pytest.fixture
def meltano_invoke_args() -> list[str]:
    """Common Meltano invoke arguments."""
    return ["--log-level", "debug", "--environment", "test"]


# Singer protocol fixtures
@pytest.fixture
def singer_schema() -> dict[str, t.JsonValue]:
    """Sample Singer schema for testing."""
    return {
        "type": "SCHEMA",
        "stream": "test_entity",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
            },
        },
        "key_properties": ["id"],
    }


@pytest.fixture
def singer_records() -> list[dict[str, t.JsonValue]]:
    """Sample Singer records for testing."""
    return [
        {
            "type": "RECORD",
            "stream": "test_entity",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2023-01-01T00:00:00Z",
            },
        },
        {
            "type": "RECORD",
            "stream": "test_entity",
            "record": {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "created_at": "2023-01-02T00:00:00Z",
            },
        },
    ]


@pytest.fixture
def singer_state() -> dict[str, t.JsonValue]:
    """Sample Singer state for testing."""
    return {
        "type": "STATE",
        "value": {
            "bookmarks": {
                "test_entity": {
                    "replication_key": "created_at",
                    "replication_key_value": "2023-01-02T00:00:00Z",
                },
            },
        },
    }


# Pipeline execution fixtures
@pytest.fixture
def pipeline_execution_config() -> dict[str, t.JsonValue]:
    """Pipeline execution configuration for testing."""
    return {
        "extractor": "tap-csv",
        "loader": "target-csv",
        "transform": "skip",
        "full_refresh": False,
        "state_backend": "local",
        "job_logging_level": "debug",
    }


# Environment fixtures
@pytest.fixture
def test_environment_config() -> dict[str, t.JsonValue]:
    """Test environment configuration."""
    return {
        "name": "test",
        "config": {
            "project_id": "test-meltano-project",
            "cli": {
                "log_level": "DEBUG",
                "log_config": False,
            },
        },
    }


# Schedule fixtures
@pytest.fixture
def sample_schedule_config() -> dict[str, t.JsonValue]:
    """Sample schedule configuration."""
    return {
        "name": "daily-sync",
        "extractor": "tap-csv",
        "loader": "target-csv",
        "transform": "skip",
        "interval": "@daily",
        "start_date": "2023-01-01",
    }


# Job fixtures
@pytest.fixture
def job_run_config() -> dict[str, t.JsonValue]:
    """Job run configuration for testing."""
    return {
        "job_id": "test-job-123",
        "run_id": "test-run-456",
        "pipeline": "tap-csv-to-target-csv",
        "environment": "test",
        "started_at": "2023-01-01T00:00:00Z",
    }


# Docker fixtures for containerized testing


@pytest.fixture(scope="session")
def docker_manager() -> FlextTestsDocker:
    """Session-scoped Docker manager fixture."""
    return FlextTestsDocker(keep_running=True)
    # Cleanup will happen via atexit


@pytest.fixture
def docker_services(
    docker_manager: FlextTestsDocker,
) -> Generator[FlextTestsDocker]:
    """Function-scoped Docker services fixture."""
    with docker_manager.service_context():
        yield docker_manager


@pytest.fixture
def postgres_service(
    docker_manager: FlextTestsDocker,
) -> Generator[str | None]:
    """PostgreSQL service fixture."""
    with docker_manager.service_context(["postgres"]):
        yield docker_manager.get_service_url("postgres", 5432)


@pytest.fixture
def redis_service(
    docker_manager: FlextTestsDocker,
) -> Generator[str | None]:
    """Redis service fixture."""
    with docker_manager.service_context(["redis"]):
        yield docker_manager.get_service_url("redis", 6379)


@pytest.fixture
def meltano_service(
    docker_manager: FlextTestsDocker,
) -> Generator[str | None]:
    """Meltano service fixture."""
    with docker_manager.service_context(["meltano"]):
        yield docker_manager.get_service_url("meltano", 3000)


# Pytest markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "meltano: Meltano-specific tests")
    config.addinivalue_line("markers", "singer: Singer protocol tests")
    config.addinivalue_line("markers", "pipeline: Pipeline execution tests")
    config.addinivalue_line("markers", "cli: CLI command tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "docker: Docker-based tests")


# Mock services
class MockMeltanoService:
    """Mock Meltano service."""

    @staticmethod
    def create_project(
        _config: dict[str, t.JsonValue],
    ) -> dict[str, t.JsonValue]:
        return {"project_id": "test-project", "status": "created"}

    @staticmethod
    def install_plugin(
        _plugin_type: str,
        plugin_name: str,
    ) -> dict[str, t.JsonValue]:
        return {"plugin": plugin_name, "status": "installed"}

    @staticmethod
    def run_pipeline(_extractor: str, _loader: str) -> dict[str, t.JsonValue]:
        return {"execution_id": "test-execution", "status": "running"}


@pytest.fixture
def mock_meltano_service() -> MockMeltanoService:
    """Mock Meltano service for testing."""
    return MockMeltanoService()


class MockSingerTap:
    """Mock Singer tap."""

    def __init__(self, config: dict[str, t.JsonValue]) -> None:
        """Initialize the instance."""
        super().__init__()
        self.config = config

    def discover(self) -> dict[str, t.JsonValue]:
        _ = self.config  # Use self to avoid PLR6301
        return {"streams": [{"stream": "test_entity", "schema": {}}]}

    def extract(self) -> list[dict[str, t.JsonValue]]:
        _ = self.config  # Use self to avoid PLR6301
        return [{"type": "RECORD", "stream": "test_entity", "record": {}}]


@pytest.fixture
def mock_singer_tap() -> type[MockSingerTap]:
    """Mock Singer tap for testing."""
    return MockSingerTap


class MockSingerTarget:
    """Mock Singer target."""

    def __init__(self, config: dict[str, t.JsonValue]) -> None:
        """Initialize the instance."""
        super().__init__()
        self.config = config

    def load(
        self,
        records: list[dict[str, t.JsonValue]],
    ) -> dict[str, t.JsonValue]:
        _ = self.config  # Use self to avoid PLR6301
        return {"records_loaded": len(records), "status": "success"}


@pytest.fixture
def mock_singer_target() -> type[MockSingerTarget]:
    """Mock Singer target for testing."""
    return MockSingerTarget
