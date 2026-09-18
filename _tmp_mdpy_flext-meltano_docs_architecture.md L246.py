# from flext-meltano/docs/architecture.md:246
from __future__ import annotations


class TapConfig(m.BaseModel):
    """Type-safe tap configuration model."""

    tap_type: str
    connection_config: m.Dict
    stream_config: m.Dict | None = None
    version: str | None = None


class StreamDefinition(m.BaseModel):
    """Type-safe stream definition model."""

    stream_name: str
    stream_schema: m.Dict
    tap_type: str
    status: str = "discovered"
    records_extracted: int = 0```
## 🛡️ Error Handling Architecture

### **r Pattern Implementation**

