"""FLEXT Pipeline Services - Generic service orchestration with flext-core patterns.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Mapping
from typing import Self, cast

from flext_meltano import FlextMeltanoServiceBase, FlextMeltanoSettings, c, p, r, t, u


class FlextMeltanoService(FlextMeltanoServiceBase):
    """Generic data pipeline service with the component factory."""

    @staticmethod
    def _settings_payload(config: Mapping[str, t.Scalar]) -> t.JsonDict | None:
        """Normalize loose scalar ``config`` into one JSON settings payload.

        Returns ``None`` for empty config so the specialized factory skips the
        settings copy entirely instead of validating an empty mapping.

        Returns:
            The resulting ``t.JsonDict | None``.

        """
        if not config:
            return None
        return {key: u.normalize_to_json_value(value) for key, value in config.items()}

    @classmethod
    def create_component_service(
        cls,
        component_name: str,
        field_name: str,
        component_label: str,
        config: Mapping[str, t.Scalar],
    ) -> p.Result[Self]:
        """Create one specialized Meltano component service.

        Pydantic v2 owns every validation step:
        - ``cls.model_validate(payload)`` validates the construction payload
          and raises ``ValidationError`` for unknown ``field_name``;
        - ``FlextMeltanoSettings.model_validate`` validates the runtime
          settings payload (per-field coercion + type narrowing).

        ``config`` stays broad because the downstream Pydantic validator
        handles every concrete value type — it keeps one call site for both
        ``Scalar`` and ``JsonValue`` callers without manual coercion at the
        boundary.

        Returns:
            The resulting ``p.Result[Self]``.

        """
        try:
            instance: Self = cls.model_validate({
                c.ContextKey.SERVICE_NAME: f"{component_name}_service",
                c.ContextKey.SERVICE_VERSION: c.Meltano.DEFAULT_SERVICE_VERSION,
                field_name: component_name,
            })
            settings_payload = cls._settings_payload(config)
            if settings_payload is not None:
                # Why: model_copy's checker-facing return loses the caller's
                # Self; the copied snapshot is re-declared at the owner type so
                # the result factory binds its value parameter exactly.
                copied: Self = instance.model_copy(
                    update={
                        "runtime_settings": FlextMeltanoSettings.model_validate(
                            settings_payload,
                        ),
                    },
                )
                instance = copied
            return r.ok(instance)
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as ex:
            # Why: fail() binds its payload type from the result class's own
            # parameter, which no caller-side spelling carries through both
            # checkers; the declared owner contract is cast once here.
            return cast(
                "p.Result[Self]",
                r.fail(
                    f"Failed to create {component_label} '{component_name}': {ex}",
                ),
            )


__all__: list[str] = ["FlextMeltanoService"]
