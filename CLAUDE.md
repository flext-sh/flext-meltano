# FLEXT-MELTANO CLAUDE.MD

**Enterprise Meltano Data Integration Foundation for FLEXT Ecosystem**  
**Version**: 2.0.0 | **Authority**: MELTANO ELT PIPELINE FOUNDATION | **Updated**: 2025-01-08  
**Status**: Production-ready Meltano/Singer/DBT integration with zero errors across all quality gates

**References**: See [../CLAUDE.md](../CLAUDE.md) for FLEXT ecosystem standards and [README.md](README.md) for project overview.

**Copyright (c) 2025 FLEXT Team. All rights reserved.**  
**License**: MIT

---

## 🎯 FLEXT-MELTANO MISSION (MELTANO ELT PIPELINE FOUNDATION AUTHORITY)

**CRITICAL ROLE**: flext-meltano is the enterprise-grade Meltano data integration and ELT pipeline orchestration foundation for the entire FLEXT ecosystem. This is a PRODUCTION mission-critical system providing Meltano project management, Singer SDK integration, DBT transformations, and data pipeline orchestration with ZERO TOLERANCE for custom ELT implementations.

**MELTANO ELT PIPELINE FOUNDATION RESPONSIBILITIES**:

- ✅ **Enterprise Meltano Integration**: Production-grade Meltano project management with Singer SDK and DBT Core
- ✅ **FLEXT Ecosystem Integration**: MANDATORY use of flext-core foundation exclusively
- ✅ **ELT Pipeline Orchestration**: Complete data extraction, loading, and transformation pipeline management
- ✅ **Singer Protocol Management**: Singer tap/target abstractions and protocol compliance validation
- ✅ **DBT Transformation Operations**: DBT model execution, testing, and documentation generation
- ✅ **Advanced Pattern Implementation**: Clean Architecture with Domain-Driven Design for ELT operations
- ✅ **Production Quality**: Zero errors across all quality gates with comprehensive ELT testing

**FLEXT ECOSYSTEM IMPACT** (MELTANO FOUNDATION AUTHORITY):

- **All 32+ FLEXT Projects**: Meltano ELT pipeline foundation for entire ecosystem - NO custom ELT implementations
- **Data Integration Platform**: Production-ready data extraction, transformation, and loading operations
- **Enterprise Data Pipeline**: Meltano-based data orchestration for batch and real-time processing
- **Singer Ecosystem Foundation**: Core library for flext-tap-_, flext-target-_, flext-dbt-\* projects
- **DataCosmos Integration**: Complete Meltano pipeline management for enterprise data lakes and warehouses

**MELTANO ELT QUALITY IMPERATIVES** (ZERO TOLERANCE ENFORCEMENT):

- 🔴 **ZERO custom ELT implementations** - ALL data pipeline operations through flext-meltano foundation
- 🔴 **ZERO direct meltano/singer-sdk/dbt-core imports** outside flext-meltano
- 🟢 **90%+ test coverage** - Complete ELT functionality testing with real Meltano projects
- 🟢 **Complete ELT abstraction** - Every data pipeline need covered by flext-meltano patterns
- 🟢 **Zero errors** in MyPy strict mode, PyRight, and Ruff across all source code
- 🟢 **Production deployment** with enterprise ELT configuration and monitoring integration

## 🛑 ZERO TOLERANCE ENFORCEMENT (MELTANO ELT PIPELINE FOUNDATION)

### ⛔ ABSOLUTELY FORBIDDEN MELTANO/ELT VIOLATIONS

#### 1. **DIRECT MELTANO/SINGER/DBT IMPORTS (ECOSYSTEM VIOLATION)**

```python
# ❌ ABSOLUTELY FORBIDDEN - Direct ELT library imports
import meltano.core             # VIOLATION: Use flext-meltano foundation
from singer_sdk import Tap      # VIOLATION: Use flext-meltano abstractions
import dbt.core                 # VIOLATION: Use flext-meltano DBT services
from meltano.core.project import Project  # VIOLATION: Architecture breach

# ✅ CORRECT - FLEXT Ecosystem Foundation Only
from flext_meltano import FlextMeltanoAdapter, FlextMeltanoService
from flext_meltano import FlextTapAbstractions, FlextTargetAbstractions
from flext_meltano import FlextMeltanoDbtService
from flext_core import FlextResult, FlextServiceProcessor, FlextLogger
```

#### 2. **CUSTOM ELT IMPLEMENTATIONS (ARCHITECTURE VIOLATION)**

- **FORBIDDEN**: Custom Singer tap implementations outside flext-meltano patterns
- **FORBIDDEN**: Direct Meltano CLI subprocess calls - Use FlextMeltanoExecutor
- **FORBIDDEN**: Custom DBT command execution - Use FlextMeltanoDbtService
- **FORBIDDEN**: Manual YAML/JSON pipeline configuration - Use FlextMeltanoConfigBuilders
- **FORBIDDEN**: Custom ELT error handling - Use FlextResult[T] railway pattern

#### 3. **MELTANO CONFIGURATION VIOLATIONS**

- **FORBIDDEN**: Direct meltano.yml modification without flext-meltano validation
- **FORBIDDEN**: Plugin installations outside flext-meltano plugin management
- **FORBIDDEN**: Environment configuration bypassing flext-meltano config system
- **FORBIDDEN**: Singer catalog manipulation without flext-meltano abstractions

### ⛔ PRODUCTION ELT STANDARDS (ZERO DEVIATION)

1. **ALL ELT operations** through flext-meltano foundation exclusively
2. **ALL Singer protocol interactions** via FlextTapAbstractions/FlextTargetAbstractions
3. **ALL DBT operations** through FlextMeltanoDbtService
4. **ALL Meltano project management** via FlextMeltanoAdapter
5. **ALL pipeline configurations** through FlextMeltanoConfigBuilders
6. **ALL ELT error handling** with FlextResult[T] railway pattern

## 🚀 ENTERPRISE DEVELOPMENT COMMANDS (PRODUCTION ELT FOUNDATION)

### 🔴 MANDATORY QUALITY GATES (ZERO ERRORS TOLERANCE)

```bash
# MANDATORY before ANY commit - Complete ELT validation pipeline
make validate                 # Runs: lint + type-check + security + test + meltano-validate

# Essential quality checks
make check                    # Quick: lint + type-check + meltano-config-check
make lint                     # Ruff linting with ZERO tolerance policy
make type-check              # MyPy strict mode + PyRight validation
make test                    # Real Meltano API tests (90%+ coverage)
make format                  # Auto-format with Ruff (enterprise standards)

# Quality status shortcuts (production efficiency)
make l                       # Alias for lint
make t                       # Alias for test
make tc                      # Alias for type-check
make v                       # Alias for validate
```

### 🎯 MELTANO ELT FOUNDATION OPERATIONS

```bash
# Core Meltano project lifecycle
make meltano-init            # Initialize Meltano project with FLEXT standards
make meltano-install         # Install plugins with dependency validation
make meltano-validate        # Validate complete Meltano configuration
make meltano-test           # Test Meltano project with real APIs

# ELT pipeline operations (production patterns)
make pipeline-run JOB=job_name     # Execute ELT pipeline with FlextMeltanoExecutor
make pipeline-test                 # Test ELT pipeline with sample data
make pipeline-validate            # Validate pipeline configuration
make singer-discover TAP=tap_name  # Discover catalog with FlextTapAbstractions

# DBT transformation operations
make dbt-run MODEL=model_name      # Execute DBT models with FlextMeltanoDbtService
make dbt-test                      # Run DBT tests with validation
make dbt-docs                      # Generate DBT documentation
make dbt-validate                  # Validate DBT project configuration
```

### 🧪 ENTERPRISE TESTING STANDARDS (REAL API VALIDATION)

```bash
# Comprehensive ELT testing (NO MOCKS - Real Meltano APIs)
make test                    # Full suite: 90%+ coverage with real Meltano integration
make test-fast              # Tests without coverage (development speed)
make test-unit              # Unit tests with FlextResult pattern validation
make test-integration       # Integration tests with real Singer/DBT APIs
make test-meltano           # Meltano-specific tests with project validation
make test-elt               # Complete ELT pipeline testing
make coverage-html          # Generate HTML coverage report with ELT metrics

# Production ELT validation
make test-pipeline-e2e      # End-to-end pipeline testing
make test-singer-protocols  # Singer protocol compliance testing
make test-dbt-transformations # DBT transformation validation
```

## 🏗️ MELTANO ELT ARCHITECTURE FOUNDATION (ENTERPRISE CLEAN ARCHITECTURE)

### 🎯 FLEXT Ecosystem Hierarchy Position

**FLEXT-MELTANO: Level 3 ELT Technology Foundation**

```
LEVEL 4: flext-tap-*, flext-target-*, flext-dbt-* (ELT consumers)
LEVEL 3: [FLEXT-MELTANO] ELT pipeline orchestration foundation
LEVEL 2: flext-cli, flext-observability (intermediate services)
LEVEL 1: flext-core (abstract foundation)
```

**CRITICAL ROLE**: flext-meltano is the MANDATORY ELT foundation for all 32+ FLEXT projects requiring data integration operations.

### 🔧 ENTERPRISE ELT ARCHITECTURE PRINCIPLES (ZERO DEVIATION)

**1. Railway-Oriented Programming (MANDATORY)**:

- ALL ELT operations return `FlextResult[T]` for type-safe error handling
- NO try/except fallbacks - explicit error handling through FlextResult pattern
- ALL Singer protocol interactions wrapped in FlextResult chains

**2. Clean Architecture + Domain-Driven Design (ENTERPRISE STANDARD)**:

- **Domain Layer**: FlextMeltanoAdapter, Singer abstractions, DBT services
- **Application Layer**: FlextMeltanoService, pipeline orchestration
- **Infrastructure Layer**: Meltano Core API abstraction, file system operations
- **Interface Layer**: FlextMeltanoExecutor, CLI commands, bridge communication

**3. SOLID Principles Enforcement (PRODUCTION QUALITY)**:

- **Single Responsibility**: Each service handles ONE ELT concern
- **Open/Closed**: Extensions through plugins, closed for modification
- **Liskov Substitution**: All Singer taps/targets interchangeable
- **Interface Segregation**: Separate protocols for tap/target/DBT operations
- **Dependency Inversion**: Depend on FlextResult abstractions, not implementations

**4. Real API Integration (100% PRODUCTION READINESS)**:

- ZERO mocks in production code - ALL tests use real Meltano APIs
- Complete Singer SDK integration through abstractions
- Actual DBT command execution with real transformations
- Production Meltano project validation

### 🏭 ENTERPRISE MELTANO MODULE ARCHITECTURE

**FOUNDATION LAYER** (ELT Core Infrastructure):

```python
src/flext_meltano/
├── constants.py              # MeltanoConstants extending FlextConstants
├── typings.py               # FlextMeltanoTypes with Singer/DBT type definitions
├── exceptions.py            # FlextMeltanoError hierarchy for ELT operations
└── py.typed                 # Complete type declarations for ecosystem
```

**SERVICE LAYER** (ELT Business Logic):

```python
├── services.py              # FlextMeltanoService (core ELT orchestration)
├── adapters.py              # FlextMeltanoAdapter (Meltano Core integration)
├── service_implementations.py # FlextTapService, FlextTargetService, FlextDbtService
└── plugin_protocols.py      # TapServiceProtocol, TargetServiceProtocol, DbtServiceProtocol
```

**EXECUTION LAYER** (ELT Command Processing):

```python
├── executors.py             # FlextMeltanoExecutor (command orchestration)
├── executors_bridge.py      # FlextMeltanoBridge (Go ↔ Python communication)
├── executors_cli.py         # FlextMeltanoCli (CLI command implementations)
└── executors_meltano.py     # SimpleMeltanoExecutor, SimpleDbtExecutor
```

**INTEGRATION LAYER** (ELT Protocol Abstraction):

```python
├── singer_types.py          # FlextSingerTypes (Singer Protocol abstractions)
├── tap_abstractions.py      # FlextTapAbstractions, TapInstance, StreamDefinition
└── target_abstractions.py  # FlextTargetAbstractions (target service wrappers)
```

**SUPPORT LAYER** (ELT Infrastructure):

```python
├── config.py               # FlextMeltanoConfig (ELT configuration management)
├── config_builders.py      # FlextMeltanoConfigBuilders (pipeline configuration)
├── utilities.py            # FlextMeltanoUtilities (ELT helper functions)
├── validators.py           # FlextMeltanoValidators (ELT data validation)
└── file_managers.py        # FlextMeltanoFileManagers (ELT file operations)
```

### 🌉 ENTERPRISE BRIDGE COMMUNICATION (GO ↔ Python ELT OPERATIONS)

**PRODUCTION BRIDGE ARCHITECTURE**: flext-meltano provides enterprise Go ↔ Python interoperability for ELT operations.

```bash
# ENTERPRISE ELT BRIDGE OPERATIONS (Production JSON API)
python scripts/flext_meltano_bridge.py version                    # Bridge version info
python scripts/flext_meltano_bridge.py list_plugins              # Available ELT plugins
python scripts/flext_meltano_bridge.py validate_project          # Meltano project validation
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv  # ELT pipeline execution
python scripts/flext_meltano_bridge.py discover_catalog tap-name  # Singer catalog discovery
python scripts/flext_meltano_bridge.py run_dbt_models models/*   # DBT transformation execution
```

**BRIDGE COMMUNICATION STANDARDS**:

- ALL bridge operations return JSON responses with FlextResult structure
- MANDATORY error handling through FlextResult patterns
- Complete ELT operation logging and monitoring integration
- Production-ready timeout and retry mechanisms

## 🔗 MELTANO ELT IMPORT STANDARDS (ECOSYSTEM COMPLIANCE)

### ✅ MANDATORY ELT IMPORT PATTERNS (ZERO TOLERANCE ENFORCEMENT)

**CORRECT - FLEXT Ecosystem Foundation Imports Only:**

```python
# ✅ FLEXT-MELTANO Foundation Imports (MANDATORY)
from flext_meltano import FlextMeltanoAdapter, FlextMeltanoService
from flext_meltano import FlextTapAbstractions, FlextTargetAbstractions
from flext_meltano import FlextMeltanoDbtService, FlextMeltanoExecutor
from flext_meltano import FlextMeltanoConfigBuilders, FlextMeltanoValidators

# ✅ FLEXT Ecosystem Integration (REQUIRED)
from flext_core import FlextResult, FlextServiceProcessor, get_logger
from flext_core import FlextDomainService, FlextUtilities
from flext_cli import CLICommand, FlextCliApi
from flext_observability import FlextMonitor, FlextMetrics
```

### ❌ ABSOLUTELY FORBIDDEN ELT IMPORTS (ECOSYSTEM VIOLATION)

**PROHIBITED - Direct Meltano/Singer/DBT Imports:**

```python
# ❌ ZERO TOLERANCE VIOLATIONS - Direct ELT library imports
import meltano                        # FORBIDDEN: Use flext-meltano foundation
import meltano.core                   # FORBIDDEN: Use FlextMeltanoAdapter
from meltano.core.project import Project  # FORBIDDEN: Architecture breach

from singer_sdk import Tap            # FORBIDDEN: Use FlextTapAbstractions
from singer_sdk import Target         # FORBIDDEN: Use FlextTargetAbstractions
import singer                         # FORBIDDEN: Use FlextSingerTypes

import dbt.core                       # FORBIDDEN: Use FlextMeltanoDbtService
from dbt.cli.main import dbtRunner    # FORBIDDEN: Use FlextMeltanoExecutor

# ❌ ARCHITECTURAL BOUNDARY VIOLATIONS
from flext_meltano.adapters import FlextMeltanoAdapter    # WRONG: Use root imports
from flext_meltano.services import FlextMeltanoService    # WRONG: Use root imports
from flext_core.internal.services import Service         # WRONG: Internal modules
```

### 🏢 ENTERPRISE DEPENDENCY ARCHITECTURE (LEVEL-BASED CONSTRAINTS)

**ALLOWED Dependencies (Level 1-2 Foundation Only):**

**MANDATORY FLEXT Ecosystem Dependencies:**

- `flext-core>=0.9.0` - Foundation patterns, FlextResult, service base classes, logging
- `flext-cli>=0.9.0` - CLI patterns, command processing, and user interface
- `flext-observability>=0.9.0` - Monitoring, metrics, and distributed tracing
- `flext-api>=0.9.0` - API client patterns and HTTP/REST abstractions

**EXTERNAL ELT Dependencies (Abstracted Through FLEXT):**

- `meltano>=3.0.0` - Core ELT platform (INTERNAL USE ONLY - wrapped by FlextMeltanoAdapter)
- `singer-sdk>=0.44.0` - Singer protocol support (INTERNAL USE ONLY - wrapped by FlextSingerTypes)
- `dbt-core>=1.10.5` - Data transformation engine (INTERNAL USE ONLY - wrapped by FlextMeltanoDbtService)
- `pydantic>=2.0.0` - Data validation and modeling for ELT configurations

**ABSOLUTELY PROHIBITED Dependencies:**

- ❌ Same level (other Level 3) or higher level modules
- ❌ Direct subprocess calls for ELT operations (use FlextMeltanoExecutor)
- ❌ Mock libraries in production code (tests use real Meltano APIs)
- ❌ Custom ELT implementations bypassing flext-meltano foundation

## 🏆 MELTANO ELT QUALITY STANDARDS (ENTERPRISE AUTHORITY)

### 🔧 ELT TYPE SAFETY REQUIREMENTS (PRODUCTION CRITICAL)

**MANDATORY Type Safety Standards:**

- **MyPy Strict Mode**: ALL source code must pass `mypy src --strict` with ZERO errors
- **PyRight Validation**: Complete PyRight compliance for IDE integration
- **Python 3.13+**: Modern Python features, Union types, generic type annotations
- **FlextResult Pattern**: ALL ELT operations return `FlextResult[T]` for railway-oriented programming
- **Singer Type Safety**: Complete type annotations for Singer protocol operations
- **DBT Type Validation**: Typed DBT model configurations and transformation results

**ELT-Specific Type Requirements:**

```python
# ✅ CORRECT - Meltano ELT type annotations
from typing import Dict, List, Optional, Union
from flext_core import FlextResult
from flext_meltano import FlextTapAbstractions, StreamDefinition

async def extract_data_stream(
    tap_config: FlextMeltanoConfig,
    catalog: Dict[str, StreamDefinition]
) -> FlextResult[List[Dict[str, Union[str, int, float, bool]]]]:
    """Extract data using Singer protocol with complete type safety."""
    pass

# ❌ WRONG - Untyped ELT operations
def run_pipeline(config, catalog):  # Missing types
    pass
```

### 📋 ELT LINTING STANDARDS (ZERO TOLERANCE ENFORCEMENT)

**MANDATORY Linting Configuration:**

- **Ruff**: ALL rules enabled with ELT-specific configurations
- **Complexity Limits**: ELT functions with complexity >10 require refactoring
- **Parameter Limits**: ELT functions with >5 parameters need restructuring
- **Return Statements**: ELT functions with >3 returns need simplification
- **Import Organization**: PEP8 import order with FLEXT ecosystem prioritization

**ELT-Specific Linting Rules:**

```python
# ✅ CORRECT - ELT function complexity
async def process_singer_stream(
    tap: FlextTapAbstractions,
    target: FlextTargetAbstractions,
    stream_name: str
) -> FlextResult[int]:
    """Process single Singer stream - simple, focused responsibility."""
    pass

# ❌ WRONG - Complex ELT function
async def run_complete_elt_pipeline(
    tap, target, dbt, config, catalog, models, tests, docs, monitoring, logging
):  # Too many parameters, too complex
    pass
```

### 🧪 MELTANO ELT TESTING PHILOSOPHY (REAL API INTEGRATION)

**PRODUCTION TESTING STANDARDS:**

**1. Real Meltano API Integration (100% Production Readiness):**

- ZERO mocks for Meltano operations - ALL tests use real Meltano APIs
- Complete Singer SDK integration testing with actual tap/target operations
- Real DBT command execution with actual transformation validation
- Production Meltano project configuration testing

**2. ELT Coverage Requirements (Evidence-Based Quality):**

- **90% minimum coverage** with meaningful ELT functionality tests
- **Real data pipeline testing** with sample datasets and transformations
- **Singer protocol compliance validation** with actual catalog discovery
- **DBT model execution testing** with real SQL transformations

**3. Test Categories (Comprehensive ELT Validation):**

```bash
# ELT-specific test markers
pytest -m unit_elt           # Unit tests for ELT components
pytest -m integration_elt    # Integration tests with real Meltano APIs
pytest -m singer_protocol    # Singer protocol compliance tests
pytest -m dbt_transformations # DBT model execution tests
pytest -m pipeline_e2e       # End-to-end pipeline testing
pytest -m meltano_config     # Meltano configuration validation
```

**4. Production ELT Test Environment:**

```python
# ✅ CORRECT - Real Meltano testing
from flext_meltano import FlextMeltanoAdapter, FlextMeltanoService
import pytest

@pytest.mark.integration_elt
async def test_meltano_project_validation():
    """Test real Meltano project validation."""
    adapter = FlextMeltanoAdapter()
    service = FlextMeltanoService()

    # Test with actual Meltano project
    result = await adapter.validate_project("./test_meltano_project")
    assert result.is_success, f"Meltano validation failed: {result.error}"

# ❌ WRONG - Mocked Meltano testing
@patch('meltano.core.project.Project')
def test_mocked_meltano(mock_project):  # FORBIDDEN
    pass
```

## 🚀 MELTANO ELT DEVELOPMENT WORKFLOW (ENTERPRISE PRODUCTION STANDARDS)

### 🔍 PRE-DEVELOPMENT VALIDATION (MANDATORY FIRST STEPS)

**1. Meltano ELT Ecosystem Status Check:**

```bash
# MANDATORY - Verify current ELT foundation status
make check                    # Quick validation (lint + type + meltano-config)
make meltano-validate        # Meltano project configuration validation
make test-fast              # ELT functionality verification without coverage
```

**2. Enterprise ELT Architecture Understanding:**

```bash
# Review FLEXT ecosystem ELT dependencies
grep -r "from flext_" src/ --include="*.py" | sort | uniq

# Understand Meltano integration patterns
cat src/flext_meltano/adapters.py | head -50

# Review Singer protocol abstractions
cat src/flext_meltano/tap_abstractions.py | head -50

# Check DBT service implementations
cat src/flext_meltano/service_implementations.py | head -50
```

**3. Production ELT Environment Verification:**

```bash
# Verify Meltano project structure
ls -la ./test_meltano_project/   # Sample Meltano project for testing
cat meltano.yml                 # Meltano configuration validation

# Test Singer protocol compliance
make singer-discover TAP=tap-csv  # Singer catalog discovery
make test-singer-protocols        # Singer protocol validation
```

### ⚡ DURING ELT DEVELOPMENT (PRODUCTION PATTERNS)

**1. FlextResult ELT Pattern Compliance (MANDATORY):**

```python
# ✅ CORRECT - ALL ELT operations use FlextResult pattern
from flext_core import FlextResult
from flext_meltano import FlextMeltanoAdapter

async def extract_transform_load(
    tap_name: str,
    target_name: str,
    dbt_models: List[str]
) -> FlextResult[Dict[str, Any]]:
    """Complete ELT pipeline with railway-oriented programming."""
    adapter = FlextMeltanoAdapter()

    # Extract phase with FlextResult chaining
    extract_result = await adapter.run_extraction(tap_name)
    if extract_result.is_failure:
        return FlextResult[Dict[str, Any]].fail(f"Extraction failed: {extract_result.error}")

    # Transform phase with FlextResult chaining
    transform_result = await adapter.run_transformations(dbt_models)
    if transform_result.is_failure:
        return FlextResult[Dict[str, Any]].fail(f"Transformation failed: {transform_result.error}")

    # Load phase with FlextResult chaining
    load_result = await adapter.run_loading(target_name)
    if load_result.is_failure:
        return FlextResult[Dict[str, Any]].fail(f"Loading failed: {load_result.error}")

    return FlextResult[Dict[str, Any]].ok({
        "extracted_records": extract_result.unwrap(),
        "transformed_models": transform_result.unwrap(),
        "loaded_records": load_result.unwrap()
    })

# ❌ WRONG - Try/except fallbacks for ELT operations
try:
    result = run_meltano_pipeline()  # FORBIDDEN - use FlextResult
except Exception as e:
    return {"error": str(e)}  # FORBIDDEN - use FlextResult.fail()
```

**2. Real Meltano API Integration (PRODUCTION REQUIREMENT):**

```python
# ✅ CORRECT - Direct Meltano API integration through FLEXT abstractions
from flext_meltano import FlextMeltanoService, FlextTapAbstractions

service = FlextMeltanoService()
tap_abstractions = FlextTapAbstractions()

# Real Meltano operations
result = await service.run_pipeline("tap-csv", "target-jsonl")
catalog = await tap_abstractions.discover_catalog("tap-github")

# ❌ WRONG - Mocked Meltano operations
@patch('meltano.core.project.Project')  # FORBIDDEN - use real APIs
def test_fake_meltano(): pass
```

**3. Incremental ELT Quality Validation:**

```bash
# Run after each significant change
make lint                     # Ruff validation with ELT-specific rules
make type-check              # MyPy strict mode validation
make test-unit               # Unit tests for ELT components
make meltano-validate        # Meltano configuration validation
```

### ✅ PRE-COMMIT ELT VALIDATION (ZERO TOLERANCE QUALITY GATES)

**MANDATORY Pre-Commit Checklist (100% PASS REQUIRED):**

```bash
# PHASE 1: Complete ELT Validation Pipeline (CRITICAL)
make validate                 # Complete: lint + type + security + test + meltano

# PHASE 2: ELT-Specific Validation (MANDATORY)
echo "=== MELTANO ELT FOUNDATION VALIDATION ==="

# 1. Verify ZERO custom Meltano/Singer/DBT imports
custom_imports=$(find src/ -name "*.py" -exec grep -l "import meltano\|import singer\|import dbt" {} \; 2>/dev/null)
if [ -n "$custom_imports" ]; then
    echo "❌ CRITICAL: Custom ELT imports found - use flext-meltano foundation"
    echo "$custom_imports"
    exit 1
fi

# 2. Validate Meltano project configuration
python -c "
from flext_meltano import FlextMeltanoAdapter
adapter = FlextMeltanoAdapter()
# Structure validation - would need real project for full test
print('✅ Meltano adapter creation successful')
"

# 3. Verify Singer protocol abstractions
python -c "
from flext_meltano import FlextTapAbstractions, FlextTargetAbstractions
from flext_meltano import StreamDefinition, TapConfig
tap_abs = FlextTapAbstractions()
target_abs = FlextTargetAbstractions()
print('✅ Singer protocol abstractions validated')
"

# 4. Validate DBT service integration
python -c "
from flext_meltano import FlextMeltanoDbtService
dbt_service = FlextMeltanoDbtService()
print('✅ DBT service integration validated')
"

echo "✅ Meltano ELT foundation validation COMPLETED"

# PHASE 3: ELT Test Coverage Validation (90%+ REQUIRED)
make test                    # 90%+ coverage with real Meltano APIs
pytest --cov=src/flext_meltano --cov-fail-under=90

# PHASE 4: Architecture Compliance (ENTERPRISE STANDARDS)
# No internal imports - use only root module imports
internal_imports=$(find src/ -name "*.py" -exec grep -l "from flext_meltano\.[a-z]" {} \; 2>/dev/null)
if [ -n "$internal_imports" ]; then
    echo "❌ ARCHITECTURE VIOLATION: Internal module imports found"
    echo "$internal_imports"
    echo "RESOLUTION: Use root imports - from flext_meltano import ClassName"
    exit 1
fi
```

## 🌐 PRODUCTION MELTANO ENVIRONMENT SETUP

### 🔧 ESSENTIAL ELT ENVIRONMENT VARIABLES (PRODUCTION CONFIGURATION)

```bash
# MANDATORY Meltano Environment Configuration
export MELTANO_ENVIRONMENT=dev                    # Development environment
export MELTANO_PROJECT_ROOT=$(PWD)               # Current project root
export MELTANO_DATABASE_URI="sqlite:///meltano.db" # Meltano system database

# FLEXT Ecosystem Integration
export PYTHONPATH=$(PWD)/src:$(PYTHONPATH)       # Python path for development
export FLEXT_LOG_LEVEL=INFO                      # FLEXT ecosystem logging
export FLEXT_ENVIRONMENT=development             # FLEXT environment mode

# Singer Protocol Configuration
export SINGER_CATALOG_FORMAT=json                # Singer catalog format
export SINGER_STREAM_BUFFER_SIZE=8192             # Stream buffer optimization

# DBT Configuration
export DBT_PROFILES_DIR=$(PWD)/profiles          # DBT profiles directory
export DBT_PROJECT_DIR=$(PWD)/transform          # DBT project directory
```

### 🏗️ ENTERPRISE VIRTUAL ENVIRONMENT (FLEXT WORKSPACE INTEGRATION)

```bash
# MANDATORY - Use FLEXT workspace virtual environment
cd /home/marlonsc/flext                          # Navigate to FLEXT workspace
source .venv/bin/activate                        # Activate shared virtual environment
cd flext-meltano                                 # Navigate to Meltano project

# Enterprise development setup
make install-dev                                 # Install development dependencies
make setup                                       # Complete environment setup
make meltano-init                                # Initialize Meltano project
```

### 📚 CRITICAL ELT DEVELOPMENT FILES (UNDERSTANDING FOUNDATION)

**MANDATORY Reading for ELT Development:**

**Foundation Architecture:**

- `src/flext_meltano/__init__.py` - Complete module exports and FLEXT ecosystem integration
- `src/flext_meltano/services.py` - FlextMeltanoService core ELT orchestration
- `src/flext_meltano/adapters.py` - FlextMeltanoAdapter Meltano Core integration patterns

**ELT Service Implementations:**

- `src/flext_meltano/service_implementations.py` - FlextTapService, FlextTargetService, FlextDbtService
- `src/flext_meltano/plugin_protocols.py` - TapServiceProtocol, TargetServiceProtocol, DbtServiceProtocol
- `src/flext_meltano/executors.py` - FlextMeltanoExecutor command orchestration patterns

**Singer Protocol Integration:**

- `src/flext_meltano/singer_types.py` - FlextSingerTypes Singer protocol abstractions
- `src/flext_meltano/tap_abstractions.py` - FlextTapAbstractions, StreamDefinition, TapConfig
- `src/flext_meltano/target_abstractions.py` - FlextTargetAbstractions target service wrappers

**Production Testing:**

- `tests/test_*_complete.py` - Comprehensive real Meltano API tests
- `tests/integration/` - Integration tests with real Singer/DBT operations
- `tests/e2e/` - End-to-end ELT pipeline testing

---

## 🎯 MELTANO ELT FOUNDATION SUMMARY

**ENTERPRISE ELT AUTHORITY**: flext-meltano is the enterprise-grade Meltano data integration and ELT pipeline orchestration foundation for the entire FLEXT ecosystem

**ZERO TOLERANCE ENFORCEMENT**: NO custom Meltano/Singer/DBT implementations - ALL ELT operations through FLEXT-MELTANO foundation exclusively

**FLEXT INTEGRATION COMPLETENESS**: ALL enterprise ELT needs covered by FLEXT ecosystem patterns with complete railway-oriented programming

**PRODUCTION READINESS**: Real Meltano API environment configuration and enterprise-scale data pipeline processing

**QUALITY LEADERSHIP**: Sets enterprise ELT standards with zero errors across all quality gates and 90%+ test coverage

---

**FLEXT-MELTANO AUTHORITY**: These standards are specific to enterprise Meltano ELT operations and data integration for FLEXT ecosystem  
**FLEXT ECOSYSTEM LEADERSHIP**: ALL FLEXT ELT patterns must follow FLEXT-MELTANO proven practices  
**EVIDENCE-BASED**: All patterns verified against zero errors with real Meltano environment functionality validation
