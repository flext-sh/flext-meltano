# flext-meltano Integration Patterns

<!-- TOC START -->
- [🎯 ELT Foundation Role](#elt-foundation-role)
- [🔌 Singer Ecosystem Integration](#singer-ecosystem-integration)
  - [Tap Implementation Pattern](#tap-implementation-pattern)
  - [Target Implementation Pattern](#target-implementation-pattern)
- [🛠️ dbt Integration Patterns](#dbt-integration-patterns)
  - [dbt Project Foundation](#dbt-project-foundation)
- [🚀 Complete ELT Pipeline Integration](#complete-elt-pipeline-integration)
  - [Enterprise Pipeline Pattern](#enterprise-pipeline-pattern)
- [🔗 Bridge Communication Patterns](#bridge-communication-patterns)
  - [Go ↔ Python Integration](#go-python-integration)
- [📊 Integration Matrix](#integration-matrix)
  - [FLEXT Project Integration Status](#flext-project-integration-status)
  - [Integration Requirements](#integration-requirements)
- [🌍 Environment Integration](#environment-integration)
  - [FLEXT Workspace Setup](#flext-workspace-setup)
  - [Consumer Project Dependencies](#consumer-project-dependencies)
- [⚠️ Integration Limitations](#integration-limitations)
  - [Current Constraints](#current-constraints)
  - [Workaround Strategies](#workaround-strategies)
  - [Resolution Timeline](#resolution-timeline)
- [🔧 Integration Best Practices](#integration-best-practices)
  - [Design Patterns](#design-patterns)
  - [Quality Standards](#quality-standards)
<!-- TOC END -->

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
from __future__ import annotations


from flext_meltano import (
    FlextMeltanoTapAbstractions,
    FlextMeltanoTapServiceBase,
    m,
    p,
    t,
    u,
)


class FlextOracleTapService(FlextMeltanoTapServiceBase):
    """Oracle tap using flext-meltano Singer abstractions."""

    tap_name: t.Annotated[
        t.NonEmptyStr, u.Field(description="Canonical tap name (e.g. tap-oracle)")
    ] = "tap-oracle"

    def discover_oracle_streams(
        self, settings: dict
    ) -> p.Result[t.SequenceOf[m.Meltano.StreamDefinition]]:
        """Discover Oracle database streams using flext-meltano."""
        abstractions = FlextMeltanoTapAbstractions()
        return abstractions.create_tap_from_config("tap-oracle", settings)

    def extract_oracle_data(self, stream: str, settings: dict) -> p.Result[list]:
        """Extract data using flext-meltano abstractions."""
        abstractions = FlextMeltanoTapAbstractions()
        return abstractions.process_source({"stream": stream, **settings})```
### Target Implementation Pattern

\__Standard pattern for flext-target-_ projects\_\*:

```python
from __future__ import annotations

from typing import Annotated

from flext_meltano import (
    FlextMeltanoTargetAbstractions,
    FlextMeltanoTargetServiceBase,
    m,
    p,
    t,
    u,
)


class FlextOracleTargetService(FlextMeltanoTargetServiceBase):
    """Oracle target using flext-meltano Singer abstractions."""

    target_name: Annotated[
        t.NonEmptyStr, u.Field(description="Canonical target name (e.g. target-oracle)")
    ] = "target-oracle"

    def create_sink(
        self, stream_name: str, schema: t.JsonMapping
    ) -> p.Meltano.SingerDrainSink:
        """Create an Oracle sink for a Singer stream."""
        raise NotImplementedError

    def load_to_oracle(
        self, records: list, settings: dict
    ) -> p.Result[m.Meltano.DataSinkInstance]:
        """Load records to Oracle using flext-meltano abstractions."""
        abstractions = FlextMeltanoTargetAbstractions()
        return abstractions.create_flext_target({
            "sink_type": "target-oracle",
            "connection_config": settings,
        })```
---

## 🛠️ dbt Integration Patterns

### dbt Project Foundation

\__Standard pattern for flext-dbt-_ projects\_\*:

```python
from __future__ import annotations

from flext_meltano import FlextMeltanoDbtServiceBase, p, t


class FlextOracleDbtService(FlextMeltanoDbtServiceBase):
    """Oracle dbt transformations using flext-meltano."""

    @property
    def connection_profile(self) -> p.Meltano.DbtConnectionProfile:
        """Oracle dbt connection profile."""
        raise NotImplementedError

    def run_oracle_models(self, models: t.StrSequence) -> p.Result[t.JsonMapping]:
        """Execute Oracle-specific dbt models."""
        return self.run_models(models)```
**Current Limitation**: dbt integration is placeholder implementation requiring dbt programmatic API integration.

---

## 🚀 Complete ELT Pipeline Integration

### Enterprise Pipeline Pattern

**Full ELT workflow using flext-meltano foundation**:

```python
from __future__ import annotations

from flext_meltano import (
    FlextMeltanoAdapter,
    FlextMeltanoDbtServiceBase,
    FlextMeltanoService,
    m,
    p,
    r,
    t,
)


class EnterpriseELTService(FlextMeltanoService):
    """Complete ELT pipeline for enterprise applications."""

    def __init__(self):
        super().__init__()
        self._meltano_service = FlextMeltanoService()
        self._adapter = FlextMeltanoAdapter()

    def execute_elt_pipeline(
        self, tap_name: str, target_name: str, dbt_models: t.StrSequence | None = None
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Execute complete ELT pipeline."""
        pipeline_result = self._adapter.execute()
        if pipeline_result.failure:
            return pipeline_result

        if dbt_models:
            transform_result = self._run_dbt_models(dbt_models)
            if transform_result.failure:
                return transform_result

        return r[m.Meltano.CommandExecutionResult].ok({
            "pipeline": pipeline_result.unwrap(),
            "models_executed": dbt_models or [],
        })

    def _run_dbt_models(
        self, models: t.StrSequence
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Run dbt models."""
        dbt_service = FlextMeltanoDbtServiceBase()
        return dbt_service.run_models(models)```
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
2. **Follow r Patterns**: Maintain consistency for future compatibility
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
from __future__ import annotations

from flext_core import FlextContainer
from flext_meltano import FlextMeltanoTapAbstractions, FlextMeltanoTargetAbstractions

# Register services for ecosystem consumption
container = FlextContainer.shared()
container.bind("tap_abstractions", FlextMeltanoTapAbstractions)
container.bind("target_abstractions", FlextMeltanoTargetAbstractions)```
**2. Configuration Management**:

```python
from __future__ import annotations

from flext_meltano import FlextMeltanoSettings

settings = FlextMeltanoSettings()
print(settings.model_dump())```
**3. Error Handling**:

```python
from __future__ import annotations

from flext_meltano import FlextMeltanoTapAbstractions, m, p, r


def handle_discovery(name: str) -> p.Result[m.Meltano.DataSourceInstance]:
    """Consistent r patterns across all integrations."""
    abstractions = FlextMeltanoTapAbstractions()
    result = abstractions.create_tap_from_config(name, {})
    if result.failure:
        return r[m.Meltano.DataSourceInstance].fail(
            f"Integration failed: {result.error}"
        )
    return result```
### Quality Standards

**Integration Requirements**:

- Use only root-level imports from flext-meltano
- Follow r patterns for all operations
- Implement proper error handling and logging
- Maintain Singer protocol compliance
- Use FLEXT service architecture patterns

---

**Integration Guide v0.12.0-dev** - Comprehensive patterns for FLEXT ecosystem ELT integration with clear guidance on current capabilities and planned improvements.
