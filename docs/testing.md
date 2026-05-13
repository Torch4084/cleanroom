# Testing

CleanRoom keeps security-sensitive logic in `cleanroom_core.py` so it can be tested
without launching GTK.

## Local Test Environment

On systems with externally managed Python packages, create a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pytest ruff
```

## Run Checks

```bash
.venv/bin/pytest
.venv/bin/ruff check .
python3 -m py_compile cleanroom.py cleanroom_core.py
```

## Current Test Coverage

The unit tests cover:

- valid and invalid container names
- path construction rejection for invalid names
- shell quoting for launch and bootstrap command builders
- unsupported bootstrap tool rejection
- AI prompt sections used by the advisory assistant

GTK workflows still need manual testing because they depend on desktop services,
terminal emulators, and local `sudo` policy.
