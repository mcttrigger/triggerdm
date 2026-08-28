#!/bin/bash
# Install triggerdm as a systemd service. Run as root.
set -e
cd "$(dirname "$0")"
pkill -f /triggerdm || true
sleep 1
install -m 755 triggerdm /usr/local/sbin/triggerdm
install -m 644 triggerdm-linux.service /etc/systemd/system/triggerdm.service
systemctl daemon-reload
systemctl enable --now triggerdm.service
systemctl status triggerdm --no-pager | head -8
