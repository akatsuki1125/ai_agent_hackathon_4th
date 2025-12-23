#!/usr/bin/env bash
set -eu

BASE="$HOME/system_logs"
TODAY="$(date +%F)"
YESTERDAY="$(date -d 'yesterday' +%F)"

ALERTS="$BASE/ALERTS.log"
DIFFDIR="$BASE/diffs"

# 比較対象（02:00の基準ファイル）
ENABLED_Y="$BASE/systemd/enabled/$YESTERDAY/0200.txt"
ENABLED_T="$BASE/systemd/enabled/$TODAY/0200.txt"
RUNNING_Y="$BASE/systemd/running/$YESTERDAY/0200.txt"
RUNNING_T="$BASE/systemd/running/$TODAY/0200.txt"

# network（interfaces/routes は自動diff向き）
NET_IF_Y="$BASE/network/interfaces/$YESTERDAY/0200.txt"
NET_IF_T="$BASE/network/interfaces/$TODAY/0200.txt"
NET_ROUTE_Y="$BASE/network/routes/$YESTERDAY/0200.txt"
NET_ROUTE_T="$BASE/network/routes/$TODAY/0200.txt"

# storage（df / df-i は事故検知に強い）
DF_Y="$BASE/storage/df/$YESTERDAY/0200.txt"
DF_T="$BASE/storage/df/$TODAY/0200.txt"
DFI_Y="$BASE/storage/df-i/$YESTERDAY/0200.txt"
DFI_T="$BASE/storage/df-i/$TODAY/0200.txt"

mkdir -p "$DIFFDIR"

diff_one () {
  local name="$1"
  local a="$2"
  local b="$3"
  local out="$DIFFDIR/${TODAY}.${name}.diff"

  # ファイルが無い場合（初日など）は静かに終了
  if [[ ! -f "$a" || ! -f "$b" ]]; then
    echo "[$(date '+%F %T')] SKIP ${name} (missing input: $a or $b)" >> "$ALERTS"
    return 0
  fi

  # diffが空なら何もしない
  if diff -u "$a" "$b" > "$out"; then
    rm -f "$out"
    return 0
  else
    # 差分があった：diffを残し、alertsに追記
    echo "[$(date '+%F %T')] CHANGE ${name} -> $out" >> "$ALERTS"
    return 0
  fi
}

diff_one "systemd-enabled" "$ENABLED_Y" "$ENABLED_T"
diff_one "systemd-running" "$RUNNING_Y" "$RUNNING_T"

diff_one "net-interfaces" "$NET_IF_Y" "$NET_IF_T"
diff_one "net-routes" "$NET_ROUTE_Y" "$NET_ROUTE_T"

diff_one "storage-df" "$DF_Y" "$DF_T"
diff_one "storage-df-i" "$DFI_Y" "$DFI_T"
