"""FLEXT Singer Target Base Class - Enterprise Singer SDK Integration.

This module provides FlextTarget, a wrapper around singer_sdk.Target that integrates
FLEXT ecosystem patterns while maintaining complete Singer SDK compatibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextContainer, FlextLogger
from singer_sdk import Target as SingerTarget


class FlextTarget(SingerTarget):
    """FLEXT wrapper for singer_sdk.Target with ecosystem integration.

    This class wraps singer_sdk.Target to enforce FLEXT domain library patterns
    while maintaining 100% Singer SDK API compatibility. All flext-target-* projects
    MUST inherit from this class instead of directly importing singer_sdk.Target.

    Features:
    - FlextLogger integration for consistent ecosystem logging
    - FlextContainer access for dependency injection
    - FLEXT patterns (FlextResult, etc.) available to subclasses
    - Complete Singer SDK compatibility (no breaking changes)

    Example:
        ```python
        from flext_meltano import FlextTarget, FlextSink


        class MyTarget(FlextTarget):
            name = "my-target"
            default_sink_class = MySink
        ```

    Note:
        This wrapper internally uses singer_sdk.Target. Target projects should
        NEVER import singer_sdk directly - use this wrapper instead.

    """

    def __init__(
        self,
        config: dict | None = None,
        *,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        """Initialize FlextTarget with FLEXT ecosystem integration.

        Args:
            config: Target configuration dictionary
            parse_env_config: Whether to parse environment variables for config
            validate_config: Whether to validate configuration

        """
        # Initialize Singer SDK Target
        super().__init__(
            config=config,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )

        # FLEXT ecosystem integration
        self._flext_logger = FlextLogger(self.name)
        self._flext_container = FlextContainer.get_global()

        # Log target initialization with FLEXT logger
        self._flext_logger.info(
            f"FlextTarget initialized: {self.name}",
            config_keys=list(self.config.keys()) if self.config else [],
        )

    @property
    def flext_logger(self) -> FlextLogger:
        """Get FLEXT ecosystem logger for this target.

        Returns:
            FlextLogger instance configured for this target

        """
        return self._flext_logger

    @property
    def flext_container(self) -> FlextContainer:
        """Get FLEXT ecosystem container for dependency injection.

        Returns:
            Global FlextContainer instance

        """
        return self._flext_container


__all__ = ["FlextTarget"]
