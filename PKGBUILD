pkgname=cleanroom
pkgver=1.0.0
pkgrel=1
pkgdesc="GTK4 GUI for managing systemd-nspawn containers"
arch=('any')
url="https://github.com/yourusername/cleanroom"
license=('MIT')
depends=('python' 'python-gobject' 'gtk4' 'systemd')
optdepends=(
    'arch-install-scripts: for bootstrapping Arch containers'
    'kitty: terminal emulator'
    'alacritty: terminal emulator'
    'gnome-terminal: terminal emulator'
)
source=("cleanroom.py" "com.cleanroom.app.desktop")
sha256sums=('SKIP' 'SKIP')

package() {
    install -Dm755 "$srcdir/cleanroom.py" "$pkgdir/opt/cleanroom/cleanroom.py"
    install -Dm644 "$srcdir/com.cleanroom.app.desktop" "$pkgdir/usr/share/applications/com.cleanroom.app.desktop"
}
