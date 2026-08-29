# Triagem SonarCloud — flext-sh/flext-meltano

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `mro-2wjm.11`

## Resumo

**51 issues** — BLOCKER 0, CRITICAL 11, MAJOR 4, MINOR 36
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 47 · **Debt total: 171min**

| regra | issues |
|---|---|
| `python:S116` | 35 |
| `python:S1192` | 4 |
| `python:S3776` | 4 |
| `python:S5754` | 2 |
| `githubactions:S8233` | 2 |
| `python:S5727` | 1 |
| `githubactions:S8264` | 1 |
| `text:S8565` | 1 |
| `python:S7504` | 1 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_meltano/pipeline_mgr.py:102` · **Effort**: 6min

> Define a constant instead of duplicating this literal "pipeline configuration JSON" 3 times.

```python
       98                  "values": config_result.value
       99              })
      100          except ValueError as exc:
      101              return e.fail_validation(
>>>   102                  "pipeline configuration JSON", error=exc, result_type=r[t.JsonMapping]
      103              )
      104          return r[t.JsonMapping].ok(config_mapping.values)
      105  
      106      def _pipeline_command(
```

**Decisão**: pendente

### 2 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_meltano/pipeline_mgr.py:112` · **Effort**: 6min

> Define a constant instead of duplicating this literal "Pipeline execution not configured" 3 times.

```python
      108      ) -> p.Result[t.StrSequence]:
      109          config_result = self._load_pipeline_config(pipeline_name)
      110          if config_result.failure:
      111              return r[t.StrSequence].fail(
>>>   112                  config_result.error or "Pipeline execution not configured"
      113              )
      114          command_value = config_result.value.get("command")
      115          if not isinstance(command_value, t.SEQUENCE_PAIR_TYPES):
      116              return r[t.StrSequence].fail("Pipeline execution not configured")
```

**Decisão**: pendente

### 3 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_meltano/pipeline_mgr.py:149` · **Effort**: 10min

> Define a constant instead of duplicating this literal "Pipeline name is invalid" 5 times.

```python
      145      ) -> p.Result[str]:
      146          """Create and persist a named pipeline configuration."""
      147          name_result = self._normalize_pipeline_name(pipeline_name)
      148          if name_result.failure:
>>>   149              return r[str].fail(name_result.error or "Pipeline name is invalid")
      150          if config_payload is None:
      151              return r[str].fail("Pipeline creation not configured")
      152          try:
      153              config_mapping = m.Meltano.ConfigMappingPayload.model_validate({
```

**Decisão**: pendente

### 4 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/consumer_bases/dbt_service_base.py:74` · **Effort**: 7min

> Refactor this function to reduce its Cognitive Complexity from 17 to the 15 allowed.

```python
       70      # ------------------------------------------------------------------
       71      # CLI dispatch
       72      # ------------------------------------------------------------------
       73  
>>>    74      def cli_main(self, args: t.StrSequence | None = None) -> int:
       75          """Run the main CLI entry point for dbt project."""
       76  
       77          def _run_cli_main() -> int:
       78              command_args = list(args) if args else sys.argv[1:]
```

**Decisão**: pendente

### 5 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_meltano/services/dbt_project.py:49` · **Effort**: 6min

> Define a constant instead of duplicating this literal "Unknown error" 3 times.

```python
       45              c.Meltano.DbtResourceType.MODEL
       46          )
       47          if model_nodes_result.failure:
       48              return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
>>>    49                  model_nodes_result.error or "Unknown error"
       50              )
       51          try:
       52              models = [
       53                  self._build_manifest_node_summary(node)
```

**Decisão**: pendente

### 6 · 🟠 CRITICAL · CODE_SMELL · `python:S5754`
**Local**: `src/flext_meltano/services/declarative_tap.py:47` · **Effort**: 5min

> Reraise this exception to stop the application as the user expects

```python
       43              try:
       44                  _ = command.main(
       45                      args=list(args), prog_name=prog_name, standalone_mode=False
       46                  )
>>>    47              except SystemExit as exc:
       48                  return exc.code if isinstance(exc.code, int) else 1
       49              return 0
       50  
       51          def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
```

**Decisão**: pendente

### 7 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/executor_base.py:203` · **Effort**: 6min

> Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.

```python
      199          }
      200          self.logger.info("FlextMeltanoExecutor executed successfully")
      201          return r[t.JsonMapping].ok(config_data)
      202  
>>>   203      def execute_meltano_command(
      204          self,
      205          command: t.StrSequence,
      206          timeout: int = c.Meltano.NETWORK_MELTANO_DEFAULT_TIMEOUT,
      207          _cwd: Path | None = None,
```

**Decisão**: pendente

### 8 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/executor_base.py:321` · **Effort**: 6min

> Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.

```python
      317              )
      318          except c.Meltano.OPERATION_ERRORS as e:
      319              return r[m.Meltano.CommandExecutionResult].fail(str(e))
      320  
>>>   321      def execute_pipeline(
      322          self, tap_name: str, target_name: str, config: t.JsonMapping | None = None
      323      ) -> p.Result[m.Meltano.CommandExecutionResult]:
      324          """Execute a complete ELT pipeline."""
      325          prepared_command: t.StrSequence | None = None
```

**Decisão**: pendente

### 9 · 🟠 CRITICAL · CODE_SMELL · `python:S5727`
**Local**: `src/flext_meltano/services/executor_base.py:398` · **Effort**: 10min

> Remove this identity check; it will always be True.

```python
      394                  failed_stage.error
      395                  if failed_stage is not None and failed_stage.error is not None
      396                  else "Failed to run Meltano pipeline"
      397              )
>>>   398          if completed_result is None:
      399              return r[m.Meltano.CommandExecutionResult].fail(
      400                  "Pipeline execution result missing"
      401              )
      402          return r[m.Meltano.CommandExecutionResult].ok(completed_result)
```

**Decisão**: pendente

### 10 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/meltano_plugin_discovery.py:73` · **Effort**: 9min

> Refactor this function to reduce its Cognitive Complexity from 19 to the 15 allowed.

```python
       69              error_msg = f"Failed to discover plugins: {e}"
       70              self.logger.exception(error_msg, error=str(e))
       71              return r[t.SequenceOf[t.StrMapping]].fail(error_msg)
       72  
>>>    73      def _discover_plugins(
       74          self, project: t.JsonPayload | t.Meltano.DbtProject | None
       75      ) -> p.Result[t.SequenceOf[t.StrMapping]]:
       76          """Discover plugins without owning the exception boundary."""
       77          self.logger.info("Discovering Meltano plugins")
```

**Decisão**: pendente

### 11 · 🟠 CRITICAL · CODE_SMELL · `python:S5754`
**Local**: `src/flext_meltano/services/singer_sdk.py:70` · **Effort**: 5min

> Reraise this exception to stop the application as the user expects

```python
       66          try:
       67              singer_command = self._tap.get_singer_command()
       68              _ = singer_command.main(args=list(args), prog_name=prog_name)
       69              return 0
>>>    70          except SystemExit as exc:
       71              return exc.code if isinstance(exc.code, int) else 1
       72  
       73      def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
       74          """Delegate stream discovery to the raw Singer tap."""
```

**Decisão**: pendente

### 12 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8264`
**Local**: `.github/workflows/docs.yml:18` · **Effort**: 5min

> Move this read permission from workflow level to job level.

```yaml
       14        - ".github/workflows/docs.yml"
       15    workflow_dispatch:
       16  
       17  permissions:
>>>    18    contents: read
       19    pages: write
       20    id-token: write
       21  
       22  concurrency:
```

**Decisão**: pendente

### 13 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:19` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       15    workflow_dispatch:
       16  
       17  permissions:
       18    contents: read
>>>    19    pages: write
       20    id-token: write
       21  
       22  concurrency:
       23    group: pages
```

**Decisão**: pendente

### 14 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:20` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       16  
       17  permissions:
       18    contents: read
       19    pages: write
>>>    20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: pendente

### 15 · 🟡 MAJOR · VULNERABILITY · `text:S8565`
**Local**: `pyproject.toml:-` · **Effort**: 5min

> Dependency versions are not predictable if the lock file (uv.lock, poetry.lock, pdm.lock or pylock.toml) is missing.

**Decisão**: pendente

### 16 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
       16      if (
       17          existing_package is None
       18          or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
       19      ):
>>>    20          for module_name in list(sys.modules):
       21              if module_name == package_name or module_name.startswith(
       22                  f"{package_name}."
       23              ):
       24                  sys.modules.pop(module_name, None)
```

**Decisão**: pendente

### 17 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:31` · **Effort**: 2min

> Rename this field "SingerTapBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       27      the canonical m.Meltano.Singer* namespace. Consumers subclass these
       28      instead of importing singer_sdk directly.
       29      """
       30  
>>>    31      SingerTapBase = Tap
       32      SingerSinkBase = Sink
       33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
       35      SingerContext = Context
```

**Decisão**: pendente

### 18 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:32` · **Effort**: 2min

> Rename this field "SingerSinkBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       28      instead of importing singer_sdk directly.
       29      """
       30  
       31      SingerTapBase = Tap
>>>    32      SingerSinkBase = Sink
       33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
       35      SingerContext = Context
       36      SingerRecord = Record
```

**Decisão**: pendente

### 19 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:33` · **Effort**: 2min

> Rename this field "SingerStreamBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       29      """
       30  
       31      SingerTapBase = Tap
       32      SingerSinkBase = Sink
>>>    33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
       35      SingerContext = Context
       36      SingerRecord = Record
       37      SingerArrayType = singer_sdk_typing.ArrayType
```

**Decisão**: pendente

### 20 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:34` · **Effort**: 2min

> Rename this field "SingerTargetBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       30  
       31      SingerTapBase = Tap
       32      SingerSinkBase = Sink
       33      SingerStreamBase = Stream
>>>    34      SingerTargetBase = Target
       35      SingerContext = Context
       36      SingerRecord = Record
       37      SingerArrayType = singer_sdk_typing.ArrayType
       38      SingerBooleanType = singer_sdk_typing.BooleanType
```

**Decisão**: pendente

### 21 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:35` · **Effort**: 2min

> Rename this field "SingerContext" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       31      SingerTapBase = Tap
       32      SingerSinkBase = Sink
       33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
>>>    35      SingerContext = Context
       36      SingerRecord = Record
       37      SingerArrayType = singer_sdk_typing.ArrayType
       38      SingerBooleanType = singer_sdk_typing.BooleanType
       39      SingerCustomType = singer_sdk_typing.CustomType
```

**Decisão**: pendente

### 22 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:36` · **Effort**: 2min

> Rename this field "SingerRecord" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       32      SingerSinkBase = Sink
       33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
       35      SingerContext = Context
>>>    36      SingerRecord = Record
       37      SingerArrayType = singer_sdk_typing.ArrayType
       38      SingerBooleanType = singer_sdk_typing.BooleanType
       39      SingerCustomType = singer_sdk_typing.CustomType
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
```

**Decisão**: pendente

### 23 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:37` · **Effort**: 2min

> Rename this field "SingerArrayType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
       35      SingerContext = Context
       36      SingerRecord = Record
>>>    37      SingerArrayType = singer_sdk_typing.ArrayType
       38      SingerBooleanType = singer_sdk_typing.BooleanType
       39      SingerCustomType = singer_sdk_typing.CustomType
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
       41      SingerDateType = singer_sdk_typing.DateType
```

**Decisão**: pendente

### 24 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:38` · **Effort**: 2min

> Rename this field "SingerBooleanType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       34      SingerTargetBase = Target
       35      SingerContext = Context
       36      SingerRecord = Record
       37      SingerArrayType = singer_sdk_typing.ArrayType
>>>    38      SingerBooleanType = singer_sdk_typing.BooleanType
       39      SingerCustomType = singer_sdk_typing.CustomType
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
       41      SingerDateType = singer_sdk_typing.DateType
       42      SingerDurationType = singer_sdk_typing.DurationType
```

**Decisão**: pendente

### 25 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:39` · **Effort**: 2min

> Rename this field "SingerCustomType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       35      SingerContext = Context
       36      SingerRecord = Record
       37      SingerArrayType = singer_sdk_typing.ArrayType
       38      SingerBooleanType = singer_sdk_typing.BooleanType
>>>    39      SingerCustomType = singer_sdk_typing.CustomType
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
       41      SingerDateType = singer_sdk_typing.DateType
       42      SingerDurationType = singer_sdk_typing.DurationType
       43      SingerIntegerType = singer_sdk_typing.IntegerType
```

**Decisão**: pendente

### 26 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:40` · **Effort**: 2min

> Rename this field "SingerDateTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       36      SingerRecord = Record
       37      SingerArrayType = singer_sdk_typing.ArrayType
       38      SingerBooleanType = singer_sdk_typing.BooleanType
       39      SingerCustomType = singer_sdk_typing.CustomType
>>>    40      SingerDateTimeType = singer_sdk_typing.DateTimeType
       41      SingerDateType = singer_sdk_typing.DateType
       42      SingerDurationType = singer_sdk_typing.DurationType
       43      SingerIntegerType = singer_sdk_typing.IntegerType
       44      SingerNumberType = singer_sdk_typing.NumberType
```

**Decisão**: pendente

### 27 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:41` · **Effort**: 2min

> Rename this field "SingerDateType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       37      SingerArrayType = singer_sdk_typing.ArrayType
       38      SingerBooleanType = singer_sdk_typing.BooleanType
       39      SingerCustomType = singer_sdk_typing.CustomType
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
>>>    41      SingerDateType = singer_sdk_typing.DateType
       42      SingerDurationType = singer_sdk_typing.DurationType
       43      SingerIntegerType = singer_sdk_typing.IntegerType
       44      SingerNumberType = singer_sdk_typing.NumberType
       45      SingerObjectType = singer_sdk_typing.ObjectType
```

**Decisão**: pendente

### 28 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:42` · **Effort**: 2min

> Rename this field "SingerDurationType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       38      SingerBooleanType = singer_sdk_typing.BooleanType
       39      SingerCustomType = singer_sdk_typing.CustomType
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
       41      SingerDateType = singer_sdk_typing.DateType
>>>    42      SingerDurationType = singer_sdk_typing.DurationType
       43      SingerIntegerType = singer_sdk_typing.IntegerType
       44      SingerNumberType = singer_sdk_typing.NumberType
       45      SingerObjectType = singer_sdk_typing.ObjectType
       46      SingerPropertiesList = singer_sdk_typing.PropertiesList
```

**Decisão**: pendente

### 29 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:43` · **Effort**: 2min

> Rename this field "SingerIntegerType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       39      SingerCustomType = singer_sdk_typing.CustomType
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
       41      SingerDateType = singer_sdk_typing.DateType
       42      SingerDurationType = singer_sdk_typing.DurationType
>>>    43      SingerIntegerType = singer_sdk_typing.IntegerType
       44      SingerNumberType = singer_sdk_typing.NumberType
       45      SingerObjectType = singer_sdk_typing.ObjectType
       46      SingerPropertiesList = singer_sdk_typing.PropertiesList
       47      SingerProperty = singer_sdk_typing.Property
```

**Decisão**: pendente

### 30 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:44` · **Effort**: 2min

> Rename this field "SingerNumberType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       40      SingerDateTimeType = singer_sdk_typing.DateTimeType
       41      SingerDateType = singer_sdk_typing.DateType
       42      SingerDurationType = singer_sdk_typing.DurationType
       43      SingerIntegerType = singer_sdk_typing.IntegerType
>>>    44      SingerNumberType = singer_sdk_typing.NumberType
       45      SingerObjectType = singer_sdk_typing.ObjectType
       46      SingerPropertiesList = singer_sdk_typing.PropertiesList
       47      SingerProperty = singer_sdk_typing.Property
       48      SingerStringType = singer_sdk_typing.StringType
```

**Decisão**: pendente

### 31 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:45` · **Effort**: 2min

> Rename this field "SingerObjectType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       41      SingerDateType = singer_sdk_typing.DateType
       42      SingerDurationType = singer_sdk_typing.DurationType
       43      SingerIntegerType = singer_sdk_typing.IntegerType
       44      SingerNumberType = singer_sdk_typing.NumberType
>>>    45      SingerObjectType = singer_sdk_typing.ObjectType
       46      SingerPropertiesList = singer_sdk_typing.PropertiesList
       47      SingerProperty = singer_sdk_typing.Property
       48      SingerStringType = singer_sdk_typing.StringType
       49      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 32 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:46` · **Effort**: 2min

> Rename this field "SingerPropertiesList" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       42      SingerDurationType = singer_sdk_typing.DurationType
       43      SingerIntegerType = singer_sdk_typing.IntegerType
       44      SingerNumberType = singer_sdk_typing.NumberType
       45      SingerObjectType = singer_sdk_typing.ObjectType
>>>    46      SingerPropertiesList = singer_sdk_typing.PropertiesList
       47      SingerProperty = singer_sdk_typing.Property
       48      SingerStringType = singer_sdk_typing.StringType
       49      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 33 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:47` · **Effort**: 2min

> Rename this field "SingerProperty" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       43      SingerIntegerType = singer_sdk_typing.IntegerType
       44      SingerNumberType = singer_sdk_typing.NumberType
       45      SingerObjectType = singer_sdk_typing.ObjectType
       46      SingerPropertiesList = singer_sdk_typing.PropertiesList
>>>    47      SingerProperty = singer_sdk_typing.Property
       48      SingerStringType = singer_sdk_typing.StringType
       49      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 34 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:48` · **Effort**: 2min

> Rename this field "SingerStringType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       44      SingerNumberType = singer_sdk_typing.NumberType
       45      SingerObjectType = singer_sdk_typing.ObjectType
       46      SingerPropertiesList = singer_sdk_typing.PropertiesList
       47      SingerProperty = singer_sdk_typing.Property
>>>    48      SingerStringType = singer_sdk_typing.StringType
       49      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 35 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:49` · **Effort**: 2min

> Rename this field "SingerTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       45      SingerObjectType = singer_sdk_typing.ObjectType
       46      SingerPropertiesList = singer_sdk_typing.PropertiesList
       47      SingerProperty = singer_sdk_typing.Property
       48      SingerStringType = singer_sdk_typing.StringType
>>>    49      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 36 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/sources.py:17` · **Effort**: 2min

> Rename this field "StreamDefinition" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       13  
       14  class FlextMeltanoModelsSources:
       15      """Source and configuration models."""
       16  
>>>    17      StreamDefinition: ClassVar[
       18          type[FlextMeltanoModelsSourcesParams.StreamDefinition]
       19      ] = FlextMeltanoModelsSourcesParams.StreamDefinition
       20  
       21      class TapConfig(m.Entity):
```

**Decisão**: pendente

### 37 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_protocols/singer.py:210` · **Effort**: 2min

> Rename this field "SingerTapSdkBackend" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
      206          def sync_all(self) -> None:
      207              """Execute sync for all selected streams."""
      208              ...
      209  
>>>   210      SingerTapSdkBackend = SingerTapBackend
      211      SingerTapSettingsBackend = SingerTapBackend
      212  
      213      @runtime_checkable
      214      class SingerDrainSink(Protocol):
```

**Decisão**: pendente

### 38 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_protocols/singer.py:211` · **Effort**: 2min

> Rename this field "SingerTapSettingsBackend" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
      207              """Execute sync for all selected streams."""
      208              ...
      209  
      210      SingerTapSdkBackend = SingerTapBackend
>>>   211      SingerTapSettingsBackend = SingerTapBackend
      212  
      213      @runtime_checkable
      214      class SingerDrainSink(Protocol):
      215          """Typed sink contract for target service drain and record operations.
```

**Decisão**: pendente

### 39 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/base.py:32` · **Effort**: 2min

> Rename this field "PluginType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       28      )
       29  
       30      type ValidatorInput = t.JsonValue
       31  
>>>    32      PluginType = c.Meltano.PluginType
       33  
       34      type VariantValue = str | t.StrSequence | t.ScalarMapping | None
       35      """Normalized plugin variant: string, string list, scalar mapping, or null."""
       36  
```

**Decisão**: pendente

### 40 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:23` · **Effort**: 2min

> Rename this field "SingerReplicationMethod" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       19      External library wrappers (singer_sdk.typing) are kept to prevent
       20      direct imports by consumer projects.
       21      """
       22  
>>>    23      SingerReplicationMethod = c.Meltano.SingerReplicationMethod
       24  
       25      # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
       26      SingerArrayType = singer_sdk_typing.ArrayType
       27      SingerBooleanType = singer_sdk_typing.BooleanType
```

**Decisão**: pendente

### 41 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:26` · **Effort**: 2min

> Rename this field "SingerArrayType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       22  
       23      SingerReplicationMethod = c.Meltano.SingerReplicationMethod
       24  
       25      # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
>>>    26      SingerArrayType = singer_sdk_typing.ArrayType
       27      SingerBooleanType = singer_sdk_typing.BooleanType
       28      SingerCustomType = singer_sdk_typing.CustomType
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
```

**Decisão**: pendente

### 42 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:27` · **Effort**: 2min

> Rename this field "SingerBooleanType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       23      SingerReplicationMethod = c.Meltano.SingerReplicationMethod
       24  
       25      # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
       26      SingerArrayType = singer_sdk_typing.ArrayType
>>>    27      SingerBooleanType = singer_sdk_typing.BooleanType
       28      SingerCustomType = singer_sdk_typing.CustomType
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
       31      SingerDurationType = singer_sdk_typing.DurationType
```

**Decisão**: pendente

### 43 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:28` · **Effort**: 2min

> Rename this field "SingerCustomType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       24  
       25      # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
       26      SingerArrayType = singer_sdk_typing.ArrayType
       27      SingerBooleanType = singer_sdk_typing.BooleanType
>>>    28      SingerCustomType = singer_sdk_typing.CustomType
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
       31      SingerDurationType = singer_sdk_typing.DurationType
       32      SingerIntegerType = singer_sdk_typing.IntegerType
```

**Decisão**: pendente

### 44 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:29` · **Effort**: 2min

> Rename this field "SingerDateTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       25      # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
       26      SingerArrayType = singer_sdk_typing.ArrayType
       27      SingerBooleanType = singer_sdk_typing.BooleanType
       28      SingerCustomType = singer_sdk_typing.CustomType
>>>    29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
       31      SingerDurationType = singer_sdk_typing.DurationType
       32      SingerIntegerType = singer_sdk_typing.IntegerType
       33      SingerNumberType = singer_sdk_typing.NumberType
```

**Decisão**: pendente

### 45 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:30` · **Effort**: 2min

> Rename this field "SingerDateType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       26      SingerArrayType = singer_sdk_typing.ArrayType
       27      SingerBooleanType = singer_sdk_typing.BooleanType
       28      SingerCustomType = singer_sdk_typing.CustomType
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
>>>    30      SingerDateType = singer_sdk_typing.DateType
       31      SingerDurationType = singer_sdk_typing.DurationType
       32      SingerIntegerType = singer_sdk_typing.IntegerType
       33      SingerNumberType = singer_sdk_typing.NumberType
       34      SingerObjectType = singer_sdk_typing.ObjectType
```

**Decisão**: pendente

### 46 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:31` · **Effort**: 2min

> Rename this field "SingerDurationType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       27      SingerBooleanType = singer_sdk_typing.BooleanType
       28      SingerCustomType = singer_sdk_typing.CustomType
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
>>>    31      SingerDurationType = singer_sdk_typing.DurationType
       32      SingerIntegerType = singer_sdk_typing.IntegerType
       33      SingerNumberType = singer_sdk_typing.NumberType
       34      SingerObjectType = singer_sdk_typing.ObjectType
       35      SingerPropertiesList = singer_sdk_typing.PropertiesList
```

**Decisão**: pendente

### 47 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:32` · **Effort**: 2min

> Rename this field "SingerIntegerType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       28      SingerCustomType = singer_sdk_typing.CustomType
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
       31      SingerDurationType = singer_sdk_typing.DurationType
>>>    32      SingerIntegerType = singer_sdk_typing.IntegerType
       33      SingerNumberType = singer_sdk_typing.NumberType
       34      SingerObjectType = singer_sdk_typing.ObjectType
       35      SingerPropertiesList = singer_sdk_typing.PropertiesList
       36      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 48 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:33` · **Effort**: 2min

> Rename this field "SingerNumberType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
       31      SingerDurationType = singer_sdk_typing.DurationType
       32      SingerIntegerType = singer_sdk_typing.IntegerType
>>>    33      SingerNumberType = singer_sdk_typing.NumberType
       34      SingerObjectType = singer_sdk_typing.ObjectType
       35      SingerPropertiesList = singer_sdk_typing.PropertiesList
       36      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 49 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:34` · **Effort**: 2min

> Rename this field "SingerObjectType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       30      SingerDateType = singer_sdk_typing.DateType
       31      SingerDurationType = singer_sdk_typing.DurationType
       32      SingerIntegerType = singer_sdk_typing.IntegerType
       33      SingerNumberType = singer_sdk_typing.NumberType
>>>    34      SingerObjectType = singer_sdk_typing.ObjectType
       35      SingerPropertiesList = singer_sdk_typing.PropertiesList
       36      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 50 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:35` · **Effort**: 2min

> Rename this field "SingerPropertiesList" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       31      SingerDurationType = singer_sdk_typing.DurationType
       32      SingerIntegerType = singer_sdk_typing.IntegerType
       33      SingerNumberType = singer_sdk_typing.NumberType
       34      SingerObjectType = singer_sdk_typing.ObjectType
>>>    35      SingerPropertiesList = singer_sdk_typing.PropertiesList
       36      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 51 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:36` · **Effort**: 2min

> Rename this field "SingerTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       32      SingerIntegerType = singer_sdk_typing.IntegerType
       33      SingerNumberType = singer_sdk_typing.NumberType
       34      SingerObjectType = singer_sdk_typing.ObjectType
       35      SingerPropertiesList = singer_sdk_typing.PropertiesList
>>>    36      SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente
