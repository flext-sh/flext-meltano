"""Shared pytest fixtures for flext-meltano tests."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from flext_tests import tf, tk

from tests.constants import c
from tests.typings import t
from tests.utilities import u

type MeltanoComponentCase = tuple[str, str, str]


MELTANO_COMPONENT_CASES: tuple[MeltanoComponentCase, ...] = (
    ("tap", "tap-csv", "source_name"),
    ("target", "target-jsonl", "sink_name"),
    ("dbt", "analytics", "transformation_name"),
)

MELTANO_COMPONENT_IDS: t.StrSequence = ("tap", "target", "dbt")


@pytest.fixture(
    params=tuple(range(len(MELTANO_COMPONENT_CASES))),
    ids=MELTANO_COMPONENT_IDS,
)
def meltano_component_case(request: pytest.FixtureRequest) -> MeltanoComponentCase:
    """Canonical public Meltano component factories with expected selectors."""
    case_index = request.param
    assert isinstance(case_index, int)
    return MELTANO_COMPONENT_CASES[case_index]


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
    with tf().temporary_directory() as temp_dir:
        project_dir = temp_dir / "test_meltano_project"
        project_dir.mkdir()
        yield project_dir


@pytest.fixture
def meltano_yml_config() -> t.JsonMapping:
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
    meltano_yml_config: t.JsonMapping,
) -> dict[str, str | Path | t.JsonMapping]:
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
def singer_state() -> t.JsonMapping:
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
def docker_manager(tmp_path_factory: pytest.TempPathFactory) -> tk:
    """Docker manager fixture for Docker-based tests."""
    temp_dir = tmp_path_factory.mktemp("flext_tests_docker")
    manager = tk.stack(
        "docker-compose.test.yml",
        container_name="flext-test-meltano",
        service="meltano",
        host=c.LOCALHOST,
        port=3389,
        workspace_root=Path(__file__).resolve().parents[2],
    )
    manager.state_file_path = temp_dir / "flext_tests_docker_state.json"
    manager.dirty_container_names.clear()
    return manager


@pytest.fixture
def docker_services(docker_manager: tk) -> Generator[tk]:
    """Function-scoped Docker services fixture."""
    result = docker_manager.execute()
    if result.failure:
        pytest.skip(f"Docker stack unavailable: {result.error}")
    yield docker_manager
    _ = docker_manager.down()


def require_docker_service(docker_services: tk, port: int, service_name: str) -> str:
    """Return a ready Docker service endpoint or skip the test."""
    ready = docker_services.ready(port=port)
    if ready.failure or not ready.value:
        pytest.skip(f"{service_name} service not available")
    return f"{c.LOCALHOST}:{port}"


@pytest.fixture
def postgres_service(docker_services: tk) -> str:
    """PostgreSQL service fixture."""
    return require_docker_service(
        docker_services,
        5433,
        "PostgreSQL",
    )


@pytest.fixture
def redis_service(docker_services: tk) -> str:
    """Redis service fixture."""
    return require_docker_service(
        docker_services,
        6380,
        "Redis",
    )


@pytest.fixture
def meltano_service(docker_services: tk) -> str:
    """Meltano service fixture."""
    return require_docker_service(
        docker_services,
        3389,
        "Meltano",
    )
