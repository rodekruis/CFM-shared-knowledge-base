"""Shared helper utilities."""

import logging
import os
import sys
import uuid

# The current run id, injected into every log record by ``_RunIdFilter`` so all
# lines from a single run can be correlated. Set by ``setup_logging``.
_run_id = "-"


class _RunIdFilter(logging.Filter):
    """Attach the current ``run_id`` to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.run_id = _run_id
        return True


def new_run_id() -> str:
    """Return a short, unique identifier for a single pipeline run."""
    return uuid.uuid4().hex[:8]


def setup_logging(run_id: str | None = None, level: int = logging.INFO) -> str:
    """Configure root logging once at the entry point; return the run id.

    Installs a single stream handler whose formatter includes a per-run
    ``run_id`` for traceability, and quiets noisy HTTP libraries. Call this once
    from the CLI entry point; modules should use ``logging.getLogger(__name__)``.
    """
    global _run_id
    _run_id = run_id or new_run_id()

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s [%(run_id)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    handler.addFilter(_RunIdFilter())

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(handler)

    # Silence noisy HTTP libraries so pipeline output stays readable.
    for noisy in ("httpx", "httpcore", "urllib3", "openai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    return _run_id


def configure_utf8_output() -> None:
    """Force stdout/stderr to UTF-8 so non-ASCII output doesn't crash on Windows.

    On Windows the default console encoding (e.g. cp1252) can't encode the
    accented / Arabic language names printed by these scripts, raising
    ``UnicodeEncodeError``. Reconfiguring the streams to UTF-8 avoids that.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")


def require_env(name: str) -> str:
    """Return the value of an environment variable or raise a friendly error."""
    value = os.environ.get(name)
    if not value:
        raise SystemExit(
            f"Missing required configuration: {name}. Set it in the .env file "
            "(local runs) or as a repository secret (GitHub Actions)."
        )
    return value
