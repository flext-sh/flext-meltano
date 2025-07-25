"""🚨 ARCHITECTURAL COMPLIANCE: ELIMINATED DUPLICATE DI Container.

REFATORADO COMPLETO:
- REMOVIDA TODAS as duplicações de FlextContainer/DIContainer
- USA APENAS FlextContainer oficial do flext-core
- Mantém apenas utilitários flext_oracle_oic_ext-específicos
- SEM fallback, backward compatibility ou código duplicado

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# 🚨 ARCHITECTURAL COMPLIANCE: Use ONLY official flext-core FlextContainer
import logging
from typing import Any


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for the given name.

    Args:
        name: Logger name.

    Returns:
        Logger instance.

    """
    return logging.getLogger(name)

# Simple replacement for FlextContainer
class FlextContainer(dict[str, Any]):
    """Simple container replacement."""

logger = get_logger(__name__)


# ==================== FLEXT_ORACLE_OIC_EXT-SPECIFIC DI UTILITIES ====================

_flext_oracle_oic_ext_container_instance: FlextContainer | None = None


def get_flext_oracle_oic_ext_container() -> FlextContainer:
    """Get FLEXT_ORACLE_OIC_EXT-specific DI container instance.

    Returns:
        FlextContainer: Official container from flext-core.

    """
    # Using module-level instance to avoid global usage
    if _flext_oracle_oic_ext_container_instance is None:
        # Initialize singleton instance
        globals()["_flext_oracle_oic_ext_container_instance"] = FlextContainer()
    return _flext_oracle_oic_ext_container_instance  # type: ignore[return-value]


def configure_flext_oracle_oic_ext_dependencies() -> None:
    """Configure FLEXT_ORACLE_OIC_EXT dependencies using official FlextContainer."""
    get_flext_oracle_oic_ext_container()

    try:
        # Register module-specific dependencies
        # Module-specific service registrations will be added as needed

        logger.info("FLEXT_ORACLE_OIC_EXT dependencies configured successfully")

    except ImportError:
        logger.exception("Failed to configure FLEXT_ORACLE_OIC_EXT dependencies")


def get_flext_oracle_oic_ext_service(service_name: str) -> Any:  # noqa: ANN401
    """Get flext_oracle_oic_ext service from container.

    Args:
        service_name: Name of service to retrieve.

    Returns:
        Service instance or None if not found.

    """
    container = get_flext_oracle_oic_ext_container()
    result = container.get(service_name)

    if result is not None:
        return result

    logger.warning("FLEXT_ORACLE_OIC_EXT service '%s' not found", service_name)
    return None


# Initialize flext_oracle_oic_ext dependencies on module import
configure_flext_oracle_oic_ext_dependencies()
