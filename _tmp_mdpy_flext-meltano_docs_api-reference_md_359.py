# from flext-meltano_docs/api-reference.md:359
from __future__ import annotations


def discover(self) -> p.Result[FlextMeltanoModels.Catalog]:
    """Discover Singer catalog for the tap.

    Returns:
        r containing catalog or error

    Example:
        >>> tap = FlextSingerTap("tap-gitlab", {"api_url": "https://gitlab.com"})
        >>> result = tap.discover()
        >>> if result.success:
        ...     catalog = result.unwrap()
        ...     u.Cli.print(f"Discovered {len(catalog.streams)} streams")

    """```
##### sync(streams=None, state=None)

**Execute tap synchronization**

