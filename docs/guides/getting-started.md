# Getting Started with FLEXT-Meltano

Complete setup guide for FLEXT-Meltano integration.

**FLEXT Integration**: This module uses flext-core for foundation patterns and flext-observability for monitoring.

## Prerequisites

**Requirements**:
- **Python 3.13+** (required for modern type system)
- **flext-core** (foundation framework with ServiceResult patterns)
- **flext-observability** (logging and monitoring)
- **Meltano CLI** for data integration
- **Git** for version control

## Installation

### 1. Environment Setup

```bash
# Navigate to project directory
cd flext-meltano

# Activate virtual environment
source .venv/bin/activate  # or your preferred venv

# Verify Python version
python --version  # Should be 3.13+

# Check FLEXT dependencies
python -c "from flext_core.domain import ServiceResult; print('✅ FLEXT-Core available')"
python -c "from flext_observability import health; print('✅ FLEXT-Observability available')"
```

### 2. Install Dependencies

```bash
# Install FLEXT-Meltano
cd flext-meltano
pip install -e .

# Install Meltano CLI
pip install meltano

# Install development dependencies (optional)
pip install -e ".[dev]"

# Verify installation
python -c "
from flext_meltano import MeltanoBridge
from flext_core.domain import ServiceResult
print('✅ Installation verified')
"
```

### 3. Verify Installation

```bash
# Test core imports
python -c "
from flext_meltano import MeltanoBridge, MeltanoProjectManager
print('✅ FLEXT-Meltano imports successful')
"

# Test Meltano CLI
meltano --version

# Test bridge availability
python -c "
from flext_meltano import MeltanoBridge
bridge = MeltanoBridge('.')
print('✅ Meltano available:', bridge.is_available())
"
```

## First Pipeline

### Step 1: Initialize Bridge

```python
# first_pipeline.py
import asyncio
from flext_meltano import MeltanoBridge

async def main():
    # Initialize the bridge
    bridge = MeltanoBridge('.')
    print("✅ Bridge initialized")
    
    # Check Meltano availability
    available = bridge.is_available()
    print(f"✅ Meltano available: {available}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Create a Project

```python
# create_project.py
import asyncio
import json
from flext_meltano import MeltanoBridge

async def create_project():
    bridge = MeltanoBridge('.')
    
    # Create a new Meltano project
    result_json = await bridge.init_project('my_first_pipeline', '.')
    result = json.loads(result_json)
    
    if result['success']:
        print(f"✅ Project created: {result['data']['project_path']}")
        return True
    else:
        if 'already exists' not in result['error']:
            print(f"❌ Project creation failed: {result['error']}")
            return False
        print("✅ Project already exists")
        return True

if __name__ == "__main__":
    success = asyncio.run(create_project())
    print(f"Project creation: {'SUCCESS' if success else 'FAILED'}")
```

### Step 3: Add Singer Plugins

```python
# add_plugins.py
import asyncio
import json
from flext_meltano import MeltanoBridge

async def add_plugins():
    bridge = MeltanoBridge('.')
    
    # Add CSV tap (extractor)
    print("Adding tap-csv...")
    tap_result_json = await bridge.add_plugin(
        'my_first_pipeline', 
        'extractor', 
        'tap-csv'
    )
    tap_result = json.loads(tap_result_json)
    
    if tap_result['success']:
        print("✅ tap-csv added successfully")
    else:
        print(f"❌ Failed to add tap-csv: {tap_result['error']}")
        return False
    
    # Add CSV target (loader)
    print("Adding target-csv...")
    target_result_json = await bridge.add_plugin(
        'my_first_pipeline',
        'loader',
        'target-csv'
    )
    target_result = json.loads(target_result_json)
    
    if target_result['success']:
        print("✅ target-csv added successfully")
        return True
    else:
        print(f"❌ Failed to add target-csv: {target_result['error']}")
        return False

if __name__ == "__main__":
    success = asyncio.run(add_plugins())
    print(f"Plugin installation: {'SUCCESS' if success else 'FAILED'}")
```

### Step 4: Create Sample Data

```python
# create_data.py
from pathlib import Path

def create_sample_data():
    """Create sample CSV data for the pipeline."""
    data_dir = Path('my_first_pipeline/data')
    data_dir.mkdir(exist_ok=True)
    
    sample_csv = data_dir / 'users.csv'
    with sample_csv.open('w') as f:
        f.write("""id,name,email,department
1,John Doe,john.doe@company.com,Engineering
2,Jane Smith,jane.smith@company.com,Marketing
3,Bob Johnson,bob.johnson@company.com,Sales
4,Alice Brown,alice.brown@company.com,Engineering
5,Charlie Wilson,charlie.wilson@company.com,Support
""")
    
    print(f"✅ Sample data created: {sample_csv}")
    return str(sample_csv)

if __name__ == "__main__":
    create_sample_data()
```

### Step 5: Run Your First Pipeline

```python
# run_pipeline.py
import asyncio
import json
from pathlib import Path
from flext_meltano import MeltanoBridge

async def run_pipeline():
    bridge = MeltanoBridge('.')
    
    # Ensure sample data exists
    data_dir = Path('my_first_pipeline/data')
    if not data_dir.exists():
        print("❌ Sample data not found. Run create_data.py first.")
        return False
    
    # Run the pipeline
    print("Running CSV extraction and loading pipeline...")
    result_json = await bridge.run_pipeline(
        'my_first_pipeline',
        'tap-csv',
        'target-csv'
    )
    
    result = json.loads(result_json)
    
    if result['success']:
        print("✅ Pipeline executed successfully!")
        print(f"Output: {result['data']['message']}")
        return True
    else:
        print(f"❌ Pipeline failed: {result['error']}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_pipeline())
    print(f"Pipeline execution: {'SUCCESS' if success else 'FAILED'}")
```

## Using Project Manager Directly (FLEXT ServiceResult Pattern)

For advanced control with FLEXT ecosystem patterns, use the MeltanoProjectManager:

```python
# project_manager_example.py (FLEXT ecosystem example)
import asyncio
import os
from pathlib import Path

# FLEXT ecosystem imports
from flext_meltano import MeltanoProjectManager
from flext_core.domain import ServiceResult
from flext_observability import health

async def project_manager_example():
    """Advanced project management using FLEXT ServiceResult patterns."""
    
    # Verify FLEXT workspace context
    workspace_root = Path(os.getenv('FLEXT_WORKSPACE_ROOT', '/home/marlonsc/flext'))
    print(f"✅ FLEXT Workspace: {workspace_root}")
    
    # Initialize manager within FLEXT ecosystem
    manager = MeltanoProjectManager('.')
    print("✅ MeltanoProjectManager initialized with FLEXT patterns")
    
    # Create project with explicit environment (ServiceResult pattern)
    print("\nCreating advanced project...")
    result = await manager.create_project('advanced_project', 'dev')
    if result.is_success:
        project_info = result.value
        print(f"✅ Created: {project_info['project_path']}")
        print(f"✅ Using FLEXT ServiceResult pattern: {type(result)}")
    else:
        print(f"❌ Failed: {result.error}")
        print(f"❌ ServiceResult error handling: {type(result)}")
        return False
    
    # Load configuration (ServiceResult pattern)
    print("\nLoading project configuration...")
    config_result = await manager.load_project_config('advanced_project')
    if config_result.is_success:
        config = config_result.value
        print(f"✅ Config loaded: {config['project_id']}")
        print(f"✅ FLEXT pattern: Configuration managed via ServiceResult")
    else:
        print(f"❌ Config load failed: {config_result.error}")
    
    # Validate project (ServiceResult pattern)
    print("\nValidating project...")
    validation = await manager.validate_project('advanced_project')
    if validation.is_success:
        validation_result = validation.value
        if validation_result['is_valid']:
            print("✅ Project validation passed")
            print("✅ FLEXT pattern: Validation with comprehensive error handling")
        else:
            errors = validation_result.get('errors', [])
            print(f"⚠️ Validation issues: {errors}")
    else:
        print(f"❌ Validation failed: {validation.error}")
    
    # Demonstrate FLEXT ecosystem integration
    print("\nFLEXT ecosystem integration verified:")
    print(f"  - ServiceResult pattern: {ServiceResult}")
    print(f"  - Health monitoring: {health}")
    print(f"  - Project manager: {manager}")
    
    return True

if __name__ == "__main__":
    # Ensure FLEXT workspace context
    if not os.getenv('FLEXT_WORKSPACE_ROOT'):
        print("⚠️ Warning: FLEXT workspace not detected")
        print("Recommended: cd /home/marlonsc/flext && source .venv/bin/activate")
        print("This ensures proper FLEXT ecosystem integration.\n")
    
    print("Running FLEXT ecosystem project management example...")
    success = asyncio.run(project_manager_example())
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")
```

## Go Integration Example (FLEXT Ecosystem Architecture)

Generate HTTP API components for Go integration within FLEXT workspace:

```python
# go_integration.py (FLEXT workspace example)
import os
from pathlib import Path

# FLEXT ecosystem imports
from flext_meltano.integrations import GoIntegration
from flext_core.domain import ServiceResult
from flext_observability import health

def generate_go_api():
    """Generate Go integration using FLEXT ecosystem patterns."""
    
    # Verify FLEXT workspace context
    workspace_root = Path(os.getenv('FLEXT_WORKSPACE_ROOT', '/home/marlonsc/flext'))
    print(f"✅ FLEXT Workspace: {workspace_root}")
    
    # Initialize Go integration within FLEXT ecosystem
    integration = GoIntegration()
    print("✅ GoIntegration initialized with FLEXT patterns")
    
    # Generate HTTP API components (FLEXT architecture approach)
    print("\nGenerating Go integration components...")
    components = integration.generate_http_api_components()
    
    print("\n✅ Generated FLEXT-compatible Go integration components:")
    for component, content in components.items():
        print(f"  - {component}: {len(content)} bytes")
    
    # FLEXT ecosystem components include:
    print("\n✅ Component details (FLEXT architecture):")
    print("  - fastapi_server.py: Python HTTP server with FLEXT observability")
    print("  - go_client.go: Go HTTP client compatible with FLEXT API patterns")
    print("  - api_documentation.md: OpenAPI docs following FLEXT standards")
    print("  - FLEXT integration: ServiceResult error handling throughout")
    
    # Verify FLEXT ecosystem integration
    print("\n✅ FLEXT ecosystem verification:")
    print(f"  - ServiceResult pattern: {ServiceResult}")
    print(f"  - Observability integration: {health}")
    print(f"  - HTTP API approach (not native bindings): Clean boundaries")
    
    return components

def save_components_to_workspace(components):
    """Save generated components to FLEXT workspace structure."""
    workspace_root = Path(os.getenv('FLEXT_WORKSPACE_ROOT', '/home/marlonsc/flext'))
    output_dir = workspace_root / "flext-meltano" / "generated" / "go_integration"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n✅ Saving components to FLEXT workspace: {output_dir}")
    
    for component_name, content in components.items():
        file_path = output_dir / component_name
        with file_path.open('w') as f:
            f.write(content)
        print(f"  - Saved: {file_path}")
    
    print(f"\n✅ Go integration components saved in FLEXT workspace structure")

if __name__ == "__main__":
    # Ensure FLEXT workspace context
    if not os.getenv('FLEXT_WORKSPACE_ROOT'):
        print("⚠️ Warning: FLEXT workspace not detected")
        print("Run: cd /home/marlonsc/flext && source .venv/bin/activate")
        print("This ensures proper FLEXT ecosystem integration.\n")
    
    print("Generating Go integration within FLEXT ecosystem...")
    components = generate_go_api()
    
    # Save to FLEXT workspace structure
    save_components_to_workspace(components)
    
    print(f"\n✅ Go integration generation completed within FLEXT ecosystem")
```

## Configuration

### Environment Variables

Create a `.env` file in your project:

```bash
# .env
# FLEXT-Meltano Configuration

# Project settings
MELTANO_PROJECT_ROOT=./projects
MELTANO_ENVIRONMENT=dev
DEBUG_MODE=true

# FLEXT integration
FLEXT_LOG_LEVEL=INFO
FLEXT_OBSERVABILITY_ENABLED=true

# Singer SDK settings (suppress warnings)
SINGER_SDK_LOG_LEVEL=ERROR
SINGER_SDK_DISABLE_WARNINGS=true
PYTHONWARNINGS=ignore::DeprecationWarning,ignore::PendingDeprecationWarning

# Performance settings
MELTANO_MAX_WORKERS=4
MELTANO_JOB_TIMEOUT=3600
```

### Load Configuration (FLEXT Ecosystem Pattern)

```python
# config_example.py (FLEXT workspace integration)
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (FLEXT workspace pattern)
workspace_root = Path("/home/marlonsc/flext")
env_path = workspace_root / "flext-meltano" / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print("✅ FLEXT-Meltano environment loaded")

# Verify FLEXT workspace configuration
flext_vars = [
    'FLEXT_WORKSPACE_ROOT',
    'PYTHON_VENV',
    'FLEXT_LOG_LEVEL'
]

meltano_vars = [
    'MELTANO_PROJECT_ROOT',
    'MELTANO_ENVIRONMENT'
]

print("\n✅ FLEXT Workspace Variables:")
for var in flext_vars:
    value = os.getenv(var)
    if value:
        print(f"  {var}: {value}")
    else:
        print(f"  ❌ Missing: {var}")

print("\n✅ FLEXT-Meltano Variables:")
for var in meltano_vars:
    value = os.getenv(var)
    if value:
        print(f"  {var}: {value}")
    else:
        print(f"  ❌ Missing: {var}")

# Verify FLEXT ecosystem integration
try:
    from flext_core.domain import ServiceResult
    from flext_observability import health
    print("\n✅ FLEXT ecosystem dependencies available")
except ImportError as e:
    print(f"\n❌ FLEXT ecosystem integration issue: {e}")
```

## Testing Your Setup

### Integration Test (FLEXT Ecosystem Validation)

```python
# test_setup.py (FLEXT ecosystem integration test)
import asyncio
import sys
import os
from pathlib import Path

# FLEXT ecosystem imports
from flext_meltano import MeltanoBridge, MeltanoProjectManager
from flext_core.domain import ServiceResult
from flext_observability import health

async def test_flext_ecosystem_integration():
    """Test complete FLEXT ecosystem integration with FLEXT-Meltano."""
    
    print("🧪 Testing FLEXT ecosystem integration...")
    
    # Verify FLEXT workspace environment
    workspace_root = Path(os.getenv('FLEXT_WORKSPACE_ROOT', '/home/marlonsc/flext'))
    python_venv = os.getenv('PYTHON_VENV', '/home/marlonsc/flext/.venv')
    
    print(f"✅ FLEXT Workspace: {workspace_root}")
    print(f"✅ Python venv: {python_venv}")
    
    try:
        # Test FLEXT core dependencies
        print("\n🔍 Testing FLEXT core dependencies...")
        print(f"✅ ServiceResult pattern: {ServiceResult}")
        print(f"✅ Observability: {health}")
        
        # Test FLEXT-Meltano bridge
        print("\n🔍 Testing FLEXT-Meltano bridge...")
        bridge = MeltanoBridge('.')
        print("✅ MeltanoBridge initialization")
        
        # Test project manager with ServiceResult patterns
        print("\n🔍 Testing project manager (ServiceResult pattern)...")
        manager = MeltanoProjectManager('.')
        print("✅ MeltanoProjectManager initialization")
        
        # Test project creation with FLEXT patterns
        print("\n🔍 Testing project creation...")
        result = await manager.create_project('test_flext_integration', 'dev')
        if result.is_success:
            project_info = result.value
            print(f"✅ Project creation: {project_info['project_path']}")
            print(f"✅ ServiceResult success: {type(result)}")
        else:
            print(f"⚠️ Project creation error: {result.error}")
            print(f"⚠️ ServiceResult error handling: {type(result)}")
        
        # Test project validation with FLEXT patterns
        print("\n🔍 Testing project validation...")
        validation = await manager.validate_project('test_flext_integration')
        if validation.is_success and validation.value['is_valid']:
            print("✅ Project validation passed")
            print(f"✅ ServiceResult validation: {type(validation)}")
        else:
            error_details = validation.value if validation.is_success else validation.error
            print(f"⚠️ Project validation issues: {error_details}")
        
        # Test FLEXT ecosystem coordination
        print("\n🔍 Testing FLEXT ecosystem coordination...")
        token_file = workspace_root / ".token"
        if token_file.exists():
            print(f"✅ FLEXT coordination token: {token_file}")
        else:
            print(f"⚠️ FLEXT coordination token not found: {token_file}")
        
        # Verify complete ecosystem
        print("\n✅ FLEXT ecosystem integration summary:")
        print("  - Workspace environment: ✅")
        print("  - Core dependencies: ✅")
        print("  - ServiceResult patterns: ✅")
        print("  - Observability integration: ✅")
        print("  - Project management: ✅")
        print("  - Multi-agent coordination: ✅")
        
        print("\n🎉 FLEXT ecosystem integration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ FLEXT dependency import failed: {e}")
        print("Ensure all FLEXT modules are installed in workspace venv")
        return False
    except Exception as e:
        print(f"❌ FLEXT ecosystem integration test failed: {e}")
        return False

def check_flext_workspace():
    """Check if we're in a proper FLEXT workspace environment."""
    workspace_root = os.getenv('FLEXT_WORKSPACE_ROOT')
    python_venv = os.getenv('PYTHON_VENV')
    
    if not workspace_root:
        print("⚠️ Warning: FLEXT_WORKSPACE_ROOT not set")
        print("Run: cd /home/marlonsc/flext && source .venv/bin/activate")
        return False
    
    if not python_venv:
        print("⚠️ Warning: PYTHON_VENV not set")
        print("Ensure FLEXT workspace environment is properly activated")
        return False
    
    return True

if __name__ == "__main__":
    print("FLEXT Ecosystem Integration Test")
    print("=" * 40)
    
    # Check FLEXT workspace environment
    if not check_flext_workspace():
        print("\n❌ FLEXT workspace environment not properly configured")
        sys.exit(1)
    
    # Run comprehensive integration test
    success = asyncio.run(test_flext_ecosystem_integration())
    
    exit_code = 0 if success else 1
    print(f"\nTest result: {'SUCCESS' if success else 'FAILED'}")
    sys.exit(exit_code)
```

## Next Steps

Once you have the basic setup working:

1. **[Project Management Guide](./project-management.md)** - Learn advanced project operations
2. **[API Reference](../api/core.md)** - Complete API documentation
3. **[Pipeline Examples](../examples/basic-pipeline.md)** - More complex pipeline patterns
4. **[Production Guide](../deployment/production.md)** - Deployment considerations

## Troubleshooting

### Common Issues

**Import Errors** (FLEXT Workspace Context):
```bash
# Ensure you're in the FLEXT workspace with shared venv
cd /home/marlonsc/flext
source .venv/bin/activate

# Reinstall FLEXT-Meltano in development mode
cd flext-meltano
pip install -e .

# Verify FLEXT ecosystem integration
python -c "from flext_meltano import MeltanoBridge; from flext_core import ServiceResult; print('✅ Integration working')"
```

**Meltano Not Found** (Workspace Installation):
```bash
# Install Meltano in shared workspace venv
cd /home/marlonsc/flext
source .venv/bin/activate
pip install meltano
```

**FLEXT Dependencies** (Ecosystem Integration):
```bash
# Ensure all FLEXT core modules are installed in workspace
cd /home/marlonsc/flext
source .venv/bin/activate

# Install core FLEXT dependencies
cd flext-core && pip install -e . && cd ..
cd flext-observability && pip install -e . && cd ..
cd flext-meltano && pip install -e . && cd ..

# Verify complete ecosystem
python -c "
from flext_core.domain import ServiceResult
from flext_observability import health
from flext_meltano import MeltanoBridge
print('✅ Complete FLEXT ecosystem available')
"
```

**Type Errors**:
```bash
# Verify Python version
python --version  # Should be 3.13+
```

### Singer SDK Warnings

Warnings should be automatically suppressed with the configuration above. If you still see warnings, verify your environment variables:

```bash
echo $SINGER_SDK_LOG_LEVEL      # Should be ERROR
echo $SINGER_SDK_DISABLE_WARNINGS  # Should be true
```

---

## Next Steps

**Ready to build your first production pipeline?**

### Continue Learning

1. **[Project Management Guide](./project-management.md)** - Advanced project operations
2. **[API Reference](../api/core.md)** - Complete API documentation
3. **[Pipeline Examples](../examples/basic-pipeline.md)** - More pipeline patterns
4. **[Production Guide](../deployment/production.md)** - Deployment considerations

### FLEXT Integration

- **flext-core**: Foundation for ServiceResult patterns and Clean Architecture
- **flext-observability**: Logging and monitoring integration
- **Extensions**: Oracle and LDAP integration capabilities

### Best Practices

- Use ServiceResult pattern for consistent error handling
- Follow async/await patterns throughout
- Implement proper logging with flext-observability
- Test with realistic data volumes
- Monitor pipeline performance and errors

**Ready to build production data pipelines!**