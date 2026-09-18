# from flext-meltano/docs/architecture/data-architecture.md:274
from __future__ import annotations


@dataclass
class PipelineConfig:
    """Pipeline configuration with validation."""

    name: str
    tap: TapConfig
    target: TargetConfig
    transforms: List[TransformConfig] = field(default_factory=list)
    schedule: Optional[str] = None

    def validate(self) -> p.Result[ValidatedConfig]:
        """Validate complete pipeline configuration."""
        return (
            self.tap
            .validate()
            .flat_map(lambda tap: self.target.validate())
            .map(
                lambda target: ValidatedConfig(
                    tap=tap, target=target, transforms=self.transforms
                )
            )
        )```
#### Singer Message Schema

