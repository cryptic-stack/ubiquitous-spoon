#!/usr/bin/env sh

if [ ! -f /etc/sentinelmesh/profile ]; then
  cat <<'EOF'

SentinelMesh NSM setup is not complete.

Run:

  sudo sm-setup

EOF
fi
