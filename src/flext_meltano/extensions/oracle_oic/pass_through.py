"""Pass-through invoker for Oracle OIC extension.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module provides a pass-through CLI for the oracle-oic-ext command.
It uses flext-core patterns and has zero tolerance for code duplication.
"""

from __future__ import annotations

import logging
import sys
from subprocess import CalledProcessError

from meltano.edk.process import Invoker, log_subprocess_error


def get_logger(name: str) -> logging.Logger:
    """Get logger for module."""
    return logging.getLogger(name)

logger = get_logger(__name__)


def pass_through_cli() -> None:
    """Pass-through CLI for oracle-oic-ext."""
    logger.debug("Running pass-through invoker with command: %s", sys.argv[1:])

    invoker = Invoker("oracle-oic-ext")
    try:
        invoker.run(*sys.argv[1:])
    except CalledProcessError as e:
        log_subprocess_error(
            "oracle-oic-ext",
            e,
            "oracle-oic-ext invocation failed",
        )
        sys.exit(1)
    except (OSError, RuntimeError, ValueError, ImportError):
        logger.exception("oracle-oic-ext invocation failed")
        sys.exit(1)


if __name__ == "__main__":
    pass_through_cli()
