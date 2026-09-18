# from flext-meltano/docs/api-reference.md:957
from __future__ import annotations


class Config(FlextBaseModel):
    """Main configuration model for FLEXT-Meltano."""

    project_root: Path | None = None
    default_environment: str = "dev"
    log_level: str = "INFO"
    plugin_dir: Path | None = None
    state_dir: Path | None = None```
#### FlextMeltanoModels.PluginInfo

**Plugin information model**

