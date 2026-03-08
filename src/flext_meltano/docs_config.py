"""FLEXT-Meltano Documentation Configuration Service.

Centralized configuration management for documentation automation using FlextSettings.
All hardcoded values and thresholds are centralized here for maintainability and consistency.

ARCHITECTURAL INTEGRATION:
- FlextSettings: Base configuration class with validation and environment variable support
- FlextContainer: Singleton pattern for global configuration access
- Railway Pattern: r[T] for configuration loading and validation
"""

from __future__ import annotations
