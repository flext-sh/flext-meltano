# from flext-meltano/docs/architecture/adr/001-railway-oriented-programming.md:174
from __future__ import annotations


def create_and_run_pipeline(settings: PipelineConfig) -> p.Result[PipelineResult]:
    return (
        validate_config(settings)
        .flat_map(lambda cfg: discover_plugins(cfg))
        .flat_map(lambda plugins: validate_plugins(plugins))
        .flat_map(lambda valid_plugins: install_plugins(valid_plugins))
        .flat_map(lambda installed: run_pipeline(installed, settings))
        .map(lambda result: PipelineResult.from_execution(result))
    )```
### Testing Error Scenarios

