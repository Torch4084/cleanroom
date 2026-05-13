# Contributing

Thanks for your interest in improving CleanRoom.

## Before opening a pull request

- Keep changes focused and easy to review.
- Prefer bug fixes, UI polish, packaging fixes, and documentation improvements.
- Open an issue first if you want to propose a larger workflow change.

## Development notes

- The app is a single GTK4 Python entry point: `cleanroom.py`
- Security-sensitive helpers live in `cleanroom_core.py` so they can be tested without launching GTK
- Privileged operations are executed through `sudo`
- Container roots are managed under `/var/lib/machines` by default
- The optional AI assistant must remain advisory only

## Suggested checks

Run these before sending a change:

```bash
pytest
python3 -m py_compile cleanroom.py cleanroom_core.py
```

If you have Ruff installed locally:

```bash
ruff check .
```

## Pull request style

- Explain the user-visible change
- Mention the Linux distribution or environment you tested on, if relevant
- Call out any command construction, path handling, `sudo`, deletion, or AI-output changes
- Include screenshots for UI changes when possible
