"""Service base for flext-meltano tests."""

from __future__ import annotations

from typing import override

from flext_meltano import m
from flext_tests import s as tests_s
from tests.settings import TestsFlextMeltanoSettings


class TestsFlextMeltanoServiceBase(tests_s):
    """Meltano test service base with source and test settings namespaces."""

    # NOTE (multi-agent): flext-tests owns fetch_settings; this project
    # declares only its more-specific bootstrap settings type.
    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextMeltanoSettings)


s = TestsFlextMeltanoServiceBase

__all__: list[str] = ["TestsFlextMeltanoServiceBase", "s"]
