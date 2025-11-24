"""FLEXT Meltano API Operations - Railway-oriented API operations with flext-core patterns.

This module provides focused API operations following flext-core patterns
with railway-oriented programming and Python 3.13+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from flext_core import FlextResult, FlextTypes

if TYPE_CHECKING:
    from flext_meltano.api import FlextMeltano
    from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoAPIOperations:
    """API operations with flext-core railway patterns.

    Provides complete API operation handling using Python 3.13+
    patterns and flext-core railway-oriented programming.

    ** Patterns Used:**
    - Railway-oriented programming for all operations
    - Python 3.13+ type parameter syntax
    - Dispatch table pattern for operation routing
    - Composition over inheritance for SOLID compliance

    Attributes:
    api: Reference to the parent API instance

    """

    def __init__(self, api: FlextMeltano) -> None:
        """Initialize API operations with API reference."""
        self.api = api

    def handle_create_pipeline_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle create_pipeline operation call with railway pattern."""
        if not isinstance(payload, dict):
            return FlextResult[FlextTypes.JsonValue].fail(
                "Payload must be a dictionary"
            )

        tap_name = payload.get("tap_name", "")
        target_name = payload.get("target_name", "")
        config = payload.get("config")

        if not tap_name or not target_name:
            return FlextResult[FlextTypes.JsonValue].fail(
                "tap_name and target_name are required"
            )

        result = self.api.create_pipeline(
            str(tap_name),
            str(target_name),
            config if isinstance(config, dict) else None,
        )
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "Pipeline creation failed"
        )

    def handle_execute_pipeline_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle execute_pipeline operation call."""
        if not isinstance(payload, dict):
            return FlextResult[FlextTypes.JsonValue].fail(
                "Payload must be a dictionary"
            )

        pipeline_id = payload.get("pipeline_id", "")
        config = payload.get("config")

        if not pipeline_id:
            return FlextResult[FlextTypes.JsonValue].fail("pipeline_id is required")

        result = self.api.execute_pipeline(
            str(pipeline_id), config if isinstance(config, dict) else None
        )
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "Pipeline execution failed"
        )

    def handle_install_plugin_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle install_plugin operation call."""
        if not isinstance(payload, dict):
            return FlextResult[FlextTypes.JsonValue].fail(
                "Payload must be a dictionary"
            )

        plugin_type = payload.get("plugin_type", "")
        plugin_name = payload.get("plugin_name", "")
        config = payload.get("config")

        if not plugin_type or not plugin_name:
            return FlextResult[FlextTypes.JsonValue].fail(
                "plugin_type and plugin_name are required"
            )

        result = self.api.install_plugin(
            str(plugin_type),
            str(plugin_name),
            config if isinstance(config, dict) else None,
        )
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "Plugin installation failed"
        )

    def handle_list_plugins_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle list_plugins operation call."""
        plugin_type = None
        if isinstance(payload, dict):
            plugin_type = payload.get("plugin_type")

        result = self.api.list_plugins(str(plugin_type) if plugin_type else None)
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "Plugin listing failed"
        )

    def handle_configure_environment_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle configure_environment operation call."""
        if not isinstance(payload, dict):
            return FlextResult[FlextTypes.JsonValue].fail(
                "Payload must be a dictionary"
            )

        environment_name = payload.get("environment_name", "")
        config = payload.get("config")

        if not environment_name:
            return FlextResult[FlextTypes.JsonValue].fail(
                "environment_name is required"
            )

        result = self.api.configure_environment(
            str(environment_name), config if isinstance(config, dict) else None
        )
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "Environment configuration failed"
        )

    def handle_run_dbt_models_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle run_dbt_models operation call."""
        models = None
        config = None
        if isinstance(payload, dict):
            models = payload.get("models")
            config = payload.get("config")

        result = self.api.run_dbt_models(
            models if isinstance(models, list) else None,
            config if isinstance(config, dict) else None,
        )
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "DBT models execution failed"
        )

    def handle_test_dbt_models_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle test_dbt_models operation call."""
        models: FlextMeltanoTypes.MeltanoCore.DbtModelList | None = None
        config: FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict | None = None
        if isinstance(payload, dict):
            models_raw = payload.get("models")
            config_raw = payload.get("config")
            if models_raw is not None and isinstance(models_raw, list):
                models = models_raw
            if config_raw is not None and isinstance(config_raw, dict):
                config = config_raw

        result = self.api.test_dbt_models(models, config)
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "DBT models testing failed"
        )

    def handle_run_elt_pipeline_call(
        self, payload: FlextTypes.JsonValue
    ) -> FlextResult[FlextTypes.JsonValue]:
        """Handle run_elt_pipeline operation call."""
        if not isinstance(payload, dict):
            return FlextResult[FlextTypes.JsonValue].fail(
                "Payload must be a dictionary"
            )

        tap_name = payload.get("tap_name", "")
        target_name = payload.get("target_name", "")
        dbt_models_raw = payload.get("dbt_models")
        config_raw = payload.get("config")

        dbt_models: FlextMeltanoTypes.MeltanoCore.DbtModelList | None = None
        config: FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict | None = None
        if dbt_models_raw is not None and isinstance(dbt_models_raw, list):
            dbt_models = dbt_models_raw
        if config_raw is not None and isinstance(config_raw, dict):
            config = config_raw

        if not tap_name or not target_name:
            return FlextResult[FlextTypes.JsonValue].fail(
                "tap_name and target_name are required"
            )

        result = self.api.run_elt_pipeline(
            str(tap_name), str(target_name), dbt_models, config
        )
        if result.is_success:
            return FlextResult[FlextTypes.JsonValue].ok(
                cast("FlextTypes.JsonValue", result.value)
            )
        return FlextResult[FlextTypes.JsonValue].fail(
            result.error or "ELT pipeline execution failed"
        )


__all__ = ["FlextMeltanoAPIOperations"]
