# from flext-meltano/docs/api-reference.md:817
from __future__ import annotations


def validate_project(
    self, project_root: Path | str
) -> p.Result[FlextMeltanoModels.ProjectValidation]:
    """Validate Meltano project structure and configuration.

    Args:
        project_root: Path to project root directory

    Returns:
        r containing validation result

    """```
##### get_project_info(project_root)

**Get project information and metadata**

