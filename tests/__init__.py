# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_tests import d, e, h, r, s, x

    from tests.conftest import *
    from tests.constants import *
    from tests.helpers import *
    from tests.integration import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "tests.helpers",
        "tests.integration",
        "tests.unit",
    ),
    {
        "CliRunner": "tests.conftest",
        "FlextMeltanoTestConstants": "tests.constants",
        "FlextMeltanoTestModels": "tests.models",
        "FlextMeltanoTestProtocols": "tests.protocols",
        "FlextMeltanoTestTypes": "tests.typings",
        "FlextMeltanoTestUtilities": "tests.utilities",
        "MockCliResult": "tests.conftest",
        "MockCliRunner": "tests.conftest",
        "MockMeltanoService": "tests.conftest",
        "MockSingerTap": "tests.conftest",
        "MockSingerTarget": "tests.conftest",
        "c": ("tests.constants", "FlextMeltanoTestConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "helpers": "tests.helpers",
        "integration": "tests.integration",
        "job_run_config": "tests.conftest",
        "m": ("tests.models", "FlextMeltanoTestModels"),
        "meltano_cli_runner": "tests.conftest",
        "meltano_invoke_args": "tests.conftest",
        "meltano_project": "tests.conftest",
        "meltano_service": "tests.conftest",
        "meltano_yml_config": "tests.conftest",
        "mock_meltano_service": "tests.conftest",
        "mock_singer_tap": "tests.conftest",
        "mock_singer_target": "tests.conftest",
        "models": "tests.models",
        "p": ("tests.protocols", "FlextMeltanoTestProtocols"),
        "pipeline_execution_config": "tests.conftest",
        "postgres_service": "tests.conftest",
        "protocols": "tests.protocols",
        "pytest_configure": "tests.conftest",
        "r": "flext_tests",
        "redis_service": "tests.conftest",
        "s": "flext_tests",
        "sample_csv_data": "tests.conftest",
        "sample_schedule_config": "tests.conftest",
        "set_test_environment": "tests.conftest",
        "singer_records": "tests.conftest",
        "singer_schema": "tests.conftest",
        "singer_state": "tests.conftest",
        "t": ("tests.typings", "FlextMeltanoTestTypes"),
        "tap_csv_config": "tests.conftest",
        "target_csv_config": "tests.conftest",
        "test_environment_config": "tests.conftest",
        "test_meltano_project_dir": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextMeltanoTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": "flext_tests",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
