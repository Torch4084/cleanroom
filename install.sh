#!/usr/bin/env bash

set -euo pipefail

echo "Installing CleanRoom..."

sudo install -d /usr/local/share/cleanroom
sudo install -m 755 cleanroom.py /usr/local/share/cleanroom/cleanroom.py
sudo install -m 644 com.cleanroom.app.desktop /usr/share/applications/com.cleanroom.app.desktop
sudo install -d /usr/local/bin
printf '#!/usr/bin/env bash\nexec python3 /usr/local/share/cleanroom/cleanroom.py "$@"\n' \
    | sudo tee /usr/local/bin/cleanroom >/dev/null
sudo chmod 755 /usr/local/bin/cleanroom

echo "Installation complete!"
echo "You can now launch CleanRoom from your application menu or run:"
echo "  cleanroom"
