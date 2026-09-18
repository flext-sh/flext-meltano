# from flext-meltano_docs/architecture.md:200
from __future__ import annotations


# ✅ FUTURE STATE - Library wrapper pattern
class _MeltanoLibraryWrapper:
    """Internal wrapper for meltano library operations."""

    @staticmethod
    def create_project(path: Path) -> p.Result[m.Meltano.ProjectModel]:
        """Create Meltano project through library API."""
        # Implementation with proper error handling```
## 📊 Type System Architecture

### **FlextMeltanoTypes Hierarchy**

