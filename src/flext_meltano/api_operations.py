"""FLEXT Meltano API Operations - Railway-oriented API operations with flext-core patterns.

This module provides focused API operations following flext-core patterns
with railway-oriented programming and Python 3.13+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import r

from flext_meltano.api import FlextMeltano
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import t
from flext_meltano.utilities import u

# Import aliases for concise usage
m = FlextMeltanoModels


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

    def handle_create_pipeline_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle create_pipeline operation call with railway pattern."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "tap_name": {"default": "", "ops": {"ensure": "str"}},
                "target_name": {"default": "", "ops": {"ensure": "str"}},
                "config": {
                    "default": {},
                    "ops": {"ensure": "dict", "ensure_default": {}},
                },
            },
        )

        tap_name_raw = u.get(fields_dict, "tap_name", default="")
        target_name_raw = u.get(fields_dict, "target_name", default="")
        config_raw = u.get(fields_dict, "config", default={})

        # Type narrowing for API call
        tap_name = str(tap_name_raw) if tap_name_raw else ""
        target_name = str(target_name_raw) if target_name_raw else ""
        config: t.MeltanoCore.MeltanoConfigDict | None = (
            config_raw if isinstance(config_raw, dict) else None
        )

        if u.none_(tap_name, target_name):
            return r[t.JsonValue].fail("tap_name and target_name are required")

        result = self.api.create_pipeline(tap_name, target_name, config)
        if result.is_success and result.value is not None:
            # MeltanoConfigDict is dict[str, JsonValue] which IS a JsonValue
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "Pipeline creation failed")

    def handle_execute_pipeline_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle execute_pipeline operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "pipeline_id": {"default": "", "ops": {"ensure": "str"}},
                "config": {
                    "default": {},
                    "ops": {"ensure": "dict", "ensure_default": {}},
                },
            },
        )

        pipeline_id_raw = u.get(fields_dict, "pipeline_id", default="")
        config_raw = u.get(fields_dict, "config", default={})

        # Type narrowing for API call
        pipeline_id = str(pipeline_id_raw) if pipeline_id_raw else ""
        config: t.MeltanoCore.MeltanoConfigDict | None = (
            config_raw if isinstance(config_raw, dict) else None
        )

        if u.none_(pipeline_id):
            return r[t.JsonValue].fail("pipeline_id is required")

        result = self.api.execute_pipeline(pipeline_id, config)
        if result.is_success and result.value is not None:
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "Pipeline execution failed")

    def handle_install_plugin_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle install_plugin operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "plugin_type": {"default": "", "ops": {"ensure": "str"}},
                "plugin_name": {"default": "", "ops": {"ensure": "str"}},
                "config": {
                    "default": {},
                    "ops": {"ensure": "dict", "ensure_default": {}},
                },
            },
        )

        plugin_type_raw = u.get(fields_dict, "plugin_type", default="")
        plugin_name_raw = u.get(fields_dict, "plugin_name", default="")
        config_raw = u.get(fields_dict, "config", default={})

        # Type narrowing for API call
        plugin_type = str(plugin_type_raw) if plugin_type_raw else ""
        plugin_name = str(plugin_name_raw) if plugin_name_raw else ""
        config: t.MeltanoCore.MeltanoConfigDict | None = (
            config_raw if isinstance(config_raw, dict) else None
        )

        if u.none_(plugin_type, plugin_name):
            return r[t.JsonValue].fail("plugin_type and plugin_name are required")

        result = self.api.install_plugin(plugin_type, plugin_name, config)
        if result.is_success and result.value is not None:
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "Plugin installation failed")

    def handle_list_plugins_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle list_plugins operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        plugin_type_raw = None
        if isinstance(payload_guard, dict):
            plugin_type_raw = u.extract(payload_guard, "plugin_type")
        plugin_type = str(plugin_type_raw) if plugin_type_raw else None

        result = self.api.list_plugins(plugin_type)
        if result.is_success and result.value is not None:
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "Plugin listing failed")

    def handle_configure_environment_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle configure_environment operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "environment_name": {"default": "", "ops": {"ensure": "str"}},
                "config": {
                    "default": {},
                    "ops": {"ensure": "dict", "ensure_default": {}},
                },
            },
        )

        environment_name_raw = u.get(fields_dict, "environment_name", default="")
        config_raw = u.get(fields_dict, "config", default={})

        # Type narrowing for API call
        environment_name = str(environment_name_raw) if environment_name_raw else ""
        config: t.MeltanoCore.MeltanoConfigDict | None = (
            config_raw if isinstance(config_raw, dict) else None
        )

        if u.none_(environment_name):
            return r[t.JsonValue].fail("environment_name is required")

        result = self.api.configure_environment(environment_name, config)
        if result.is_success and result.value is not None:
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "Environment configuration failed")

    def handle_run_dbt_models_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle run_dbt_models operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "models": {
                    "default": [],
                    "ops": {"ensure": "list", "ensure_default": []},
                },
                "config": {
                    "default": {},
                    "ops": {"ensure": "dict", "ensure_default": {}},
                },
            },
        )

        models_raw = u.get(fields_dict, "models", default=[])
        config_raw = u.get(fields_dict, "config", default={})

        # Type narrowing for API call
        models: list[str] | None = (
            [str(m) for m in models_raw] if isinstance(models_raw, list) else None
        )
        config: t.MeltanoCore.MeltanoConfigDict | None = (
            config_raw if isinstance(config_raw, dict) else None
        )

        result = self.api.run_dbt_models(models, config)
        if result.is_success and result.value is not None:
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "DBT models execution failed")

    def handle_test_dbt_models_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle test_dbt_models operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "models": {
                    "default": [],
                    "ops": {"ensure": "list", "ensure_default": []},
                },
                "config": {
                    "default": {},
                    "ops": {"ensure": "dict", "ensure_default": {}},
                },
            },
        )

        models_raw = u.get(fields_dict, "models", default=[])
        config_raw = u.get(fields_dict, "config", default={})

        # Type narrowing for API call
        models: list[str] | None = (
            [str(m) for m in models_raw] if isinstance(models_raw, list) else None
        )
        config: t.MeltanoCore.MeltanoConfigDict | None = (
            config_raw if isinstance(config_raw, dict) else None
        )

        result = self.api.test_dbt_models(models, config)
        if result.is_success and result.value is not None:
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "DBT models testing failed")

    def handle_run_elt_pipeline_call(self, payload: t.JsonValue) -> r[t.JsonValue]:
        """Handle run_elt_pipeline operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "tap_name": {"default": "", "ops": {"ensure": "str"}},
                "target_name": {"default": "", "ops": {"ensure": "str"}},
                "dbt_models": {
                    "default": [],
                    "ops": {"ensure": "list", "ensure_default": []},
                },
                "config": {
                    "default": {},
                    "ops": {"ensure": "dict", "ensure_default": {}},
                },
            },
        )

        tap_name_raw = u.get(fields_dict, "tap_name", default="")
        target_name_raw = u.get(fields_dict, "target_name", default="")
        dbt_models_raw = u.get(fields_dict, "dbt_models", default=[])
        config_raw = u.get(fields_dict, "config", default={})

        # Type narrowing for API call
        tap_name = str(tap_name_raw) if tap_name_raw else ""
        target_name = str(target_name_raw) if target_name_raw else ""
        dbt_models: list[str] | None = (
            [str(m) for m in dbt_models_raw]
            if isinstance(dbt_models_raw, list)
            else None
        )
        config: t.MeltanoCore.MeltanoConfigDict | None = (
            config_raw if isinstance(config_raw, dict) else None
        )

        if u.none_(tap_name, target_name):
            return r[t.JsonValue].fail("tap_name and target_name are required")

        result = self.api.run_elt_pipeline(tap_name, target_name, dbt_models, config)
        if result.is_success and result.value is not None:
            return r[t.JsonValue].ok(result.value)
        return r[t.JsonValue].fail(result.error or "ELT pipeline execution failed")


__all__ = ["FlextMeltanoAPIOperations"]
