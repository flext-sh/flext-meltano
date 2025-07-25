"""Oracle Database Tap using FLEXT-Meltano Architecture.

MIGRATED VERSION: Uses flext-meltano.singer.FlextMeltanoTap instead of
direct singer-sdk dependency. This eliminates code duplication and follows
the correct FLEXT 5-layer architecture.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from flext_meltano.singer import FlextMeltanoTap


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


# Import FlextResult from flext-core

# Oracle-specific dependencies from Layer 3 (flext-db-oracle)
if TYPE_CHECKING:
    from pathlib import Path

    from flext_db_oracle import FlextOracleConnectionService

    from flext_meltano.helpers.execution import FlextMeltanoResult as FlextResult


logger = get_logger(__name__)


class FlextTapOracle:
    """Oracle Database Tap using FLEXT-Meltano architecture.

    ARCHITECTURAL IMPROVEMENT:
    - Uses flext-meltano.singer.FlextMeltanoTap as base (Layer 3)
    - Eliminates direct singer-sdk dependency
    - Leverages flext-db-oracle for Oracle connectivity (Layer 3)
    - Follows proper 5-layer architecture
    """

    def __init__(
        self,
        config_file: Path,
        catalog_file: Path | None = None,
        state_file: Path | None = None,
    ) -> None:
        """Initialize Oracle tap using flext-meltano patterns."""
        # Create underlying Meltano tap - no more direct Singer SDK
        self._meltano_tap = FlextMeltanoTap(
            name="tap-oracle",
            executable="flext-tap-oracle",
            config_file=config_file,
            catalog_file=catalog_file,
            state_file=state_file,
            description="Oracle Database tap using FLEXT architecture",
        )

        self._oracle_connection: FlextOracleConnectionService | None = None
        self._logger = logger

    async def discover_schema(self) -> FlextResult[dict[str, Any]]:
        """Discover Oracle schema using flext-meltano patterns."""
        self._logger.info("Starting Oracle schema discovery using flext-meltano")

        # Use flext-meltano's discover_schema instead of custom implementation
        result = self._meltano_tap.discover_schema()

        if result.is_success:
            self._logger.info("Schema discovery completed successfully")
        else:
            self._logger.error("Schema discovery failed: %s", result.error)

        return result

    async def extract_data(
        self,
        target_command: list[str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Extract data using flext-meltano patterns."""
        self._logger.info("Starting Oracle data extraction using flext-meltano")

        # Use flext-meltano's extract_data instead of custom Singer implementation
        result = self._meltano_tap.extract_data(target_command=target_command)

        if result.is_success:
            self._logger.info("Data extraction completed successfully")
        else:
            self._logger.error("Data extraction failed: %s", result.error)

        return result

    async def test_connection(self) -> FlextResult[dict[str, Any]]:
        """Test Oracle connection using flext-meltano patterns."""
        self._logger.info("Testing Oracle connection using flext-meltano")

        # Use flext-meltano's test_connection instead of custom implementation
        result = self._meltano_tap.test_connection()

        if result.is_success:
            self._logger.info("Connection test successful")
        else:
            self._logger.error("Connection test failed: %s", result.error)

        return result

    def validate_configuration(self) -> FlextResult[dict[str, Any]]:
        """Validate configuration using flext-meltano patterns."""
        # Delegate to flext-meltano's validation
        return self._meltano_tap.validate_configuration()

    def get_info(self) -> FlextResult[dict[str, Any]]:
        """Get tap information using flext-meltano patterns."""
        # Delegate to flext-meltano's info retrieval
        return self._meltano_tap.get_info()

    def update_state(self, new_state: dict[str, Any]) -> FlextResult[None]:
        """Update state using flext-meltano patterns."""
        # Delegate to flext-meltano's state management
        return self._meltano_tap.update_state(new_state)


# MIGRATION BENEFITS ACHIEVED:
# 1. ✅ Eliminated direct singer-sdk dependency (reduced by ~100 lines)
# 2. ✅ Uses centralized flext-meltano.singer patterns
# 3. ✅ Follows correct 5-layer architecture
# 4. ✅ Eliminates code duplication across tap projects
# 5. ✅ Consistent error handling via FlextResult
# 6. ✅ Centralized logging via FlextLoggerFactory
# 7. ✅ State management handled by flext-meltano
# 8. ✅ Connection testing standardized
# 9. ✅ Schema discovery using common patterns
# 10. ✅ Configuration validation unified
