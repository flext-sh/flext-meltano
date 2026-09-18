# from flext-meltano_docs/guides/architecture-analysis.md:249
# Quality gate integration
from flext_quality import FlextQualityGates

gates = FlextQualityGates()
gates.register_plugin_validator("meltano", MeltanoPluginValidator())
gates.register_pipeline_validator("meltano", MeltanoPipelineValidator())```
### External System Integration

#### Meltano CLI Integration

