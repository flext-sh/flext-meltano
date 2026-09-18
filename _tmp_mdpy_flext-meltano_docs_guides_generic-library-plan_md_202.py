# from flext-meltano_docs/guides/generic-library-plan.md:202
# Protocol-based execution
singer_service = FlextSingerService()
tap = singer_service.create_tap("tap-gitlab", settings)
catalog = tap.discover()
sync_result = tap.sync(selected_streams)```
## API Design

### Generic Plugin Interface

#### Plugin Discovery API

