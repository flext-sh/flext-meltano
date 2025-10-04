"""FLEXT Singer Tap Base Class - Enterprise Singer SDK Integration.

This module provides FlextTap, a wrapper around singer_sdk.Tap that integrates
FLEXT ecosystem patterns while maintaining complete Singer SDK compatibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextContainer, FlextLogger
from singer_sdk import Tap as SingerTap


class FlextTap(SingerTap):
    """FLEXT wrapper for singer_sdk.Tap with ecosystem integration.

    This class wraps singer_sdk.Tap to enforce FLEXT domain library patterns
    while maintaining 100% Singer SDK API compatibility. All flext-tap-* projects
    MUST inherit from this class instead of directly importing singer_sdk.Tap.

    Features:
    - FlextLogger integration for consistent ecosystem logging
    - FlextContainer access for dependency injection
    - FLEXT patterns (FlextResult, etc.) available to subclasses
    - Complete Singer SDK compatibility (no breaking changes)

    Example:
        ```python
        from flext_meltano import FlextTap, FlextStream


        class MyTap(FlextTap):
            name = "my-tap"

            def discover_streams(self):
                return [MyStream(self)]
        ```

    Note:
        This wrapper internally uses singer_sdk.Tap. Tap projects should
        NEVER import singer_sdk directly - use this wrapper instead.

    """

    def __init__(
        self,
        config: dict | None = None,
        catalog: dict | None = None,
        state: dict | None = None,
        *,
        parse_env_config: bool = False,
        validate_config: bool = True,
        setup_mapper: bool = True,
    ) -> None:
        """Initialize FlextTap with FLEXT ecosystem integration.

        Args:
            config: Tap configuration dictionary
            catalog: Singer catalog dictionary
            state: Singer state dictionary
            parse_env_config: Whether to parse environment variables for config
            validate_config: Whether to validate configuration
            setup_mapper: Whether to setup stream mapper

        """
        # Initialize Singer SDK Tap
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
            setup_mapper=setup_mapper,
        )

        # FLEXT ecosystem integration
        self._flext_logger = FlextLogger(self.name)
        self._flext_container = FlextContainer.get_global()

        # Log tap initialization with FLEXT logger
        self._flext_logger.info(
            f"FlextTap initialized: {self.name}",
            config_keys=list(self.config.keys()) if self.config else [],
        )

    @property
    def flext_logger(self) -> FlextLogger:
        """Get FLEXT ecosystem logger for this tap.

        Returns:
            FlextLogger instance configured for this tap

        """
        return self._flext_logger

    @property
    def flext_container(self) -> FlextContainer:
        """Get FLEXT ecosystem container for dependency injection.

        Returns:
            Global FlextContainer instance

        """
        return self._flext_container


__all__ = ["FlextTap"]
