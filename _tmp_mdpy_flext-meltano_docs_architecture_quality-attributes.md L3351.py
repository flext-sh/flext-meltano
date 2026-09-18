# from flext-meltano/docs/architecture/quality-attributes.md:3351
from __future__ import annotations
class TestDataBuilder:
    """Fluent builder for test data creation."""

    def __init__(self):
        self.data = {}

    def with_name(self, name: str) -> "TestDataBuilder":
        self.data["name"] = name
        return self

    def u.with_config(
        self, settings: Dict[str, t.JsonValue]
    ) -> "TestDataBuilder":
        self.data["settings"] = settings
        return self

    def with_tags(self, *tags: str) -> "TestDataBuilder":
        self.data["tags"] = list(tags)
        return self

    def build(self) -> TestEntity:
        """Build the test entity."""
        return TestEntity(**self.data)


# Usage in tests
def test_entity_processing():
    entity = (
        TestDataBuilder()
        .with_name("test-entity")
        .u.with_config({"key": "value"})
        .with_tags("important", "test")
        .build()
    )

    result = service.process_entity(entity)

    assert result.success
    assert result.value.tags == ["important", "test"]```
#### 3. Test Fixtures and Context Managers

