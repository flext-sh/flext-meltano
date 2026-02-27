# Claude

Placeholder generated for documentation link consistency.

**See [../CLAUDE.md](../CLAUDE.md) for full workspace standards.**

### Zero Tolerance Rules (Completely Prohibited)
1. **Hacks**: ❌ PROHIBITED - `model_rebuild()`, `eval()`, `exec()`.
2. **Inline/Lazy Imports**: ❌ PROHIBITED - No imports inside functions or `.try / except ImportError:`.
3. **# type: ignore**: ❌ PROHIBITED COMPLETELY - Zero tolerance, no exceptions
4. **Root Aliases**: ❌ PROHIBITED COMPLETELY - Always use complete namespace.
5. **cast()**: ❌ PROHIBITED - Replace with Models/Protocols/TypeGuards
6. **Any**: ❌ PROHIBITED - Replace with specific types.
