# from flext-meltano_docs/configuration.md:156
from flext_meltano import TapConfig, FlextMeltanoSettingsBuilders

# Create tap configuration
tap_config = TapConfig(
    name="tap-csv",
    executable="tap-csv",
    settings={"files": [{"entity": "users", "path": "data/users.csv", "keys": ["id"]}]},
)

# Build pipeline configuration
builder = FlextMeltanoSettingsBuilders()
pipeline_config = builder.build_tap_config(tap_config.dict())```
### Target Configuration

