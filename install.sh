#!/bin/bash

set -e

echo "Installing CleanRoom..."

sudo mkdir -p /opt/cleanroom
sudo cp cleanroom.py /opt/cleanroom/
sudo chmod +x /opt/cleanroom/cleanroom.py

sudo cp com.cleanroom.app.desktop /usr/share/applications/

echo "Installation complete!"
echo "You can now launch CleanRoom from your application menu or run:"
echo "  python3 /opt/cleanroom/cleanroom.py"
