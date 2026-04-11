"""FLEXT Meltano Test Configuration - Enterprise testing standards.

This module provides pytest fixtures and configuration for testing flext-meltano
using real Meltano projects and flext-core patterns with enterprise testing standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Callable, Generator, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

import pytest
from flext_tests import tk

from flext_core import r
from flext_meltano import FlextMeltano, meltano
from tests import u

if TYPE_CHECKING:
    from tests import t

pytest_plugins = ["flext_tests.conftest_plugin"]

type MeltanoComponentFactory = Callable[..., r[FlextMeltano]]
type MeltanoComponentSelector = Callable[[FlextMeltano], str | None]
type MeltanoComponentCase = tuple[
    MeltanoComponentFactory,
    str,
    MeltanoComponentSelector,
]


class MockCliResult:
    """Mock CLI invocation result."""

    def __init__(self, exit_code: int = 0, output: str = "") -> None:
        """Initialize the instance."""
        self.exit_code = exit_code
        self.output = output


class CliRunner(Protocol):
    """Protocol for CLI runner interface.

    Canonical definition lives in ``TestsFlextMeltanoProtocols.Meltano.Tests.CliRunner``.
    Re-exported here for backward compatibility with auto-generated ``tests/__init__.py``.
    """

    def invoke(self, *args: t.Scalar, **kwargs: t.Scalar) -> MockCliResult:
        """Invoke CLI command."""
        ...


def select_source_name(service: FlextMeltano) -> str | None:
    """Select the source name from a specialized Tap facade."""
    return service.source_name


def select_sink_name(service: FlextMeltano) -> str | None:
    """Select the sink name from a specialized Target facade."""
    return service.sink_name


def select_transformation_name(service: FlextMeltano) -> str | None:
    """Select the transformation name from a specialized DBT facade."""
    return service.transformation_name


@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "DEBUG"
    os.environ["MELTANO_ENVIRONMENT"] = "test"
    yield
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)
    os.environ.pop("MELTANO_ENVIRONMENT", None)


@pytest.fixture(
    params=[
        (meltano.Tap, "tap-csv", select_source_name),
        (meltano.Target, "target-jsonl", select_sink_name),
        (meltano.Dbt, "analytics", select_transformation_name),
    ],
    ids=["tap", "target", "dbt"],
)
def meltano_component_case(request: pytest.FixtureRequest) -> MeltanoComponentCase:
    """Canonical public Meltano component factories with expected selectors."""
    return request.param


@pytest.fixture(
    params=["version", "service_name", "status", "handlers"],
    ids=["version", "service-name", "status", "handlers"],
)
def meltano_execute_field(request: pytest.FixtureRequest) -> str:
    """Expected fields exposed by the public execute payload."""
    return str(request.param)


@pytest.fixture
def test_meltano_project_dir() -> Generator[Path]:
    """Temporary Meltano project directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir) / "test_meltano_project"
        project_dir.mkdir()
        yield project_dir


@pytest.fixture
def meltano_yml_config() -> t.ContainerMapping:
    """Sample pipeline.yml configuration for testing."""
    return {
        "version": 1,
        "default_environment": "test",
        "project_id": "test-project",
        "environments": [
            {
                "name": "test",
                "settings": {
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
                    "settings": {
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
                    "settings": {"destination_path": "output"},
                },
            ],
        },
    }


@pytest.fixture
def meltano_project(
    test_meltano_project_dir: Path,
    meltano_yml_config: t.ContainerMapping,
) -> t.ContainerMapping:
    """Meltano project for testing."""
    meltano_yml = test_meltano_project_dir / "pipeline.yml"
    u.Cli.yaml_dump(meltano_yml, meltano_yml_config)
    return {
        "name": "test-project",
        "directory": test_meltano_project_dir,
        "config_path": test_meltano_project_dir / "pipeline.yml",
        "description": "Test project for flext-meltano",
        "version": "1",
        "settings": meltano_yml_config,
    }


@pytest.fixture
def tap_csv_config() -> t.ContainerMapping:
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
def target_csv_config() -> t.ContainerMapping:
    """Target CSV configuration for testing."""
    return {"destination_path": "output", "file_format": "csv", "delimiter": ","}


@pytest.fixture
def sample_csv_data() -> str:
    """Sample CSV data for testing."""
    return "id,name,email,created_at\n1,John Doe,john@example.com,2023-01-01\n2,Jane Smith,jane@example.com,2023-01-02\n3,Bob Johnson,bob@example.com,2023-01-03"


class MockCliRunner:
    """Mock CLI runner."""

    @staticmethod
    def invoke(*args: t.Scalar, **kwargs: t.Scalar) -> MockCliResult:
        """Mock invoke method."""
        _ = args
        _ = kwargs
        return MockCliResult()


@pytest.fixture
def meltano_cli_runner() -> MockCliRunner:
    """Meltano CLI runner for testing using flext-cli patterns."""
    return MockCliRunner()


@pytest.fixture
def meltano_invoke_args() -> t.StrSequence:
    """Common Meltano invoke arguments."""
    return ["--log-level", "debug", "--environment", "test"]


@pytest.fixture
def singer_schema() -> t.ContainerMapping:
    """Sample Singer schema for testing."""
    return {
        "type": "SCHEMA",
        "stream": "test_entity",
        "schema": {
            "type": "t.NormalizedValue",
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
def singer_records() -> Sequence[t.ContainerMapping]:
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
def singer_state() -> t.ContainerMapping:
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


@pytest.fixture
def pipeline_execution_config() -> t.ContainerMapping:
    """Pipeline execution configuration for testing."""
    return {
        "extractor": "tap-csv",
        "loader": "target-csv",
        "transform": "skip",
        "full_refresh": False,
        "state_backend": "local",
        "job_logging_level": "debug",
    }


@pytest.fixture
def test_environment_config() -> t.ContainerMapping:
    """Test environment configuration."""
    return {
        "name": "test",
        "settings": {
            "project_id": "test-meltano-project",
            "cli": {"log_level": "DEBUG", "log_config": False},
        },
    }


@pytest.fixture
def sample_schedule_config() -> t.ContainerMapping:
    """Sample schedule configuration."""
    return {
        "name": "daily-sync",
        "extractor": "tap-csv",
        "loader": "target-csv",
        "transform": "skip",
        "interval": "@daily",
        "start_date": "2023-01-01",
    }


@pytest.fixture
def job_run_config() -> t.ContainerMapping:
    """Job run configuration for testing."""
    return {
        "job_id": "test-job-123",
        "run_id": "test-run-456",
        "pipeline": "tap-csv-to-target-csv",
        "environment": "test",
        "started_at": "2023-01-01T00:00:00Z",
    }


@pytest.fixture
def docker_manager(tmp_path_factory: pytest.TempPathFactory) -> tk:
    """Docker manager fixture for Docker-based tests."""
    temp_dir = tmp_path_factory.mktemp("flext_tests_docker")
    manager = tk(workspace_root=Path(__file__).resolve().parents[1])
    manager._state_file = temp_dir / "flext_tests_docker_state.json"
    manager._dirty_containers.clear()
    return manager


@pytest.fixture
def docker_services(docker_manager: tk) -> Generator[tk]:
    """Function-scoped Docker services fixture."""
    result = docker_manager.start_compose_stack("docker-compose.test.yml")
    if result.failure:
        pytest.skip(f"Docker stack unavailable: {result.error}")
    yield docker_manager
    _ = docker_manager.compose_down("docker-compose.test.yml")


@pytest.fixture
def postgres_service(docker_services: tk) -> Generator[str | None]:
    """PostgreSQL service fixture."""
    ready = docker_services.wait_for_port_ready("localhost", 5433)
    if ready.failure or not ready.value:
        yield None
        return
    yield "localhost:5433"


@pytest.fixture
def redis_service(docker_services: tk) -> Generator[str | None]:
    """Redis service fixture."""
    ready = docker_services.wait_for_port_ready("localhost", 6380)
    if ready.failure or not ready.value:
        yield None
        return
    yield "localhost:6380"


@pytest.fixture
def meltano_service(docker_services: tk) -> Generator[str | None]:
    """Meltano service fixture."""
    ready = docker_services.wait_for_port_ready("localhost", 3389)
    if ready.failure or not ready.value:
        yield None
        return
    yield "localhost:3389"


def pytest_configure(settings: pytest.Settings) -> None:
    """Settingsure pytest markers."""
    settings.addinivalue_line("markers", "unit: Unit tests")
    settings.addinivalue_line("markers", "integration: Integration tests")
    settings.addinivalue_line("markers", "e2e: End-to-end tests")
    settings.addinivalue_line("markers", "meltano: Meltano-specific tests")
    settings.addinivalue_line("markers", "singer: Singer protocol tests")
    settings.addinivalue_line("markers", "pipeline: Pipeline execution tests")
    settings.addinivalue_line("markers", "cli: CLI command tests")
    settings.addinivalue_line("markers", "slow: Slow tests")
    settings.addinivalue_line("markers", "docker: Docker-based tests")


class MockMeltanoService:
    """Mock Meltano service."""

    @staticmethod
    def create_project(
        _config: t.ContainerMapping,
    ) -> t.ContainerMapping:
        return {"project_id": "test-project", "status": "created"}

    @staticmethod
    def install_plugin(
        _plugin_type: str,
        plugin_name: str,
    ) -> t.ContainerMapping:
        return {"plugin": plugin_name, "status": "installed"}

    @staticmethod
    def run_pipeline(
        _extractor: str,
        _loader: str,
    ) -> t.ContainerMapping:
        return {"execution_id": "test-execution", "status": "running"}


@pytest.fixture
def mock_meltano_service() -> MockMeltanoService:
    """Mock Meltano service for testing."""
    return MockMeltanoService()


class MockSingerTap:
    """Mock Singer tap."""

    def __init__(self, settings: t.ContainerMapping) -> None:
        """Initialize the instance."""
        super().__init__()
        self.settings = settings

    def discover(self) -> t.ContainerMapping:
        _ = self.settings
        return {
            "streams": [
                {
                    "stream": "test_entity",
                    "schema": {
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    },
                }
            ]
        }

    def extract(self) -> Sequence[t.ContainerMapping]:
        _ = self.settings
        return [{"type": "RECORD", "stream": "test_entity", "record": {}}]


@pytest.fixture
def mock_singer_tap() -> type[MockSingerTap]:
    """Mock Singer tap for testing."""
    return MockSingerTap


class MockSingerTarget:
    """Mock Singer target."""

    def __init__(self, settings: t.ContainerMapping) -> None:
        """Initialize the instance."""
        super().__init__()
        self.settings = settings

    def load(
        self,
        records: Sequence[t.ContainerMapping],
    ) -> t.ContainerMapping:
        _ = self.settings
        return {"records_loaded": len(records), "status": "success"}


@pytest.fixture
def mock_singer_target() -> type[MockSingerTarget]:
    """Mock Singer target for testing."""
    return MockSingerTarget
