# FLEXT Development Commands

## Environment Setup

```bash
# Activate virtual environment (MANDATORY)
source ~/flext/.venv/bin/activate

# Project setup (first time)
make setup
```

## Quality Gates (Mandatory Order)

```bash
# Complete validation pipeline
make validate

# Quick health check
make check

# Individual checks (in order)
ruff check .                # 1. Lint check
mypy .                      # 2. Type check
pyright                     # 3. Secondary type check
pytest -q --maxfail=1 --cov=src --cov=examples --cov=tests --cov=. \
       --cov-report=term-missing:skip-covered \
       --cov-fail-under=100  # 4. Tests with 100% coverage
```

## Development Commands

```bash
# Code formatting
make format
ruff format .

# Auto-fix issues
make fix
ruff check . --fix

# Testing
make test                   # Full test suite with coverage
make test-unit             # Unit tests only
make test-integration      # Integration tests only

# Security
make security              # Bandit + pip-audit
```

## flext-core Specific Commands

```bash
cd flext-core

# Foundation library validation
make validate              # All quality gates
make test                  # 75% minimum coverage
make type-check            # MyPy strict mode
make lint                  # Ruff linting
```

## Quick Enforcement Scans

```bash
# Find violations
rg -n "# type: ignore"     # Find type ignores
rg -n "\bAny\b"           # Find object usage
rg -n "(wrapper|alias|legacy|compat)"  # Find wrappers
rg -n "\bpass\b|TODO|try:\\s*pass"     # Find stubs
```

## One-Liner Gate Check

```bash
ruff check . && mypy . && pyright && \
pytest -q --maxfail=1 --cov=src --cov=examples --cov=tests --cov=. \
       --cov-report=term-missing:skip-covered \
       --cov-fail-under=100
```

## MCP Servers (Available)

- **serena**: Semantic code operations
- **sequential-thinking**: Problem decomposition
- **context7**: Third-party documentation
- **github**: Repository operations
- **puppeteer**: Web automation
