# flext-meltano Integration Patterns

**ELT foundation integration patterns for the FLEXT ecosystem**

> **⚠️ INTEGRATION STATUS**: Direct meltano.core imports limit some integration patterns. Full ecosystem compatibility requires abstraction layer.

---

## 🎯 ELT Foundation Role

flext-meltano serves as the **mandatory ELT foundation** for the FLEXT ecosystem, providing:

- **Singer Protocol Abstractions** - Foundation for flext-tap-_and flext-target-_ projects
- **Meltano Integration** - Enterprise project management and orchestration
- **dbt Operations** - Transformation pipeline coordination
- **ELT Orchestration** - Complete extract-load-transform workflows

**Integration Authority**: All FLEXT projects requiring ELT operations must use flext-meltano patterns.

---

## 🔌 Singer Ecosystem Integration

### Tap Implementation Pattern

\__Standard pattern for flext-tap-_ projects\_\*:

```python
# Example: flext-tap-oracle integration
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_meltano import FlextMeltanoTapAbstractions, StreamDefinition

class FlextOracleTapService(FlextService):
    """Oracle tap using flext-meltano Singer abstractions."""

    def __init__(self):
        super().__init__()
        self._tap_abstractions = FlextMeltanoTapAbstractions()

    def discover_oracle_streams(self, config: dict) -> FlextResult[list[StreamDefinition]]:
        """Discover Oracle database streams using flext-meltano."""
        return self._tap_abstractions.discover_catalog("tap-oracle")

    def extract_oracle_data(self, stream: str, config: dict) -> FlextResult[list]:
        """Extract data using flext-meltano abstractions."""
        return self._tap_abstractions.extract_data("tap-oracle", config)
```

### Target Implementation Pattern

\__Standard pattern for flext-target-_ projects\_\*:

```python
# Example: flext-target-oracle integration
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_meltano import FlextMeltanoTargetAbstractions

class FlextOracleTargetService(FlextService):
    """Oracle target using flext-meltano Singer abstractions."""

    def __init__(self):
        super().__init__()
        self._target_abstractions = FlextMeltanoTargetAbstractions()

    def load_to_oracle(self, records: list, config: dict) -> FlextResult[FlextTypes.Dict]:
        """Load records to Oracle using flext-meltano abstractions."""
        return self._target_abstractions.load_data("target-oracle", records)
```

---

## 🛠️ dbt Integration Patterns

### dbt Project Foundation

\__Standard pattern for flext-dbt-_ projects\_\*:

```python
# Example: flext-dbt-oracle integration
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_meltano import FlextMeltanoDbtService

class FlextOracleDbtService(FlextService):
    """Oracle dbt transformations using flext-meltano."""

    def __init__(self):
        super().__init__()
        self._dbt_service = FlextMeltanoDbtService()

    def run_oracle_models(self, models: FlextTypes.StringList) -> FlextResult[FlextTypes.Dict]:
        """Execute Oracle-specific dbt models."""
        # Note: Current implementation returns placeholder data
        return self._dbt_service.execute_dbt_operation()
```

**Current Limitation**: dbt integration is placeholder implementation requiring dbt programmatic API integration.

---

## 🚀 Complete ELT Pipeline Integration

### Enterprise Pipeline Pattern

**Full ELT workflow using flext-meltano foundation**:

```python
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_meltano import FlextMeltanoService, FlextMeltanoAdapter

class EnterpriseELTService(FlextService):
    """Complete ELT pipeline for enterprise applications."""

    def __init__(self):
        super().__init__()
        self._meltano_service = FlextMeltanoService()
        self._adapter = FlextMeltanoAdapter()

    def execute_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: FlextTypes.StringList = None
    ) -> FlextResult[FlextTypes.Dict]:
        """Execute complete ELT pipeline."""

        # 1. Extract and Load using Meltano
        pipeline_result = self._adapter.run_pipeline(tap_name, target_name)
        if pipeline_result.is_failure:
            return pipeline_result

        # 2. Transform using dbt (if specified)
        if dbt_models:
            # Note: Requires dbt integration completion
            transform_result = self._execute_transformations(dbt_models)
            if transform_result.is_failure:
                return transform_result

        return FlextResult[FlextTypes.Dict].ok({
            "pipeline": pipeline_result.unwrap(),
            "models_executed": dbt_models or []
        })
```

---

## 🔗 Bridge Communication Patterns

### Go ↔ Python Integration

**Bridge command patterns for ecosystem integration**:

```bash
# Standard bridge operations for ecosystem consumption
python scripts/flext_meltano_bridge.py version
python scripts/flext_meltano_bridge.py list_plugins
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-jsonl
python scripts/flext_meltano_bridge.py discover_catalog tap-oracle
```

**JSON API Response Pattern**:

```python
from flext_meltano import FlextMeltanoBridge

bridge = FlextMeltanoBridge()
response = bridge.handle_bridge_request({
    "command": "run_pipeline",
    "args": ["tap-csv", "target-jsonl"]
})

# Response format follows FlextResult structure
{
    "success": True,
    "data": {"records_processed": 1000},
    "error": None
}
```

---

## 📊 Integration Matrix

### FLEXT Project Integration Status

| Project Category        | Integration Pattern            | Status     | Notes                        |
| ----------------------- | ------------------------------ | ---------- | ---------------------------- |
| **flext-tap-csv**       | FlextMeltanoTapAbstractions    | ✅ Active  | Working Singer abstractions  |
| **flext-tap-oracle**    | FlextMeltanoTapAbstractions    | ✅ Active  | Real Meltano integration     |
| **flext-tap-ldap**      | FlextMeltanoTapAbstractions    | ✅ Active  | Singer protocol compliance   |
| **flext-target-oracle** | FlextMeltanoTargetAbstractions | ✅ Active  | Target service wrappers      |
| **flext-target-ldap**   | FlextMeltanoTargetAbstractions | ✅ Active  | Load operation abstractions  |
| **flext-dbt-oracle**    | FlextMeltanoDbtService         | 🔴 Limited | Placeholder implementation   |
| **DataCosmos**          | Complete ELT Foundation        | 🟡 Partial | Blocked by compliance issues |

### Integration Requirements

\__For flext-tap-_ projects\_\*:

1. Use FlextMeltanoTapAbstractions for all Singer operations
2. Follow FlextResult patterns for error handling
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

```bash
# FLEXT workspace virtual environment
cd ../..
source .venv/bin/activate

# flext-meltano specific variables
export PYTHONPATH=..flext-meltano/src:$PYTHONPATH
export MELTANO_PROJECT_ROOT=..flext-meltano
export MELTANO_ENVIRONMENT=dev
```

### Consumer Project Dependencies

**Standard dependency pattern**:

```toml
# pyproject.toml for flext-tap-*/flext-target-*/flext-dbt-* projects
[tool.poetry.dependencies]
python = "^3.13"
flext-core = "^0.9.9"
flext-meltano = "^0.9.9"  # Mandatory ELT foundation

[tool.poetry.group.dev.dependencies]
flext-cli = "^0.9.9"      # CLI development tools
```

---

## ⚠️ Integration Limitations

### Current Constraints

**Architecture Compliance Issues**:

- **Direct meltano.core imports** (adapters.py lines 17-25) limit some integration patterns
- **dbt placeholder implementation** affects flext-dbt-\* project functionality
- **Modern ELT patterns** missing for 2025 industry standards

**Integration Impact**:

- **Singer Operations**: ✅ Fully functional through abstractions
- **Meltano Integration**: 🟡 Working but non-compliant
- **dbt Operations**: 🔴 Limited to placeholder data
- **Enterprise Use**: 🔴 Not recommended for production

### Workaround Strategies

**Current Development Approach**:

1. **Use Working Abstractions**: FlextMeltanoTapAbstractions and FlextMeltanoTargetAbstractions are fully functional
2. **Follow FlextResult Patterns**: Maintain consistency for future compatibility
3. **Plan for Updates**: Design integration patterns to accommodate resolution
4. **Document Limitations**: Clear communication about current constraints

### Resolution Timeline

**Integration Improvement Phases**:

- **Phase 1** (4-6 weeks): Abstraction layer for meltano.core compliance
- **Phase 2** (3-4 weeks): dbt programmatic API integration
- **Phase 3** (2-3 weeks): Modern ELT patterns adoption
- **Phase 4** (1-2 weeks): Complete ecosystem integration validation

---

## 🔧 Integration Best Practices

### Design Patterns

**1. Dependency Injection**:

```python
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_meltano import FlextMeltanoTapAbstractions

# Register services for ecosystem consumption
container = FlextContainer.get_global()
container.register("tap_abstractions", FlextMeltanoTapAbstractions)
container.register("target_abstractions", FlextMeltanoTargetAbstractions)
```

**2. Configuration Management**:

```python
from flext_meltano import FlextMeltanoConfigBuilders

builder = FlextMeltanoConfigBuilders()
config = builder.build_pipeline_config(tap_settings, target_settings)
```

**3. Error Handling**:

```python
# Consistent FlextResult patterns across all integrations
result = tap_abstractions.discover_catalog("tap-name")
if result.is_failure:
    return FlextResult[FlextTypes.Dict].fail(f"Integration failed: {result.error}")
```

### Quality Standards

**Integration Requirements**:

- Use only root-level imports from flext-meltano
- Follow FlextResult patterns for all operations
- Implement proper error handling and logging
- Maintain Singer protocol compliance
- Use FLEXT service architecture patterns

---

**Integration Guide v0.9.9** - Comprehensive patterns for FLEXT ecosystem ELT integration with clear guidance on current capabilities and planned improvements.
