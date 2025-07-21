"""Test configuration for flext-meltano.

Provides pytest fixtures and configuration for testing Meltano integration functionality
using real Meltano projects and flext-core patterns.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "debug"
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
def meltano_yml_config() -> dict[str, Any]:
    """Sample meltano.yml configuration for testing."""
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
    meltano_yml_config: dict[str, Any],
) -> Any:
    """Meltano project for testing."""
    # Create meltano.yml
    import yaml

    from flext_meltano.domain.entities import MeltanoProject

    meltano_yml = test_meltano_project_dir / "meltano.yml"
    with open(meltano_yml, "w", encoding="utf-8") as f:
        yaml.dump(meltano_yml_config, f)

    return MeltanoProject(
        name="test-project",
        project_root=str(test_meltano_project_dir),
        meltano_file_path=str(test_meltano_project_dir / "meltano.yml"),
        meltano_version="3.0.0",
    )


# Plugin fixtures
@pytest.fixture
def tap_csv_config() -> dict[str, Any]:
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
def target_csv_config() -> dict[str, Any]:
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
@pytest.fixture
def meltano_cli_runner() -> Any:
    """Meltano CLI runner for testing."""
    from click.testing import CliRunner

    return CliRunner()


@pytest.fixture
def meltano_invoke_args() -> list[str]:
    """Common Meltano invoke arguments."""
    return ["--log-level", "debug", "--environment", "test"]


# Singer protocol fixtures
@pytest.fixture
def singer_schema() -> dict[str, Any]:
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
def singer_records() -> list[dict[str, Any]]:
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
def singer_state() -> dict[str, Any]:
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
def pipeline_execution_config() -> dict[str, Any]:
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
def test_environment_config() -> dict[str, Any]:
    """Test environment configuration."""
    return {
        "name": "test",
        "config": {
            "project_id": "test-meltano-project",
            "cli": {
                "log_level": "debug",
                "log_config": False,
            },
        },
    }


# Schedule fixtures
@pytest.fixture
def sample_schedule_config() -> dict[str, Any]:
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
def job_run_config() -> dict[str, Any]:
    """Job run configuration for testing."""
    return {
        "job_id": "test-job-123",
        "run_id": "test-run-456",
        "pipeline": "tap-csv-to-target-csv",
        "environment": "test",
        "started_at": "2023-01-01T00:00:00Z",
    }


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


# Mock services
@pytest.fixture
def mock_meltano_service() -> object:
    """Mock Meltano service for testing."""

    class MockMeltanoService:
        async def create_project(self, config: dict[str, Any]) -> dict[str, Any]:
            return {"project_id": "test-project", "status": "created"}

        async def install_plugin(
            self,
            plugin_type: str,
            plugin_name: str,
        ) -> dict[str, Any]:
            return {"plugin": plugin_name, "status": "installed"}

        async def run_pipeline(self, extractor: str, loader: str) -> dict[str, Any]:
            return {"execution_id": "test-execution", "status": "running"}

    return MockMeltanoService()


@pytest.fixture
def mock_singer_tap() -> type[object]:
    """Mock Singer tap for testing."""

    class MockSingerTap:
        def __init__(self, config: dict[str, Any]) -> None:
            self.config = config

        async def discover(self) -> dict[str, Any]:
            return {"streams": [{"stream": "test_entity", "schema": {}}]}

        async def extract(self) -> list[dict[str, Any]]:
            return [{"type": "RECORD", "stream": "test_entity", "record": {}}]

    return MockSingerTap


@pytest.fixture
def mock_singer_target() -> object:
    """Mock Singer target for testing."""

    class MockSingerTarget:
        def __init__(self, config: dict[str, Any]) -> None:
            self.config = config

        async def load(self, records: list[dict[str, Any]]) -> dict[str, Any]:
            return {"records_loaded": len(records), "status": "success"}

    return MockSingerTarget
