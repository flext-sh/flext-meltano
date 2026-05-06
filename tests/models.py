"""Test models for flext-meltano.

Provides test-specific models extending TestsFlextModels and m
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_tests import FlextTestsModels

from flext_meltano import m
from tests import c, p, t


class TestsFlextMeltanoModels(FlextTestsModels, m):
    """Test models - composition of TestsFlextModels + m.

    Hierarchy:
    - TestsFlextModels: Generic test utilities from flext-tests
    - m: Domain models from flext-meltano
    - TestsFlextMeltanoModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Meltano.* - Production domain models (inherited)
    """

    class Meltano(m.Meltano):
        """Meltano domain models test namespace."""

        class Tests(FlextTestsModels.Tests):
            """Test fixtures namespace for flext-meltano.

            Contains test-specific models and fixtures that should not
            be part of production code.
            """

            class SingerSdkStreamInfo(m.BaseModel):
                """Minimal Singer stream fixture consumed by the SDK adapter tests."""

                name: t.NonEmptyStr = m.Field(
                    description="Singer stream name exposed by the adapter fixture.",
                )

            class SingerSdkSuccessfulTap(m.BaseModel):
                """Singer tap fixture that exercises the successful adapter path."""

                model_config = m.ConfigDict(validate_assignment=True)

                settings: t.MappingKV[str, t.JsonPayload] = m.Field(
                    default_factory=lambda: dict(
                        c.Meltano.Tests.SINGER_SDK_ADAPTER_SETTINGS,
                    ),
                    description="Settings mapping exposed through the adapter bridge.",
                )
                synced: bool = False

                @classmethod
                def get_singer_command(cls) -> t.Cli.ExternalCli:
                    """Return the canonical success CLI command for the fixture."""
                    _ = cls
                    return t.Cli.ExternalCli(
                        c.Meltano.Tests.SINGER_SDK_ADAPTER_SUCCESS_COMMAND,
                    )

                def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
                    """Return deterministic stream info fixtures."""
                    return [
                        TestsFlextMeltanoModels.Meltano.Tests.SingerSdkStreamInfo(
                            name=c.Meltano.Tests.SINGER_SDK_ADAPTER_STREAM_USERS,
                        ),
                    ]

                def sync_all(self) -> None:
                    """Mark the fixture as synchronized."""
                    self.synced = True

            class SingerSdkFailingTap(SingerSdkSuccessfulTap):
                """Singer tap fixture that raises SystemExit from the CLI path."""

                @classmethod
                @override
                def get_singer_command(cls) -> t.Cli.ExternalCli:
                    """Return the canonical failing CLI command for the fixture."""
                    _ = cls

                    def _raise_exit() -> None:
                        raise SystemExit(
                            c.Meltano.Tests.SINGER_SDK_ADAPTER_FAILURE_EXIT_CODE,
                        )

                    return t.Cli.ExternalCli(
                        c.Meltano.Tests.SINGER_SDK_ADAPTER_FAILURE_COMMAND,
                        callback=_raise_exit,
                    )


m = TestsFlextMeltanoModels

__all__: list[str] = ["TestsFlextMeltanoModels", "m"]
