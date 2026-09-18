# from flext-meltano_docs/architecture.md:185
from flext_meltano import FlextMeltanoTypes

# Comprehensive type system extending flext-core
pipeline_config: FlextMeltanoTypes.ELT.PipelineConfig
tap_config: FlextMeltanoTypes.Singer.TapConfig
result: p.Result[FlextMeltanoTypes.ELT.PipelineResult]```
### **External Library Integration**

**Current Status (Direct Imports)**:

