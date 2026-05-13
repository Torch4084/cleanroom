# Threat Model

CleanRoom is a local desktop application for managing `systemd-nspawn` container
roots. It is not a sandbox implementation and does not replace Linux permissions,
`sudo` policy, or `systemd-nspawn` security boundaries.

## Assets

- Host filesystem outside the configured machines directory
- Container roots under `/var/lib/machines` or `CLEANROOM_MACHINES_PATH`
- User trust in generated bootstrap and launch commands
- Optional AI assistant API credentials supplied through environment variables

## Trust Boundaries

- User input enters through container names and AI-assistant goals.
- Privileged actions cross into `sudo`-controlled host operations.
- AI suggestions cross from an external model into a local advisory UI.
- Terminal launchers execute shell commands after user approval.

## Security Controls

- Container names are restricted to letters, numbers, dots, underscores, and dashes.
- Reserved path names such as `.` and `..` are rejected.
- Container paths are built through a shared helper and command paths are shell-quoted.
- Bootstrap and launch commands are previewed before opening a terminal.
- Deletion requires confirmation.
- The AI assistant returns text only. It cannot execute commands or mutate containers.

## Important Non-Goals

- CleanRoom does not harden `systemd-nspawn` itself.
- CleanRoom does not run untrusted commands safely by default.
- CleanRoom does not bypass local administrator policy.
- CleanRoom does not automatically apply AI-generated commands.

## Review Hotspots

Changes in these areas need extra review:

- command construction
- container path handling
- `sudo` invocation
- recursive deletion
- AI response parsing and display
- terminal launcher behavior
