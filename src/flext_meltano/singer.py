"""FLEXT Meltano Singer - Singer Protocol Integration.

**Architecture Layer**: Singer Integration Layer
**Status**: ✅ STABLE - Core Singer protocol implementation
**Dependencies**: flext-core (FlextResult), Singer SDK, base module

## Module Purpose

This module provides **Singer protocol integration** for FLEXT Meltano's bridge
architecture, implementing Singer SDK patterns with enterprise integration for
Go service consumption through subprocess orchestration.

## Design Principles

1. **Singer Protocol Compliance**: Full Singer specification implementation
2. **Enterprise Integration**: FlextResult patterns and structured error handling
3. **Bridge-Friendly**: JSON-serializable Singer operations for Go services
4. **Stream Management**: Efficient stream processing and state management
5. **Schema Evolution**: Dynamic schema discovery and catalog management

## Core Components

### Singer Base Classes
- `FlextMeltanoTap`: Enterprise Singer tap implementation
- `FlextMeltanoTarget`: Enterprise Singer target implementation
- Integration with base service patterns and configuration management
- FlextResult integration for consistent error handling

### Bridge Integration
- Singer operations designed for subprocess execution
- JSON-serializable catalog and schema information
- State management for incremental extraction
- Stream metadata and capabilities reporting

This module provides essential **Singer protocol integration** capabilities for
FLEXT Meltano's bridge architecture, enabling reliable data extraction and
loading operations for Go service integration.
"""

from __future__ import annotations

from flext_meltano.base import (
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
)

FlextMeltanoTap = FlextMeltanoTapService
FlextMeltanoTarget = FlextMeltanoTargetService

__all__: list[str] = [
    "FlextMeltanoTap",
    "FlextMeltanoTarget",
]
