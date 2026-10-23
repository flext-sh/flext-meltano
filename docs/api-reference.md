# FLEXT-Meltano API Reference

<!-- TOC START -->

- [Public Surface](#public-surface)
- [The `meltano` Facade](#the-meltano-facade)
- [Consumer Bases](#consumer-bases)
- [Singer Utilities](#singer-utilities)
- [Pipeline Manager and CLI](#pipeline-manager-and-cli)
- [Models, Protocols, Types, Constants](#models-protocols-types-constants)
- [Integration Examples](#integration-examples)
- [Related Documentation](#related-documentation)

<!-- TOC END -->

> **Manual supplement**: This page summarizes the public surface that the
> runtime exposes today. The generated reference and the package root
> `flext_meltano.__all__` are the canonical, complete inventory.

Every operation returns `p.Result[T]` (`r[T]`); failures carry the original
error text.

## Public Surface

Import every public name from the package root:

```python notest
from flext_meltano import (
    FlextMeltano,  # MRO facade class
    FlextMeltanoAbstractions,  # Meltano runtime abstraction (tap entry points)
    FlextMeltanoDbtServiceBase,  # dbt consumer base
    FlextMeltanoLibraryRunner,  # dbt transformation runner
    FlextMeltanoSingerTapAdapter,  # bridge for a singer_sdk tap instance
    FlextMeltanoTapServiceBase,  # Singer tap consumer base
    FlextMeltanoTargetAbstractions,  # Singer target entry-point base
    FlextMeltanoTargetServiceBase,  # Singer target consumer base
    c,
    m,
    meltano,  # shared facade instance
    p,
    settings,
    t,
    u,
)
```

Consumers never import `flext_meltano.services.*` or private `_*` modules; the
`rewire-consumer-deep-import-to-root` codemod rule rewrites such imports to the
root.

## The `meltano` Facade

`FlextMeltano` composes the runtime services by MRO; `meltano` is its shared
instance.

| Operation                                      | Purpose                                                         |
| ---------------------------------------------- | --------------------------------------------------------------- |
| `fetch_version()`                              | Installed Meltano distribution version                          |
| `discover_installed_plugins()`                 | Names of the plugins declared in the active Meltano project     |
| `fetch_project_plugins(plugin_type=None)`      | Plugin definitions of the active project, optionally filtered   |
| `discover_plugins()` / `fetch_plugin_info(...)` | Plugin discovery used by the `plugin list` / `plugin info` CLI  |
| `execute_meltano_command(command)`             | Run a Meltano CLI command in-process; typed `CommandExecutionResult` |
| `execute_dbt_command(subcommand, args)`        | Run `meltano invoke dbt-postgres:<subcommand>`                  |
| `run_dbt_transformation(models, project_dir)`  | Run dbt models through the executor                             |
| `health()`                                     | Meltano runtime health payload                                  |
| `run_cli()`                                    | CLI readiness payload used by `status show`                     |
| `tap(name)` / `target(name)` / `dbt(name)`     | Specialized facade bound to a source, sink, or transformation   |
| `execute()`                                    | Service status payload                                          |

## Consumer Bases

Connector projects (`flext-tap-*`, `flext-target-*`, `flext-dbt-*`) are thin
drivers over these bases (ADR-006):

- `FlextMeltanoTapServiceBase` — implement `create_tap_instance()`; the base
  provides `cli_main()` and `build_declarative_tap(spec, fetcher)`, which turns
  an `m.Meltano.TapSpec` plus a `p.Meltano.RecordFetcher` into a real Singer tap.
- `FlextMeltanoTargetServiceBase` — implement `create_sink()`; the base drains
  Singer messages from stdin (`cli_main()`), manages sinks
  (`fetch_or_create_sink`, `flush`) and processes records.
- `FlextMeltanoDbtServiceBase` — implement `connection_profile`; the base
  dispatches `run`, `test`, `compile` and `docs` from `cli_main()`.
- `FlextMeltanoAbstractions` / `FlextMeltanoTargetAbstractions` — entry-point
  bases for taps and targets that run through the Meltano runtime.

## Singer Utilities

- `u.Meltano.process_stdin(handler)` — route Singer SCHEMA/RECORD/STATE
  messages from stdin to a `p.Meltano.SingerTargetHandler`.
- `u.Meltano.build_catalog_entry(...)` — build an `m.Meltano.SingerCatalogEntry`.
- `m.Meltano.Singer*` — the Singer SDK base classes and typing wrappers
  (`SingerTapBase`, `SingerStreamBase`, `SingerProperty`, ...).

## Pipeline Manager and CLI

The `flext-meltano` console script (`flext_meltano.cli:main`) exposes `version`,
`status show|health`, `tap`, `target`, `dbt`, `plugin list|info|install`, and
`pipeline create|run|list|status|stop|delete`. Pipeline commands are served by
`FlextMeltanoPipelineManager`, which persists pipeline definitions under
`settings.Meltano.pipelines_dir`.

## Models, Protocols, Types, Constants

- `m.Meltano` — Singer messages and catalog, tap/target configuration
  (`TapConfig`, `TargetConfig`), `StreamDefinition`, `TapInstance`,
  `CommandExecutionResult`, CLI input models, plugin discovery models.
- `p.Meltano` — `MeltanoExecutor`, `DbtConnectionProfile`, `SingerTapInstance`,
  `RecordFetcher`, `SingerDrainSink`, `SingerTargetHandler`.
- `t.Meltano` — `DbtProject`, `NestedStrMapping`, `ValidatorInput`,
  `SingerSchema`, `NormalizedValue`, `MutableContainerValueMapping`.
- `c.Meltano` — Meltano/Singer/dbt enumerations and runtime constants.

## Integration Examples

### Runtime command

```python notest
from flext_meltano import meltano

result = meltano.execute_meltano_command(["meltano", "--version"])
if result.success and result.value.success:
    print(result.value.output)
```

### dbt transformation

```python notest
from flext_meltano import meltano

result = meltano.run_dbt_transformation(models=["staging_orders"])
```

### Declarative tap

```python notest
from flext_meltano import FlextMeltanoTapServiceBase, m, p


class MyTapService(FlextMeltanoTapServiceBase):
    def create_tap_instance(self, _settings=None) -> p.Meltano.SingerTapInstance:
        return self.build_declarative_tap(MY_TAP_SPEC, MyFetcher())
```

`examples/simple_working.py` (`make examples`) exercises the facade end to end.

## Related Documentation

- [Getting Started](getting-started.md)
- [Architecture](architecture.md)
- [Examples](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-meltano/examples/)
