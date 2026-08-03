# AGENTS.md — flext-meltano

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_meltano` · ~10.7k src LOC · deps: `flext-cli`, `flext-core`

## Overview

Enterprise data-integration layer. Owns the thin-driver Singer base classes (ADR-006) that every `flext-tap-*`, `flext-target-*`, and `flext-dbt-*` connector extends. Connectors stay thin; reusable pipeline/executor/consumer lifecycle lives here.

## Structure

```text
src/flext_meltano/
├── api.py cli.py base.py pipeline_mgr.py
├── services/
│   ├── consumer_bases/   # Tap / Target / Dbt bases (connectors subclass)
│   ├── declarative_tap.py  # sole singer_sdk integration point
│   ├── executor_base.py dbt_runner.py dbt_project.py bridge.py adapters.py
├── constants.py typings.py protocols.py models.py utilities.py
└── _constants/ _typings/ _protocols/ _models/ _utilities/
```

## Code Map

| Symbol | Kind | Location | Role |
| --- | --- | --- | --- |
| `FlextMeltano` | class | `api.py` | facade: `.tap` / `.target` / `.dbt` / `.execute` |
| `Tap` / `Target` / `Dbt` | ABC | `services/consumer_bases/facade.py` | connector bases |
| `FlextMeltanoTapServiceBase` | class | `services/consumer_bases/tap_service_base.py` | tap lifecycle |
| `FlextMeltanoExecutorBase` | class | `services/executor_base.py` | execution mechanics |
| `FlextMeltanoPipelineManager` | class | `pipeline_mgr.py` | CLI pipeline boundary |

## Conventions (specific to this package)

- Connectors extend `Tap` / `Target` / `Dbt` and keep connector-specific behavior in their own package (ADR-006).
- Never `import singer_sdk` in a connector — only via `services/declarative_tap.py`.
- Do not fork executor/consumer lifecycle; extend the bases. CLI-domain `u` helpers come from `flext_cli`.

## Commands

```bash
make check PROJECT=flext-meltano
make test  PROJECT=flext-meltano
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
