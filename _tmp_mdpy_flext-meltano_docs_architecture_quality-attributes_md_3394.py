# from flext-meltano_docs/architecture/quality-attributes.md:3394
from __future__ import annotations


@pytest.fixture
def test_database():
    """Database fixture for testing."""
    # Setup
    db = create_test_database()
    yield db
    # Teardown
    db.cleanup()


@pytest.fixture
def mock_external_service():
    """Mock external service for testing."""
    with patch("external_service.Client") as mock_client:
        mock_client.return_value.get_data.return_value = {"status": "success"}
        yield mock_client


@pytest.fixture
def authenticated_user():
    """Authenticated user fixture."""
    user = User(id=123, name="Test User", role="REDACTED_LDAP_BIND_PASSWORD")
    # Set up authentication context
    with authenticated_context(user):
        yield user


class TestContext:
    """Test context manager for complex setup."""

    def __init__(self, setup_data: Dict[str, t.JsonValue] = None):
        self.setup_data = setup_data or {}

    def __enter__(self):
        # Complex setup logic
        self.db = create_test_database()
        self.user = create_test_user()
        self.pipeline = create_test_pipeline(self.user)

        # Store cleanup functions
        self.cleanup_funcs = [
            lambda: self.db.cleanup(),
            lambda: cleanup_test_user(self.user),
            lambda: cleanup_test_pipeline(self.pipeline),
        ]

        return {"db": self.db, "user": self.user, "pipeline": self.pipeline}

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup in reverse order
        for cleanup_func in reversed(self.cleanup_funcs):
            try:
                cleanup_func()
            except Exception as e:
                u.Cli.print(f"Cleanup failed: {e}")


# Usage
def test_complex_pipeline_operation():
    with TestContext() as context:
        service = PipelineService(context["db"])

        result = service.execute_pipeline(context["pipeline"])

        assert result.success
        # Context automatically cleaned up```
#### 4. Property-Based Testing

