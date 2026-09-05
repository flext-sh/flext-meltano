# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import integration as integration
    from . import unit as unit
    from enum import StrEnum, unique
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x
    from pathlib import Path
    from typing import Final, TYPE_CHECKING

    from .base import TestsFlextMeltanoServiceBase, TestsFlextMeltanoServiceBase as s
    from .constants import TestsFlextMeltanoConstants, TestsFlextMeltanoConstants as c
    from .models import TestsFlextMeltanoModels, TestsFlextMeltanoModels as m
    from .protocols import TestsFlextMeltanoProtocols, TestsFlextMeltanoProtocols as p
    from .settings import TestsFlextMeltanoSettings
    from .typings import TestsFlextMeltanoTypes, TestsFlextMeltanoTypes as t
    from .unit.fixtures import (
        MELTANO_COMPONENT_CASES,
        MELTANO_COMPONENT_IDS,
        docker_manager,
        docker_services,
        meltano_component_case,
        meltano_execute_field,
        meltano_project,
        meltano_service,
        meltano_yml_config,
        postgres_service,
        redis_service,
        require_docker_service,
        singer_state,
        test_meltano_project_dir,
    )
    from .unit.tests_pipeline_cli_managers import TestFlextMeltanoPipelineCliManagers
    from .utilities import TestsFlextMeltanoUtilities, TestsFlextMeltanoUtilities as u
__all__: tuple[str, ...] = (
    "MELTANO_COMPONENT_CASES",
    "MELTANO_COMPONENT_IDS",
    "TYPE_CHECKING",
    "Final",
    "FlextTestsConstants",
    "MappingProxyType",
    "Path",
    "StrEnum",
    "TestFlextMeltanoPipelineCliManagers",
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoServiceBase",
    "TestsFlextMeltanoSettings",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoUtilities",
    "c",
    "d",
    "docker_manager",
    "docker_services",
    "e",
    "h",
    "integration",
    "m",
    "meltano_component_case",
    "meltano_execute_field",
    "meltano_project",
    "meltano_service",
    "meltano_yml_config",
    "p",
    "postgres_service",
    "r",
    "redis_service",
    "require_docker_service",
    "s",
    "singer_state",
    "t",
    "td",
    "test_meltano_project_dir",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "unique",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextMeltanoServiceBase", "s"),
            ".constants": ("TestsFlextMeltanoConstants", "c"),
            ".integration": ("integration",),
            ".models": ("TestsFlextMeltanoModels", "m"),
            ".protocols": ("TestsFlextMeltanoProtocols", "p"),
            ".settings": ("TestsFlextMeltanoSettings",),
            ".typings": ("TestsFlextMeltanoTypes", "t"),
            ".unit": ("unit",),
            ".unit.fixtures": (
                "MELTANO_COMPONENT_CASES",
                "MELTANO_COMPONENT_IDS",
                "docker_manager",
                "docker_services",
                "meltano_component_case",
                "meltano_execute_field",
                "meltano_project",
                "meltano_service",
                "meltano_yml_config",
                "postgres_service",
                "redis_service",
                "require_docker_service",
                "singer_state",
                "test_meltano_project_dir",
            ),
            ".unit.tests_pipeline_cli_managers": (
                "TestFlextMeltanoPipelineCliManagers",
            ),
            ".utilities": ("TestsFlextMeltanoUtilities", "u"),
            "enum": ("StrEnum", "unique"),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
            "pathlib": ("Path",),
            "types": ("MappingProxyType",),
            "typing": ("Final", "TYPE_CHECKING"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
