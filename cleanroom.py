#!/usr/bin/env python3

import gi
import os
import subprocess
import shutil

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, GLib

class CleanRoom(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.cleanroom.app', flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.machines_path = '/var/lib/machines/'
        self.window = None
        self.listbox = None

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

        bootstrap_button = Gtk.Button(label='Bootstrap')
        bootstrap_button.connect('clicked', self.on_bootstrap_clicked)
        header.pack_start(bootstrap_button)

        launch_button = Gtk.Button(label='Launch Terminal')
        launch_button.connect('clicked', self.on_launch_clicked)
        header.pack_start(launch_button)

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

        self.window.set_child(scrolled)
        self.refresh_container_list()
        self.window.present()

    def refresh_container_list(self):
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
                        check = self.run_command(['sudo', 'test', '-d', full_path], check=False)
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
            except Exception:
                pass

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

    def run_command(self, command, check=True):
        return subprocess.run(command, capture_output=True, text=True, check=check)

    def open_terminal(self, shell_command):
        terminal = self.detect_terminal()
        if terminal is None:
            self.show_error(
                'No terminal launcher found',
                'Install kitty, alacritty, or gnome-terminal to launch container actions.',
            )
            return False

        if terminal == 'kitty':
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

    def get_selected_container(self):
        row = self.listbox.get_selected_row()
        if row is not None:
            label = row.get_child()
            if label is not None:
                text = label.get_text()
                return text.split(' [')[0]
        return None

    def detect_terminal(self):
        terminals = ['kitty', 'alacritty', 'gnome-terminal']
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
                    container_path = os.path.join(self.machines_path, name)
                    try:
                        subprocess.run(['sudo', 'mkdir', '-p', container_path], check=True)
                        self.refresh_container_list()
                    except Exception:
                        pass
            d.destroy()

        dialog.connect('response', on_response)
        dialog.present()

    def on_bootstrap_clicked(self, button):
        selected = self.get_selected_container()
        if selected is None:
            self.show_error('No container selected', 'Select a container before bootstrapping it.')
            return

        container_path = os.path.join(self.machines_path, selected)
        
        if shutil.which('pacstrap'):
            bootstrap_cmd = f'sudo pacstrap -c {container_path} base; echo "\\n\\nBootstrap complete. Press Enter to close."; read'
        elif shutil.which('debootstrap'):
            bootstrap_cmd = f'sudo debootstrap stable {container_path}; echo "\\n\\nBootstrap complete. Press Enter to close."; read'
        else:
            bootstrap_cmd = 'echo "No bootstrap tool found (need pacstrap or debootstrap)"; read'

        self.open_terminal(bootstrap_cmd)

    def on_launch_clicked(self, button):
        selected = self.get_selected_container()
        if selected is None:
            self.show_error('No container selected', 'Select a container before launching it.')
            return

        container_path = os.path.join(self.machines_path, selected)
        nspawn_cmd = f'sudo systemd-nspawn -D {container_path} /bin/bash; echo "\\n\\nContainer exited. Press Enter to close."; read'
        self.open_terminal(nspawn_cmd)

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
                container_path = os.path.join(self.machines_path, selected)
                try:
                    subprocess.run(['sudo', 'rm', '-rf', container_path], check=True)
                    self.refresh_container_list()
                except Exception:
                    pass
            d.destroy()

        dialog.connect('response', on_response)
        dialog.present()


def main():
    app = CleanRoom()
    app.run(None)


if __name__ == '__main__':
    main()
