# from flext-meltano/docs/guides/architecture-analysis.md:241
# CLI command integration
from flext_cli import cli

cli.register_command("meltano", MeltanoCommandHandler())
cli.register_command("pipeline", PipelineCommandHandler())```
#### flext-quality Integration

