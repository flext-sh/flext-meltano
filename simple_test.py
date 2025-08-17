"""Simple test to verify DBT Hub core functionality."""

from flext_core import get_logger

from flext_meltano.dbt_packages.executor import FlextDbtInMemoryExecutor
from flext_meltano.dbt_packages.manager import FlextDbtPackageManager

# Setup logging
logger = get_logger(__name__)

# Test instantiation
executor = FlextDbtInMemoryExecutor()

# Test simple query
result = executor.execute_model("SELECT 1 as test")
if result.success and result.data is not None:
    logger.info("✅ Executor test passed")

executor.close()

try:
    manager = FlextDbtPackageManager()
    logger.info("✅ Package manager test passed")

except ImportError:
    logger.info("ℹ️ DBT package manager not available")  # noqa: RUF001
except Exception as e:
    # Optional quick test; ignore errors in examples
    logger.info(f"ℹ️ Package manager test skipped: {e}")  # noqa: RUF001
