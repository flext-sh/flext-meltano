#!/usr/bin/env python3
"""BRIDGE GO->PYTHON: Interface que USA flext-meltano biblioteca.

Este script agora REALMENTE usa a biblioteca flext-meltano
em vez de reimplementar subprocess.
"""

import sys

# USAR A BIBLIOTECA - não reimplementar
from flext_meltano.simple_bridge import FlextMeltanoBridge


def main() -> None:
    """Interface CLI que USA a biblioteca flext-meltano."""
    if len(sys.argv) < 2:
        sys.exit(1)

    operation = sys.argv[1]
    bridge = FlextMeltanoBridge()

    try:
        if operation == "version":
            bridge.get_version()
        elif operation == "list_plugins":
            bridge.list_plugins()
        elif operation == "add_plugin" and len(sys.argv) >= 4:
            bridge.add_plugin(sys.argv[2], sys.argv[3])
        elif operation == "discover" and len(sys.argv) >= 3:
            bridge.discover_catalog(sys.argv[2])
        elif operation == "run_pipeline" and len(sys.argv) >= 4:
            bridge.run_pipeline(sys.argv[2], sys.argv[3])
        elif operation == "invoke_dbt" and len(sys.argv) >= 3:
            bridge.invoke_dbt(sys.argv[2], *sys.argv[3:])
        else:
            pass

    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
