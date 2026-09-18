# from flext-meltano_docs/getting-started.md:98
from __future__ import annotations
from flext_cli import u


# All flext-meltano operations return r[T]
def example_operation() -> p.Result[str]:
    try:
        # Your operation logic
        return r.ok("Operation successful")
    except Exception as e:
        return r.fail(f"Operation failed: {e}")


# Usage pattern
result = example_operation()
if result.success:
    data = result.unwrap()
    u.Cli.print(f"Success: {data}")
else:
    u.Cli.print(f"Error: {result.error}")```
______________________________________________________________________

## 🔧 Development Workflow

### **Quality Gates**

