"""Core module for FLEXT Meltano integration."""

from .config import MeltanoConfig
from .executor import MeltanoExecutor

# Initialize after imports
__all__ = ["MeltanoConfig", "MeltanoExecutor"]
