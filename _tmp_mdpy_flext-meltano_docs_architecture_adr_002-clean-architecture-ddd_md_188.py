# from flext-meltano_docs/architecture/adr/002-clean-architecture-ddd.md:188
from __future__ import annotations


# services.py
def create_pipeline(self, settings: dict) -> p.Result[Pipeline]:
    validated_config = self.config_validator.validate(settings)
    return validated_config.map(lambda cfg: Pipeline.create(cfg))```
**Application Layer → Infrastructure Layer**

