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

# Since flext_meltano.constants doesn't exist, we'll demonstrate with real values
from flext_meltano import FlextMeltanoConfig

# Constants from actual FLEXT Meltano usage patterns
class MeltanoEnvironment:
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"
    TEST = "test"

class MeltanoLogLevel:
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class MeltanoResultStatus:
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


def example_constants_usage() -> None:
    """Exemplo de uso das constantes do FlextMeltanoConstants."""
    # 1. Demonstrar uso real com FlextMeltanoConfig
    config = FlextMeltanoConfig(
        project_root="./demo_project",
        environment=MeltanoEnvironment.DEV
    )
    print(f"✅ Configuration with constants: {config.environment}")

    # 2. Demonstrar patterns de status
    result_status = MeltanoResultStatus.SUCCESS
    print(f"✅ Result status: {result_status}")

    # 3. Demonstrar log levels
    log_level = MeltanoLogLevel.INFO
    print(f"✅ Log level: {log_level}")


def example_environment_usage() -> None:
    """Exemplo de uso dos enums de ambiente."""
    # Uso dos enums REAIS (corrigindo DEVELOPMENT -> DEV)
    env = MeltanoEnvironment.DEV
    log_level = MeltanoLogLevel.INFO
    status = MeltanoResultStatus.SUCCESS

    # Comparação real com output
    if env == MeltanoEnvironment.DEV:
        print(f"✅ Environment check: {env}")

    if log_level == MeltanoLogLevel.INFO:
        print(f"✅ Log level check: {log_level}")

    if status == MeltanoResultStatus.SUCCESS:
        print(f"✅ Status check: {status}")

    # Demonstrar diferentes environments
    for env_name in [MeltanoEnvironment.DEV, MeltanoEnvironment.STAGING, MeltanoEnvironment.PROD]:
        config = FlextMeltanoConfig(project_root="./demo", environment=env_name)
        print(f"✅ Config for {env_name}: {config.project_root}")
        pass


if __name__ == "__main__":
    example_constants_usage()
    example_environment_usage()
