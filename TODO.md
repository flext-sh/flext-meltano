# TODO.md - FLEXT-MELTANO Advanced ELT Foundation Implementation

**Last Updated**: 2025-01-08
**Project Status**: 🚨 CRITICAL VIOLATIONS - Architecture Non-Compliance Blocking Production
**Authority**: MELTANO ELT PIPELINE FOUNDATION for entire FLEXT ecosystem (32+ projects)

## 🚨 ZERO TOLERANCE VIOLATIONS (IMMEDIATE ACTION REQUIRED)

### 1. CRITICAL: Direct Meltano/Singer Library Imports ⛔

**VIOLATION LOCATION**: `src/flext_meltano/adapters.py` lines 14, 17-25

```python
# ❌ ABSOLUTELY FORBIDDEN - Direct imports found:
import meltano                                    # LINE 14
from meltano.core.elt_context import ELTContext  # LINE 17
from meltano.core.hub import MeltanoHubService   # LINE 18
from meltano.core.job.job import Job             # LINE 19
from meltano.core.plugin.base import PluginType # LINE 20
from meltano.core.plugin_invoker import PluginInvoker # LINE 21
from meltano.core.project import Project        # LINE 22
from meltano.core.project_add_service import ProjectAddService # LINE 23
from meltano.core.runner import RunnerError     # LINE 24
from meltano.core.runner.singer import SingerRunner # LINE 25
```

**MANDATORY REMEDIATION**:
- [ ] **REMOVE ALL direct meltano imports** from adapters.py
- [ ] **IMPLEMENT FlextMeltanoLibraryAdapter** following flext-core patterns
- [ ] **USE ONLY library APIs** through FLEXT abstractions
- [ ] **VALIDATE ZERO direct imports** across entire codebase

### 2. CRITICAL: pyproject.toml Duplicate Dependencies

**VIOLATION**: Dependencies declared in both `[project.dependencies]` and `[tool.poetry.dependencies]`

**MANDATORY REMEDIATION**:
- [ ] **REMOVE duplicate entries** from `[project.dependencies]` section
- [ ] **KEEP ONLY** `[tool.poetry.dependencies]` declarations
- [ ] **VALIDATE** no conflicting version constraints

## 🏗️ ADVANCED MELTANO RUNNER ARCHITECTURE (LIBRARY-BASED FOUNDATION)

### 1. FlextMeltanoLibraryAdapter - Replace Direct Imports ⚠️

**PURPOSE**: Advanced meltano runner functionality through library APIs (not CLI runtime)

```python
# ✅ CORRECT - Library API Integration Pattern
from flext_core import FlextDomainService, FlextResult, FlextLogger
from flext_meltano.constants import FlextMeltanoConstants

class FlextMeltanoLibraryAdapter(FlextDomainService):
    """Advanced Meltano runner using library APIs exclusively."""

    def __init__(self) -> None:
        super().__init__()
        self._logger = FlextLogger(__name__)

    class _MeltanoProjectManager:
        """Nested helper for Meltano Project API integration."""

        @staticmethod
        def create_project_instance(project_dir: Path) -> FlextResult[object]:
            """Create Meltano Project using library API."""
            # IMPLEMENTATION: Use meltano library API patterns
            pass

    class _PluginManager:
        """Nested helper for Meltano Plugin API integration."""

        @staticmethod
        def invoke_plugin(plugin_name: str, args: list) -> FlextResult[dict]:
            """Invoke plugin using library API."""
            # IMPLEMENTATION: Use PluginInvoker library patterns
            pass

    async def run_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        **config: object
    ) -> FlextResult[dict]:
        """Execute ELT pipeline using advanced library integration."""
        # IMPLEMENTATION: Full library API integration
        pass
```

**TASKS**:
- [ ] **IMPLEMENT** FlextMeltanoLibraryAdapter with proper library API usage
- [ ] **ABSTRACT** all meltano.core.* usage behind FlextResult patterns
- [ ] **PROVIDE** advanced meltano runner functionality for ecosystem
- [ ] **ENSURE** complete singer plugin compatibility

### 2. FlextDbtLibraryRunner - Programmatic DBT Integration 🔧

**PURPOSE**: DBT runner by library (not CLI runtime) using dbtRunner

```python
# ✅ CORRECT - DBT Library Integration Pattern
from flext_core import FlextDomainService, FlextResult
from flext_meltano.constants import FlextMeltanoConstants

class FlextDbtLibraryRunner(FlextDomainService):
    """Advanced DBT runner using library APIs exclusively."""

    class _DbtProjectManager:
        """Nested helper for DBT project management."""

        @staticmethod
        def create_runner_instance() -> FlextResult[object]:
            """Create dbtRunner for programmatic execution."""
            # IMPLEMENTATION: from dbt.cli.main import dbtRunner
            pass

    class _DbtCommandExecutor:
        """Nested helper for DBT command execution."""

        @staticmethod
        def execute_models(
            runner: object,
            models: list[str],
            **options: object
        ) -> FlextResult[dict]:
            """Execute DBT models programmatically."""
            # IMPLEMENTATION: dbtRunner.invoke(cli_args) patterns
            pass

    async def run_transformations(
        self,
        project_dir: Path,
        models: list[str],
        **config: object
    ) -> FlextResult[dict]:
        """Execute DBT transformations using advanced library integration."""
        # IMPLEMENTATION: Full dbtRunner library integration
        pass
```

**TASKS**:
- [ ] **IMPLEMENT** FlextDbtLibraryRunner with dbtRunner API
- [ ] **USE** pre-loaded profile and project patterns for performance
- [ ] **PROVIDE** advanced DBT runner functionality for ecosystem
- [ ] **ENSURE** complete DBT transformation compatibility

### 3. FlextSingerLibraryProtocol - Singer SDK Integration 🎵

**PURPOSE**: Singer protocol foundation using singer-sdk library patterns

```python
# ✅ CORRECT - Singer SDK Library Integration Pattern
from flext_core import FlextDomainService, FlextResult
from flext_meltano.typings import FlextMeltanoTypes

class FlextSingerLibraryProtocol(FlextDomainService):
    """Advanced Singer protocol using library APIs exclusively."""

    class _TapManager:
        """Nested helper for Singer Tap integration."""

        @staticmethod
        def create_tap_instance(tap_config: dict) -> FlextResult[object]:
            """Create Singer Tap using SDK library patterns."""
            # IMPLEMENTATION: from singer_sdk.singerlib import SingerTap
            pass

    class _TargetManager:
        """Nested helper for Singer Target integration."""

        @staticmethod
        def create_target_instance(target_config: dict) -> FlextResult[object]:
            """Create Singer Target using SDK library patterns."""
            # IMPLEMENTATION: singer-sdk library target patterns
            pass

    async def execute_tap_target_pipeline(
        self,
        tap_config: FlextMeltanoTypes.TapConfig,
        target_config: FlextMeltanoTypes.TargetConfig
    ) -> FlextResult[dict]:
        """Execute tap-target pipeline using advanced library integration."""
        # IMPLEMENTATION: Full singer-sdk library integration
        pass
```

**TASKS**:
- [ ] **IMPLEMENT** FlextSingerLibraryProtocol with singer-sdk.singerlib
- [ ] **MAINTAIN** strict singer protocol compatibility
- [ ] **PROVIDE** tap/target foundation patterns for ecosystem
- [ ] **ENSURE** complete stream processing capabilities

## 🌐 FLEXT ECOSYSTEM FOUNDATION PATTERNS

### 1. Unified ELT Interface Architecture 🏢

**PURPOSE**: Single interface for all FLEXT projects requiring ELT operations

```python
# ✅ CORRECT - Unified ELT Foundation Pattern
class FlextMeltanoUnifiedService(FlextDomainService):
    """Unified ELT service providing all ecosystem foundation patterns."""

    def __init__(self) -> None:
        super().__init__()
        self._meltano_adapter = FlextMeltanoLibraryAdapter()
        self._dbt_runner = FlextDbtLibraryRunner()
        self._singer_protocol = FlextSingerLibraryProtocol()

    async def execute_complete_elt_pipeline(
        self,
        extraction_config: FlextMeltanoTypes.ExtractionConfig,
        transformation_config: FlextMeltanoTypes.TransformationConfig,
        loading_config: FlextMeltanoTypes.LoadingConfig
    ) -> FlextResult[FlextMeltanoTypes.ELTPipelineResult]:
        """Execute complete ELT pipeline for FLEXT ecosystem projects."""
        # IMPLEMENTATION: Orchestrate E-L-T phases using library APIs
        pass
```

**ECOSYSTEM INTEGRATION TASKS**:
- [ ] **DESIGN** unified interface for 32+ FLEXT projects
- [ ] **IMPLEMENT** complete ELT orchestration patterns
- [ ] **PROVIDE** flext-core alike interfaces for all operations
- [ ] **ENSURE** foundation for flext-tap-*, flext-target-*, flext-dbt-*

### 2. flext-cli Integration for All Output Operations 💻

**TASKS**:
- [ ] **REMOVE** any direct click/rich usage (verified: none found - ✅)
- [ ] **USE ONLY** flext-cli for all CLI operations and file manipulation
- [ ] **IMPLEMENT** CLI command patterns through FlextCliApi
- [ ] **ENSURE** consistent output formatting across ecosystem

### 3. Advanced Plugin Architecture 🔌

**PURPOSE**: Foundation for all FLEXT tap/target/dbt plugins

```python
# ✅ CORRECT - Plugin Foundation Pattern
class FlextMeltanoPluginFoundation(FlextDomainService):
    """Foundation patterns for all FLEXT ecosystem plugins."""

    class _PluginRegistry:
        """Nested helper for plugin registration and discovery."""

        @staticmethod
        def register_plugin(
            plugin_type: FlextMeltanoTypes.PluginType,
            plugin_config: dict
        ) -> FlextResult[FlextMeltanoTypes.PluginInstance]:
            """Register plugin with ecosystem foundation."""
            pass

    async def create_ecosystem_plugin(
        self,
        plugin_spec: FlextMeltanoTypes.PluginSpecification
    ) -> FlextResult[FlextMeltanoTypes.EcosystemPlugin]:
        """Create ecosystem plugin following FLEXT patterns."""
        # IMPLEMENTATION: Plugin factory with flext-core integration
        pass
```

**PLUGIN FOUNDATION TASKS**:
- [ ] **IMPLEMENT** plugin architecture for ecosystem consumption
- [ ] **PROVIDE** base classes for flext-tap-*, flext-target-*, flext-dbt-*
- [ ] **ENSURE** consistent plugin patterns across ecosystem
- [ ] **MAINTAIN** backward compatibility with existing plugins

## 🧪 COMPREHENSIVE TESTING STRATEGY (REAL API INTEGRATION)

### 1. Real Meltano API Testing (NO MOCKS) ✅

**CURRENT STATUS**: Need to expand real API testing coverage

**TASKS**:
- [ ] **IMPLEMENT** comprehensive Meltano Project API tests
- [ ] **TEST** complete plugin lifecycle with real APIs
- [ ] **VALIDATE** ELT pipeline execution with sample projects
- [ ] **ENSURE** 90%+ coverage with meaningful functionality tests

### 2. Real DBT Library Testing 🧪

**TASKS**:
- [ ] **IMPLEMENT** dbtRunner programmatic execution tests
- [ ] **TEST** pre-loaded profile and project scenarios
- [ ] **VALIDATE** complete transformation lifecycle
- [ ] **ENSURE** real SQL transformation execution

### 3. Singer Protocol Compliance Testing 🎵

**TASKS**:
- [ ] **IMPLEMENT** singer-sdk.singerlib integration tests
- [ ] **TEST** catalog discovery and stream processing
- [ ] **VALIDATE** tap-target communication protocols
- [ ] **ENSURE** strict Singer specification compliance

## 📋 IMPLEMENTATION PRIORITY SEQUENCE

### PHASE 1: CRITICAL VIOLATIONS (IMMEDIATE - Week 1)
1. [ ] **Remove direct meltano imports** from adapters.py
2. [ ] **Fix pyproject.toml** duplicate dependencies
3. [ ] **Implement FlextMeltanoLibraryAdapter** basic structure
4. [ ] **Validate zero forbidden imports** across codebase

### PHASE 2: LIBRARY INTEGRATION (Week 2-3)
1. [ ] **Complete FlextMeltanoLibraryAdapter** implementation
2. [ ] **Implement FlextDbtLibraryRunner** with dbtRunner
3. [ ] **Implement FlextSingerLibraryProtocol** with singer-sdk
4. [ ] **Create unified ELT interface** architecture

### PHASE 3: ECOSYSTEM FOUNDATION (Week 4-5)
1. [ ] **Design plugin foundation** patterns
2. [ ] **Implement ecosystem integration** interfaces
3. [ ] **Create comprehensive testing** with real APIs
4. [ ] **Validate foundation** for all FLEXT projects

### PHASE 4: PRODUCTION READINESS (Week 6)
1. [ ] **Achieve 90%+ test coverage** with real API tests
2. [ ] **Complete quality gate validation**
3. [ ] **Documentation and examples** for ecosystem consumption
4. [ ] **Release production-ready** ELT foundation

## 🎯 SUCCESS CRITERIA (PRODUCTION DEPLOYMENT)

### IMMEDIATE (Zero Tolerance Compliance)
- [ ] **ZERO** direct meltano/singer/dbt imports outside abstractions
- [ ] **100%** FlextResult pattern usage for error handling
- [ ] **90%+** test coverage with real library API integration
- [ ] **ALL** quality gates passing (lint, type, security, test)

### ECOSYSTEM READINESS
- [ ] **Complete ELT foundation** for 32+ FLEXT projects
- [ ] **Advanced meltano runner** functionality by library (not CLI)
- [ ] **Advanced dbt runner** functionality with dbtRunner API
- [ ] **Strict singer protocol** compatibility maintained
- [ ] **Foundation patterns** for flext-tap-*, flext-target-*, flext-dbt-*

### PRODUCTION AUTHORITY
- [ ] **FLEXT-MELTANO** recognized as ELT foundation authority
- [ ] **ALL** FLEXT ecosystem projects using flext-meltano patterns
- [ ] **ZERO** custom ELT implementations across ecosystem
- [ ] **COMPLETE** library integration (not mere facade architecture)

---

**ARCHITECTURAL PRINCIPLE**: flext-meltano MUST USE meltano, dbt, and singer libraries to provide core functionality with flext-core alike interfaces, NOT be merely a facade using FLEXT-CORE architecture to simplify development.

**ECOSYSTEM AUTHORITY**: These requirements are specific to flext-meltano's role as the MANDATORY ELT pipeline foundation for the entire FLEXT ecosystem.

**ZERO TOLERANCE**: Direct library imports outside FLEXT abstractions are ABSOLUTELY FORBIDDEN and block production deployment.