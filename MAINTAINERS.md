# Maintainers

## Primary Maintainer

- Torch4084: <https://github.com/Torch4084>

## Maintainer Responsibilities

CleanRoom maintainers are responsible for:

- reviewing bug reports and security-hardening issues
- keeping privileged command construction explicit and test-covered
- triaging packaging, GTK, and distribution compatibility reports
- reviewing changes to `sudo`, path handling, deletion, bootstrap, launch, and AI
  assistant behavior carefully
- keeping release notes and security documentation current

## Review Expectations

Changes that touch privileged operations should explain:

- what command or path handling changed
- how user approval remains explicit
- what tests or manual checks were run
- whether the AI assistant remains advisory only
