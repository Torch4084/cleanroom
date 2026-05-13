# Changelog

## 1.0.0 - 2026-05-13

Initial maintained release of CleanRoom.

### Added

- GTK4 desktop workflow for creating, bootstrapping, launching, and deleting
  `systemd-nspawn` container roots.
- Optional AI assistant for advisory container setup plans.
- Command preview before privileged bootstrap and launch operations.
- Unit tests for container-name validation, path handling, command builders, and
  AI prompt structure.
- GitHub Actions CI for tests, linting, and Python compilation.
- Security policy, issue templates, PR template, roadmap, and distribution
  workflow documentation.

### Security

- Container names are validated before path construction.
- Bootstrap and launch command paths are shell-quoted before terminal execution.
- AI assistance remains advisory only and cannot perform container operations.
