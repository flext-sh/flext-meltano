# from flext-meltano_docs/architecture/adr/003-singer-protocol-abstraction.md:171
from __future__ import annotations


class FlextMeltanoTap(FlextMeltanoSingerBase):
    def discover_streams(self) -> p.Result[List[FlextMeltanoStream]]:
        try:
            # Singer SDK operations
            streams = super().discover_streams()
            # Convert to FLEXT streams
            flext_streams = [FlextMeltanoStream.from_sdk(stream) for stream in streams]
            return r.ok(flext_streams)
        except Exception as e:
            return r.fail(SingerError(f"Stream discovery failed: {e}"))

    def run_tap(self, settings: dict, state: dict) -> p.Result[TapResult]:
        # Railway pattern for tap execution
        return (
            self
            .validate_config(settings)
            .flat_map(lambda _: self.initialize_state(state))
            .flat_map(lambda _: self.execute_streams())
            .map(lambda result: TapResult.from_execution(result))
        )```
### State Management

