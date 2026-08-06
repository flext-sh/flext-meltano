# Triagem SonarCloud — flext-sh/flext-meltano

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `mro-2wjm.11`

## Resumo

**51 issues** — BLOCKER 0, CRITICAL 11, MAJOR 4, MINOR 36
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 47

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

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_meltano/pipeline_mgr.py` | 102 | |
| 2 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_meltano/pipeline_mgr.py` | 112 | |
| 3 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_meltano/pipeline_mgr.py` | 149 | |
| 4 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_meltano/services/consumer_bases/dbt_service_base.py` | 74 | |
| 5 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_meltano/services/dbt_project.py` | 49 | |
| 6 | CRITICAL | CODE_SMELL | `python:S5754` | `src/flext_meltano/services/declarative_tap.py` | 47 | |
| 7 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_meltano/services/executor_base.py` | 203 | |
| 8 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_meltano/services/executor_base.py` | 321 | |
| 9 | CRITICAL | CODE_SMELL | `python:S5727` | `src/flext_meltano/services/executor_base.py` | 398 | |
| 10 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_meltano/services/meltano_plugin_discovery.py` | 73 | |
| 11 | CRITICAL | CODE_SMELL | `python:S5754` | `src/flext_meltano/services/singer_sdk.py` | 70 | |
| 12 | MAJOR | VULNERABILITY | `githubactions:S8264` | `.github/workflows/docs.yml` | 18 | |
| 13 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 19 | |
| 14 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 20 | |
| 15 | MAJOR | VULNERABILITY | `text:S8565` | `pyproject.toml` | - | |
| 16 | MINOR | CODE_SMELL | `python:S7504` | `conftest.py` | 20 | |
| 17 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 31 | |
| 18 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 32 | |
| 19 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 33 | |
| 20 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 34 | |
| 21 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 35 | |
| 22 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 36 | |
| 23 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 37 | |
| 24 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 38 | |
| 25 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 39 | |
| 26 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 40 | |
| 27 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 41 | |
| 28 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 42 | |
| 29 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 43 | |
| 30 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 44 | |
| 31 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 45 | |
| 32 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 46 | |
| 33 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 47 | |
| 34 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 48 | |
| 35 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/singer_sdk.py` | 49 | |
| 36 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_models/sources.py` | 17 | |
| 37 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_protocols/singer.py` | 210 | |
| 38 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_protocols/singer.py` | 211 | |
| 39 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/base.py` | 32 | |
| 40 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 23 | |
| 41 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 26 | |
| 42 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 27 | |
| 43 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 28 | |
| 44 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 29 | |
| 45 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 30 | |
| 46 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 31 | |
| 47 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 32 | |
| 48 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 33 | |
| 49 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 34 | |
| 50 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 35 | |
| 51 | MINOR | CODE_SMELL | `python:S116` | `src/flext_meltano/_typings/singer.py` | 36 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/flext-sh__flext-meltano.json`

