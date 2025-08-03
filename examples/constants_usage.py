"""FLEXT Meltano Constants Usage Examples - Enterprise Configuration Patterns.

**Purpose**: Demonstrate FlextMeltanoConstants usage following flext-core patterns
**Scope**: Configuration constants, environment management, enterprise standards
**Target Audience**: Developers implementing configuration management
**Dependencies**: FLEXT Meltano constants module, flext-core patterns

## Overview

This example demonstrates how to use the FLEXT Meltano constants following
enterprise patterns and flext-core configuration standards.
"""

from __future__ import annotations

from flext_meltano.constants import (
    MeltanoEnvironment,
    MeltanoLogLevel,
    MeltanoResultStatus,
)


def example_constants_usage() -> None:
    """Exemplo de uso das constantes do FlextMeltanoConstants."""
    # 1. Acesso direto às constantes (padrão flext-core)


def example_environment_usage() -> None:
    """Exemplo de uso dos enums de ambiente."""
    # Uso dos enums
    env = MeltanoEnvironment.DEVELOPMENT
    log_level = MeltanoLogLevel.INFO
    status = MeltanoResultStatus.SUCCESS

    # Comparação
    if env == MeltanoEnvironment.DEVELOPMENT:
        pass

    if log_level == MeltanoLogLevel.INFO:
        pass

    if status == MeltanoResultStatus.SUCCESS:
        pass


if __name__ == "__main__":
    example_constants_usage()
    example_environment_usage()
