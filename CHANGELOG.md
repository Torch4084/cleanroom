# Changelog

## 1.1.0 - 2026-05-13

Maintenance and safety-focused release.

### Added

- Command preview before privileged bootstrap and launch operations.
- Unit tests for container-name validation, path handling, command builders, and
  AI prompt structure.
- GitHub Actions CI for tests, linting, and Python compilation.
- Security policy, threat model, maintainer docs, release checklist, issue
  templates, PR template, roadmap, screenshots, and distribution workflow
  documentation.

### Fixed

- System install and Arch packaging now install `cleanroom_core.py`, which is
  required by the refactored application entry point.

### Security

- Container names are validated before path construction.
- Bootstrap and launch command paths are shell-quoted before terminal execution.
- AI assistance remains advisory only and cannot perform container operations.

## 1.0.0 - 2026-01-01

Initial public release of CleanRoom.

### Added

- GTK4 desktop workflow for creating, bootstrapping, launching, and deleting
  `systemd-nspawn` container roots.
- Status indicators for ready and empty container roots.
- Arch and Debian bootstrap support through `pacstrap` and `debootstrap`.
- Desktop entry and install script.
