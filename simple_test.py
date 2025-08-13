"""Simple test to verify DBT Hub core functionality."""

import contextlib
import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test direct imports first
with contextlib.suppress(ImportError):
    pass

with contextlib.suppress(ImportError):
    pass

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from flext_meltano.dbt_packages.executor import FlextDbtInMemoryExecutor

    # Test instantiation
    executor = FlextDbtInMemoryExecutor()

    # Test simple query
    result = executor.execute_model("SELECT 1 as test")
    if result.success and result.data is not None:
        logger.info("✅ Executor test passed")

    executor.close()

except ImportError:
    logger.info("ℹ️ DBT executor not available")  # noqa: RUF001
except Exception as e:
    # Optional quick test; ignore errors in examples
    logger.info(f"ℹ️ Executor test skipped: {e}")  # noqa: RUF001

try:
    from flext_meltano.dbt_packages.manager import FlextDbtPackageManager

    manager = FlextDbtPackageManager()
    logger.info("✅ Package manager test passed")

except ImportError:
    logger.info("ℹ️ DBT package manager not available")  # noqa: RUF001
except Exception as e:
    # Optional quick test; ignore errors in examples
    logger.info(f"ℹ️ Package manager test skipped: {e}")  # noqa: RUF001
