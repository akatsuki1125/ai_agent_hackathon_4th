#!/usr/bin/env bash
set -eu

BASE="$HOME/system_logs"
DATE="$(date +%F)"
TIME="$(date +%H%M)"

OUTDIR_SYSTEMD_RUNNING="$BASE/systemd/running/$DATE"
OUTDIR_SYSTEMD_ENABLED="$BASE/systemd/enabled/$DATE"
OUTDIR_APT_MANUAL="$BASE/apt/manual/$DATE"

# network
OUTDIR_NET_SOCKETS="$BASE/network/sockets/$DATE"
OUTDIR_NET_INTERFACES="$BASE/network/interfaces/$DATE"
OUTDIR_NET_ROUTES="$BASE/network/routes/$DATE"
OUTDIR_NET_STATS="$BASE/network/stats/$DATE"

OUTDIR_STORAGE_DF="$BASE/storage/df/$DATE"
OUTDIR_STORAGE_DFI="$BASE/storage/df-i/$DATE"

OUTDIR_CPU="$BASE/cpu/$DATE"

df -h > "$OUTDIR_STORAGE_DF/$TIME.txt"
df -i > "$OUTDIR_STORAGE_DFI/$TIME.txt"


mkdir -p \
  "$OUTDIR_SYSTEMD_RUNNING" \
  "$OUTDIR_SYSTEMD_ENABLED" \
  "$OUTDIR_APT_MANUAL" \
  "$OUTDIR_NET_SOCKETS" \
  "$OUTDIR_NET_INTERFACES" \
  "$OUTDIR_NET_ROUTES" \
  "$OUTDIR_NET_STATS" \
  "$OUTDIR_STORAGE_DF" \
  "$OUTDIR_STORAGE_DFI" \
  "$OUTDIR_CPU"

# systemd: running services
systemctl list-units --type=service --state=running \
  > "$OUTDIR_SYSTEMD_RUNNING/$TIME.txt"

# systemd: enabled services
systemctl list-unit-files --state=enabled \
  > "$OUTDIR_SYSTEMD_ENABLED/$TIME.txt"

# apt: manual packages
apt-mark showmanual | sort \
  > "$OUTDIR_APT_MANUAL/$TIME.txt"

# sockets
ss -tunap \
  > "$OUTDIR_NET_SOCKETS/$TIME.txt"

# interfaces
ip addr \
  > "$OUTDIR_NET_INTERFACES/$TIME.txt"

# routes
ip route \
  > "$OUTDIR_NET_ROUTES/$TIME.txt"

# kernel stats
{
  echo "### /proc/net/snmp"
  cat /proc/net/snmp
  echo
  echo "### /proc/net/netstat"
  cat /proc/net/netstat
} > "$OUTDIR_NET_STATS/$TIME.txt"

df -h > "$OUTDIR_STORAGE_DF/$TIME.txt"
df -i > "$OUTDIR_STORAGE_DFI/$TIME.txt"

# cpu stats
{
  echo "### uptime"
  uptime
  echo
  echo "### /proc/stat (cpu line)"
  grep '^cpu ' /proc/stat
  echo
  echo "### top5 cpu"
  ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 6
  echo
  echo "### top5 mem"
  ps -eo pid,comm,%mem,%cpu --sort=-%mem | head -n 6
} > "$OUTDIR_CPU/$TIME.txt"
