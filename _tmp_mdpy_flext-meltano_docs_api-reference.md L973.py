# from flext-meltano/docs/api-reference.md:973
from __future__ import annotations


class PluginInfo(FlextBaseModel):
    """Plugin information model."""

    name: str
    namespace: str
    variant: str
    pip_url: str | None = None
    executable: str | None = None
    settings: m.Dict | None = None
    version: str | None = None```
#### FlextMeltanoModels.PipelineConfig

**Pipeline configuration model**

