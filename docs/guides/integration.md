# flext-meltano Integration Patterns

<!-- TOC START -->

- [🎯 ELT Foundation Role](#elt-foundation-role)
- [🔌 Singer Ecosystem Integration](#singer-ecosystem-integration)
  - [Tap Implementation Pattern](#tap-implementation-pattern)
  - [Target Implementation Pattern](#target-implementation-pattern)
- [🛠️ dbt Integration Patterns](#dbt-integration-patterns)
  - [dbt Project Foundation](#dbt-project-foundation)
- [📊 Integration Matrix](#integration-matrix)
  - [Integration Requirements](#integration-requirements)
- [🌍 Environment Integration](#environment-integration)
  - [Consumer Project Dependencies](#consumer-project-dependencies)
- [🔧 Integration Best Practices](#integration-best-practices)

<!-- TOC END -->

**ELT foundation integration patterns for the FLEXT ecosystem**

---

## 🎯 ELT Foundation Role

flext-meltano is the ELT foundation of the FLEXT ecosystem (ADR-006). The
`flext-tap-*`, `flext-target-*` and `flext-dbt-*` connectors are thin drivers over
its consumer bases; reusable CLI dispatch, Singer message handling and dbt
execution live here once. Connectors import every flext-meltano name from the
package root and never import `singer_sdk` directly.

---

## 🔌 Singer Ecosystem Integration

### Tap Implementation Pattern

Declarative taps describe their streams as data and fetch records with their own
domain library; flext-meltano builds the Singer tap and its flat CLI
(`--config/--discover/--catalog/--state`):

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_meltano import FlextMeltanoTapServiceBase, m, p, r


class FlextExampleTapService(FlextMeltanoTapServiceBase):
    """Declarative tap: streams as data, records from the domain fetcher."""

    tap_name: str = "tap-example"

    def create_tap_instance(self, _settings=None) -> p.Meltano.SingerTapInstance:
        return self.build_declarative_tap(TAP_SPEC, ExampleFetcher())


class ExampleFetcher:
    def fetch(self, request: m.Meltano.FetchRequest) -> p.Result[m.Meltano.FetchResult]:
        return r[m.Meltano.FetchResult].ok(m.Meltano.FetchResult(records=()))
```

Taps that already own a `singer_sdk` tap class (subclassing
`m.Meltano.SingerTapBase`) return `FlextMeltanoSingerTapAdapter(tap)` from
`create_tap_instance`. The console entry point calls `cli_main(args)`.

### Target Implementation Pattern

The runnable example lives in `examples/target_service.py`: the service declares
`sink_factory: ClassVar[p.Meltano.SinkFactory]` and defines no method, and
`examples/target_sink.py` provides a drain sink whose constructor
`(*, stream_name, schema, target_config)` is the factory. A connector binds its
stateless `u.<Namespace>.create_sink` the same way.

```python
from examples import ExamplesFlextMeltanoTargetService

service = ExamplesFlextMeltanoTargetService()
created = service.fetch_or_create_sink("orders", {"properties": {}})
if created.failure:
    raise RuntimeError(created.error)
```

`cli_main()` routes SCHEMA/RECORD/STATE messages through
`u.Meltano.process_stdin`, creates sinks on demand through `sink_factory` (with
`target_config` taken from the service settings overrides) and flushes them at STATE
boundaries and at end of input.

---

## 🛠️ dbt Integration Patterns

### dbt Project Foundation

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_meltano import FlextMeltanoDbtServiceBase, p


class FlextExampleDbtService(FlextMeltanoDbtServiceBase):
    """dbt project: run/test/compile/docs through the Meltano executor."""

    @property
    def connection_profile(self) -> p.Meltano.DbtConnectionProfile:
        return EXAMPLE_PROFILE
```

`cli_main(["run", "model_a"])` dispatches to `run_models`; `test`, `compile` and
`docs` dispatch to `run_tests`, `compile_models` and `generate_docs`. Each returns
the typed `m.Meltano.CommandExecutionResult`.

---

## 📊 Integration Matrix

| Consumer base                     | Connectors                                                   |
| --------------------------------- | ------------------------------------------------------------ |
| `FlextMeltanoTapServiceBase`      | flext-tap-ldap, flext-tap-ldif, flext-tap-oracle, flext-tap-oracle-oic, flext-tap-oracle-wms |
| `FlextMeltanoTargetServiceBase`   | flext-target-ldif, flext-target-oracle, flext-target-oracle-oic, flext-target-oracle-wms |
| `FlextMeltanoDbtServiceBase`      | flext-dbt-ldap, flext-dbt-ldif, flext-dbt-oracle, flext-dbt-oracle-wms |
| `FlextMeltanoLibraryRunner`       | flext-dbt-oracle-wms (`run_dbt_transformation`)              |
| `FlextMeltanoAbstractions`        | flext-tap-oracle-oic                                         |
| `FlextMeltanoTargetAbstractions`  | flext-target-oracle-oic                                      |

### Integration Requirements

1. Import flext-meltano names from the package root only.
2. Provide only the base's capability (`create_tap_instance`, the declared
   `sink_factory`, `connection_profile`); the base owns CLI dispatch. Targets declare
   `sink_factory` in `api.py` and define no method there (ADR-006, amended 2026-10-25).
3. Return `r[T]` results; never import `singer_sdk` in a connector.

---

## 🌍 Environment Integration

### Consumer Project Dependencies

Consumer dependency declarations and Python constraints are generated from the workspace
topology and `flext-infra/config/codegen.yaml`. Do not edit the generated
`pyproject.toml` or introduce a parallel Poetry/uv dependency table. Reconcile the
declared dependency floors and regenerate consumers from the workspace root:

```bash
make upg
make gen
```

---

## 🔧 Integration Best Practices

- Use only root-level imports from flext-meltano; the
  `rewire-consumer-deep-import-to-root` codemod rule repairs deep imports.
- Follow `r` patterns for all operations.
- Keep connector-specific behavior in the connector (ADR-006); shared Singer and
  dbt mechanics belong in flext-meltano once.

---

**Integration Guide v0.12.0-dev**
