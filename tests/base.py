"""Service base for flext-meltano tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_meltano import m
from tests.settings import TestsFlextMeltanoSettings


class TestsFlextMeltanoServiceBase(tests_s):
    """Meltano test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextMeltanoSettings:
        """Return the typed Meltano+Tests settings singleton."""

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextMeltanoSettings)


s = TestsFlextMeltanoServiceBase

__all__: list[str] = ["TestsFlextMeltanoServiceBase", "s"]
