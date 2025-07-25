"""Stream implementations for the Oracle Database Tap.

This package provides stream classes for Oracle Database data sources:
- OracleTableStream: Direct Oracle Database table access

All streams follow Singer SDK patterns and provide enterprise features
like error handling, circuit breakers, and performance optimization.
"""

from __future__ import annotations

from flext_tap_oracle.streams.database import OracleTableStream

__all__ = [
    "OracleTableStream",
]
