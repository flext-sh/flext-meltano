# from flext-meltano_docs/troubleshooting.md:228
from __future__ import annotations


# ❌ Incorrect
class UtilityClass:
    @staticmethod
    def do_something():
        pass


# ✅ Correct


class FlextMeltanoUtilityService(s):
    def do_something(self) -> p.Result[m.Dict]:
        # Implementation with proper error handling
        pass```
______________________________________________________________________

## 🆘 Getting Help

### **Debug Information**

When reporting issues, include:

