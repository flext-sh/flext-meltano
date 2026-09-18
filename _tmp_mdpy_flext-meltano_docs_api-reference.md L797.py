# from flext-meltano/docs/api-reference.md:797
from __future__ import annotations


def create_project(
    self, project_config: FlextMeltanoModels.ProjectConfig
) -> p.Result[FlextMeltanoModels.Project]:
    """Create a new Meltano project.

    Args:
        project_config: Project configuration

    Returns:
        r containing created project

    """```
##### validate_project(project_root)

**Validate Meltano project structure**

