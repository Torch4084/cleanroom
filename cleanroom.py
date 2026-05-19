#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import threading
import urllib.error
import urllib.request

import gi

from cleanroom_core import (
    build_ai_prompt,
    build_bootstrap_command,
    build_launch_command,
    container_path,
    validate_container_name,
)

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gio, GLib, Gtk  # noqa: E402


class CleanRoom(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.cleanroom.app', flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.machines_path = os.environ.get('CLEANROOM_MACHINES_PATH', '/var/lib/machines/')
        self.window = None
        self.listbox = None
        self.status_label = None
        self.ai_api_key = os.environ.get('CLEANROOM_AI_API_KEY', '').strip()
        self.ai_base_url = os.environ.get('CLEANROOM_AI_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
        self.ai_model = os.environ.get('CLEANROOM_AI_MODEL', 'gpt-5-mini')
        self.ai_org = os.environ.get('OPENAI_ORGANIZATION', '').strip()
        self.ai_project = os.environ.get('OPENAI_PROJECT', '').strip()

    def validate_container_name(self, name):
        return validate_container_name(name)

    def get_bootstrap_options(self):
        options = []
        if shutil.which('pacstrap'):
            options.append(
                (
                    'Arch Linux',
                    'pacstrap',
                )
            )
        if shutil.which('debootstrap'):
            options.append(
                (
                    'Debian stable',
                    'debootstrap',
                )
            )
        return options

    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title('CleanRoom')
        self.window.set_default_size(500, 400)

        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)

        title_label = Gtk.Label(label='CleanRoom')
        title_label.add_css_class('title')
        header.set_title_widget(title_label)

        new_button = Gtk.Button(label='New')
        new_button.connect('clicked', self.on_new_clicked)
        header.pack_start(new_button)

        refresh_button = Gtk.Button(label='Refresh')
        refresh_button.connect('clicked', self.on_refresh_clicked)
        header.pack_start(refresh_button)

        bootstrap_button = Gtk.Button(label='Bootstrap')
        bootstrap_button.connect('clicked', self.on_bootstrap_clicked)
        header.pack_start(bootstrap_button)

        launch_button = Gtk.Button(label='Launch Terminal')
        launch_button.connect('clicked', self.on_launch_clicked)
        header.pack_start(launch_button)

        ai_button = Gtk.Button(label='AI Assist')
        ai_button.connect('clicked', self.on_ai_assist_clicked)
        header.pack_end(ai_button)

        delete_button = Gtk.Button(label='Delete')
        delete_button.connect('clicked', self.on_delete_clicked)
        header.pack_end(delete_button)

        self.window.set_titlebar(header)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        scrolled.set_child(self.listbox)

        self.status_label = Gtk.Label()
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.set_margin_start(12)
        self.status_label.set_margin_end(12)
        self.status_label.set_margin_top(8)
        self.status_label.set_margin_bottom(8)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.append(scrolled)
        content.append(self.status_label)

        self.window.set_child(content)
        self.refresh_container_list()
        self.window.present()

    def refresh_container_list(self):
        container_count = 0
        while True:
            row = self.listbox.get_row_at_index(0)
            if row is None:
                break
            self.listbox.remove(row)

        if os.path.isdir(self.machines_path):
            try:
                result = self.run_command(['sudo', 'ls', self.machines_path])
                entries = sorted(result.stdout.strip().split('\n')) if result.stdout.strip() else []
                for entry in entries:
                    if entry:
                        full_path = os.path.join(self.machines_path, entry)
                        self.run_command(['sudo', 'test', '-d', full_path], check=False)
                        has_bin = self.run_command(
                            ['sudo', 'test', '-d', os.path.join(full_path, 'bin')],
                            check=False,
                        )
                        status = ' [ready]' if has_bin.returncode == 0 else ' [empty]'
                        label = Gtk.Label(label=entry + status)
                        label.set_halign(Gtk.Align.START)
                        label.set_margin_start(10)
                        label.set_margin_end(10)
                        label.set_margin_top(8)
                        label.set_margin_bottom(8)
                        self.listbox.append(label)
                        container_count += 1
            except Exception:
                pass
        self.update_status(f'{container_count} container(s) in {self.machines_path}')

    def show_message(self, title, body, message_type=Gtk.MessageType.INFO):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            modal=True,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=title,
            secondary_text=body,
        )
        dialog.connect('response', lambda d, _response: d.destroy())
        dialog.present()

    def show_error(self, title, body):
        self.show_message(title, body, Gtk.MessageType.ERROR)

    def update_status(self, text):
        if self.status_label is not None:
            self.status_label.set_text(text)

    def run_command(self, command, check=True):
        return subprocess.run(command, capture_output=True, text=True, check=check)

    def has_ai_support(self):
        return bool(self.ai_api_key)

    def build_ai_prompt(self, user_goal, selected_container):
        return build_ai_prompt(user_goal, selected_container, self.machines_path)

    def request_ai_plan(self, user_goal, selected_container):
        payload = json.dumps(
            {
                'model': self.ai_model,
                'instructions': (
                    'You are helping a Linux desktop application called CleanRoom. '
                    'Provide practical, conservative guidance for setting up '
                    'systemd-nspawn containers. Never assume Docker. Keep commands '
                    'safe, explicit, and easy to review.'
                ),
                'input': self.build_ai_prompt(user_goal, selected_container),
            }
        ).encode('utf-8')

        request = urllib.request.Request(
            f'{self.ai_base_url}/responses',
            data=payload,
            headers={
                'Authorization': f'Bearer {self.ai_api_key}',
                'Content-Type': 'application/json',
                **({'OpenAI-Organization': self.ai_org} if self.ai_org else {}),
                **({'OpenAI-Project': self.ai_project} if self.ai_project else {}),
            },
            method='POST',
        )

        with urllib.request.urlopen(request, timeout=45) as response:
            raw_body = response.read().decode('utf-8')

        data = json.loads(raw_body)
        output_text = data.get('output_text', '').strip()
        if output_text:
            return output_text

        parts = []
        for item in data.get('output', []):
            for content in item.get('content', []):
                if content.get('type') == 'output_text' and content.get('text'):
                    parts.append(content['text'])
        return '\n'.join(parts).strip() or 'No response text was returned.'

    def open_terminal(self, shell_command):
        terminal = self.detect_terminal()
        if terminal is None:
            self.show_error(
                'No terminal launcher found',
                'Install konsole, kitty, alacritty, or gnome-terminal to launch container actions.',
            )
            return False
        if terminal == 'konsole':
            cmd = ['konsole', '-e', 'bash', '-c', shell_command]
        elif terminal == 'kitty':
            cmd = ['kitty', '-e', 'bash', '-c', shell_command]
        elif terminal == 'alacritty':
            cmd = ['alacritty', '-e', 'bash', '-c', shell_command]
        else:
            cmd = ['gnome-terminal', '--', 'bash', '-c', shell_command]

        try:
            subprocess.Popen(cmd)
            return True
        except Exception as exc:
            self.show_error('Failed to launch terminal', str(exc))
            return False

    def confirm_terminal_command(self, title, intro, shell_command):
        dialog = Gtk.Dialog(transient_for=self.window, modal=True)
        dialog.set_title(title)
        dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        dialog.add_button('Run in Terminal', Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        content.set_margin_start(10)
        content.set_margin_end(10)
        content.set_spacing(10)

        intro_label = Gtk.Label(label=intro)
        intro_label.set_wrap(True)
        intro_label.set_halign(Gtk.Align.START)
        content.append(intro_label)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(140)
        scrolled.set_hexpand(True)

        command_view = Gtk.TextView()
        command_view.set_editable(False)
        command_view.set_cursor_visible(False)
        command_view.set_monospace(True)
        command_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        command_view.get_buffer().set_text(shell_command)
        scrolled.set_child(command_view)
        content.append(scrolled)

        warning = Gtk.Label(
            label='Review this command before continuing. It may request sudo privileges.',
        )
        warning.set_wrap(True)
        warning.set_halign(Gtk.Align.START)
        content.append(warning)

        def on_response(d, response):
            if response == Gtk.ResponseType.OK:
                self.open_terminal(shell_command)
            d.destroy()

        dialog.connect('response', on_response)
        dialog.present()

    def get_selected_container(self):
        row = self.listbox.get_selected_row()
        if row is not None:
            label = row.get_child()
            if label is not None:
                text = label.get_text()
                return text.split(' [')[0]
        return None

    def detect_terminal(self):
        terminals = ['konsole', 'kitty', 'alacritty', 'gnome-terminal']
        for term in terminals:
            if shutil.which(term):
                return term
        return None

    def on_new_clicked(self, button):
        dialog = Gtk.Dialog(transient_for=self.window, modal=True)
        dialog.set_title('New Container')
        dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        dialog.add_button('Create', Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        content.set_margin_start(10)
        content.set_margin_end(10)
        content.set_spacing(10)

        label = Gtk.Label(label='Enter container name:')
        content.append(label)

        entry = Gtk.Entry()
        entry.set_activates_default(True)
        content.append(entry)

        dialog.set_default_response(Gtk.ResponseType.OK)

        def on_response(d, response):
            if response == Gtk.ResponseType.OK:
                name = entry.get_text().strip()
                if name:
                    validation_error = self.validate_container_name(name)
                    if validation_error:
                        self.show_error('Invalid container name', validation_error)
                        d.destroy()
                        return

                    target_path = container_path(self.machines_path, name)
                    try:
                        exists = self.run_command(
                            ['sudo', 'test', '-e', target_path],
                            check=False,
                        )
                        if exists.returncode == 0:
                            self.show_error(
                                'Container already exists',
                                f'A container named "{name}" already exists.',
                            )
                            d.destroy()
                            return

                        self.run_command(['sudo', 'mkdir', '-p', target_path])
                        self.refresh_container_list()
                    except subprocess.CalledProcessError as exc:
                        details = exc.stderr.strip() or str(exc)
                        self.show_error('Failed to create container', details)
            d.destroy()

        dialog.connect('response', on_response)
        dialog.present()

    def on_bootstrap_clicked(self, button):
        selected = self.get_selected_container()
        if selected is None:
            self.show_error('No container selected', 'Select a container before bootstrapping it.')
            return

        target_path = container_path(self.machines_path, selected)
        options = self.get_bootstrap_options()
        if not options:
            self.show_error(
                'No bootstrap tool found',
                'Install arch-install-scripts or debootstrap before bootstrapping a container.',
            )
            return

        dialog = Gtk.Dialog(transient_for=self.window, modal=True)
        dialog.set_title('Choose bootstrap source')
        dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        dialog.add_button('Start', Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        content.set_margin_start(10)
        content.set_margin_end(10)
        content.set_spacing(10)

        label = Gtk.Label(label=f'Bootstrap "{selected}" with:')
        label.set_halign(Gtk.Align.START)
        content.append(label)

        combo = Gtk.ComboBoxText()
        for display_name, _template in options:
            combo.append_text(display_name)
        combo.set_active(0)
        content.append(combo)

        def on_response(d, response):
            if response == Gtk.ResponseType.OK:
                selected_option = combo.get_active()
                if selected_option is None or selected_option < 0:
                    self.show_error(
                        'No bootstrap source selected',
                        'Choose a bootstrap source first.',
                    )
                    d.destroy()
                    return

                _display_name, tool = options[selected_option]
                command = build_bootstrap_command(tool, target_path)
                self.confirm_terminal_command(
                    'Review bootstrap command',
                    f'CleanRoom will bootstrap "{selected}" using {tool}.',
                    command,
                )
            d.destroy()

        dialog.connect('response', on_response)
        dialog.present()

    def on_refresh_clicked(self, button):
        self.refresh_container_list()

    def on_ai_assist_clicked(self, button):
        selected = self.get_selected_container()

        dialog = Gtk.Dialog(transient_for=self.window, modal=True)
        dialog.set_title('AI Container Assistant')
        dialog.add_button('Close', Gtk.ResponseType.CLOSE)
        generate_button = dialog.add_button('Generate', Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        content.set_margin_start(10)
        content.set_margin_end(10)
        content.set_spacing(10)

        intro = Gtk.Label(
            label='Describe what you want the container to be used for. '
            'The assistant will suggest a setup plan but will not make changes automatically.'
        )
        intro.set_wrap(True)
        intro.set_halign(Gtk.Align.START)
        content.append(intro)

        context_label = Gtk.Label(
            label=f'Selected container: {selected or "none"}',
        )
        context_label.set_halign(Gtk.Align.START)
        content.append(context_label)

        goal_entry = Gtk.Entry()
        goal_entry.set_placeholder_text(
            'Example: Python malware analysis lab with curl, git, and strace'
        )
        goal_entry.set_activates_default(True)
        content.append(goal_entry)

        setup_label = Gtk.Label(
            label=(
                'Set CLEANROOM_AI_API_KEY to enable AI suggestions. '
                'Optional: CLEANROOM_AI_MODEL, CLEANROOM_AI_BASE_URL, '
                'OPENAI_ORGANIZATION, OPENAI_PROJECT.'
            ),
        )
        setup_label.set_wrap(True)
        setup_label.set_halign(Gtk.Align.START)
        content.append(setup_label)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(260)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        result_view = Gtk.TextView()
        result_view.set_editable(False)
        result_view.set_cursor_visible(False)
        result_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        result_buffer = result_view.get_buffer()
        result_buffer.set_text(
            'AI suggestions are disabled until CLEANROOM_AI_API_KEY is configured.'
            if not self.has_ai_support()
            else 'Enter a goal and click Generate.'
        )
        scrolled.set_child(result_view)
        content.append(scrolled)

        def set_result(text):
            result_buffer.set_text(text)

        def run_generation():
            user_goal = goal_entry.get_text().strip()
            if not user_goal:
                set_result('Enter a goal first.')
                return

            if not self.has_ai_support():
                set_result(
                    'AI suggestions are not configured.\n\n'
                    'Set CLEANROOM_AI_API_KEY and restart CleanRoom to enable this feature.'
                )
                return

            generate_button.set_sensitive(False)
            set_result('Generating setup plan...')

            def worker():
                try:
                    plan = self.request_ai_plan(user_goal, selected)
                except urllib.error.HTTPError as exc:
                    details = exc.read().decode('utf-8', errors='replace').strip()
                    message = f'API request failed ({exc.code}).\n\n{details or exc.reason}'
                except Exception as exc:
                    message = f'Failed to generate AI suggestion.\n\n{exc}'
                else:
                    message = plan

                GLib.idle_add(set_result, message)
                GLib.idle_add(generate_button.set_sensitive, True)

            threading.Thread(target=worker, daemon=True).start()

        def on_response(d, response):
            if response == Gtk.ResponseType.OK:
                run_generation()
                return
            d.destroy()

        dialog.connect('response', on_response)
        dialog.present()

    def on_launch_clicked(self, button):
        selected = self.get_selected_container()
        if selected is None:
            self.show_error('No container selected', 'Select a container before launching it.')
            return

        target_path = container_path(self.machines_path, selected)
        self.confirm_terminal_command(
            'Review launch command',
            f'CleanRoom will launch an interactive shell inside "{selected}".',
            build_launch_command(target_path),
        )

    def on_delete_clicked(self, button):
        selected = self.get_selected_container()
        if selected is None:
            return

        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f'Are you sure you want to delete {selected}?'
        )

        def on_response(d, response):
            if response == Gtk.ResponseType.YES:
                target_path = container_path(self.machines_path, selected)
                try:
                    self.run_command(['sudo', 'rm', '-rf', target_path])
                    self.refresh_container_list()
                except subprocess.CalledProcessError as exc:
                    details = exc.stderr.strip() or str(exc)
                    self.show_error('Failed to delete container', details)
            d.destroy()

        dialog.connect('response', on_response)
        dialog.present()


def main():
    app = CleanRoom()
    app.run(None)


if __name__ == '__main__':
    main()
