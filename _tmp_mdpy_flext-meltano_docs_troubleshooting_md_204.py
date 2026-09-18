# from flext-meltano_docs/troubleshooting.md:204
from __future__ import annotations


# ❌ Incorrect
def risky_operation():
    try:
        # operation
        return data
    except Exception:
        return None  # Lost error information


# ✅ Correct
def safe_operation() -> p.Result[m.Dict]:
    try:
        # operation
        return r.ok(data)
    except Exception as e:
        return r.fail(f"Operation failed: {e}")```
### **Service Pattern Violations**

**Problem**: Not following flext-core service patterns

