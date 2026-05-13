# Release Checklist

Use this checklist before publishing a CleanRoom release.

## Code Checks

```bash
pytest
ruff check .
python3 -m py_compile cleanroom.py cleanroom_core.py
```

## Manual Checks

- Start CleanRoom from source.
- Create a test container entry.
- Confirm invalid container names are rejected.
- Confirm bootstrap command preview appears before terminal launch.
- Confirm launch command preview appears before terminal launch.
- Confirm delete confirmation appears before removal.
- Confirm AI assistant remains advisory and does not execute commands.

## Documentation Checks

- Update `CHANGELOG.md`.
- Confirm `README.md` reflects current behavior.
- Confirm `SECURITY.md` still matches the safety model.
- Confirm packaging files install every required Python module.

## Release Notes

Release notes should mention:

- user-visible changes
- security-sensitive changes
- packaging changes
- known limitations
