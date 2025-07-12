# Project Management Guide

This guide covers advanced project management features in FLEXT-Meltano, including project lifecycle, configuration management, and enterprise operations.

## 🏗️ Project Lifecycle Management

### Project Creation Patterns

#### Basic Project Creation

```python
# basic_project.py
import asyncio
from src.flext_meltano.project_manager import MeltanoProjectManager

async def create_basic_project():
    manager = MeltanoProjectManager('.')
    
    # Create project with default settings
    result = await manager.create_project(
        project_name='analytics_pipeline',
        environment='dev'
    )
    
    if result.is_success:
        project_info = result.value
        print(f"✅ Project created: {project_info['project_path']}")
        print(f"   Environment: {project_info['environment']}")
        print(f"   Created at: {project_info['created_at']}")
    else:
        print(f"❌ Creation failed: {result.error}")
    
    return result.is_success

asyncio.run(create_basic_project())
```

#### Enterprise Project with Custom Configuration

```python
# enterprise_project.py
import asyncio
from datetime import datetime, UTC
from src.flext_meltano.project_manager import FlextProjectManager

async def create_enterprise_project():
    # Use FlextProjectManager for enterprise features
    manager = FlextProjectManager('.', event_bus=None)  # Add event bus in production
    
    # Create project with events
    result = await manager.create_project_with_events(
        project_name='enterprise_etl',
        environment='production'
    )
    
    if result.is_success:
        print("✅ Enterprise project created with events")
        
        # Create backup immediately
        backup_result = await manager.backup_project(
            'enterprise_etl',
            backup_path=Path(f'backups/enterprise_etl_{datetime.now(UTC).strftime("%Y%m%d_%H%M%S")}')
        )
        
        if backup_result.is_success:
            print(f"✅ Initial backup created: {backup_result.value}")
        
    return result.is_success

asyncio.run(create_enterprise_project())
```

### Project Configuration Management

#### Loading and Modifying Configuration

```python
# config_management.py
import asyncio
from src.flext_meltano.project_manager import MeltanoProjectManager

async def manage_project_config():
    manager = MeltanoProjectManager('.')
    project_name = 'analytics_pipeline'
    
    # Load current configuration
    config_result = await manager.load_project_config(project_name)
    if not config_result.is_success:
        print(f"❌ Failed to load config: {config_result.error}")
        return
    
    config = config_result.value
    print(f"✅ Loaded config for project: {config['project_id']}")
    
    # Add environment-specific settings
    if 'environments' not in config:
        config['environments'] = []
    
    # Add production environment
    prod_env = {
        'name': 'prod',
        'config': {
            'plugins': {
                'extractors': [{
                    'name': 'tap-postgres',
                    'variant': 'meltanolabs',
                    'config': {
                        'host': '${POSTGRES_HOST}',
                        'port': '${POSTGRES_PORT}',
                        'user': '${POSTGRES_USER}',
                        'password': '${POSTGRES_PASSWORD}',
                        'database': '${POSTGRES_DATABASE}'
                    }
                }],
                'loaders': [{
                    'name': 'target-snowflake',
                    'variant': 'meltanolabs',
                    'config': {
                        'account': '${SNOWFLAKE_ACCOUNT}',
                        'user': '${SNOWFLAKE_USER}',
                        'password': '${SNOWFLAKE_PASSWORD}',
                        'database': '${SNOWFLAKE_DATABASE}',
                        'warehouse': '${SNOWFLAKE_WAREHOUSE}'
                    }
                }]
            }
        }
    }
    
    # Check if prod environment exists
    prod_exists = any(env.get('name') == 'prod' for env in config['environments'])
    if not prod_exists:
        config['environments'].append(prod_env)
        print("✅ Added production environment")
    
    # Save updated configuration
    save_result = await manager.save_project_config(project_name, config)
    if save_result.is_success:
        print("✅ Configuration saved successfully")
    else:
        print(f"❌ Failed to save config: {save_result.error}")

asyncio.run(manage_project_config())
```

#### Configuration Templates

```python
# config_templates.py
from typing import Dict, Any

class MeltanoConfigTemplates:
    """Predefined configuration templates for common use cases."""
    
    @staticmethod
    def postgres_to_snowflake() -> Dict[str, Any]:
        """Template for PostgreSQL to Snowflake pipeline."""
        return {
            'version': 1,
            'default_environment': 'dev',
            'environments': [
                {'name': 'dev'},
                {'name': 'staging'},
                {'name': 'prod'}
            ],
            'plugins': {
                'extractors': [{
                    'name': 'tap-postgres',
                    'variant': 'meltanolabs',
                    'config': {
                        'host': 'localhost',
                        'port': 5432,
                        'user': 'postgres',
                        'password': 'password',
                        'database': 'source_db'
                    },
                    'select': [
                        'public-users.*',
                        'public-orders.*',
                        'public-products.*'
                    ]
                }],
                'loaders': [{
                    'name': 'target-snowflake',
                    'variant': 'meltanolabs',
                    'config': {
                        'account': 'your_account',
                        'user': 'your_user',
                        'password': 'your_password',
                        'database': 'ANALYTICS',
                        'warehouse': 'COMPUTE_WH',
                        'schema': 'RAW'
                    }
                }],
                'transformers': [{
                    'name': 'dbt-snowflake',
                    'variant': 'dbt-labs'
                }]
            },
            'schedules': [{
                'name': 'daily_sync',
                'interval': '@daily',
                'job': 'tap-postgres target-snowflake'
            }]
        }
    
    @staticmethod
    def api_to_postgres() -> Dict[str, Any]:
        """Template for API to PostgreSQL pipeline."""
        return {
            'version': 1,
            'default_environment': 'dev',
            'plugins': {
                'extractors': [{
                    'name': 'tap-rest-api-msdk',
                    'variant': 'meltanolabs',
                    'config': {
                        'api_url': 'https://api.example.com',
                        'api_key': '${API_KEY}',
                        'pagination_type': 'offset',
                        'pagination_limit': 100
                    }
                }],
                'loaders': [{
                    'name': 'target-postgres',
                    'variant': 'meltanolabs',
                    'config': {
                        'host': 'localhost',
                        'port': 5432,
                        'user': 'postgres',
                        'password': '${POSTGRES_PASSWORD}',
                        'database': 'warehouse'
                    }
                }]
            }
        }

# Usage example
async def create_from_template():
    manager = MeltanoProjectManager('.')
    
    # Create project
    await manager.create_project('api_pipeline', 'dev')
    
    # Apply template
    template_config = MeltanoConfigTemplates.api_to_postgres()
    await manager.save_project_config('api_pipeline', template_config)
    
    print("✅ Project created from template")
```

## 🔧 Plugin Management

### Advanced Plugin Operations

```python
# plugin_management.py
import asyncio
from src.flext_meltano.project_manager import MeltanoProjectManager

async def advanced_plugin_management():
    manager = MeltanoProjectManager('.')
    project_name = 'analytics_pipeline'
    
    # Add plugins with specific variants and configuration
    plugins_to_add = [
        {
            'type': 'extractor',
            'name': 'tap-csv',
            'variant': 'meltanolabs',
            'config': {
                'files': [
                    {
                        'path': 'data/users.csv',
                        'name': 'users',
                        'pattern': 'users*.csv'
                    }
                ]
            }
        },
        {
            'type': 'loader', 
            'name': 'target-postgres',
            'variant': 'meltanolabs',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'user': 'analytics',
                'password': '${POSTGRES_PASSWORD}',
                'database': 'warehouse',
                'schema': 'raw'
            }
        },
        {
            'type': 'transformer',
            'name': 'dbt-postgres',
            'variant': 'dbt-labs'
        }
    ]
    
    for plugin_config in plugins_to_add:
        print(f"Adding {plugin_config['name']}...")
        
        result = await manager.add_plugin(
            project_name=project_name,
            plugin_type=plugin_config['type'],
            plugin_name=plugin_config['name'],
            variant=plugin_config.get('variant', ''),
            **plugin_config.get('config', {})
        )
        
        if result.is_success:
            print(f"✅ {plugin_config['name']} added successfully")
        else:
            print(f"❌ Failed to add {plugin_config['name']}: {result.error}")

asyncio.run(advanced_plugin_management())
```

### Plugin Configuration Updates

```python
# plugin_config.py
import asyncio
import yaml
from pathlib import Path
from src.flext_meltano.project_manager import MeltanoProjectManager

async def update_plugin_configs():
    manager = MeltanoProjectManager('.')
    project_name = 'analytics_pipeline'
    
    # Load current config
    config_result = await manager.load_project_config(project_name)
    config = config_result.value
    
    # Update tap-csv configuration
    extractors = config.get('plugins', {}).get('extractors', [])
    for extractor in extractors:
        if extractor.get('name') == 'tap-csv':
            extractor['config'] = {
                'files': [
                    {
                        'path': 'data/users.csv',
                        'name': 'users',
                        'keys': ['id'],
                        'encoding': 'utf-8'
                    },
                    {
                        'path': 'data/orders.csv',
                        'name': 'orders', 
                        'keys': ['order_id'],
                        'encoding': 'utf-8'
                    }
                ]
            }
            break
    
    # Update target-postgres configuration
    loaders = config.get('plugins', {}).get('loaders', [])
    for loader in loaders:
        if loader.get('name') == 'target-postgres':
            loader['config'].update({
                'default_target_schema': 'raw_data',
                'hard_delete': True,
                'add_record_metadata': True
            })
            break
    
    # Save updated configuration
    save_result = await manager.save_project_config(project_name, config)
    if save_result.is_success:
        print("✅ Plugin configurations updated")
    else:
        print(f"❌ Failed to update configs: {save_result.error}")

asyncio.run(update_plugin_configs())
```

## 🔍 Project Validation and Health Checks

### Comprehensive Project Validation

```python
# validation.py
import asyncio
from pathlib import Path
from src.flext_meltano.project_manager import MeltanoProjectManager

async def comprehensive_validation():
    manager = MeltanoProjectManager('.')
    project_name = 'analytics_pipeline'
    
    print(f"🔍 Validating project: {project_name}")
    
    # Basic validation
    validation_result = await manager.validate_project(project_name)
    if not validation_result.is_success:
        print(f"❌ Validation failed: {validation_result.error}")
        return
    
    validation = validation_result.value
    print(f"✅ Project exists: {validation['project_exists']}")
    print(f"✅ Config exists: {validation['config_exists']}")
    print(f"✅ Meltano dir exists: {validation['meltano_dir_exists']}")
    print(f"✅ Config valid: {validation['config_valid']}")
    
    if validation['errors']:
        print("⚠️ Validation warnings:")
        for error in validation['errors']:
            print(f"   - {error}")
    
    # Additional health checks
    project_path = Path('.') / project_name
    
    # Check for required directories
    required_dirs = ['.meltano', 'data', 'transform', 'orchestrate']
    for dir_name in required_dirs:
        dir_path = project_path / dir_name
        if dir_path.exists():
            print(f"✅ Directory exists: {dir_name}")
        else:
            print(f"⚠️ Directory missing: {dir_name}")
            # Create missing directories
            dir_path.mkdir(exist_ok=True)
            print(f"   Created: {dir_name}")
    
    # Check plugin installations
    meltano_dir = project_path / '.meltano'
    if meltano_dir.exists():
        plugin_dirs = [d for d in meltano_dir.iterdir() if d.is_dir()]
        print(f"✅ Installed plugins: {len(plugin_dirs)}")
        for plugin_dir in plugin_dirs[:5]:  # Show first 5
            print(f"   - {plugin_dir.name}")
    
    return validation['is_valid']

asyncio.run(comprehensive_validation())
```

### Performance Health Checks

```python
# performance_checks.py
import asyncio
import time
from pathlib import Path
from src.flext_meltano.project_manager import MeltanoProjectManager

async def performance_health_check():
    manager = MeltanoProjectManager('.')
    
    # Measure project creation time
    start_time = time.time()
    result = await manager.create_project('perf_test', 'dev')
    creation_time = time.time() - start_time
    
    if result.is_success:
        print(f"✅ Project creation time: {creation_time:.2f}s")
    
    # Measure config loading time
    start_time = time.time()
    config_result = await manager.load_project_config('perf_test')
    load_time = time.time() - start_time
    
    if config_result.is_success:
        print(f"✅ Config loading time: {load_time:.3f}s")
    
    # Measure validation time
    start_time = time.time()
    validation_result = await manager.validate_project('perf_test')
    validation_time = time.time() - start_time
    
    if validation_result.is_success:
        print(f"✅ Validation time: {validation_time:.3f}s")
    
    # Performance thresholds
    thresholds = {
        'creation_time': 5.0,  # 5 seconds
        'load_time': 0.1,      # 100ms
        'validation_time': 0.5  # 500ms
    }
    
    # Check performance
    checks = [
        ('Project Creation', creation_time, thresholds['creation_time']),
        ('Config Loading', load_time, thresholds['load_time']),
        ('Validation', validation_time, thresholds['validation_time'])
    ]
    
    print("\n📊 Performance Summary:")
    for check_name, actual_time, threshold in checks:
        status = "✅" if actual_time <= threshold else "⚠️"
        print(f"{status} {check_name}: {actual_time:.3f}s (threshold: {threshold}s)")

asyncio.run(performance_health_check())
```

## 💾 Backup and Recovery

### Automated Backup System

```python
# backup_system.py
import asyncio
from datetime import datetime, UTC
from pathlib import Path
from src.flext_meltano.project_manager import FlextProjectManager

class ProjectBackupManager:
    def __init__(self, base_backup_path: str = 'backups'):
        self.manager = FlextProjectManager('.')
        self.backup_base = Path(base_backup_path)
        self.backup_base.mkdir(exist_ok=True)
    
    async def create_timestamped_backup(self, project_name: str) -> Path:
        """Create backup with timestamp."""
        timestamp = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')
        backup_name = f"{project_name}_backup_{timestamp}"
        backup_path = self.backup_base / backup_name
        
        result = await self.manager.backup_project(project_name, backup_path)
        if result.is_success:
            print(f"✅ Backup created: {result.value}")
            return result.value
        else:
            print(f"❌ Backup failed: {result.error}")
            raise Exception(result.error)
    
    async def create_scheduled_backup(self, project_name: str) -> None:
        """Create backup with retention policy."""
        try:
            backup_path = await self.create_timestamped_backup(project_name)
            
            # Implement retention policy - keep last 5 backups
            project_backups = sorted([
                f for f in self.backup_base.glob(f"{project_name}_backup_*.zip")
            ], key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove old backups beyond retention limit
            for old_backup in project_backups[5:]:
                old_backup.unlink()
                print(f"🗑️ Removed old backup: {old_backup.name}")
            
        except Exception as e:
            print(f"❌ Scheduled backup failed: {e}")
    
    async def restore_from_backup(self, backup_path: Path, target_name: str) -> bool:
        """Restore project from backup."""
        try:
            import zipfile
            import shutil
            
            # Extract backup to temporary location
            temp_dir = Path('.') / f'temp_restore_{target_name}'
            
            with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Move to final location
            target_path = Path('.') / target_name
            if target_path.exists():
                shutil.rmtree(target_path)
            
            shutil.move(str(temp_dir), str(target_path))
            
            print(f"✅ Project restored: {target_name}")
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False

# Usage example
async def backup_demo():
    backup_manager = ProjectBackupManager()
    
    # Create scheduled backup
    await backup_manager.create_scheduled_backup('analytics_pipeline')
    
    # List available backups
    backups = list(backup_manager.backup_base.glob('analytics_pipeline_backup_*.zip'))
    print(f"📦 Available backups: {len(backups)}")
    
    if backups:
        # Restore from latest backup
        latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
        await backup_manager.restore_from_backup(latest_backup, 'restored_pipeline')

asyncio.run(backup_demo())
```

## 🔄 Project Migration and Cloning

### Project Cloning

```python
# project_cloning.py
import asyncio
import shutil
from pathlib import Path
from src.flext_meltano.project_manager import MeltanoProjectManager

async def clone_project(source_project: str, target_project: str, new_environment: str = None):
    manager = MeltanoProjectManager('.')
    
    # Load source configuration
    source_config_result = await manager.load_project_config(source_project)
    if not source_config_result.is_success:
        print(f"❌ Failed to load source project: {source_config_result.error}")
        return False
    
    source_config = source_config_result.value
    
    # Create target project
    target_env = new_environment or source_config.get('default_environment', 'dev')
    create_result = await manager.create_project(target_project, target_env)
    
    if not create_result.is_success:
        print(f"❌ Failed to create target project: {create_result.error}")
        return False
    
    # Clone configuration
    cloned_config = source_config.copy()
    cloned_config['project_id'] = f"{target_project}-{datetime.now(UTC).strftime('%Y%m%d')}"
    if new_environment:
        cloned_config['default_environment'] = new_environment
    
    # Save cloned configuration
    save_result = await manager.save_project_config(target_project, cloned_config)
    if not save_result.is_success:
        print(f"❌ Failed to save cloned config: {save_result.error}")
        return False
    
    # Copy additional files (data, transforms, etc.)
    source_path = Path('.') / source_project
    target_path = Path('.') / target_project
    
    # Copy data directory if it exists
    source_data = source_path / 'data'
    if source_data.exists():
        target_data = target_path / 'data'
        shutil.copytree(source_data, target_data, dirs_exist_ok=True)
        print(f"✅ Copied data directory")
    
    # Copy transform directory if it exists
    source_transform = source_path / 'transform'
    if source_transform.exists():
        target_transform = target_path / 'transform'
        shutil.copytree(source_transform, target_transform, dirs_exist_ok=True)
        print(f"✅ Copied transform directory")
    
    print(f"✅ Project cloned: {source_project} → {target_project}")
    return True

# Usage
asyncio.run(clone_project('analytics_pipeline', 'analytics_pipeline_staging', 'staging'))
```

## 📊 Project Analytics and Monitoring

### Project Metrics Collection

```python
# project_metrics.py
import asyncio
from datetime import datetime, UTC
from pathlib import Path
from src.flext_meltano.project_manager import MeltanoProjectManager

class ProjectAnalytics:
    def __init__(self):
        self.manager = MeltanoProjectManager('.')
    
    async def collect_project_metrics(self, project_name: str) -> dict:
        """Collect comprehensive project metrics."""
        metrics = {
            'project_name': project_name,
            'timestamp': datetime.now(UTC).isoformat(),
        }
        
        # Basic project info
        config_result = await self.manager.load_project_config(project_name)
        if config_result.is_success:
            config = config_result.value
            metrics.update({
                'project_id': config.get('project_id'),
                'default_environment': config.get('default_environment'),
                'version': config.get('version'),
            })
            
            # Plugin metrics
            plugins = config.get('plugins', {})
            metrics['plugin_counts'] = {
                'extractors': len(plugins.get('extractors', [])),
                'loaders': len(plugins.get('loaders', [])),
                'transformers': len(plugins.get('transformers', [])),
                'orchestrators': len(plugins.get('orchestrators', [])),
                'utilities': len(plugins.get('utilities', []))
            }
            
            # Environment metrics
            environments = config.get('environments', [])
            metrics['environment_count'] = len(environments)
            metrics['environments'] = [env.get('name') for env in environments]
        
        # File system metrics
        project_path = Path('.') / project_name
        if project_path.exists():
            metrics['file_system'] = await self._collect_filesystem_metrics(project_path)
        
        # Performance metrics
        validation_result = await self.manager.validate_project(project_name)
        if validation_result.is_success:
            metrics['validation'] = validation_result.value
        
        return metrics
    
    async def _collect_filesystem_metrics(self, project_path: Path) -> dict:
        """Collect file system metrics for project."""
        metrics = {
            'total_size_bytes': 0,
            'file_counts': {},
            'directory_structure': []
        }
        
        # Count files by type
        file_types = {}
        total_size = 0
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                suffix = file_path.suffix.lower() or 'no_extension'
                file_types[suffix] = file_types.get(suffix, 0) + 1
                total_size += file_path.stat().st_size
        
        metrics['total_size_bytes'] = total_size
        metrics['file_counts'] = file_types
        
        # Directory structure
        for item in project_path.iterdir():
            if item.is_dir():
                metrics['directory_structure'].append(item.name)
        
        return metrics

# Usage example
async def analyze_projects():
    analytics = ProjectAnalytics()
    
    # Analyze specific project
    metrics = await analytics.collect_project_metrics('analytics_pipeline')
    
    print(f"📊 Project Analysis: {metrics['project_name']}")
    print(f"   Project ID: {metrics.get('project_id', 'N/A')}")
    print(f"   Environment: {metrics.get('default_environment', 'N/A')}")
    print(f"   Total Size: {metrics.get('file_system', {}).get('total_size_bytes', 0):,} bytes")
    
    plugin_counts = metrics.get('plugin_counts', {})
    print(f"   Plugins: {sum(plugin_counts.values())} total")
    for plugin_type, count in plugin_counts.items():
        if count > 0:
            print(f"     - {plugin_type}: {count}")

asyncio.run(analyze_projects())
```

---

**Next**: Continue with [Pipeline Orchestration Guide](./orchestration.md) to learn about advanced pipeline management.