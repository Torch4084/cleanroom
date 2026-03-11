# CleanRoom

CleanRoom is a GTK4 desktop application for managing `systemd-nspawn` containers without dropping down to raw shell commands for every task.

It is aimed at developers, tinkerers, and security-minded Linux users who want lightweight isolated environments for testing packages, reproducing issues, or experimenting without polluting the host system.

## What it does

- Create new container directories under `/var/lib/machines`
- Bootstrap Arch or Debian-based roots with `pacstrap` or `debootstrap`
- Launch an interactive shell inside a selected container
- Delete containers with confirmation
- Show whether a container looks ready or still empty

## Requirements

### Runtime dependencies

- `python`
- `python-gobject`
- `gtk4`
- `libadwaita`
- `systemd-container`

### Optional bootstrap tools

- `arch-install-scripts` for `pacstrap`
- `debootstrap` for Debian-based roots

### Supported terminal launchers

CleanRoom currently looks for one of:

- `kitty`
- `alacritty`
- `gnome-terminal`

## Installation

### Run from source

```bash
python3 cleanroom.py
```

### System install

```bash
chmod +x install.sh
./install.sh
```

### Arch packaging

The repository includes a `PKGBUILD` for packaging on Arch-based systems.

## Workflow

1. Create a new container entry.
2. Bootstrap it with a base distribution.
3. Launch a terminal inside the container.
4. Delete the container when you are done with it.

## Notes

- CleanRoom shells out to `sudo` for privileged operations.
- Containers live in `/var/lib/machines` by default.
- This project is intentionally small and focused on the most common `systemd-nspawn` workflows.

## Contributing

Bug reports, packaging fixes, and UI improvements are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

CleanRoom is released under the [MIT License](LICENSE).
