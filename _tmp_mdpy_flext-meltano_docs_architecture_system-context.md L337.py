# from flext-meltano/docs/architecture/system-context.md:337
from __future__ import annotations


class FlextMeltanoTap(FlextMeltanoSingerBase, SingerTap):
    """FLEXT tap implementation with ecosystem integration."""

    def __init__(self, settings: t.JsonMapping = None, **kwargs):
        super().__init__(settings, **kwargs)
        # FLEXT logging integration
        self.logger = FlextLogger.get_logger(self.__class__.__name__)

    def discover_streams(self) -> List[FlextMeltanoStream]:
        """Discover streams with FLEXT error handling."""
        try:
            # Singer SDK discovery
            discovered = super().discover_streams()

            # Convert to FLEXT streams
            flext_streams = []
            for stream in discovered:
                flext_stream = FlextMeltanoStream.from_singer_stream(stream)
                flext_streams.append(flext_stream)

            self.logger.info(f"Discovered {len(flext_streams)} streams")
            return flext_streams

        except Exception as e:
            self.logger.error(f"Stream discovery failed: {e}")
            raise SingerDiscoveryError(f"Failed to discover streams: {e}")

    def run_tap(self) -> None:
        """Run tap with FLEXT state management."""
        try:
            # FLEXT state initialization
            state_manager = FlextMeltanoStateManager(self.settings)

            # Run with state tracking
            with state_manager.state_context():
                super().run_tap()

        except Exception as e:
            self.logger.error(f"Tap execution failed: {e}")
            raise SingerExecutionError(f"Tap execution failed: {e}")```
### Integration Patterns

#### Adapter Pattern for External Systems

