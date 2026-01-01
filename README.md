# CleanRoom

A lightweight GTK4 GUI for managing systemd-nspawn containers. Create isolated environments for testing software, experimenting with dependencies, or running untrusted code — without polluting your host system.

![CleanRoom Screenshot](screenshot.png)

## Features

- **Create Containers** — Quickly create new container directories
- **Bootstrap OS** — Install a minimal Linux distribution (Arch via `pacstrap` or Debian via `debootstrap`)
- **Launch Terminal** — Drop into an interactive shell inside any container
- **Delete Containers** — Remove containers with confirmation dialog
- **Status Indicators** — See at a glance which containers are ready vs empty

## Requirements

### System Dependencies

| Package | Purpose |
|---------|---------|
| `systemd-container` | Provides `systemd-nspawn` for running containers |
| `gtk4` | GUI toolkit |
| `python-gobject` | Python bindings for GTK4 |

### Optional (for bootstrapping)

| Package | Distribution |
|---------|--------------|
| `arch-install-scripts` | Arch Linux (provides `pacstrap`) |
| `debootstrap` | Debian/Ubuntu |

### Terminal Emulator

CleanRoom will auto-detect and use one of:
- `kitty`
- `alacritty`  
- `gnome-terminal`

## Installation

### Arch Linux

```bash
sudo pacman -S systemd gtk4 python-gobject arch-install-scripts
```

### Debian/Ubuntu

```bash
sudo apt install systemd-container gir1.2-gtk-4.0 python3-gi debootstrap
```

### Fedora

```bash
sudo dnf install systemd-container gtk4 python3-gobject
```

## Usage

```bash
python3 cleanroom.py
```

> **Note:** The application runs as a regular user but uses `sudo` internally for privileged operations. You may be prompted for your password.

### Workflow

1. **New** — Create a new container (just an empty directory)
2. **Bootstrap** — Select the container and install a minimal OS
3. **Launch Terminal** — Enter the container's shell
4. **Delete** — Remove when no longer needed

## How It Works

CleanRoom is a simple frontend for `systemd-nspawn`, which provides lightweight OS-level virtualization using Linux namespaces and cgroups. Unlike Docker, containers share the host kernel and have minimal overhead.

Containers are stored in `/var/lib/machines/` — the standard location for `systemd-nspawn` and `machinectl`.

## License

MIT License — see [LICENSE](LICENSE)

## Contributing

Pull requests welcome! Please open an issue first to discuss major changes.
