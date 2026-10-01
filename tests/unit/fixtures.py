<<<<<<< HEAD
    """Docker manager fixture for Docker-based tests.

    The host-scoped container state lives in the shared store
    (~/.flext/scratch scheme owned by flext-tests); tests that need
    isolation plant their own state through the public seal API.
    """
=======
    return tk.stack(
        c.Meltano.Tests.COMPOSE_FILE,
        target=m.Tests.ContainerConfig(
            container_name="flext-test-meltano",
            service=c.Meltano.Tests.PRIMARY_SERVICE,
            host=c.Meltano.Tests.HOST,
            port=c.Meltano.Tests.MELTANO_PORT,
        ),
        repository_root=Path(__file__).resolve().parents[2],
    )


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
    return f"{c.Meltano.Tests.HOST}:{port}"


@pytest.fixture
def postgres_service(docker_services: tk) -> str:
    """PostgreSQL service fixture."""
    return require_docker_service(
        docker_services, c.Meltano.Tests.POSTGRES_PORT, "PostgreSQL"
    )


@pytest.fixture
def redis_service(docker_services: tk) -> str:
    """Redis service fixture."""
    return require_docker_service(docker_services, c.Meltano.Tests.REDIS_PORT, "Redis")


@pytest.fixture
def meltano_service(docker_services: tk) -> str:
    """Meltano service fixture."""
    info = docker_services.fetch_container_info(c.Meltano.Tests.PRIMARY_CONTAINER_NAME)
    if info.failure:
        pytest.skip(f"Meltano container unavailable: {info.error}")
    host_port = info.value.ports.get(f"{c.Meltano.Tests.MELTANO_PORT}/tcp")
    if host_port is None:
        pytest.skip("Meltano service host port is not published")
    ready = docker_services.wait_for_port_ready(c.Meltano.Tests.HOST, int(host_port))
    if ready.failure or not ready.value:
        pytest.skip("Meltano service not available")
    return f"{c.Meltano.Tests.HOST}:{host_port}"
