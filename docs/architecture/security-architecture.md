# Security Architecture

<!-- TOC START -->

- [Scope](#scope)
- [Redaction of sensitive configuration](#redaction-of-sensitive-configuration)
  - [Behavior](#behavior)
  - [Example](#example)
- [Immutability of configuration payloads](#immutability-of-configuration-payloads)
- [Environment-driven settings](#environment-driven-settings)
- [Meltano command execution](#meltano-command-execution)
- [Out of scope](#out-of-scope)

<!-- TOC END -->

This document describes the security-relevant behavior that `flext-meltano`
implements today. Every statement below cites the source that owns it.

## Scope

`flext-meltano` is a library that wraps the Meltano runtime for FLEXT
pipelines. Its only security-specific mechanism is the redaction of sensitive
keys when a tap or target configuration is serialized. Everything else in
this document is a property of how configuration is modeled and how commands
are run.

## Redaction of sensitive configuration

### Behavior

- `FlextMeltanoModelsCore.protect_sensitive_config` replaces the value of any
  key whose lowercased name contains one of `password`, `token`, `api_key`,
  `secret`, or `credentials` with the literal `[PROTECTED]`
  (`src/flext_meltano/_models/core.py:47-68`).
- The match is by substring, so `db_password` and `Auth_Token` are redacted
  (`core.py:49-51`).
- Redaction is recursive through nested mappings and lists
  (`core.py:53-63`). A sensitive key at any depth is replaced; non-sensitive
  values are returned unchanged.
- The mixin `SensitiveConfigSerializer` registers a field serializer for
  `connection_config` that applies the redaction (`core.py:70-89`).
- `TapConfig` and `TargetConfig` both inherit that mixin
  (`src/flext_meltano/_models/sources.py:21-22` and `:78-79`), so
  `model_dump` and `model_dump_json` of either model never contain the
  original sensitive values.
- The stored value is not modified: serialization produces a redacted copy and
  the original mapping keeps its real values. The example
  `examples/simple_working.py` (`serialization_example`, line 27 onward)
  exercises exactly this, asserting that sensitive input is absent from both
  `model_dump(mode="json")` and `model_dump_json()`, that non-sensitive values
  are preserved, and that the retained configuration is not mutated.

The key list is fixed in code. There is no per-deployment configuration of it,
and values stored under other key names are not redacted.

### Example

```python
import secrets

from flext_meltano import m

secret = secrets.token_urlsafe(16)
tap = m.Meltano.TapConfig.model_validate({
    "tap_type": "tap-example",
    "connection_config": {"password": secret, "host": "db.example.invalid"},
})

exported = tap.model_dump_json()
assert secret not in exported
assert "db.example.invalid" in exported
```

## Immutability of configuration payloads

- `TapConfig.stream_config` and `TargetConfig.connection_config` default to an
  empty read-only mapping (`sources.py:34-35`, `:88-89`).
- After validation those mappings are frozen into `MappingProxyType` views
  (`sources.py:41-56` for tap `stream_config`, `:105-120` for target
  `connection_config`), so consumers cannot mutate them in place.
- A `TapConfig` with an empty `tap_type` or an empty `connection_config` is
  rejected at validation time (`sources.py:61-76`).

## Environment-driven settings

- Runtime settings read environment variables with the `FLEXT_MELTANO_`
  prefix (`src/flext_meltano/_settings.py:44-45`); the project root also
  accepts `MELTANO_PROJECT_ROOT` (`_settings.py:56`).
- The `environment` setting is validated against the declared set of
  environment names and aliases (`_settings.py:116-118`).
- The settings model declares no credential fields; credentials are not read or
  stored by `flext-meltano` itself (a search of `src/` finds no secret type and
  no credential loading).

## Meltano command execution

- Commands run in-process through the Meltano CLI entry point, not through a
  shell or an external subprocess
  (`src/flext_meltano/services/executor_base.py:251-257`). No `subprocess`,
  `Popen`, or `shell=True` use exists in `src/`.
- The command is an argument list. The runtime prepends the selected
  environment option and `--cwd` before the caller's arguments
  (`executor_base.py:231-238`).
- A non-positive timeout and an empty command are rejected before execution
  (`executor_base.py:209-224`).
- Execution is logged with the command arguments, timeout, and working
  directory (`executor_base.py:242-247`). Command arguments are logged as given;
  do not pass secrets as command-line arguments.

## Out of scope

`flext-meltano` does not provide, and this document does not describe:

- authentication (users, OAuth, client certificates, API keys);
- authorization (RBAC, ABAC, permission checks);
- session management;
- network controls (TLS termination, firewalls, segmentation);
- encryption of data at rest or in transit;
- audit logging, security monitoring, incident response, or compliance
  controls.

These belong to the deploying platform and to the Meltano plugins it runs.
Secrets should be supplied to plugins through the platform's secret
management, and the redaction above should be treated as protection against
accidental disclosure in serialized output only.
