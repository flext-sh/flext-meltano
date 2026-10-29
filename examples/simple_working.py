"""Simple working example using ONLY real FLEXT Meltano APIs.

This example demonstrates the actual working functionality that exists,
using only classes and functions that are actually exported from flext_meltano.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from jsonschema import Draft202012Validator, ValidationError

from examples import c, m, meltano, p, t, u
from flext_meltano import FlextMeltanoSettings


class ExamplesFlextMeltanoSimple:
    """Simple working examples over the public FLEXT Meltano facade."""

    logger = u.fetch_logger(__name__)

    @staticmethod
    def serialization_example() -> None:
        """Exercise public serialization against the actual JSON Schema consumer.

        Raises:
            ValueError: If Serialization mutated the original connection
                configuration or a retained nested configuration; or if
                Serialized connection configuration exposed sensitive input; or
                if Serialization changed a non-sensitive input; or if Serialized
                nested configuration exposed sensitive input; or if
                Serialization changed a configuration list; or if Serialized
                configuration list violated its contract.

        """
        marker = "serialization-input-marker"
        connection = {
            "password": marker,
            "display_name": "serialization-consumer",
            "database": {"password": marker, "name": "serialization-consumer"},
            "options": [{"token": marker, "enabled": True}],
        }
        tap = m.Meltano.TapConfig.model_validate({
            "tap_type": "tap-serialization-consumer",
            "connection_config": connection,
        })
        target = m.Meltano.TargetConfig.model_validate({
            "target_type": "target-serialization-consumer",
            "connection_config": connection,
        })
        adapter = u.type_adapter(t.TypeForm(t.JsonMapping))
        for config in (tap, target):
            payloads = (
                adapter.validate_python(config.model_dump(mode="json")),
                adapter.validate_json(config.model_dump_json()),
            )
            for payload in payloads:
                exported = adapter.validate_python(payload["connection_config"])
                if exported["password"] == marker:
                    msg = "Serialized connection configuration exposed sensitive input"
                    raise ValueError(msg)
                if exported["display_name"] != connection["display_name"]:
                    msg = "Serialization changed a non-sensitive input"
                    raise ValueError(msg)
                database = adapter.validate_python(exported["database"])
                options = u.type_adapter(t.TypeForm(t.JsonValue)).validate_python(
                    exported["options"]
                )
                if database["password"] == marker:
                    msg = "Serialized nested configuration exposed sensitive input"
                    raise ValueError(msg)
                if not isinstance(options, list) or not options:
                    msg = "Serialization changed a configuration list"
                    raise ValueError(msg)
                option = adapter.validate_python(options[0])
                if option["token"] == marker or option["enabled"] is not True:
                    msg = "Serialized configuration list violated its contract"
                    raise ValueError(msg)
            if config.connection_config["password"] != marker:
                msg = "Serialization mutated the original connection configuration"
                raise ValueError(msg)
            original_database = adapter.validate_python(
                config.connection_config["database"]
            )
            if original_database["password"] != marker:
                msg = "Serialization mutated a retained nested configuration"
                raise ValueError(msg)
        ExamplesFlextMeltanoSimple.schema_serialization_example()
        ExamplesFlextMeltanoSimple.logger.info(
            "Public serialization and JSON Schema consumer validated"
        )

    @staticmethod
    def schema_serialization_example() -> None:
        """Exercise the exported stream schema with the actual JSON Schema validator.

        Raises:
            ValueError: The serialized schema accepted an invalid record.

        """
        adapter = u.type_adapter(t.TypeForm(t.JsonMapping))
        stream = m.Meltano.StreamDefinition.model_validate({
            "stream_name": "serialization-consumer",
            "source_type": "serialization-consumer",
            "stream_schema": {
                "properties": {"id": {"type": "integer"}},
                "required": ["id"],
            },
        })
        payload = adapter.validate_json(stream.model_dump_json())
        schema = adapter.validate_python(payload["stream_schema"])
        Draft202012Validator.check_schema(schema)
        validator = cast(
            "p.Cli.JsonSchemaValidator",
            Draft202012Validator(schema),
        )
        validator.validate({"id": 1})
        rejected = u.try_(
            lambda: validator.validate({"id": "not-an-integer"}),
            catch=ValidationError,
            op_name="schema serialization rejection probe",
        )
        if rejected.success:
            msg = "Serialized schema accepted an invalid record"
            raise ValueError(msg)
        ExamplesFlextMeltanoSimple.logger.info(
            "Serialized schema rejected the invalid record"
        )

    @staticmethod
    def simple_api_example() -> None:
        """Demonstrate the public Meltano facade."""
        version = meltano.fetch_version().unwrap()
        ExamplesFlextMeltanoSimple.logger.info("Meltano version", version=version)
        plugins = meltano.discover_installed_plugins().unwrap()
        ExamplesFlextMeltanoSimple.logger.info(
            "Installed plugins discovered", count=len(plugins)
        )

    @staticmethod
    def simple_component_example() -> None:
        """Demonstrate canonical component factories."""
        tap = meltano.tap("tap-csv").unwrap()
        target = meltano.target("target-jsonl").unwrap()
        dbt = meltano.dbt("analytics").unwrap()
        ExamplesFlextMeltanoSimple.logger.info("Tap source", name=tap.source_name)
        ExamplesFlextMeltanoSimple.logger.info("Target sink", name=target.sink_name)
        ExamplesFlextMeltanoSimple.logger.info(
            "DBT transformation", name=dbt.transformation_name
        )

    @staticmethod
    def simple_runtime_example() -> None:
        """Demonstrate the public runtime command surface.

        Raises:
            RuntimeError: If The actual Meltano runtime command failed.

        """
        command = meltano.execute_meltano_command([
            c.Meltano.CMD_BINARY,
            c.Meltano.CMD_VERSION_OPTION,
        ]).unwrap()
        if not command.success or command.exit_code != 0:
            msg = "The actual Meltano runtime command failed"
            raise RuntimeError(msg)
        ExamplesFlextMeltanoSimple.logger.info(
            "Runtime command result", result=command.model_dump(mode="python")
        )

    @staticmethod
    def simple_config_example() -> None:
        """Demonstrate typed settings through the public facade."""
        typed_settings = FlextMeltanoSettings.fetch_global()
        ExamplesFlextMeltanoSimple.logger.info(
            "Config created",
            project_root=typed_settings.Meltano.project_root,
            config_dir=typed_settings.Meltano.config_dir,
        )
        ExamplesFlextMeltanoSimple.logger.info(
            "Environment", environment=typed_settings.Meltano.environment
        )

    @staticmethod
    def run_examples() -> None:
        """Run all examples in display order."""
        ExamplesFlextMeltanoSimple.serialization_example()
        ExamplesFlextMeltanoSimple.simple_api_example()
        ExamplesFlextMeltanoSimple.logger.info("")
        ExamplesFlextMeltanoSimple.simple_component_example()
        ExamplesFlextMeltanoSimple.logger.info("")
        ExamplesFlextMeltanoSimple.simple_runtime_example()
        ExamplesFlextMeltanoSimple.logger.info("")
        ExamplesFlextMeltanoSimple.simple_config_example()

    @staticmethod
    def main() -> None:
        """Executable entry point running all examples.

        Raises:
            ValueError: If a serialization example violated its contract.
            RuntimeError: If a runtime command failed.
            OSError: If the runtime command could not execute.

        """
        ExamplesFlextMeltanoSimple.logger.info(
            "=== FLEXT Meltano Simple Working Examples ==="
        )
        try:
            ExamplesFlextMeltanoSimple.run_examples()
        except (ValueError, RuntimeError, OSError):
            ExamplesFlextMeltanoSimple.logger.exception("Error executing examples")
            raise


if __name__ == "__main__":
    ExamplesFlextMeltanoSimple.main()

__all__: list[str] = ["ExamplesFlextMeltanoSimple"]
