"""FLEXT Meltano Common - Shared patterns for Taps/Targets.

This module consolidates common configuration, validation, and base classes
that were duplicated across multiple tap and target projects.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Common base classes for taps/targets
from flext_meltano.common.base import (
    FlextMeltanoBaseStream,
    FlextMeltanoBaseTap,
    FlextMeltanoBaseTarget,
)

# Base configuration classes
from flext_meltano.common.config import (
    FlextMeltanoAuthConfig,
    FlextMeltanoBaseConfig,
    FlextMeltanoConnectionConfig,
    FlextMeltanoLDAPConnectionConfig,
    FlextMeltanoStreamConfig,
    FlextMeltanoValidationConfig,
)

# Common exception patterns
from flext_meltano.common.exceptions import (
    FlextMeltanoCommonConfigurationError,
    FlextMeltanoCommonConnectionError,
    FlextMeltanoCommonError,
    FlextMeltanoCommonValidationError,
    FlextMeltanoTargetAuthenticationError,
    FlextMeltanoTargetError,
    FlextMeltanoTargetProcessingError,
    FlextMeltanoTargetTransformationError,
)

# Common validation patterns
from flext_meltano.common.validation import (
    FlextMeltanoConfigValidator,
    validate_auth_config,
    validate_base_url,
    validate_connection_config,
    validate_directory_path,
    validate_file_path,
    validate_log_level,
    validate_stream_config,
)

__all__ = [
    "FlextMeltanoAuthConfig",
    # Base configuration classes
    "FlextMeltanoBaseConfig",
    "FlextMeltanoBaseStream",
    # Base classes
    "FlextMeltanoBaseTap",
    "FlextMeltanoBaseTarget",
    "FlextMeltanoCommonConfigurationError",
    "FlextMeltanoCommonConnectionError",
    # Exception classes
    "FlextMeltanoCommonError",
    "FlextMeltanoCommonValidationError",
    "FlextMeltanoConfigValidator",
    "FlextMeltanoConnectionConfig",
    "FlextMeltanoLDAPConnectionConfig",
    "FlextMeltanoStreamConfig",
    "FlextMeltanoTargetAuthenticationError",
    "FlextMeltanoTargetError",
    "FlextMeltanoTargetProcessingError",
    "FlextMeltanoTargetTransformationError",
    "FlextMeltanoValidationConfig",
    "validate_auth_config",
    "validate_base_url",
    # Validation functions and classes
    "validate_connection_config",
    "validate_directory_path",
    "validate_file_path",
    "validate_log_level",
    "validate_stream_config",
]
