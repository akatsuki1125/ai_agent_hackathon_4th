#!/usr/bin/env bash
set -eu

BASE="$HOME/system_logs"
DATE="$(date +%F)"
TIME="$(date +%H%M)"

OUTDIR_SYSTEMD_RUNNING="$BASE/systemd/running/$DATE"
OUTDIR_SYSTEMD_ENABLED="$BASE/systemd/enabled/$DATE"
OUTDIR_APT_MANUAL="$BASE/apt/manual/$DATE"

mkdir -p \
  "$OUTDIR_SYSTEMD_RUNNING" \
  "$OUTDIR_SYSTEMD_ENABLED" \
  "$OUTDIR_APT_MANUAL"

# systemd: running services
systemctl list-units --type=service --state=running \
  > "$OUTDIR_SYSTEMD_RUNNING/$TIME.txt"

# systemd: enabled services
systemctl list-unit-files --state=enabled \
  > "$OUTDIR_SYSTEMD_ENABLED/$TIME.txt"

# apt: manual packages
apt-mark showmanual | sort \
  > "$OUTDIR_APT_MANUAL/$TIME.txt"