# from flext-meltano/docs/configuration.md:171
from flext_meltano import FlextMeltanoSettingsBuilders

target_settings = {
    "destination_path": "output/",
    "file_naming_scheme": "{stream_name}.jsonl",
}

builder = FlextMeltanoSettingsBuilders()
target_config = builder.build_target_config(target_settings)```
### Singer Catalog Configuration

