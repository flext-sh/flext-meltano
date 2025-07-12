# Basic Pipeline Examples

This guide provides comprehensive examples for building and running basic data pipelines with FLEXT-Meltano.

## 🚀 Quick Start Example

### Simple CSV to PostgreSQL Pipeline

This example demonstrates a complete end-to-end pipeline that extracts data from CSV files and loads it into PostgreSQL.

```python
# basic_csv_pipeline.py
import asyncio
import json
from pathlib import Path
from src.flext_meltano.integrations.bridge import MeltanoBridge

async def create_csv_to_postgres_pipeline():
    """Complete CSV to PostgreSQL pipeline example."""
    
    print("🚀 Creating CSV to PostgreSQL pipeline...")
    
    # Initialize bridge
    bridge = MeltanoBridge('.')
    project_name = 'csv_to_postgres'
    
    # Step 1: Create project
    print("\n📁 Creating Meltano project...")
    project_result = await bridge.init_project(project_name, '.')
    project_data = json.loads(project_result)
    
    if project_data['success']:
        print(f"✅ Project created: {project_data['data']['project_path']}")
    else:
        if 'already exists' in project_data['error']:
            print("✅ Project already exists")
        else:
            print(f"❌ Project creation failed: {project_data['error']}")
            return False
    
    # Step 2: Create sample data
    print("\n📊 Creating sample CSV data...")
    await create_sample_csv_data(project_name)
    
    # Step 3: Add extractor (tap-csv)
    print("\n🔌 Adding CSV extractor...")
    tap_result = await bridge.add_plugin(
        project_name, 
        'extractor', 
        'tap-csv',
        'meltanolabs'
    )
    tap_data = json.loads(tap_result)
    
    if tap_data['success']:
        print("✅ tap-csv added successfully")
    else:
        print(f"⚠️ tap-csv issue: {tap_data['error']}")
    
    # Step 4: Add loader (target-postgres)
    print("\n🎯 Adding PostgreSQL loader...")
    target_result = await bridge.add_plugin(
        project_name,
        'loader',
        'target-postgres',
        'meltanolabs'
    )
    target_data = json.loads(target_result)
    
    if target_data['success']:
        print("✅ target-postgres added successfully")
    else:
        print(f"⚠️ target-postgres issue: {target_data['error']}")
    
    # Step 5: Configure plugins
    print("\n⚙️ Configuring plugins...")
    await configure_csv_postgres_plugins(project_name)
    
    # Step 6: Run pipeline
    print("\n🏃 Running pipeline...")
    pipeline_result = await bridge.run_pipeline(
        project_name,
        'tap-csv',
        'target-postgres'
    )
    
    pipeline_data = json.loads(pipeline_result)
    if pipeline_data['success']:
        print("✅ Pipeline executed successfully!")
        print(f"   Result: {pipeline_data['data']['message']}")
    else:
        print(f"❌ Pipeline failed: {pipeline_data['error']}")
    
    # Step 7: Verify results
    print("\n✅ Pipeline Summary:")
    info_result = await bridge.get_project_info(project_name)
    info_data = json.loads(info_result)
    
    if info_data['success']:
        config = info_data['data']['config']
        extractors = len(config.get('plugins', {}).get('extractors', []))
        loaders = len(config.get('plugins', {}).get('loaders', []))
        print(f"   Project: {config.get('project_id')}")
        print(f"   Extractors: {extractors}")
        print(f"   Loaders: {loaders}")
    
    return True

async def create_sample_csv_data(project_name: str):
    """Create sample CSV files for the pipeline."""
    
    data_dir = Path(project_name) / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Create customers.csv
    customers_csv = data_dir / 'customers.csv'
    with customers_csv.open('w') as f:
        f.write("""customer_id,name,email,signup_date,plan_type,monthly_revenue
1,Alice Johnson,alice@techcorp.com,2023-01-15,enterprise,2500
2,Bob Smith,bob@startup.io,2023-02-20,professional,500
3,Carol Brown,carol@agency.co,2023-03-10,enterprise,3000
4,David Wilson,david@freelance.dev,2023-04-05,basic,50
5,Emma Davis,emma@consulting.biz,2023-05-12,professional,750
6,Frank Miller,frank@design.studio,2023-06-18,basic,25
7,Grace Lee,grace@datacompany.com,2023-07-22,enterprise,5000
8,Henry Garcia,henry@marketing.pro,2023-08-14,professional,600
9,Ivy Chen,ivy@tech.startup,2023-09-09,basic,75
10,Jack Taylor,jack@internal.invalid,2023-10-03,enterprise,4500
""")
    
    # Create orders.csv
    orders_csv = data_dir / 'orders.csv'
    with orders_csv.open('w') as f:
        f.write("""order_id,customer_id,product_name,quantity,unit_price,order_date,status
1001,1,Data Analytics Platform,1,2500.00,2023-07-15,completed
1002,2,API Integration Tool,3,150.00,2023-07-16,completed
1003,3,Custom Dashboard,1,3000.00,2023-07-17,processing
1004,4,Basic Analytics,2,25.00,2023-07-18,completed
1005,5,Professional Reports,1,750.00,2023-07-19,completed
1006,1,Advanced Features,1,500.00,2023-07-20,shipped
1007,6,Starter Package,1,25.00,2023-07-21,completed
1008,7,Enterprise Suite,1,5000.00,2023-07-22,processing
1009,2,Premium Support,1,200.00,2023-07-23,completed
1010,8,Marketing Analytics,2,300.00,2023-07-24,shipped
""")
    
    # Create products.csv
    products_csv = data_dir / 'products.csv'
    with products_csv.open('w') as f:
        f.write("""product_id,name,category,price,description,in_stock
101,Data Analytics Platform,enterprise,2500.00,Complete analytics solution,true
102,API Integration Tool,professional,150.00,REST API integration toolkit,true
103,Custom Dashboard,enterprise,3000.00,Personalized data visualization,true
104,Basic Analytics,basic,25.00,Simple analytics for small teams,true
105,Professional Reports,professional,750.00,Advanced reporting capabilities,true
106,Advanced Features,enterprise,500.00,Premium feature set,true
107,Starter Package,basic,25.00,Entry-level analytics,true
108,Enterprise Suite,enterprise,5000.00,Full enterprise solution,false
109,Premium Support,professional,200.00,24/7 technical support,true
110,Marketing Analytics,professional,300.00,Marketing-focused analytics,true
""")
    
    print(f"✅ Created sample data files:")
    print(f"   - {customers_csv} (10 customers)")
    print(f"   - {orders_csv} (10 orders)")
    print(f"   - {products_csv} (10 products)")

async def configure_csv_postgres_plugins(project_name: str):
    """Configure tap-csv and target-postgres plugins."""
    
    from src.flext_meltano.project_manager import MeltanoProjectManager
    
    manager = MeltanoProjectManager('.')
    
    # Load current configuration
    config_result = await manager.load_project_config(project_name)
    if not config_result.is_success:
        print(f"Failed to load config: {config_result.error}")
        return
    
    config = config_result.value
    
    # Configure tap-csv
    extractors = config.get('plugins', {}).get('extractors', [])
    for extractor in extractors:
        if extractor.get('name') == 'tap-csv':
            extractor['config'] = {
                'files': [
                    {
                        'path': 'data/customers.csv',
                        'name': 'customers',
                        'keys': ['customer_id'],
                        'encoding': 'utf-8'
                    },
                    {
                        'path': 'data/orders.csv',
                        'name': 'orders',
                        'keys': ['order_id'],
                        'encoding': 'utf-8'
                    },
                    {
                        'path': 'data/products.csv',
                        'name': 'products',
                        'keys': ['product_id'],
                        'encoding': 'utf-8'
                    }
                ]
            }
            break
    
    # Configure target-postgres
    loaders = config.get('plugins', {}).get('loaders', [])
    for loader in loaders:
        if loader.get('name') == 'target-postgres':
            loader['config'] = {
                'host': 'localhost',
                'port': 5432,
                'user': 'postgres',
                'password': 'password',
                'database': 'analytics',
                'default_target_schema': 'raw_data',
                'hard_delete': True,
                'add_record_metadata': True
            }
            break
    
    # Save updated configuration
    save_result = await manager.save_project_config(project_name, config)
    if save_result.is_success:
        print("✅ Plugin configurations updated")
    else:
        print(f"❌ Failed to update configs: {save_result.error}")

# Run the example
if __name__ == "__main__":
    success = asyncio.run(create_csv_to_postgres_pipeline())
    print(f"\n🎉 Pipeline example: {'SUCCESS' if success else 'FAILED'}")
```

## 📊 API to Database Pipeline

### REST API to PostgreSQL with Incremental Loading

```python
# api_to_postgres_pipeline.py
import asyncio
import json
from datetime import datetime, UTC
from src.flext_meltano.integrations.bridge import MeltanoBridge

async def create_api_to_postgres_pipeline():
    """API to PostgreSQL pipeline with incremental loading."""
    
    bridge = MeltanoBridge('.')
    project_name = 'api_to_postgres'
    
    print("🌐 Creating API to PostgreSQL pipeline...")
    
    # Create project
    await bridge.init_project(project_name, '.')
    
    # Add API extractor
    print("🔌 Adding REST API extractor...")
    await bridge.add_plugin(
        project_name,
        'extractor', 
        'tap-rest-api-msdk',
        'meltanolabs'
    )
    
    # Add PostgreSQL loader
    print("🎯 Adding PostgreSQL loader...")
    await bridge.add_plugin(
        project_name,
        'loader',
        'target-postgres'
    )
    
    # Configure plugins
    await configure_api_postgres_plugins(project_name)
    
    # Run pipeline
    print("🏃 Running API pipeline...")
    result = await bridge.run_pipeline(
        project_name,
        'tap-rest-api-msdk',
        'target-postgres'
    )
    
    return json.loads(result)['success']

async def configure_api_postgres_plugins(project_name: str):
    """Configure API and PostgreSQL plugins."""
    
    from src.flext_meltano.project_manager import MeltanoProjectManager
    
    manager = MeltanoProjectManager('.')
    config_result = await manager.load_project_config(project_name)
    config = config_result.value
    
    # Configure tap-rest-api-msdk
    extractors = config.get('plugins', {}).get('extractors', [])
    for extractor in extractors:
        if 'rest-api' in extractor.get('name', ''):
            extractor['config'] = {
                'api_url': 'https://jsonplaceholder.typicode.com',
                'pagination_type': 'offset',
                'pagination_limit': 100,
                'streams': [
                    {
                        'name': 'users',
                        'path': '/users',
                        'primary_keys': ['id'],
                        'replication_key': 'id'
                    },
                    {
                        'name': 'posts', 
                        'path': '/posts',
                        'primary_keys': ['id'],
                        'replication_key': 'id'
                    },
                    {
                        'name': 'comments',
                        'path': '/comments',
                        'primary_keys': ['id'],
                        'replication_key': 'id'
                    }
                ]
            }
            break
    
    # Configure target-postgres
    loaders = config.get('plugins', {}).get('loaders', [])
    for loader in loaders:
        if loader.get('name') == 'target-postgres':
            loader['config'] = {
                'host': 'localhost',
                'port': 5432,
                'user': 'postgres',
                'password': 'password',
                'database': 'api_data',
                'default_target_schema': 'public',
                'hard_delete': False,  # Keep historical data
                'add_record_metadata': True
            }
            break
    
    await manager.save_project_config(project_name, config)
    print("✅ API and PostgreSQL configurations updated")
```

## 🔄 File-Based ETL Pipeline

### Multi-Format File Processing

```python
# file_etl_pipeline.py
import asyncio
import json
import csv
import pandas as pd
from pathlib import Path
from src.flext_meltano.integrations.bridge import MeltanoBridge

async def create_file_etl_pipeline():
    """Multi-format file processing pipeline."""
    
    bridge = MeltanoBridge('.')
    project_name = 'file_etl'
    
    print("📁 Creating file ETL pipeline...")
    
    # Create project
    await bridge.init_project(project_name, '.')
    
    # Create diverse sample data
    await create_diverse_sample_data(project_name)
    
    # Add file extractors
    await bridge.add_plugin(project_name, 'extractor', 'tap-csv')
    await bridge.add_plugin(project_name, 'extractor', 'tap-spreadsheets-anywhere')
    
    # Add target
    await bridge.add_plugin(project_name, 'loader', 'target-csv')
    
    # Configure for multiple file types
    await configure_file_etl_plugins(project_name)
    
    # Run pipeline
    print("🏃 Running file ETL pipeline...")
    result = await bridge.run_pipeline(
        project_name,
        'tap-csv',
        'target-csv'
    )
    
    return json.loads(result)['success']

async def create_diverse_sample_data(project_name: str):
    """Create sample data in multiple formats."""
    
    data_dir = Path(project_name) / 'input_data'
    data_dir.mkdir(exist_ok=True)
    
    # Sample sales data
    sales_data = [
        {'date': '2023-01-01', 'product': 'Widget A', 'quantity': 100, 'revenue': 1000.00, 'region': 'North'},
        {'date': '2023-01-02', 'product': 'Widget B', 'quantity': 75, 'revenue': 1500.00, 'region': 'South'},
        {'date': '2023-01-03', 'product': 'Widget C', 'quantity': 150, 'revenue': 2250.00, 'region': 'East'},
        {'date': '2023-01-04', 'product': 'Widget A', 'quantity': 120, 'revenue': 1200.00, 'region': 'West'},
        {'date': '2023-01-05', 'product': 'Widget B', 'quantity': 90, 'revenue': 1800.00, 'region': 'North'},
    ]
    
    # Create CSV file
    csv_file = data_dir / 'sales.csv'
    with csv_file.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'product', 'quantity', 'revenue', 'region'])
        writer.writeheader()
        writer.writerows(sales_data)
    
    # Create Excel file using pandas
    excel_file = data_dir / 'sales_summary.xlsx'
    df = pd.DataFrame(sales_data)
    df.to_excel(excel_file, index=False, sheet_name='Sales')
    
    # Create TSV file
    tsv_file = data_dir / 'sales.tsv'
    with tsv_file.open('w') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'product', 'quantity', 'revenue', 'region'], 
                               delimiter='\t')
        writer.writeheader()
        writer.writerows(sales_data)
    
    print("✅ Created diverse sample data:")
    print(f"   - {csv_file} (CSV format)")
    print(f"   - {excel_file} (Excel format)")
    print(f"   - {tsv_file} (TSV format)")

async def configure_file_etl_plugins(project_name: str):
    """Configure file processing plugins."""
    
    from src.flext_meltano.project_manager import MeltanoProjectManager
    
    manager = MeltanoProjectManager('.')
    config_result = await manager.load_project_config(project_name)
    config = config_result.value
    
    # Configure tap-csv for multiple file types
    extractors = config.get('plugins', {}).get('extractors', [])
    for extractor in extractors:
        if extractor.get('name') == 'tap-csv':
            extractor['config'] = {
                'files': [
                    {
                        'path': 'input_data/sales.csv',
                        'name': 'sales_csv',
                        'keys': ['date', 'product'],
                        'encoding': 'utf-8'
                    },
                    {
                        'path': 'input_data/sales.tsv',
                        'name': 'sales_tsv',
                        'keys': ['date', 'product'],
                        'encoding': 'utf-8',
                        'delimiter': '\t'
                    }
                ]
            }
            break
    
    # Configure target-csv for consolidated output
    loaders = config.get('plugins', {}).get('loaders', [])
    for loader in loaders:
        if loader.get('name') == 'target-csv':
            loader['config'] = {
                'destination_path': f'{project_name}/output_data',
                'file_naming_scheme': '{stream_name}_{date}.csv',
                'delimiter': ',',
                'quotechar': '"'
            }
            break
    
    await manager.save_project_config(project_name, config)
    print("✅ File ETL configurations updated")
```

## 🔄 Orchestrated Multi-Step Pipeline

### Complex Pipeline with Multiple Stages

```python
# orchestrated_pipeline.py
import asyncio
import json
from src.flext_meltano.orchestrator import FlextMeltanoOrchestrator, OrchestrationMode, RunMode

async def create_orchestrated_pipeline():
    """Complex multi-step pipeline with orchestration."""
    
    # This example shows how to use the orchestrator directly
    # for complex multi-step pipelines
    
    print("🎼 Creating orchestrated multi-step pipeline...")
    
    # Pipeline definition with multiple stages
    pipeline_definition = {
        'name': 'customer_analytics_pipeline',
        'description': 'Complete customer analytics with multiple data sources',
        'blocks': [
            {
                'name': 'extract_customer_data',
                'block_type': 'meltano',
                'extractor': 'tap-postgres',
                'loader': 'target-snowflake',
                'description': 'Extract customer data from operational database'
            },
            {
                'name': 'extract_web_analytics',
                'block_type': 'meltano', 
                'extractor': 'tap-google-analytics',
                'loader': 'target-snowflake',
                'description': 'Extract web analytics data'
            },
            {
                'name': 'run_staging_transforms',
                'block_type': 'run',
                'commands': ['dbt', 'run', '--models', 'staging'],
                'description': 'Run staging transformations'
            },
            {
                'name': 'run_mart_transforms', 
                'block_type': 'run',
                'commands': ['dbt', 'run', '--models', 'marts'],
                'description': 'Run mart transformations'
            },
            {
                'name': 'test_data_quality',
                'block_type': 'run',
                'commands': ['dbt', 'test'],
                'description': 'Run data quality tests'
            },
            {
                'name': 'generate_reports',
                'block_type': 'invoke',
                'commands': ['python generate_reports.py'],
                'description': 'Generate business reports'
            }
        ]
    }
    
    # For this example, we'll simulate the orchestrator
    # In a real implementation, you would inject the required dependencies
    print("📋 Pipeline Definition:")
    for i, block in enumerate(pipeline_definition['blocks'], 1):
        print(f"   {i}. {block['name']}: {block['description']}")
    
    # Simulate pipeline execution
    print("\n🏃 Executing pipeline stages...")
    
    for i, block in enumerate(pipeline_definition['blocks'], 1):
        print(f"   Stage {i}: {block['name']} - ⏳ Running...")
        await asyncio.sleep(1)  # Simulate processing time
        print(f"   Stage {i}: {block['name']} - ✅ Completed")
    
    print("\n🎉 Orchestrated pipeline completed successfully!")
    return True

# Example of using the pipeline with error handling
async def robust_pipeline_execution():
    """Example with comprehensive error handling and monitoring."""
    
    print("🛡️ Creating robust pipeline with error handling...")
    
    pipeline_definition = {
        'name': 'robust_data_pipeline',
        'blocks': [
            {
                'name': 'data_validation',
                'block_type': 'run',
                'commands': ['python', 'validate_sources.py'],
                'retry_count': 3,
                'timeout': 300
            },
            {
                'name': 'extract_transform_load',
                'block_type': 'meltano',
                'extractor': 'tap-csv',
                'loader': 'target-postgres',
                'on_failure': 'continue'  # Continue even if this fails
            },
            {
                'name': 'data_quality_checks',
                'block_type': 'run',
                'commands': ['great_expectations', 'checkpoint', 'run'],
                'critical': True  # Pipeline fails if this fails
            },
            {
                'name': 'send_notification',
                'block_type': 'invoke',
                'commands': ['python', 'send_slack_notification.py', '--status', 'success'],
                'always_run': True  # Run regardless of previous failures
            }
        ]
    }
    
    # Simulate execution with error scenarios
    for block in pipeline_definition['blocks']:
        try:
            print(f"🔄 Executing: {block['name']}")
            
            # Simulate different outcomes
            if block['name'] == 'extract_transform_load':
                print("   ⚠️ Warning: Some records skipped due to data quality issues")
            elif block['name'] == 'data_quality_checks':
                print("   ✅ All data quality checks passed")
            
            await asyncio.sleep(0.5)  # Simulate processing
            print(f"   ✅ {block['name']} completed successfully")
            
        except Exception as e:
            if block.get('critical', False):
                print(f"   ❌ Critical failure in {block['name']}: {e}")
                break
            else:
                print(f"   ⚠️ Non-critical failure in {block['name']}: {e}")
                continue
    
    return True
```

## 📈 Real-Time Streaming Pipeline

### Streaming Data Processing Example

```python
# streaming_pipeline.py
import asyncio
import json
from datetime import datetime, UTC
from src.flext_meltano.integrations.bridge import MeltanoBridge

async def create_streaming_pipeline():
    """Real-time streaming data pipeline example."""
    
    bridge = MeltanoBridge('.')
    project_name = 'streaming_pipeline'
    
    print("📡 Creating streaming data pipeline...")
    
    # Create project
    await bridge.init_project(project_name, '.')
    
    # Add streaming extractors
    await bridge.add_plugin(project_name, 'extractor', 'tap-kafka')
    await bridge.add_plugin(project_name, 'loader', 'target-postgres')
    
    # Configure for streaming
    await configure_streaming_plugins(project_name)
    
    # Run streaming pipeline
    print("🌊 Starting streaming pipeline...")
    result = await bridge.run_pipeline(
        project_name,
        'tap-kafka',
        'target-postgres'
    )
    
    return json.loads(result)['success']

async def configure_streaming_plugins(project_name: str):
    """Configure streaming plugins."""
    
    from src.flext_meltano.project_manager import MeltanoProjectManager
    
    manager = MeltanoProjectManager('.')
    config_result = await manager.load_project_config(project_name)
    config = config_result.value
    
    # Configure tap-kafka
    extractors = config.get('plugins', {}).get('extractors', [])
    for extractor in extractors:
        if extractor.get('name') == 'tap-kafka':
            extractor['config'] = {
                'bootstrap_servers': 'localhost:9092',
                'group_id': 'flext_meltano_consumer',
                'topics': ['user_events', 'transaction_events', 'system_metrics'],
                'value_format': 'json',
                'auto_offset_reset': 'earliest',
                'batch_size': 1000,
                'batch_timeout_ms': 5000
            }
            break
    
    # Configure target for streaming
    loaders = config.get('plugins', {}).get('loaders', [])
    for loader in loaders:
        if loader.get('name') == 'target-postgres':
            loader['config'] = {
                'host': 'localhost',
                'port': 5432,
                'user': 'postgres',
                'password': 'password',
                'database': 'streaming_data',
                'default_target_schema': 'events',
                'batch_size': 1000,  # Optimize for streaming
                'flush_all_streams': True
            }
            break
    
    await manager.save_project_config(project_name, config)
    print("✅ Streaming configurations updated")

# Simulate real-time events
async def simulate_streaming_events():
    """Simulate real-time event generation."""
    
    import random
    
    events = []
    
    for i in range(100):
        event = {
            'timestamp': datetime.now(UTC).isoformat(),
            'user_id': random.randint(1000, 9999),
            'event_type': random.choice(['page_view', 'click', 'purchase', 'signup']),
            'value': random.uniform(1.0, 100.0),
            'metadata': {
                'source': 'web_app',
                'version': '1.0.0'
            }
        }
        events.append(event)
        
        # Simulate real-time generation
        await asyncio.sleep(0.1)
        
        if i % 10 == 0:
            print(f"📊 Generated {i+1} events...")
    
    print(f"✅ Generated {len(events)} streaming events")
    return events
```

## 🧪 Testing Pipeline Examples

### Pipeline Testing and Validation

```python
# test_pipelines.py
import asyncio
import json
import tempfile
from pathlib import Path
from src.flext_meltano.integrations.bridge import MeltanoBridge

async def test_pipeline_validation():
    """Test pipeline setup and validation."""
    
    print("🧪 Testing pipeline validation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Use temporary directory for testing
        bridge = MeltanoBridge(temp_dir)
        test_project = 'test_validation'
        
        # Test 1: Project creation
        print("  Test 1: Project creation...")
        result = await bridge.init_project(test_project, '.')
        data = json.loads(result)
        assert data['success'], f"Project creation failed: {data['error']}"
        print("  ✅ Project creation passed")
        
        # Test 2: Plugin addition
        print("  Test 2: Plugin addition...")
        result = await bridge.add_plugin(test_project, 'extractor', 'tap-csv')
        data = json.loads(result)
        assert data['success'], f"Plugin addition failed: {data['error']}"
        print("  ✅ Plugin addition passed")
        
        # Test 3: Project info retrieval
        print("  Test 3: Project info...")
        result = await bridge.get_project_info(test_project)
        data = json.loads(result)
        assert data['success'], f"Project info failed: {data['error']}"
        print("  ✅ Project info passed")
        
        # Test 4: Configuration validation
        print("  Test 4: Configuration validation...")
        config = data['data']['config']
        assert 'plugins' in config, "Plugins section missing"
        assert 'extractors' in config['plugins'], "Extractors section missing"
        print("  ✅ Configuration validation passed")
        
        print("🎉 All pipeline validation tests passed!")
        return True

async def benchmark_pipeline_performance():
    """Benchmark pipeline creation and execution performance."""
    
    import time
    
    print("⏱️ Benchmarking pipeline performance...")
    
    bridge = MeltanoBridge('.')
    project_name = 'benchmark_test'
    
    # Benchmark project creation
    start_time = time.time()
    await bridge.init_project(project_name, '.')
    creation_time = time.time() - start_time
    
    # Benchmark plugin addition
    start_time = time.time()
    await bridge.add_plugin(project_name, 'extractor', 'tap-csv')
    plugin_time = time.time() - start_time
    
    # Benchmark info retrieval
    start_time = time.time()
    await bridge.get_project_info(project_name)
    info_time = time.time() - start_time
    
    print(f"📊 Performance Results:")
    print(f"   Project Creation: {creation_time:.3f}s")
    print(f"   Plugin Addition: {plugin_time:.3f}s")
    print(f"   Info Retrieval: {info_time:.3f}s")
    
    # Performance assertions
    assert creation_time < 10.0, f"Project creation too slow: {creation_time}s"
    assert plugin_time < 60.0, f"Plugin addition too slow: {plugin_time}s"
    assert info_time < 1.0, f"Info retrieval too slow: {info_time}s"
    
    print("✅ Performance benchmarks passed!")
    return True

# Run all examples
async def run_all_examples():
    """Run all pipeline examples."""
    
    examples = [
        ("CSV to PostgreSQL", create_csv_to_postgres_pipeline),
        ("API to PostgreSQL", create_api_to_postgres_pipeline),
        ("File ETL", create_file_etl_pipeline),
        ("Orchestrated Pipeline", create_orchestrated_pipeline),
        ("Robust Pipeline", robust_pipeline_execution),
        ("Streaming Pipeline", create_streaming_pipeline),
        ("Pipeline Validation", test_pipeline_validation),
        ("Performance Benchmark", benchmark_pipeline_performance)
    ]
    
    results = {}
    
    for name, example_func in examples:
        print(f"\n{'='*60}")
        print(f"Running: {name}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            success = await example_func()
            duration = time.time() - start_time
            results[name] = {'success': success, 'duration': duration}
            print(f"✅ {name} completed in {duration:.2f}s")
        except Exception as e:
            results[name] = {'success': False, 'error': str(e)}
            print(f"❌ {name} failed: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("EXECUTION SUMMARY")
    print(f"{'='*60}")
    
    for name, result in results.items():
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        duration = f"({result.get('duration', 0):.2f}s)" if 'duration' in result else ""
        print(f"{status} {name} {duration}")
    
    total_success = sum(1 for r in results.values() if r['success'])
    print(f"\nTotal: {total_success}/{len(examples)} examples successful")
    
    return total_success == len(examples)

if __name__ == "__main__":
    import time
    overall_success = asyncio.run(run_all_examples())
    print(f"\n🎯 Overall Result: {'SUCCESS' if overall_success else 'FAILED'}")
```

---

These basic pipeline examples demonstrate the full range of FLEXT-Meltano capabilities, from simple CSV processing to complex orchestrated workflows. Each example includes complete code, configuration, and error handling patterns that can be adapted for production use.

**Next**: Continue with [Oracle Integration Examples](./oracle-integration.md) for enterprise data integration patterns.