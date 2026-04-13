"""Unit tests for small Meltano CLI managers."""

from __future__ import annotations

from flext_tests import tm

from flext_meltano import (
    FlextMeltanoDbtManager,
    FlextMeltanoPluginManager,
    FlextMeltanoSingerManager,
    FlextMeltanoStatusManager,
)
from tests import p, r, t


class _StubDbtCli:
    def __init__(self) -> None:
        self.help_called = False

    def show_dbt_help(self) -> None:
        self.help_called = True


class _StubPluginCli:
    def __init__(self) -> None:
        self.help_called = False

    def show_plugin_help(self) -> None:
        self.help_called = True


class _StubSingerCli:
    def __init__(self) -> None:
        self.tap_help_called = False
        self.target_help_called = False

    def show_tap_help(self) -> None:
        self.tap_help_called = True

    def show_target_help(self) -> None:
        self.target_help_called = True


class _StubStatusCli:
    def __init__(self) -> None:
        self.help_called = False

    def show_status_help(self) -> None:
        self.help_called = True


class _StubDbtService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str]]] = []

    def run_operation(self, operation: str, args: t.StrSequence) -> p.Result[str]:
        self.calls.append((operation, list(args)))
        return r[str].ok(f"dbt:{operation}")


class _StubPluginService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[str, ...]]] = []

    def install_plugin(self, plugin_type: str, plugin_name: str) -> p.Result[str]:
        self.calls.append(("install", (plugin_type, plugin_name)))
        return r[str].ok(f"installed:{plugin_type}:{plugin_name}")

    def get_plugin_info(self, plugin_name: str) -> p.Result[str]:
        self.calls.append(("info", (plugin_name,)))
        return r[str].ok(f"info:{plugin_name}")

    def list_plugins(self, plugin_type: str | None = None) -> p.Result[str]:
        plugin_value = "" if plugin_type is None else plugin_type
        self.calls.append(("list", (plugin_value,)))
        return r[str].ok("[]")


class _StubStatusService:
    def get_version(self) -> p.Result[str]:
        return r[str].ok("3.9.1")

    def run_health_check(self) -> p.Result[str]:
        return r[str].ok('{"status": "healthy"}')

    def show_status(self) -> p.Result[str]:
        return r[str].ok('{"status": "ready"}')


class TestFlextMeltanoCliSmallManagers:
    """Unit tests for small Meltano CLI managers."""

    def test_dbt_manager_routes_supported_operation_to_service(
        self,
    ) -> None:
        cli = _StubDbtCli()
        service = _StubDbtService()
        manager = FlextMeltanoDbtManager(cli, service=service)

        result = manager.handle_command(["run", "--models", "orders"])

        tm.ok(result)
        tm.that(result.value, eq="dbt:run")
        tm.that(service.calls, eq=[("run", ["--models", "orders"])])

    def test_dbt_manager_fails_for_unsupported_operation(self) -> None:
        manager = FlextMeltanoDbtManager(_StubDbtCli(), service=_StubDbtService())

        result = manager.handle_command(["seed"])

        tm.fail(result)
        tm.that(str(result.error), has="not supported")

    def test_plugin_manager_routes_list_and_install(self) -> None:
        cli = _StubPluginCli()
        service = _StubPluginService()
        manager = FlextMeltanoPluginManager(cli, service=service)

        list_result = manager.handle_command(["list", "extractors"])
        install_result = manager.handle_command(["install", "extractors", "tap-demo"])

        tm.ok(list_result)
        tm.ok(install_result)
        tm.that(
            service.calls,
            eq=[("list", ("extractors",)), ("install", ("extractors", "tap-demo"))],
        )

    def test_status_manager_routes_show_health_and_version(self) -> None:
        manager = FlextMeltanoStatusManager(
            _StubStatusCli(), service=_StubStatusService()
        )

        show_result = manager.handle_command(["show"])
        health_result = manager.handle_command(["health"])
        version_result = manager.handle_version_command([])

        tm.ok(show_result)
        tm.ok(health_result)
        tm.ok(version_result)
        tm.that(show_result.value, has='"ready"')
        tm.that(health_result.value, has='"healthy"')
        tm.that(version_result.value, eq="3.9.1")

    def test_singer_manager_returns_failure_for_placeholder_tap_and_target_ops(
        self,
    ) -> None:
        manager = FlextMeltanoSingerManager(_StubSingerCli())

        tap_result = manager.handle_tap_command(["run", "tap-demo"])
        target_result = manager.handle_target_command(["run", "target-demo"])

        tm.fail(tap_result)
        tm.fail(target_result)
        tm.that(str(tap_result.error), has="not supported")
        tm.that(str(target_result.error), has="not supported")
