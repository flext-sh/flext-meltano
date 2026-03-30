# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import *

    from tests import (
        conftest,
        constants,
        helpers,
        integration,
        models,
        protocols,
        typings,
        unit,
        utilities,
    )
    from tests.conftest import *
    from tests.constants import *
    from tests.helpers import docker_test_manager
    from tests.helpers.docker_test_manager import *
    from tests.integration import test_docker_integration
    from tests.integration.test_docker_integration import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import (
        pipeline_cli_managers_tests,
        test_api,
        test_cli_integration,
        test_config,
        test_constants,
        test_execution_result,
        test_executors,
        test_file_managers,
        test_library_runner,
        test_models,
        test_plugin_protocols,
        test_services,
        test_singer_cli_translator,
        test_singer_types,
        test_tap_abstractions,
        test_target_abstractions,
        test_typings,
        test_utilities,
        test_validators,
    )
    from tests.unit.pipeline_cli_managers_tests import *
    from tests.unit.test_api import *
    from tests.unit.test_cli_integration import *
    from tests.unit.test_config import *
    from tests.unit.test_constants import *
    from tests.unit.test_execution_result import *
    from tests.unit.test_executors import *
    from tests.unit.test_file_managers import *
    from tests.unit.test_library_runner import *
    from tests.unit.test_models import *
    from tests.unit.test_plugin_protocols import *
    from tests.unit.test_services import *
    from tests.unit.test_singer_cli_translator import *
    from tests.unit.test_singer_types import *
    from tests.unit.test_tap_abstractions import *
    from tests.unit.test_target_abstractions import *
    from tests.unit.test_typings import *
    from tests.unit.test_utilities import *
    from tests.unit.test_validators import *
    from tests.utilities import *

from tests.helpers import _LAZY_IMPORTS as _HELPERS_LAZY
from tests.integration import _LAZY_IMPORTS as _INTEGRATION_LAZY
from tests.unit import _LAZY_IMPORTS as _UNIT_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_HELPERS_LAZY,
    **_INTEGRATION_LAZY,
    **_UNIT_LAZY,
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
    "c": ["tests.constants", "FlextMeltanoTestConstants"],
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": "flext_tests",
    "e": "flext_tests",
    "h": "flext_tests",
    "helpers": "tests.helpers",
    "integration": "tests.integration",
    "job_run_config": "tests.conftest",
    "m": ["tests.models", "FlextMeltanoTestModels"],
    "meltano_cli_runner": "tests.conftest",
    "meltano_invoke_args": "tests.conftest",
    "meltano_project": "tests.conftest",
    "meltano_service": "tests.conftest",
    "meltano_yml_config": "tests.conftest",
    "mock_meltano_service": "tests.conftest",
    "mock_singer_tap": "tests.conftest",
    "mock_singer_target": "tests.conftest",
    "models": "tests.models",
    "p": ["tests.protocols", "FlextMeltanoTestProtocols"],
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
    "t": ["tests.typings", "FlextMeltanoTestTypes"],
    "tap_csv_config": "tests.conftest",
    "target_csv_config": "tests.conftest",
    "test_environment_config": "tests.conftest",
    "test_meltano_project_dir": "tests.conftest",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextMeltanoTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
