# Distribution Workflows

CleanRoom is intentionally small: it creates container roots, bootstraps them with common
host tools, and launches `systemd-nspawn` in a terminal after showing the command that will
run.

## Arch Linux Hosts

Install the runtime and bootstrap dependencies:

```bash
sudo pacman -S python python-gobject gtk4 libadwaita systemd arch-install-scripts
```

CleanRoom uses `pacstrap` when it is available. New container roots are created under
`/var/lib/machines` unless `CLEANROOM_MACHINES_PATH` is set.

## Debian And Ubuntu Hosts

Install the runtime and bootstrap dependencies:

```bash
sudo apt install python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 systemd-container debootstrap
```

CleanRoom uses `debootstrap stable` when `debootstrap` is available. Review the generated
command before continuing, especially if your host distribution expects a specific release
name instead of `stable`.

## Terminal Launchers

CleanRoom currently detects these terminal launchers:

- `kitty`
- `alacritty`
- `gnome-terminal`

Bootstrap and launch operations open in a terminal so `sudo` prompts, long-running output,
and exit status are visible to the user.

## Permission Notes

The default machines directory is `/var/lib/machines`, which usually requires elevated
permissions. CleanRoom does not bypass host policy; privileged actions still go through
`sudo` and require the user to approve the command preview first.
