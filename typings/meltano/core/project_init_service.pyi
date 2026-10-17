from os import PathLike

from meltano.core.project import Project

class ProjectInitServiceError(Exception): ...

class ProjectInitService:
    def __init__(self, project_directory: PathLike[str]) -> None: ...
    def init(
        self,
        *,
        activate: bool = True,
        force: bool = False,
    ) -> Project: ...
