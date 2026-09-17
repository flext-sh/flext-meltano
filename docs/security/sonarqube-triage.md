# Triagem SonarCloud — flext-sh/flext-meltano

<!-- TOC START -->
- [Resumo](#resumo)
- [Como usar](#como-usar)
- [Issues](#issues)
  - [1 · 🟠 CRITICAL · CODE_SMELL · python:S1192](#1-critical-code_smell-pythons1192)
  - [2 · 🟠 CRITICAL · CODE_SMELL · python:S1192](#2-critical-code_smell-pythons1192)
  - [3 · 🟠 CRITICAL · CODE_SMELL · python:S1192](#3-critical-code_smell-pythons1192)
  - [4 · 🟠 CRITICAL · CODE_SMELL · python:S3776](#4-critical-code_smell-pythons3776)
  - [5 · 🟠 CRITICAL · CODE_SMELL · python:S1192](#5-critical-code_smell-pythons1192)
  - [6 · 🟠 CRITICAL · CODE_SMELL · python:S5754](#6-critical-code_smell-pythons5754)
  - [7 · 🟠 CRITICAL · CODE_SMELL · python:S3776](#7-critical-code_smell-pythons3776)
  - [8 · 🟠 CRITICAL · CODE_SMELL · python:S3776](#8-critical-code_smell-pythons3776)
  - [9 · 🟠 CRITICAL · CODE_SMELL · python:S5727](#9-critical-code_smell-pythons5727)
  - [10 · 🟠 CRITICAL · CODE_SMELL · python:S3776](#10-critical-code_smell-pythons3776)
  - [11 · 🟠 CRITICAL · CODE_SMELL · python:S5754](#11-critical-code_smell-pythons5754)
  - [12 · 🟡 MAJOR · VULNERABILITY · githubactions:S8264](#12-major-vulnerability-githubactionss8264)
  - [13 · 🟡 MAJOR · VULNERABILITY · githubactions:S8233](#13-major-vulnerability-githubactionss8233)
  - [14 · 🟡 MAJOR · VULNERABILITY · githubactions:S8233](#14-major-vulnerability-githubactionss8233)
  - [15 · 🟡 MAJOR · VULNERABILITY · text:S8565](#15-major-vulnerability-texts8565)
  - [16 · ⚪ MINOR · CODE_SMELL · python:S7504](#16-minor-code_smell-pythons7504)
  - [17 · ⚪ MINOR · CODE_SMELL · python:S116](#17-minor-code_smell-pythons116)
  - [18 · ⚪ MINOR · CODE_SMELL · python:S116](#18-minor-code_smell-pythons116)
  - [19 · ⚪ MINOR · CODE_SMELL · python:S116](#19-minor-code_smell-pythons116)
  - [20 · ⚪ MINOR · CODE_SMELL · python:S116](#20-minor-code_smell-pythons116)
  - [21 · ⚪ MINOR · CODE_SMELL · python:S116](#21-minor-code_smell-pythons116)
  - [22 · ⚪ MINOR · CODE_SMELL · python:S116](#22-minor-code_smell-pythons116)
  - [23 · ⚪ MINOR · CODE_SMELL · python:S116](#23-minor-code_smell-pythons116)
  - [24 · ⚪ MINOR · CODE_SMELL · python:S116](#24-minor-code_smell-pythons116)
  - [25 · ⚪ MINOR · CODE_SMELL · python:S116](#25-minor-code_smell-pythons116)
  - [26 · ⚪ MINOR · CODE_SMELL · python:S116](#26-minor-code_smell-pythons116)
  - [27 · ⚪ MINOR · CODE_SMELL · python:S116](#27-minor-code_smell-pythons116)
  - [28 · ⚪ MINOR · CODE_SMELL · python:S116](#28-minor-code_smell-pythons116)
  - [29 · ⚪ MINOR · CODE_SMELL · python:S116](#29-minor-code_smell-pythons116)
  - [30 · ⚪ MINOR · CODE_SMELL · python:S116](#30-minor-code_smell-pythons116)
  - [31 · ⚪ MINOR · CODE_SMELL · python:S116](#31-minor-code_smell-pythons116)
  - [32 · ⚪ MINOR · CODE_SMELL · python:S116](#32-minor-code_smell-pythons116)
  - [33 · ⚪ MINOR · CODE_SMELL · python:S116](#33-minor-code_smell-pythons116)
  - [34 · ⚪ MINOR · CODE_SMELL · python:S116](#34-minor-code_smell-pythons116)
  - [35 · ⚪ MINOR · CODE_SMELL · python:S116](#35-minor-code_smell-pythons116)
  - [36 · ⚪ MINOR · CODE_SMELL · python:S116](#36-minor-code_smell-pythons116)
  - [37 · ⚪ MINOR · CODE_SMELL · python:S116](#37-minor-code_smell-pythons116)
  - [38 · ⚪ MINOR · CODE_SMELL · python:S116](#38-minor-code_smell-pythons116)
  - [39 · ⚪ MINOR · CODE_SMELL · python:S116](#39-minor-code_smell-pythons116)
  - [40 · ⚪ MINOR · CODE_SMELL · python:S116](#40-minor-code_smell-pythons116)
  - [41 · ⚪ MINOR · CODE_SMELL · python:S116](#41-minor-code_smell-pythons116)
  - [42 · ⚪ MINOR · CODE_SMELL · python:S116](#42-minor-code_smell-pythons116)
  - [43 · ⚪ MINOR · CODE_SMELL · python:S116](#43-minor-code_smell-pythons116)
  - [44 · ⚪ MINOR · CODE_SMELL · python:S116](#44-minor-code_smell-pythons116)
  - [45 · ⚪ MINOR · CODE_SMELL · python:S116](#45-minor-code_smell-pythons116)
  - [46 · ⚪ MINOR · CODE_SMELL · python:S116](#46-minor-code_smell-pythons116)
  - [47 · ⚪ MINOR · CODE_SMELL · python:S116](#47-minor-code_smell-pythons116)
  - [48 · ⚪ MINOR · CODE_SMELL · python:S116](#48-minor-code_smell-pythons116)
  - [49 · ⚪ MINOR · CODE_SMELL · python:S116](#49-minor-code_smell-pythons116)
  - [50 · ⚪ MINOR · CODE_SMELL · python:S116](#50-minor-code_smell-pythons116)
  - [51 · ⚪ MINOR · CODE_SMELL · python:S116](#51-minor-code_smell-pythons116)
<!-- TOC END -->

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
"values": config_result.value
})
except ValueError as exc:
return e.fail_validation(
"pipeline configuration JSON", error=exc, result_type=r[t.JsonMapping]
)
return r[t.JsonMapping].ok(config_mapping.values)

def _pipeline_command(
```

**Decisão**: pendente

### 2 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_meltano/pipeline_mgr.py:112` · **Effort**: 6min

> Define a constant instead of duplicating this literal "Pipeline execution not configured" 3 times.

```python
) -> p.Result[t.StrSequence]:
config_result = self._load_pipeline_config(pipeline_name)
if config_result.failure:
return r[t.StrSequence].fail(
config_result.error or "Pipeline execution not configured"
)
command_value = config_result.value.get("command")
if not isinstance(command_value, t.SEQUENCE_PAIR_TYPES):
return r[t.StrSequence].fail("Pipeline execution not configured")
```

**Decisão**: pendente

### 3 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_meltano/pipeline_mgr.py:149` · **Effort**: 10min

> Define a constant instead of duplicating this literal "Pipeline name is invalid" 5 times.

```python
) -> p.Result[str]:
"""Create and persist a named pipeline configuration."""
name_result = self._normalize_pipeline_name(pipeline_name)
if name_result.failure:
return r[str].fail(name_result.error or "Pipeline name is invalid")
if config_payload is None:
return r[str].fail("Pipeline creation not configured")
try:
config_mapping = m.Meltano.ConfigMappingPayload.model_validate({
```

**Decisão**: pendente

### 4 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/consumer_bases/dbt_service_base.py:74` · **Effort**: 7min

> Refactor this function to reduce its Cognitive Complexity from 17 to the 15 allowed.

```python
# ------------------------------------------------------------------
# CLI dispatch
# ------------------------------------------------------------------

def cli_main(self, args: t.StrSequence | None = None) -> int:
"""Run the main CLI entry point for dbt project."""

def _run_cli_main() -> int:
command_args = list(args) if args else sys.argv[1:]
```

**Decisão**: pendente

### 5 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_meltano/services/dbt_project.py:49` · **Effort**: 6min

> Define a constant instead of duplicating this literal "Unknown error" 3 times.

```python
c.Meltano.DbtResourceType.MODEL
)
if model_nodes_result.failure:
return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
model_nodes_result.error or "Unknown error"
)
try:
models = [
self._build_manifest_node_summary(node)
```

**Decisão**: pendente

### 6 · 🟠 CRITICAL · CODE_SMELL · `python:S5754`
**Local**: `src/flext_meltano/services/declarative_tap.py:47` · **Effort**: 5min

> Reraise this exception to stop the application as the user expects

```python
try:
_ = command.main(
args=list(args), prog_name=prog_name, standalone_mode=False
)
except SystemExit as exc:
return exc.code if isinstance(exc.code, int) else 1
return 0

def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
```

**Decisão**: pendente

### 7 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/executor_base.py:203` · **Effort**: 6min

> Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.

```python
}
self.logger.info("FlextMeltanoExecutor executed successfully")
return r[t.JsonMapping].ok(config_data)

def execute_meltano_command(
self,
command: t.StrSequence,
timeout: int = c.Meltano.NETWORK_MELTANO_DEFAULT_TIMEOUT,
_cwd: Path | None = None,
```

**Decisão**: pendente

### 8 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/executor_base.py:321` · **Effort**: 6min

> Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.

```python
)
except c.Meltano.OPERATION_ERRORS as e:
return r[m.Meltano.CommandExecutionResult].fail(str(e))

def execute_pipeline(
self, tap_name: str, target_name: str, config: t.JsonMapping | None = None
) -> p.Result[m.Meltano.CommandExecutionResult]:
"""Execute a complete ELT pipeline."""
prepared_command: t.StrSequence | None = None
```

**Decisão**: pendente

### 9 · 🟠 CRITICAL · CODE_SMELL · `python:S5727`
**Local**: `src/flext_meltano/services/executor_base.py:398` · **Effort**: 10min

> Remove this identity check; it will always be True.

```python
failed_stage.error
if failed_stage is not None and failed_stage.error is not None
else "Failed to run Meltano pipeline"
)
if completed_result is None:
return r[m.Meltano.CommandExecutionResult].fail(
"Pipeline execution result missing"
)
return r[m.Meltano.CommandExecutionResult].ok(completed_result)
```

**Decisão**: pendente

### 10 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_meltano/services/meltano_plugin_discovery.py:73` · **Effort**: 9min

> Refactor this function to reduce its Cognitive Complexity from 19 to the 15 allowed.

```python
error_msg = f"Failed to discover plugins: {e}"
self.logger.exception(error_msg, error=str(e))
return r[t.SequenceOf[t.StrMapping]].fail(error_msg)

def _discover_plugins(
self, project: t.JsonPayload | t.Meltano.DbtProject | None
) -> p.Result[t.SequenceOf[t.StrMapping]]:
"""Discover plugins without owning the exception boundary."""
self.logger.info("Discovering Meltano plugins")
```

**Decisão**: pendente

### 11 · 🟠 CRITICAL · CODE_SMELL · `python:S5754`
**Local**: `src/flext_meltano/services/singer_sdk.py:70` · **Effort**: 5min

> Reraise this exception to stop the application as the user expects

```python
try:
singer_command = self._tap.get_singer_command()
_ = singer_command.main(args=list(args), prog_name=prog_name)
return 0
except SystemExit as exc:
return exc.code if isinstance(exc.code, int) else 1

def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
"""Delegate stream discovery to the raw Singer tap."""
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
18    contents: read
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
19    pages: write
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
20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: pendente

### 15 · 🟡 MAJOR · VULNERABILITY · `text:S8565`
**Local**: `pyproject.toml:-` · **Effort**: 5min

> Dependency versions are not predictable if the lock file (uv.lock, uv.lock, pdm.lock or pylock.toml) is missing.

**Decisão**: pendente

### 16 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
if (
existing_package is None
or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
):
for module_name in list(sys.modules):
if module_name == package_name or module_name.startswith(
f"{package_name}."
):
sys.modules.pop(module_name, None)
```

**Decisão**: pendente

### 17 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:31` · **Effort**: 2min

> Rename this field "SingerTapBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
the canonical m.Meltano.Singer* namespace. Consumers subclass these
instead of importing singer_sdk directly.
"""

SingerTapBase = Tap
SingerSinkBase = Sink
SingerStreamBase = Stream
SingerTargetBase = Target
SingerContext = Context
```

**Decisão**: pendente

### 18 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:32` · **Effort**: 2min

> Rename this field "SingerSinkBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
instead of importing singer_sdk directly.
"""

SingerTapBase = Tap
SingerSinkBase = Sink
SingerStreamBase = Stream
SingerTargetBase = Target
SingerContext = Context
SingerRecord = Record
```

**Decisão**: pendente

### 19 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:33` · **Effort**: 2min

> Rename this field "SingerStreamBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
"""

SingerTapBase = Tap
SingerSinkBase = Sink
SingerStreamBase = Stream
SingerTargetBase = Target
SingerContext = Context
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
```

**Decisão**: pendente

### 20 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:34` · **Effort**: 2min

> Rename this field "SingerTargetBase" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python

SingerTapBase = Tap
SingerSinkBase = Sink
SingerStreamBase = Stream
SingerTargetBase = Target
SingerContext = Context
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
```

**Decisão**: pendente

### 21 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:35` · **Effort**: 2min

> Rename this field "SingerContext" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerTapBase = Tap
SingerSinkBase = Sink
SingerStreamBase = Stream
SingerTargetBase = Target
SingerContext = Context
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
```

**Decisão**: pendente

### 22 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:36` · **Effort**: 2min

> Rename this field "SingerRecord" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerSinkBase = Sink
SingerStreamBase = Stream
SingerTargetBase = Target
SingerContext = Context
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
```

**Decisão**: pendente

### 23 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:37` · **Effort**: 2min

> Rename this field "SingerArrayType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerStreamBase = Stream
SingerTargetBase = Target
SingerContext = Context
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
```

**Decisão**: pendente

### 24 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:38` · **Effort**: 2min

> Rename this field "SingerBooleanType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerTargetBase = Target
SingerContext = Context
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
```

**Decisão**: pendente

### 25 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:39` · **Effort**: 2min

> Rename this field "SingerCustomType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerContext = Context
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
```

**Decisão**: pendente

### 26 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:40` · **Effort**: 2min

> Rename this field "SingerDateTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerRecord = Record
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
```

**Decisão**: pendente

### 27 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:41` · **Effort**: 2min

> Rename this field "SingerDateType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
```

**Decisão**: pendente

### 28 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:42` · **Effort**: 2min

> Rename this field "SingerDurationType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
```

**Decisão**: pendente

### 29 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:43` · **Effort**: 2min

> Rename this field "SingerIntegerType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerProperty = singer_sdk_typing.Property
```

**Decisão**: pendente

### 30 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:44` · **Effort**: 2min

> Rename this field "SingerNumberType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerProperty = singer_sdk_typing.Property
SingerStringType = singer_sdk_typing.StringType
```

**Decisão**: pendente

### 31 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:45` · **Effort**: 2min

> Rename this field "SingerObjectType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerProperty = singer_sdk_typing.Property
SingerStringType = singer_sdk_typing.StringType
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 32 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:46` · **Effort**: 2min

> Rename this field "SingerPropertiesList" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerProperty = singer_sdk_typing.Property
SingerStringType = singer_sdk_typing.StringType
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 33 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:47` · **Effort**: 2min

> Rename this field "SingerProperty" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerProperty = singer_sdk_typing.Property
SingerStringType = singer_sdk_typing.StringType
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 34 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:48` · **Effort**: 2min

> Rename this field "SingerStringType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerProperty = singer_sdk_typing.Property
SingerStringType = singer_sdk_typing.StringType
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 35 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/singer_sdk.py:49` · **Effort**: 2min

> Rename this field "SingerTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerProperty = singer_sdk_typing.Property
SingerStringType = singer_sdk_typing.StringType
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 36 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_models/sources.py:17` · **Effort**: 2min

> Rename this field "StreamDefinition" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python

class FlextMeltanoModelsSources:
"""Source and configuration models."""

StreamDefinition: ClassVar[
type[FlextMeltanoModelsSourcesParams.StreamDefinition]
] = FlextMeltanoModelsSourcesParams.StreamDefinition

class TapConfig(m.Entity):
```

**Decisão**: pendente

### 37 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_protocols/singer.py:210` · **Effort**: 2min

> Rename this field "SingerTapSdkBackend" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
def sync_all(self) -> None:
"""Execute sync for all selected streams."""
...

SingerTapSdkBackend = SingerTapBackend
SingerTapSettingsBackend = SingerTapBackend

@runtime_checkable
class SingerDrainSink(Protocol):
```

**Decisão**: pendente

### 38 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_protocols/singer.py:211` · **Effort**: 2min

> Rename this field "SingerTapSettingsBackend" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
"""Execute sync for all selected streams."""
...

SingerTapSdkBackend = SingerTapBackend
SingerTapSettingsBackend = SingerTapBackend

@runtime_checkable
class SingerDrainSink(Protocol):
"""Typed sink contract for target service drain and record operations.
```

**Decisão**: pendente

### 39 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/base.py:32` · **Effort**: 2min

> Rename this field "PluginType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
)

type ValidatorInput = t.JsonValue

PluginType = c.Meltano.PluginType

type VariantValue = str | t.StrSequence | t.ScalarMapping | None
"""Normalized plugin variant: string, string list, scalar mapping, or null."""

```

**Decisão**: pendente

### 40 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:23` · **Effort**: 2min

> Rename this field "SingerReplicationMethod" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
External library wrappers (singer_sdk.typing) are kept to prevent
direct imports by consumer projects.
"""

SingerReplicationMethod = c.Meltano.SingerReplicationMethod

# Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
```

**Decisão**: pendente

### 41 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:26` · **Effort**: 2min

> Rename this field "SingerArrayType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python

SingerReplicationMethod = c.Meltano.SingerReplicationMethod

# Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
```

**Decisão**: pendente

### 42 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:27` · **Effort**: 2min

> Rename this field "SingerBooleanType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerReplicationMethod = c.Meltano.SingerReplicationMethod

# Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
```

**Decisão**: pendente

### 43 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:28` · **Effort**: 2min

> Rename this field "SingerCustomType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python

# Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
```

**Decisão**: pendente

### 44 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:29` · **Effort**: 2min

> Rename this field "SingerDateTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
# Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
```

**Decisão**: pendente

### 45 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:30` · **Effort**: 2min

> Rename this field "SingerDateType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerArrayType = singer_sdk_typing.ArrayType
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
```

**Decisão**: pendente

### 46 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:31` · **Effort**: 2min

> Rename this field "SingerDurationType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerBooleanType = singer_sdk_typing.BooleanType
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
```

**Decisão**: pendente

### 47 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:32` · **Effort**: 2min

> Rename this field "SingerIntegerType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerCustomType = singer_sdk_typing.CustomType
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 48 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:33` · **Effort**: 2min

> Rename this field "SingerNumberType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerDateTimeType = singer_sdk_typing.DateTimeType
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 49 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:34` · **Effort**: 2min

> Rename this field "SingerObjectType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerDateType = singer_sdk_typing.DateType
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 50 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:35` · **Effort**: 2min

> Rename this field "SingerPropertiesList" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerDurationType = singer_sdk_typing.DurationType
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente

### 51 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_meltano/_typings/singer.py:36` · **Effort**: 2min

> Rename this field "SingerTimeType" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
SingerIntegerType = singer_sdk_typing.IntegerType
SingerNumberType = singer_sdk_typing.NumberType
SingerObjectType = singer_sdk_typing.ObjectType
SingerPropertiesList = singer_sdk_typing.PropertiesList
SingerTimeType = singer_sdk_typing.TimeType
```

**Decisão**: pendente
