# from flext-meltano/docs/architecture/quality-attributes.md:3685
from __future__ import annotations
import pathlib


class TestDataManager:
    """Centralized test data management."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.data_cache = {}

    def get_test_data(
        self, dataset_name: str, scenario: str = "default"
    ) -> Dict[str, t.JsonValue]:
        """Get test data for specific dataset and scenario."""
        cache_key = f"{dataset_name}:{scenario}"

        if cache_key not in self.data_cache:
            data_file = self.base_path / "fixtures" / dataset_name / f"{scenario}.json"

            if data_file.exists():
                with pathlib.Path(data_file).open("r") as f:
                    self.data_cache[cache_key] = json.load(f)
            else:
                raise FileNotFoundError(f"Test data not found: {data_file}")

        return self.data_cache[cache_key]

    def create_dynamic_test_data(
        self, template: str, overrides: Dict[str, t.JsonValue] = None
    ) -> Dict[str, t.JsonValue]:
        """Create dynamic test data from templates."""
        template_data = self.get_test_data("templates", template)
        overrides = overrides or {}

        # Deep merge overrides
        result = self._deep_merge(template_data, overrides)

        # Add dynamic values
        result["id"] = str(uuid.uuid4())
        result["created_at"] = datetime.utcnow().isoformat()
        result["test_run_id"] = os.environ.get("PYTEST_CURRENT_TEST")

        return result

    def _deep_merge(
        self, base: Dict[str, t.JsonValue], override: Dict[str, t.JsonValue]
    ) -> Dict[str, t.JsonValue]:
        """Deep merge dictionaries."""
        result = base.copy()

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result```
#### 3. Test Result Analysis

