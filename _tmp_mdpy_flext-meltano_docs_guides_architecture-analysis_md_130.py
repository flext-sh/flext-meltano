# from flext-meltano_docs/guides/architecture-analysis.md:130
from __future__ import annotations
class FlextSingerTap(s):
    """Singer tap with discovery, sync, and state management."""

    def __init__(self, tap_name: str, settings: m.Dict, state: m.Dict | None = None)
    async def discover(self) -> p.Result[Catalog]
    async def sync(self, streams: t.StringList | None = None) -> p.Result[SyncResult]```
**FlextSingerTarget Architecture:**

