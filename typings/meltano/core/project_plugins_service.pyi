# Copyright (c) 2026 FLEXT Team. All rights reserved.

from collections.abc import Iterator

from meltano.core.plugin.base import PluginType
from meltano.core.plugin.project_plugin import ProjectPlugin
from meltano.core.project import Project

class ProjectPluginsService:
    def __init__(self, project: Project) -> None: ...
    def plugins(
        self,
        *,
        ensure_parent: bool = True,
    ) -> Iterator[ProjectPlugin]: ...
    def plugins_by_type(
        self,
        *,
        ensure_parent: bool = True,
    ) -> dict[PluginType, list[ProjectPlugin]]: ...
