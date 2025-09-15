# CLI Testing Architecture Fix Required

## Problem

The CLI tests in `tests/unit/test_cli_coverage.py` violate FLEXT ecosystem requirements by:

1. Using Click's CliRunner to test functions that return FlextResult objects
2. Direct Click imports (forbidden by FLEXT standards)
3. Testing FlextResult-returning functions as if they were Click commands

## Required Changes

All `self.runner.invoke()` calls need to be replaced with direct function calls:

```python
# BEFORE (incorrect)
result = self.runner.invoke(
    authenticate_user, ["--username", "testuser", "--password", "testpass"]
)
assert result.exit_code == 0

# AFTER (correct FLEXT pattern)
result = authenticate_user(
    username="testuser",
    password="testpass"
)
assert result.is_success
```

## Lines to Fix

Based on PyRight errors, these 10 lines still need fixing:

- Line 164, 194, 224, 262, 299, 326, 341, 366, 380, 397

## FLEXT Compliance

- Remove all Click imports
- Test FlextResult patterns directly
- Use flext-cli when CLI functionality is actually needed
- Follow FlextResult railway pattern in tests
