from pathlib import Path
from typing import ClassVar

from meltano.core.project_plugins_service import ProjectPluginsService

class MeltanoFile:
    environments: list[Environment]

class Environment:
    name: str

class Project:
    _default: ClassVar[Project | None]

    root: Path
    """The resolved project root directory."""

    def __init__(
        self,
        root: Path | str,
        environment: Environment | None = None,
        *,
        readonly: bool = False,
        dotenv_file: Path | None = None,
    ) -> None: ...
    @classmethod
    def find(
        cls,
        project_root: Path | str | None = None,
        *,
        activate: bool = True,
        dotenv_file: Path | None = None,
    ) -> Project: ...
    @classmethod
    def deactivate(cls) -> None: ...
    @property
    def plugins(self) -> ProjectPluginsService: ...
    @property
    def meltano(self) -> MeltanoFile: ...
    @property
    def meltanofile(self) -> Path: ...
