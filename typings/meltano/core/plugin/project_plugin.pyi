# Copyright (c) 2026 FLEXT Team. All rights reserved.

from meltano.core.plugin.base import PluginType

class PluginRef:
    name: str
    variant: str | None
    type: PluginType

class ProjectPlugin(PluginRef):
    namespace: str | None
    pip_url: str | None
