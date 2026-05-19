pkgname=cleanroom
pkgver=1.1.0
pkgrel=1
pkgdesc="GTK4 GUI for managing systemd-nspawn containers"
arch=('any')
url="https://github.com/Torch4084/cleanroom"
license=('MIT')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'systemd')
optdepends=(
    'arch-install-scripts: for bootstrapping Arch containers'
    'debootstrap: for bootstrapping Debian containers'
    'konsole: terminal emulator'
    'kitty: terminal emulator'
    'alacritty: terminal emulator'
    'gnome-terminal: terminal emulator'
)
source=("cleanroom.py" "cleanroom_core.py" "com.cleanroom.app.desktop")
sha256sums=('SKIP' 'SKIP' 'SKIP')

package() {
    install -Dm755 "$srcdir/cleanroom.py" "$pkgdir/usr/local/share/cleanroom/cleanroom.py"
    install -Dm644 "$srcdir/cleanroom_core.py" "$pkgdir/usr/local/share/cleanroom/cleanroom_core.py"
    install -Dm755 /dev/stdin "$pkgdir/usr/local/bin/cleanroom" <<'EOF'
#!/usr/bin/env bash
exec python3 /usr/local/share/cleanroom/cleanroom.py "$@"
EOF
    install -Dm644 "$srcdir/com.cleanroom.app.desktop" "$pkgdir/usr/share/applications/com.cleanroom.app.desktop"
}
