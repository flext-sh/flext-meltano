# from flext-meltano/docs/guides/integration.md:229
from __future__ import annotations

from flext_meltano import FlextMeltanoBridge

bridge = FlextMeltanoBridge()
response = bridge.execute_bridge_command(
    "run_pipeline", args={"tap": "tap-csv", "target": "target-jsonl"}
)

# Response format follows r structure
print(response.unwrap())```
---

## 📊 Integration Matrix

### FLEXT Project Integration Status

| Project Category        | Integration Pattern            | Status      | Notes                        |
| ----------------------- | ------------------------------ | ----------- | ---------------------------- |
| **flext-tap-csv**       | FlextMeltanoTapAbstractions    | ✅ Active   | Working Singer abstractions  |
| **flext-tap-oracle**    | FlextMeltanoTapAbstractions    | ✅ Active   | Real Meltano integration     |
| **flext-tap-ldap**      | FlextMeltanoTapAbstractions    | ✅ Active   | Singer protocol compliance   |
| **flext-target-oracle** | FlextMeltanoTargetAbstractions | ✅ Active   | Target service wrappers      |
| **flext-target-ldap**   | FlextMeltanoTargetAbstractions | ✅ Active   | Load operation abstractions  |
| **flext-dbt-oracle**    | FlextMeltanoDbtService         | 🔴 Limited | Placeholder implementation   |
| **DataCosmos**          | Complete ELT Foundation        | 🟡 Partial | Blocked by compliance issues |

### Integration Requirements

\__For flext-tap-_ projects\_\*:

1. Use FlextMeltanoTapAbstractions for all Singer operations
2. Follow r patterns for error handling
3. Implement stream discovery and data extraction
4. Maintain Singer protocol compliance

\__For flext-target-_ projects\_\*:

1. Use FlextMeltanoTargetAbstractions for all load operations
2. Implement record loading with validation
3. Handle Singer message processing
4. Follow FLEXT service patterns

\__For flext-dbt-_ projects\_\*:

1. Use FlextMeltanoDbtService for transformations
2. Plan for dbt programmatic API integration
3. Implement model execution workflows
4. Maintain transformation validation

---

## 🌍 Environment Integration

### FLEXT Workspace Setup

**Required environment configuration for consumers**:

