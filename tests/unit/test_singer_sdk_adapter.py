"""Tests for the Singer SDK tap adapter bridge."""

from __future__ import annotations

from typing import override

from flext_cli import t as cli_t

from flext_meltano import FlextMeltanoSingerTapAdapter
from tests import t

_SingerCommand: type = cli_t.Cli.ExternalCli


class _StreamInfo:
    def __init__(self, name: str) -> None:
        self.name = name


class _SuccessfulTap:
    def __init__(self) -> None:
        self.settings = {"tap": "ok"}
        self.synced = False

    @classmethod
    def get_singer_command(cls) -> _SingerCommand:
        return _SingerCommand("tap-ok")

    def discover_streams(self) -> t.SequenceOf[_StreamInfo]:
        return [_StreamInfo("users")]

    def sync_all(self) -> None:
        self.synced = True


class _FailingTap(_SuccessfulTap):
    @classmethod
    @override
    def get_singer_command(cls) -> _SingerCommand:
        class _FailingCommand(_SingerCommand):
            @override
            def main(
                self,
                args: t.SequenceOf[str] | None = None,
                prog_name: str | None = None,
                complete_var: str | None = None,
                standalone_mode: bool = True,
                windows_expand_args: bool = True,
                **extra: t.JsonValue,
            ) -> t.JsonValue:
                _ = (
                    args,
                    prog_name,
                    complete_var,
                    standalone_mode,
                    windows_expand_args,
                    extra,
                )
                raise SystemExit(3)

        return _FailingCommand("tap-fail")


class TestsFlextMeltanoSingerSdkAdapter:
    """Test suite for the Singer SDK tap adapter bridge."""

    def test_adapter_exposes_config_and_streams(self) -> None:
        """The adapter preserves the internal tap runtime contract."""
        adapter = FlextMeltanoSingerTapAdapter(_SuccessfulTap())
        assert adapter.settings == {"tap": "ok"}
        assert [stream.name for stream in adapter.discover_streams()] == ["users"]

    def test_adapter_delegates_sync(self) -> None:
        """Sync execution is delegated to the wrapped Singer tap."""
        tap = _SuccessfulTap()
        adapter = FlextMeltanoSingerTapAdapter(tap)
        adapter.sync_all()
        assert tap.synced is True

    def test_adapter_normalizes_successful_cli_exit_code(self) -> None:
        """Successful Singer CLI execution returns zero."""
        adapter = FlextMeltanoSingerTapAdapter(_SuccessfulTap())
        assert adapter.run_cli([], "tap-ok") == 0

    def test_adapter_normalizes_system_exit(self) -> None:
        """Singer CLI failures are converted into integer exit codes."""
        adapter = FlextMeltanoSingerTapAdapter(_FailingTap())
        assert adapter.run_cli([], "tap-fail") == 3
