# from flext-meltano_docs/architecture/adr/002-clean-architecture-ddd.md:179
from __future__ import annotations


# api.py
def create_pipeline(settings: dict) -> p.Result[Pipeline]:
    return FlextMeltanoService().create_pipeline(settings)```
**Application Layer → Domain Layer**

