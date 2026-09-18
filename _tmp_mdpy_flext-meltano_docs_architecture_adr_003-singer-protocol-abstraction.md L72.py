# from flext-meltano/docs/architecture/adr/003-singer-protocol-abstraction.md:72
# Automatic error wrapping and context preservation
result = tap.discover_streams()
if result.failure:
    # FLEXT error handling patterns
    logger.error(f"Stream discovery failed: {result.error}")```
**Testability**: Singer components can be tested in isolation

