# from flext-meltano_docs/architecture/adr/001-railway-oriented-programming.md:154
from __future__ import annotations


class FlextMeltanoError(Exception):
    """Base error for all FLEXT-Meltano operations."""


class ConfigurationError(FlextMeltanoError):
    """Configuration-related errors."""


class PluginError(FlextMeltanoError):
    """Plugin operation errors."""


class PipelineError(FlextMeltanoError):
    """Pipeline execution errors."""```
### Railway Pattern Usage

