"""Real-execution tests for the Meltano public executor surface.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_meltano import FlextMeltano, FlextMeltanoCli, FlextMeltanoSettings, meltano
from tests import c, tm, u


class TestsFlextMeltanoExecutors:
    """Validate the public executor APIs through real Meltano execution paths."""

    @staticmethod
    def test_discovery_reads_real_project_plugins_without_resolving_parents(
        tmp_path: Path,
    ) -> None:
        """Local discovery reads SDK plugin groups without a Hub or installed plugin."""
        project_root = tmp_path / "discovery-project"
        project_root.mkdir()
        meltanofile = project_root / c.Meltano.PATH_MELTANO_PROJECT_FILE
        u.Cli.yaml_dump(
            meltanofile,
            {"project_id": "discovery-project"},
        ).unwrap()
        executor = FlextMeltano(
            runtime_settings=FlextMeltanoSettings.model_validate({
                "Meltano": {"MELTANO_PROJECT_ROOT": str(project_root)},
            }),
        )
        tm.that(executor.fetch_project_plugins(_cwd=project_root).unwrap(), empty=True)
        plugin_cases = (
            (c.Meltano.PluginType.EXTRACTORS.value, "tap-regression-unresolved"),
            (c.Meltano.PluginType.LOADERS.value, "target-regression-unresolved"),
        )
        configuration = u.Cli.yaml_safe_load(meltanofile).unwrap()
        u.Cli.yaml_dump(
            meltanofile,
            {
                **configuration,
                "plugins": {
                    plugin_type: [{"name": plugin_name}]
                    for plugin_type, plugin_name in plugin_cases
                },
            },
        ).unwrap()

        discovered = executor.fetch_project_plugins(_cwd=project_root).unwrap()
        tm.that(
            {(plugin["type"], plugin["name"]) for plugin in discovered},
            eq=set(plugin_cases),
        )
        tm.that(
            set(executor.discover_installed_plugins().unwrap()),
            eq={plugin_name for _, plugin_name in plugin_cases},
        )
        for plugin_type, plugin_name in plugin_cases:
            filtered = executor.fetch_project_plugins(
                plugin_type=plugin_type,
                _cwd=project_root,
            ).unwrap()
            tm.that([item["name"] for item in filtered], eq=[plugin_name])

    @staticmethod
    def test_executor_initialization() -> None:
        """The public Meltano facade is available as a singleton executor."""
        tm.that(meltano, none=False)

    @staticmethod
    def test_health_and_execute_surfaces() -> None:
        """Health and execute expose stable public payloads."""
        health_result = meltano.health()
        execute_result = meltano.execute()

        tm.ok(health_result)
        tm.ok(execute_result)
        tm.that(health_result.value["health"], eq="OK")
        tm.that(health_result.value["status"], eq="healthy")
        tm.that(
            execute_result.value[c.ContextKey.SERVICE_NAME], eq=meltano.service_name
        )
        tm.that(execute_result.value["status"], eq="active")

    @staticmethod
    def test_fetch_version_and_run_cli_surfaces() -> None:
        """Version lookup and the CLI readiness payload stay available."""
        fetch_result = meltano.fetch_version()
        ready_result = meltano.run_cli()

        tm.ok(fetch_result)
        tm.ok(ready_result)
        tm.that(fetch_result.value, is_=str)
        tm.that(ready_result.value["status"], eq="ready")

    @staticmethod
    def test_execute_meltano_command_normalizes_runtime_commands() -> None:
        """Executor runtime commands normalize both prefixed and unprefixed forms."""
        prefixed_result = meltano.execute_meltano_command(["meltano", "version"])
        unprefixed_result = meltano.execute_meltano_command(["help"])

        tm.ok(prefixed_result)
        tm.ok(unprefixed_result)
        tm.ok(prefixed_result.value.success)
        tm.ok(unprefixed_result.value.success)
        tm.that(prefixed_result.value.command[0], eq="--version")
        tm.that(unprefixed_result.value.command[0], eq="--help")

    @staticmethod
    def test_execute_meltano_command_rejects_empty_command() -> None:
        """Executor runtime commands fail fast on an empty command sequence."""
        result = meltano.execute_meltano_command([])

        tm.fail(result, has="empty")

    @staticmethod
    def test_project_root_property_returns_path() -> None:
        """Executor project_root remains a concrete filesystem path."""
        tm.that(meltano.project_root, is_=Path)

    @staticmethod
    def test_cli_run_version_returns_successful_result() -> None:
        """The public CLI runs the version command and returns a successful result."""
        cli_instance = FlextMeltanoCli()

        result = cli_instance.run(["version"])

        tm.ok(result)
        tm.ok(result.value)
