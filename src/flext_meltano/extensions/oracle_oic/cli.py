"""CLI entry point for flext-extensions.oracle.flext-oracle-oic-ext.

REFACTORED:
            Uses flext-core patterns.
Zero tolerance for code duplication.
"""

from flext_oracle_oic_ext.main import app, main

__all__ = ["app", "main"]
