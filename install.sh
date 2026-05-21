#!/usr/bin/env bash

set -euo pipefail

install_prefix="/usr/local/share/cleanroom"
launcher_path="/usr/local/bin/cleanroom"
desktop_path="/usr/share/applications/com.cleanroom.app.desktop"

usage() {
    cat <<'EOF'
Usage: ./install.sh [install|uninstall|reinstall|--help]

Commands:
  install     Install CleanRoom files and launcher
  uninstall   Remove installed CleanRoom files and launcher
  reinstall   Uninstall, then install again
  --help      Show this help text

Running without a command defaults to: install
EOF
}

install_cleanroom() {
    echo "Installing CleanRoom..."

    sudo install -d "$install_prefix"
    sudo install -m 755 cleanroom.py "$install_prefix/cleanroom.py"
    sudo install -m 644 cleanroom_core.py "$install_prefix/cleanroom_core.py"
    sudo install -m 644 cleanroom.png "/usr/share/pixmaps/cleanroom.png"
    sudo install -d "/usr/share/icons/hicolor/scalable/apps"
    sudo install -m 644 cleanroom.png "/usr/share/icons/hicolor/scalable/apps/cleanroom.png"
    sudo install -m 644 com.cleanroom.app.desktop "$desktop_path"
    sudo install -d /usr/local/bin
    printf '#!/usr/bin/env bash\nexec python3 /usr/local/share/cleanroom/cleanroom.py "$@"\n' \
        | sudo tee "$launcher_path" >/dev/null
    sudo chmod 755 "$launcher_path"

    echo "Installation complete!"
    echo "You can now launch CleanRoom from your application menu or run:"
    echo "  cleanroom"
}

uninstall_cleanroom() {
    echo "Removing CleanRoom..."

    sudo rm -f "$launcher_path"
    sudo rm -f "$desktop_path"
    sudo rm -f "/usr/share/pixmaps/cleanroom.png"
    sudo rm -f "/usr/share/icons/hicolor/scalable/apps/cleanroom.png"
    sudo rm -f "$install_prefix/cleanroom.py"
    sudo rm -f "$install_prefix/cleanroom_core.py"
    sudo rmdir "$install_prefix" 2>/dev/null || true

    echo "Uninstall complete."
}

reinstall_cleanroom() {
    uninstall_cleanroom
    install_cleanroom
}

command="${1:-install}"

case "$command" in
    install)
        install_cleanroom
        ;;
    uninstall)
        uninstall_cleanroom
        ;;
    reinstall)
        reinstall_cleanroom
        ;;
    --help|-h|help)
        usage
        ;;
    *)
        echo "Unknown command: $command" >&2
        usage >&2
        exit 1
        ;;
esac
