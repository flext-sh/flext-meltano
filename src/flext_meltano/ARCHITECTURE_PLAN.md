# FLEXT-MELTANO ARCHITECTURE PLAN

## FUNÇÃO 1: WRAPPERS (Adaptação para flext-core)

### singer.py - DEVE TER:
```python
class MeltanoSingerWrapper:
    """Wrapper principal para Singer SDK → flext-core"""
    def create_tap(self, tap_config: dict) -> FlextResult[Tap]
    def create_target(self, target_config: dict) -> FlextResult[Target]
    def run_pipeline(self, tap: Tap, target: Target) -> FlextResult[dict]

class FlextSingerAdapter:
    """Adaptador de padrões Singer → FLEXT"""
    def adapt_catalog(self, singer_catalog: dict) -> FlextResult[FlextCatalog]
    def adapt_schema(self, singer_schema: dict) -> FlextResult[FlextSchema]
```

### dbt.py - DEVE TER:
```python
class MeltanoDbtWrapper:
    """Wrapper principal para DBT Core → flext-core"""
    def create_project(self, project_config: dict) -> FlextResult[DbtProject]
    def run_models(self, models: list[str]) -> FlextResult[dict]
    def test_models(self, models: list[str]) -> FlextResult[dict]

class FlextDbtAdapter:
    """Adaptador de padrões DBT → FLEXT"""
    def adapt_results(self, dbt_results: dict) -> FlextResult[FlextResults]
```

### bridge.py - DEVE TER:
```python
class MeltanoBridge:
    """Bridge principal para Meltano Core → flext-core"""
    def initialize_project(self, config: dict) -> FlextResult[MeltanoProject]
    def discover_plugins(self) -> FlextResult[list[Plugin]]
    def install_plugin(self, plugin_type: str, plugin_name: str) -> FlextResult[bool]
```

## FUNÇÃO 2: RUNTIME (Go bridge execution)

### execution.py - DEVE TER:
```python
class FlextMeltanoExecutor:
    """Executor principal para runtime via subprocess"""
    def execute_command(self, command: list[str]) -> FlextResult[dict]
    def run_pipeline_async(self, pipeline_config: dict) -> FlextResult[str]  # job_id
    def get_execution_status(self, job_id: str) -> FlextResult[dict]
```

### adapter.py - DEVE TER:
```python
class FlextMeltanoBridge:
    """Bridge para comunicação Go ↔ Python"""
    def get_version(self) -> FlextResult[dict]
    def list_plugins(self) -> FlextResult[list[dict]]
    def run_pipeline(self, tap_name: str, target_name: str) -> FlextResult[dict]
    def invoke_dbt(self, command: str, *args: str) -> FlextResult[dict]
```

### cli.py - DEVE TER:
```python
class FlextMeltanoCli:
    """Interface CLI para operações diretas"""
    def run_command(self, args: list[str]) -> FlextResult[dict]
    def get_help(self) -> str
```

## FUNÇÃO 3: BASE COMPONENTS (Para projetos flext-*)

### base.py - DEVE TER:
```python
class FlextMeltanoTapService(FlextMeltanoBaseService):
    """Base service para taps Singer"""
    def discover_streams(self) -> FlextResult[list[Stream]]
    def sync_stream(self, stream: Stream) -> FlextResult[Iterator[Record]]

class FlextMeltanoTargetService(FlextMeltanoBaseService):
    """Base service para targets Singer"""
    def write_record(self, stream: str, record: dict) -> FlextResult[bool]
    def write_batch(self, stream: str, records: list[dict]) -> FlextResult[bool]

class FlextMeltanoDbtService(FlextMeltanoBaseService):
    """Base service para projetos DBT"""
    def run_models(self, models: list[str]) -> FlextResult[dict]
    def test_models(self, models: list[str]) -> FlextResult[dict]
```

### plugins.py - DEVE TER:
```python
class FlextTapPlugin(FlextPlugin):
    """Plugin base para taps nos projetos flext-tap-*"""
    def discover(self) -> FlextResult[Catalog]
    def sync(self, catalog: Catalog) -> FlextResult[Iterator[Message]]

class FlextTargetPlugin(FlextPlugin):
    """Plugin base para targets nos projetos flext-target-*"""
    def process_messages(self, messages: Iterator[Message]) -> FlextResult[dict]
```

## INTERFACES PÚBLICAS OBRIGATÓRIAS

### Para projetos flext-tap-*:
```python
from flext_meltano import FlextTapPlugin, MeltanoSingerWrapper
```

### Para projetos flext-target-*:
```python
from flext_meltano import FlextTargetPlugin, MeltanoSingerWrapper
```

### Para projetos flext-dbt-*:
```python
from flext_meltano import FlextMeltanoDbtService, MeltanoDbtWrapper
```

### Para Go services:
```python
from flext_meltano import FlextMeltanoBridge, FlextMeltanoExecutor
```