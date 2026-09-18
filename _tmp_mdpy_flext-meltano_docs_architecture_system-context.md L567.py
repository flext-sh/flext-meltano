# from flext-meltano/docs/architecture/system-context.md:567
from __future__ import annotations

# Standard FLEXT project structure
from flext_meltano import FlextMeltanoTap, FlextMeltanoTarget


class MyFLEXTProject(s):
    """FLEXT project extending foundation patterns."""

    def __init__(self):
        super().__init__()
        # Use FLEXT-Meltano for data integration
        self.tap = FlextMeltanoTap()
        self.target = FlextMeltanoTarget()

    def execute_pipeline(self) -> p.Result[PipelineResult]:
        """Execute pipeline using FLEXT foundation."""
        return (
            self.tap
            .discover_streams()
            .flat_map(lambda streams: self.validate_streams(streams))
            .flat_map(lambda _: self.target.initialize())
            .flat_map(lambda _: self.run_data_flow())
            .map(lambda result: PipelineResult.from_execution(result))
        )```
#### Plugin Ecosystem Integration

