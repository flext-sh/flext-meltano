"""FLEXT Meltano settings constants — logging, service, defaults, capabilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar, Self

from flext_core import FlextSettings

from flext_meltano import t
from flext_meltano._constants import FlextMeltanoConstantsEnums


class FlextMeltanoConstantsSettings(FlextSettings):
    """Meltano configuration, defaults, and operational constants.

    All constants are flat with descriptive prefixes to explain their usage.
    The MRO carries ``FlextSettings`` (ENFORCE-042); the class is a namespace
    holder, never instantiated — class-attribute access resolves via the MRO.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton/validation machinery cannot leak into instantiated
    # facade composites (e.g. the ``u`` logging facade).
    #
    # Tooling ruling 2026-10-05 (bead gc-eqvqx5, PR #158): the ``object``
    # annotations on this plumbing are the narrowest spellings pyright's LSP
    # override contract admits for ``__new__``/``__init__``/``__setattr__``/
    # ``__eq__`` (the family's own canonical plumbing — flext-core
    # ``FlextSettings.__new__`` and ``Entity.__eq__`` — uses the same), while
    # the ``ban-broad-annotation`` codemod rule bans that identifier outright.
    # The rule has no dunder-override carve-out, so each directive below is a
    # scoped, dated admission of the tooling conflict, not a code dodge; the
    # durable cure is a dunder carve-out in the flext-infra rule owner.
    def __new__(
        cls,
        *args: object,  # ast-grep-ignore: ban-broad-annotation
        **kwargs: object,  # ast-grep-ignore: ban-broad-annotation
    ) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    def __init__(
        self,
        *args: object,  # ast-grep-ignore: ban-broad-annotation
        **kwargs: object,  # ast-grep-ignore: ban-broad-annotation
    ) -> None:
        _ = self, args, kwargs

    def __setattr__(
        self,
        name: str,
        value: object,  # ast-grep-ignore: ban-broad-annotation
    ) -> None:
        object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:  # ast-grep-ignore: ban-broad-annotation
        """Identity equality per the namespace-holder contract.

        Returns:
            The resulting ``bool``.

        """
        return object.__eq__(self, other)

    def __hash__(self) -> int:
        """Identity hash per the namespace-holder contract.

        Returns:
            The resulting ``int``.

        """
        return object.__hash__(self)

    # Environments
    ENVIRONMENT_RUNTIME_ALIASES: ClassVar[t.StrMapping] = MappingProxyType({
        FlextMeltanoConstantsEnums.Environment.DEVELOPMENT.value: (
            FlextMeltanoConstantsEnums.ProjectEnvironment.DEV
        ),
        FlextMeltanoConstantsEnums.Environment.TESTING.value: (
            FlextMeltanoConstantsEnums.EnvironmentAlias.TEST
        ),
        FlextMeltanoConstantsEnums.Environment.PRODUCTION.value: (
            FlextMeltanoConstantsEnums.ProjectEnvironment.PROD
        ),
    })

    # Defaults
    DEFAULT_SERVICE_VERSION: ClassVar[str] = "0.9.9"
    DEFAULT_TIMEOUT_SECONDS: ClassVar[int] = 300

    # CliDefaults
    CLI_DEFAULT_PIPELINES_ROOT_ENV: ClassVar[str] = "FLEXT_MELTANO_PIPELINES_DIR"
    CLI_DEFAULT_PIPELINE_CONFIG_FILE: ClassVar[str] = "pipeline.json"
    CLI_DEFAULT_PIPELINE_PID_FILE: ClassVar[str] = "pipeline.pid"

    # Capabilities
    PLUGIN_GROUP_ALIASES: ClassVar[
        t.MappingKV[str, FlextMeltanoConstantsEnums.PluginType]
    ] = MappingProxyType({
        "extractor": FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        FlextMeltanoConstantsEnums.PluginType.EXTRACTORS: (
            FlextMeltanoConstantsEnums.PluginType.EXTRACTORS
        ),
        "tap": FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        "loader": FlextMeltanoConstantsEnums.PluginType.LOADERS,
        FlextMeltanoConstantsEnums.PluginType.LOADERS: (
            FlextMeltanoConstantsEnums.PluginType.LOADERS
        ),
        "target": FlextMeltanoConstantsEnums.PluginType.LOADERS,
        "transformer": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
        "transformers": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
        FlextMeltanoConstantsEnums.PluginType.TRANSFORMS: (
            FlextMeltanoConstantsEnums.PluginType.TRANSFORMS
        ),
        "dbt": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
    })
    DBT_DEFAULT_DOCS_ARGS: ClassVar[
        tuple[FlextMeltanoConstantsEnums.DbtCommand, ...]
    ] = (FlextMeltanoConstantsEnums.DbtCommand.GENERATE,)

    # Handlers
    HANDLER_ALL: ClassVar[tuple[FlextMeltanoConstantsEnums.HandlerType, ...]] = (
        FlextMeltanoConstantsEnums.HandlerType.SOURCE,
        FlextMeltanoConstantsEnums.HandlerType.SINK,
        FlextMeltanoConstantsEnums.HandlerType.PIPELINE,
    )

    # BatchDefaults
    BATCH_DEFAULT_DEFAULT_BATCH_SIZE: ClassVar[int] = 1000


__all__: list[str] = ["FlextMeltanoConstantsSettings"]
