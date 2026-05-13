# Security Policy

CleanRoom manages local `systemd-nspawn` container directories and launches privileged
commands through `sudo`. Security reports are welcome for issues that could affect the
host system, container boundaries, generated setup guidance, or command execution.

## Supported Versions

CleanRoom is currently pre-1.0. Security fixes target the default branch until tagged
releases are published.

## Reporting a Vulnerability

Please report security issues privately by emailing the maintainer or opening a minimal
GitHub security advisory if available. Avoid public proof-of-concept details until a fix
is available.

Include:

- Affected commit or version
- Linux distribution and desktop environment
- Steps to reproduce
- Expected and actual behavior
- Any relevant logs or terminal output

## Security Model

CleanRoom is a local desktop tool. It does not provide a sandbox by itself; it helps users
manage `systemd-nspawn` roots under a configured machines directory.

- Container names are validated before paths are constructed.
- Privileged filesystem operations are run through explicit `sudo` commands.
- Bootstrap and launch commands are previewed before opening a terminal-driven workflow.
- The optional AI assistant is advisory only and does not create, bootstrap, launch, or
  delete containers.
- AI-generated commands must be reviewed and manually applied by the user.

## Out of Scope

- Vulnerabilities in `systemd-nspawn`, `pacstrap`, `debootstrap`, terminal emulators, or
  the host Linux distribution
- Issues caused by intentionally running untrusted commands inside a container
- Requests to bypass local administrator or `sudo` policy
