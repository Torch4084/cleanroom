import os
import re
import shlex

CONTAINER_NAME_PATTERN = re.compile(r'[a-zA-Z0-9._-]+')


def validate_container_name(name):
    if not name:
        return 'Container name cannot be empty.'
    if not CONTAINER_NAME_PATTERN.fullmatch(name):
        return 'Use only letters, numbers, dots, underscores, and dashes.'
    if name in {'.', '..'}:
        return 'Reserved path names are not allowed.'
    return None


def container_path(machines_path, container_name):
    validation_error = validate_container_name(container_name)
    if validation_error:
        raise ValueError(validation_error)
    return os.path.join(machines_path, container_name)


def build_bootstrap_command(tool, target_path):
    quoted_path = shlex.quote(target_path)
    if tool == 'pacstrap':
        bootstrap = f'sudo pacstrap -c {quoted_path} base'
    elif tool == 'debootstrap':
        bootstrap = f'sudo debootstrap stable {quoted_path}'
    else:
        raise ValueError(f'Unsupported bootstrap tool: {tool}')
    return f'{bootstrap}; echo "\\n\\nBootstrap complete. Press Enter to close."; read'


def build_launch_command(target_path):
    quoted_path = shlex.quote(target_path)
    return (
        f'sudo systemd-nspawn -D {quoted_path} /bin/bash; '
        'echo "\\n\\nContainer exited. Press Enter to close."; read'
    )


def build_ai_prompt(user_goal, selected_container, machines_path):
    container_text = selected_container or 'No existing container selected'
    return (
        'Help me prepare a systemd-nspawn container for this goal.\n\n'
        f'Goal: {user_goal}\n'
        f'Selected container: {container_text}\n'
        f'Machines path: {machines_path}\n\n'
        'Return a concise plan with these sections:\n'
        '1. Recommended base distro\n'
        '2. Bootstrap approach\n'
        '3. Packages to install\n'
        '4. Suggested commands\n'
        '5. Validation steps\n'
        '6. Security notes\n'
    )
