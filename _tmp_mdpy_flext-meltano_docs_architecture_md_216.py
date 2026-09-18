# from flext-meltano_docs/architecture.md:216
from __future__ import annotations


class FlextMeltanoTypes:
    """Comprehensive type system for ELT operations."""

    class Plugin:
        """Meltano plugin management types."""

        type Name = str
        type Config = ConfigDict
        type Command = t.StringList

    class Singer:
        """Singer protocol integration types."""

        type Tap = SingerTap
        type Target = SingerTarget
        type MessageType = str
        type RecordMessage = JsonObject

    class ELT:
        """Extract-Load-Transform pipeline types."""

        type Pipeline = ConfigDict
        type PipelineResult = JsonObject
        type ExtractResult = JsonObject```
### **Pydantic Model Integration**

