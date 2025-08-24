#!/usr/bin/env python3
"""BRIDGE GO->PYTHON: Interface that USES flext-meltano library.

This script now ACTUALLY uses the flext-meltano library
instead of reimplementing subprocess.
"""

import sys

# USE THE LIBRARY - don't reimplement
from pathlib import Path

from flext_meltano import MeltanoBridge

# Constants to avoid magic values
MIN_ARGS_FOR_COMMAND = 2
MIN_ARGS_FOR_ADD_PLUGIN = 4
MIN_ARGS_FOR_DISCOVER = 3
MIN_ARGS_FOR_RUN_PIPELINE = 4
MIN_ARGS_FOR_INVOKE_DBT = 3


def main() -> None:
    """Interface CLI que USA a biblioteca flext-meltano."""
    if len(sys.argv) < MIN_ARGS_FOR_COMMAND:
        sys.exit(1)

    operation = sys.argv[1]
    bridge = MeltanoBridge()

    try:
        if operation == "version":
            bridge.get_version()
        elif operation == "list_plugins":
            bridge.discover_plugins()
        elif operation == "add_plugin" and len(sys.argv) >= MIN_ARGS_FOR_ADD_PLUGIN:
            bridge.install_plugin(Path(), sys.argv[2], sys.argv[3])
        elif operation == "discover" and len(sys.argv) >= MIN_ARGS_FOR_DISCOVER:
            bridge.discover_plugins()
        elif operation == "run_pipeline" and len(sys.argv) >= MIN_ARGS_FOR_RUN_PIPELINE:
            bridge.run_elt_pipeline(sys.argv[2], sys.argv[3])
        elif operation == "invoke_dbt" and len(sys.argv) >= MIN_ARGS_FOR_INVOKE_DBT:
            bridge.execute_meltano_command_real(Path(), ["dbt", *sys.argv[2:]])

    except (RuntimeError, ValueError, TypeError):
        sys.exit(1)


if __name__ == "__main__":
    main()
