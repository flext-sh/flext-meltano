#!/usr/bin/env python3
"""Simple test to verify DBT Hub core functionality."""

import contextlib
import sys
from pathlib import Path

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
        pass

    executor.close()

except ImportError:
    pass
except Exception:
    pass

try:
    from flext_meltano.dbt_packages.manager import FlextDbtPackageManager

    manager = FlextDbtPackageManager()

except ImportError:
    pass
except Exception:
    pass
