# from flext-meltano_docs/configuration.md:263
from flext_meltano import FlextMeltanoService, FlextMeltanoSettingsBuilders

# Build complete pipeline configuration
builder = FlextMeltanoSettingsBuilders()

# Tap configuration
tap_config = {
    "name": "tap-csv",
    "settings": {"files": [{"entity": "users", "path": "data/users.csv"}]},
}

# Target configuration
target_config = {"name": "target-jsonl", "settings": {"destination_path": "output/"}}

# Build pipeline
pipeline_config = builder.build_pipeline_config(tap_config, target_config)

# Initialize service
service = FlextMeltanoService(service_type="pipeline")
execution_result = service.execute()```
### Configuration Validation

