"""FLEXT Meltano API Operations - Railway-oriented API operations with flext-core patterns.

This module provides focused API operations following flext-core patterns
with railway-oriented programming and Python 3.13+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextResult, u

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.typings import FlextMeltanoTypes

if TYPE_CHECKING:
    from flext_meltano.api import FlextMeltano

# Import aliases for concise usage
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
p = FlextMeltanoProtocols
r = FlextResult


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
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
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
                "config": {"default": {}, "ops": {"ensure": "dict", "ensure_default": {}}},
            },
            on_error="stop",
        )

        tap_name = u.get(fields_dict, "tap_name", default="")
        target_name = u.get(fields_dict, "target_name", default="")
        config = u.get(fields_dict, "config", default={})

        if u.none_(tap_name, target_name):
            return r[t.JsonValue].fail("tap_name and target_name are required")

        result = self.api.create_pipeline(tap_name, target_name, config)
        return u.cast(result, default_error="Pipeline creation failed")

    def handle_execute_pipeline_call(
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
        """Handle execute_pipeline operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "pipeline_id": {"default": "", "ops": {"ensure": "str"}},
                "config": {"default": {}, "ops": {"ensure": "dict", "ensure_default": {}}},
            },
            on_error="stop",
        )

        pipeline_id = u.get(fields_dict, "pipeline_id", default="")
        config = u.get(fields_dict, "config", default={})

        if u.none_(pipeline_id):
            return r[t.JsonValue].fail("pipeline_id is required")

        result = self.api.execute_pipeline(pipeline_id, config)
        return u.cast(result, default_error="Pipeline execution failed")

    def handle_install_plugin_call(
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
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
                "config": {"default": {}, "ops": {"ensure": "dict", "ensure_default": {}}},
            },
            on_error="stop",
        )

        plugin_type = u.get(fields_dict, "plugin_type", default="")
        plugin_name = u.get(fields_dict, "plugin_name", default="")
        config = u.get(fields_dict, "config", default={})

        if u.none_(plugin_type, plugin_name):
            return r[t.JsonValue].fail("plugin_type and plugin_name are required")

        result = self.api.install_plugin(plugin_type, plugin_name, config)
        return u.cast(result, default_error="Plugin installation failed")

    def handle_list_plugins_call(
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
        """Handle list_plugins operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        plugin_type_raw = u.extract(payload_guard, "plugin_type") if payload_guard else None
        plugin_type = str(plugin_type_raw) if plugin_type_raw else None

        result = self.api.list_plugins(plugin_type)
        return u.cast(result, default_error="Plugin listing failed")

    def handle_configure_environment_call(
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
        """Handle configure_environment operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "environment_name": {"default": "", "ops": {"ensure": "str"}},
                "config": {"default": {}, "ops": {"ensure": "dict", "ensure_default": {}}},
            },
            on_error="stop",
        )

        environment_name = u.get(fields_dict, "environment_name", default="")
        config = u.get(fields_dict, "config", default={})

        if u.none_(environment_name):
            return r[t.JsonValue].fail("environment_name is required")

        result = self.api.configure_environment(environment_name, config)
        return u.cast(result, default_error="Environment configuration failed")

    def handle_run_dbt_models_call(
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
        """Handle run_dbt_models operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "models": {"default": [], "ops": {"ensure": "list", "ensure_default": []}},
                "config": {"default": {}, "ops": {"ensure": "dict", "ensure_default": {}}},
            },
            on_error="stop",
        )

        models = u.get(fields_dict, "models", default=[])
        config = u.get(fields_dict, "config", default={})

        result = self.api.run_dbt_models(models, config)
        return u.cast(result, default_error="DBT models execution failed")

    def handle_test_dbt_models_call(
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
        """Handle test_dbt_models operation call."""
        payload_guard = u.guard(payload, dict, return_value=True)
        if u.empty(payload_guard):
            return r[t.JsonValue].fail("Payload must be a dictionary")

        # DSL mnemonic pattern: extract and validate fields
        fields_dict = u.fields(
            payload_guard,
            {
                "models": {"default": [], "ops": {"ensure": "list", "ensure_default": []}},
                "config": {"default": {}, "ops": {"ensure": "dict", "ensure_default": {}}},
            },
            on_error="stop",
        )

        models = u.get(fields_dict, "models", default=[])
        config = u.get(fields_dict, "config", default={})

        result = self.api.test_dbt_models(models, config)
        return u.cast(result, default_error="DBT models testing failed")

    def handle_run_elt_pipeline_call(
        self, payload: t.JsonValue
    ) -> r[t.JsonValue]:
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
                "dbt_models": {"default": [], "ops": {"ensure": "list", "ensure_default": []}},
                "config": {"default": {}, "ops": {"ensure": "dict", "ensure_default": {}}},
            },
            on_error="stop",
        )

        tap_name = u.get(fields_dict, "tap_name", default="")
        target_name = u.get(fields_dict, "target_name", default="")
        dbt_models = u.get(fields_dict, "dbt_models", default=[])
        config = u.get(fields_dict, "config", default={})

        if u.none_(tap_name, target_name):
            return r[t.JsonValue].fail("tap_name and target_name are required")

        result = self.api.run_elt_pipeline(tap_name, target_name, dbt_models, config)
        return u.cast(result, default_error="ELT pipeline execution failed")


__all__ = ["FlextMeltanoAPIOperations"]
