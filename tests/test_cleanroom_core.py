import pytest

from cleanroom_core import (
    build_ai_prompt,
    build_bootstrap_command,
    build_launch_command,
    container_path,
    validate_container_name,
)


@pytest.mark.parametrize('name', ['arch', 'debian_12', 'lab.vm', 'test-env'])
def test_valid_container_names(name):
    assert validate_container_name(name) is None


@pytest.mark.parametrize(
    'name',
    ['', '.', '..', '../host', 'bad/name', 'name with spaces', '$(id)'],
)
def test_invalid_container_names(name):
    assert validate_container_name(name) is not None


def test_container_path_rejects_invalid_name():
    with pytest.raises(ValueError):
        container_path('/var/lib/machines', '../host')


def test_container_path_joins_valid_name():
    assert container_path('/var/lib/machines', 'arch') == '/var/lib/machines/arch'


def test_launch_command_quotes_machines_path():
    command = build_launch_command('/tmp/clean room/test-env')
    assert "sudo systemd-nspawn -D '/tmp/clean room/test-env' /bin/bash" in command


def test_bootstrap_command_quotes_machines_path():
    command = build_bootstrap_command('debootstrap', '/tmp/clean room/debian')
    assert "sudo debootstrap stable '/tmp/clean room/debian'" in command


def test_bootstrap_command_rejects_unknown_tool():
    with pytest.raises(ValueError):
        build_bootstrap_command('curl', '/tmp/container')


def test_ai_prompt_preserves_advisory_sections():
    prompt = build_ai_prompt('Python package testing', 'arch', '/var/lib/machines')
    assert 'systemd-nspawn container' in prompt
    assert 'Security notes' in prompt
    assert 'Python package testing' in prompt
