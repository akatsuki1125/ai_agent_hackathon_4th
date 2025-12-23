#!/usr/bin/env bash
# Session-only logger: records terminal I/O via `script` without JSON logs.

vps_session_start() {
  local log_dir log_file
  if [[ "${VPS_SESSION_ACTIVE:-}" == "1" ]]; then
    return 0
  fi
  export VPS_SESSION_ACTIVE="1"
  log_dir="${VPS_LOG_DIR:-$HOME/vps_checker_logs}"
  mkdir -p "$log_dir"
  log_file="${log_dir}/session_$(date +%Y%m%dT%H%M%S)_$$.log"

  echo "starting session log: $log_file" >&2
  exec env TERM=dumb LS_COLORS= script -q -f "$log_file"
}
