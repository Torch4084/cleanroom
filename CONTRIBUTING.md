# Contributing

Thanks for your interest in improving CleanRoom.

## Before opening a pull request

- Keep changes focused and easy to review.
- Prefer bug fixes, UI polish, packaging fixes, and documentation improvements.
- Open an issue first if you want to propose a larger workflow change.

## Development notes

- The app is a single GTK4 Python entry point: `cleanroom.py`
- Privileged operations are executed through `sudo`
- Container roots are managed under `/var/lib/machines` by default

## Suggested checks

Run these before sending a change:

```bash
python3 -m py_compile cleanroom.py
```

If you have Ruff installed locally:

```bash
ruff check .
```

## Pull request style

- Explain the user-visible change
- Mention the Linux distribution or environment you tested on, if relevant
- Include screenshots for UI changes when possible
