# from flext-meltano/docs/api-reference.md:244
from __future__ import annotations


def validate_project(self) -> p.Result[FlextMeltanoModels.ProjectValidation]:
    """Validate Meltano project configuration and structure.

    Returns:
        r containing validation result or error

    """```
##### list_plugins(plugin_type=None)

**List available Meltano plugins**

