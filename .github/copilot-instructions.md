# Copilot Instructions — ETL / Data Pipeline

Build data pipelines (extract → transform → load) for NLRC 510. Follow these conventions exactly. They are
the consolidated 510 best practices; deviate only with a documented reason.

## Working with the Engineer (Responsible AI Use)

Follow these principles: you assist, the human decides, reviews, and owns the output.

- **Think with the engineer, not for them.** Before generating non-trivial code, briefly discuss the
  approach and trade-offs. Surface design decisions rather than silently picking one.
- **Ask clarifying questions.** If a request is ambiguous, under-specified, or looks like the wrong
  approach, ask first — do not guess and produce a large answer. A short question beats a long wrong
  implementation.
- **Protect the engineer's understanding.** Don't just hand over answers to questions the engineer can
  reason through. Prompt them to attempt it, explain *why* a solution works, and call out edge cases.
  Optimize for long-term comprehension over speed.
- **Don't reinvent the wheel.** Prefer well-maintained existing libraries over bespoke implementations.
  Before writing custom code for a common problem (parsing, retries, validation, HTTP, dates), check
  whether the stdlib or an already-used dependency solves it, and say why a library is better.
- **Small, reviewable changes.** Keep diffs focused; separate refactors from features. Never produce
  massive, opaque changes.
- **Be transparent.** AI-assisted contributions should be disclosed (e.g. commit trailers) and must be
  fully understood by the human who commits them.
- **No secrets or PII into prompts/tools.** Never paste beneficiary, donor, or personnel data into AI
  tooling. Treat all generated code as untrusted until reviewed.

## Stack & Tooling

- **Python 3.12+**, managed with **uv** (never pip/poetry/virtualenv).
- Lint/format with **ruff**; type-check with **ty** (fallback **mypy**).
- Test with **pytest**. CLI with **Click** (YAML-config pipelines) or **tyro** (dataclass-config pipelines).
- Logging with stdlib `logging` or **loguru**. Deploy as a **Docker** image (`ENTRYPOINT` = the pipeline).
- License: **Apache-2.0**. Built by [NLRC 510](https://www.510.global/).

```bash
uv sync                 # install (incl. dev)
uv add requests         # add runtime dep
uv add --dev pytest     # add dev dep
uv run pytest           # test
uv run ruff check .     # lint
uv run ty check         # type check
```

## Project Structure

Use a `src/` layout. Separate **infra** (extract/load mechanics, maintained by engineers) from **domain**
(pure transform logic). Folders mirror data flow.

```
src/my_pipeline/
├── infra/
│   ├── orchestrator.py      # wires extract → transform → load per entity
│   ├── config_reader.py     # load + validate YAML
│   ├── data_provider.py     # read-only abstraction over all sources
│   ├── data_submitter.py    # write/validate/dispatch output (builder pattern)
│   ├── data_types/          # config_types, domain_types, output_types (dataclasses + StrEnums)
│   ├── utils/               # api_client, data_fetchers, integrity_checks
│   └── configs/*.yaml       # per-domain run config
├── <domain>/transform.py    # pure transform fn per pipeline variant
└── storage/                 # Storage ABC + LocalStorage / AzureBlobStorage (Protocol-based pipelines)
run_pipeline.py / cli.py     # CLI entry point
tests/{unit, integration_infra, integration_pipeline}/
```

For many heterogeneous async sources, the **Protocol-based** layout
(`extract/extractors/`, `transform/transformers/`, `load/`, `storage/`, `config/` with a `CONFIGS` registry
and an `ETLPipeline` class running `asyncio.gather`) is preferred. Use bronze/silver/gold paths for layered storage.

## Pipeline Architecture

- Strict **extract → transform → load** separation; config drives *what* to fetch and *where* to send.
- **DataProvider** loads each source into typed containers and exposes `get_data(source, expected_type)`
  with runtime type checking. **DataSubmitter** accumulates results, runs integrity checks, then dispatches.
- Pipelines must support run targets **`debug`** (local/dummy → local files), **`test`** (CI), **`prod`**
  (real sources → API/DB).
- Make runs **idempotent** (timestamped output dirs, or upsert with natural keys). Transforms must avoid
  in-place mutation of inputs.

## Configuration

- **YAML config per domain** (Click pipelines) or **dataclass `CONFIGS` registry** (tyro pipelines). Validate
  config on load; return `False`/raise on any error.
- Use **`StrEnum`** for all categorical values (`DataSource`, `OutputMode`, `RunTarget`, `PipelineType`) and
  **frozen dataclasses** for config objects — never raw dicts.
- **Environment variables hold secrets/hosts only** (`API_HOST`, `API_KEY`, `DB_PASSWORD`,
  `APPLICATIONINSIGHTS_CONNECTION_STRING`); keep `.env` gitignored with a committed `example.env`.
- Precedence: CLI flags > env vars > YAML > defaults.

## Data Types & Validation

- **Parse raw data to dataclasses at the boundary** (`Station.from_api(raw)`); never pass raw dicts/JSON
  through the pipeline. Validate API responses with **Pydantic** schemas when shapes are uncertain (skip/log
  invalid records).
- Provide explicit `to_dict()` for output serialization (camelCase, dates, enums) rather than
  `dataclasses.asdict()`. Keep output dataclasses in sync with the target API DTOs.
- Use **pandas only** for genuine vectorized work (groupby, merge, resample) — not for passing records or config.

## Extract

- One fetch function per source; dispatch with `match`. Use a **resilient `requests.Session`**
  (`Retry` with backoff on 429/5xx, idempotent methods only) and explicit **timeouts**; call
  `raise_for_status()`. Handle pagination explicitly.
- **Cache** large static reference data (TTL); **never** cache data that changes between runs (forecasts,
  realtime). Stub/dummy data must match real shape and be tracked as tech debt.
- Async pipelines: extractors expose `async def extract()`; use `asyncio.TaskGroup` / semaphores for
  concurrent downloads through the `Storage` abstraction.

## Transform

- Transform functions are **pure and I/O-free**: no `os`, no `requests`, no env reads, no file access.
  Inputs come from `DataProvider`; outputs go to `DataSubmitter`. Fully type-annotated with a docstring.
- Use **guard clauses** for missing data (record an error and return). Split complex transforms into pure
  sub-modules. Log at meaningful checkpoints only.

## Load

- **Validate before sending**: `DataSubmitter.send_all()` runs all integrity checks first and aborts on any
  error (all-or-nothing). Integrity checks return `list[str]` of contextual error messages.
- Dispatch by `OutputMode` (`LOCAL` → JSON/CSV; `API` → single batched, idempotent request). Prefer atomic
  writes (temp file + move). Check API response bodies, not just status codes; log the request ID.

## Error Handling

- **Accumulate errors and continue** across entities; return `list[str]` (empty = success). Reserve
  exceptions for truly unexpected failures. **Fail fast** only on invalid config / missing required env /
  unestablishable connections.
- Error messages follow `"{entity}: {what happened} {relevant values}"`. Never swallow exceptions silently
  (`except: pass`); catch specific exceptions and log. Never put secrets/PII in error messages.
- Use exit codes: `0` success, `1` pipeline error, `2` config error (schedulers/CI/monitoring rely on these).

## Testing

- Tiers: `unit/` (pure logic, no I/O), `integration_infra/` (scenario-driven infra runs), `integration_pipeline/`
  (end-to-end with mock data). Mark with `@pytest.mark.integration` and `@pytest.mark.needs_secrets`
  (registered in `pyproject.toml`).
- Unit-test integrity checks, config reader, and domain computations. Mock external APIs with **responses**.
  Use scenario flags (`alert`/`no-alert`) to test infra paths while bypassing domain logic.

```bash
uv run pytest tests/unit/
uv run pytest --cov=my_pipeline --cov-report=term-missing
uv run pytest -m "not integration"
```

## CLI & Entrypoints

- Prefer **Click** for YAML-config pipelines (typed options, `Choice`, `group()` for multi-pipeline repos);
  **tyro** when config is already a dataclass. Register a `[project.scripts]` entry point.
- Standard options: `--config`, `--run-target`, `--scenario`, `--issued-at`, `--dry-run`. Module-level
  `if __name__ == "__main__"` blocks are for dev smoke tests only — not the production entry point.

## Logging & Observability

- One logger per module; configure once at the entry point. Use `extra=` for structured fields and a per-run
  `run_id` for traceability. Silence noisy HTTP libs. **Never log secrets/PII.** Use a `Timer` context
  manager to record phase durations.
- Log levels: INFO for progress (counts, durations), WARNING for skipped/fallback, ERROR for affected output,
  CRITICAL when the run cannot continue.
- Production telemetry: **`azure-monitor-opentelemetry`** via `configure_azure_monitor()` (gated on
  `APPLICATIONINSIGHTS_CONNECTION_STRING`). Do **not** use the deprecated `opencensus` packages. Alert on
  non-zero exit.

## Docker & Deployment

`ENTRYPOINT` is the pipeline CLI. Layer deps before code (`--no-dev --frozen`); include `configs/`; exclude
`output/`, `data/` via `.dockerignore`. Schedule via cron / Azure Container Apps Jobs / GitHub Actions cron.

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src/ src/
COPY configs/ configs/
RUN uv sync --frozen --no-dev
ENTRYPOINT ["uv", "run", "run-pipeline"]
```

## CI/CD (GitHub Actions)

`lint-and-test` on push/PR: `uv sync` → `ruff check` → `ruff format --check` → `ty check` → `pytest --cov`
(skip `needs_secrets` without credentials). Build/push Docker image for deployment. Pin actions to major
versions; authenticate with **Azure OIDC**; protect `main`.

## pyproject.toml essentials

```toml
[project]
requires-python = ">=3.12"
dependencies = ["requests", "pyyaml", "click", "pydantic"]

[project.scripts]
run-pipeline = "my_pipeline.infra.orchestrator:main"

[dependency-groups]
dev = ["pytest>=8.0", "pytest-cov>=6.0", "responses", "ruff>=0.8", "ty"]

[tool.ruff]
line-length = 100
target-version = "py312"
[tool.ruff.lint]
select = ["E","W","F","I","UP","B","SIM","T20","N","RET","PTH"]

[tool.pytest.ini_options]
markers = ["integration: integration tests", "needs_secrets: needs API keys/credentials"]
```

**Always commit `uv.lock`**. On OneDrive set `UV_LINK_MODE=copy`.

## Anti-Patterns

- Raw dicts flowing through the pipeline
- I/O or env reads inside transforms
- Loading data via shared global state
- Sending output before integrity checks
- `except: pass`
- Aborting the whole run on one entity's failure
- Secrets/PII in logs or errors
- Argparse spaghetti (use Click/tyro)
- `print()` (use logging)
- Caching volatile data
- Custom retry loops or parsers where `tenacity`/`pydantic` and established clients already solve it
- Reinventing `DataProvider`/`DataSubmitter` abstractions instead of reusing them
