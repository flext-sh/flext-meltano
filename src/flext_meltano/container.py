"""FLEXT Meltano Container - Simplified DI Configuration (SOLID Refactored).

**Architecture Layer**: Infrastructure Layer
**Status**: ✅ REFACTORED - Removed wrapper class, follows SOLID principles
**Dependencies**: flext-core (FlextContainer only), service factories

## Refactoring Rationale

The previous FlextMeltanoContainer class was pure boilerplate - a wrapper around
FlextContainer that violated SOLID principles. This refactored version:

1. **Single Responsibility**: Only provides Meltano-specific service configuration
2. **Open/Closed**: Easy to extend without modifying core container
3. **Dependency Inversion**: Depends on abstractions (FlextContainer), not wrapper
4. **Removes Boilerplate**: No redundant container wrapper class

## Usage Patterns

### Direct Container Usage (Recommended)
```python
from flext_core import get_flext_container
from flext_meltano.container import configure_meltano_services

# Get flext-core container directly (no wrapper)
container = get_flext_container()

# Configure with Meltano-specific services
result = configure_meltano_services(container)
if result.is_success:
    print("Meltano services configured")

# Use services directly
tap_factory = container.get("tap_service_factory").unwrap()
```

### Legacy Support (Backward Compatibility)
```python
from flext_meltano.container import get_meltano_container

# Legacy function - returns flext-core container with Meltano services
container = get_meltano_container()
```

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_flext_container

if TYPE_CHECKING:
    from flext_core import FlextContainer

from flext_meltano.base import (
    create_meltano_dbt_service,
    create_meltano_tap_service,
    create_meltano_target_service,
)
from flext_meltano.config import FlextMeltanoConfig


def configure_meltano_services(
    container: FlextContainer,
    config: FlextMeltanoConfig | None = None,
) -> FlextResult[None]:
    """Configure Meltano-specific services in existing container.

    This replaces the redundant FlextMeltanoContainer wrapper with direct
    service configuration following SOLID principles.

    Args:
        container: FlextContainer instance to configure
        config: Optional configuration (creates default if None)

    Returns:
        FlextResult indicating success or failure

    """
    try:
        # Use provided config or create default
        used_config = config or FlextMeltanoConfig()

        # Register configuration
        container.register("meltano_config", used_config)

        # Register factory functions for Singer services
        container.register(
            "tap_service_factory",
            create_meltano_tap_service,
        )
        container.register(
            "target_service_factory",
            create_meltano_target_service,
        )
        container.register(
            "dbt_service_factory",
            create_meltano_dbt_service,
        )

        return FlextResult.ok(None)

    except (ValueError, TypeError, AttributeError, KeyError) as e:
        return FlextResult.fail(f"Service configuration failed: {e}")


def get_meltano_container() -> FlextContainer:
    """Get flext-core container with Meltano services configured.

    LEGACY FUNCTION: For backward compatibility only.
    Prefer using get_flext_container() + configure_meltano_services() directly.

    Returns:
        FlextContainer with Meltano services pre-configured

    """
    warnings.warn(
        "get_meltano_container() is deprecated. "
        "Use get_flext_container() + configure_meltano_services() instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    container = get_flext_container()

    # Configure if not already done
    if not container.get("meltano_config").is_success:
        result = configure_meltano_services(container)
        if result.is_failure:
            error_msg = f"Container configuration failed: {result.error}"
            raise RuntimeError(error_msg)

    return container


def configure_meltano_container(
    custom_config: FlextMeltanoConfig | None = None,
) -> FlextResult[None]:
    """Configure global container with Meltano services.

    LEGACY FUNCTION: For backward compatibility only.
    Prefer using configure_meltano_services() directly.

    Args:
        custom_config: Optional custom configuration

    Returns:
        FlextResult indicating configuration success or failure

    """
    warnings.warn(
        "configure_meltano_container() is deprecated. "
        "Use configure_meltano_services() directly.",
        DeprecationWarning,
        stacklevel=2,
    )

    container = get_flext_container()
    return configure_meltano_services(container, custom_config)


# Clean public API - remove redundant classes, keep essential functions
__all__ = [
    "configure_meltano_container",  # Legacy
    "configure_meltano_services",  # Recommended
    "get_meltano_container",  # Legacy
]
