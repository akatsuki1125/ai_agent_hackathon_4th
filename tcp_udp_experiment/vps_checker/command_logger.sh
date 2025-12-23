#!/usr/bin/env bash
# This file is meant to be sourced; avoid changing shell options globally.

# Enable command logging in the current bash session.
# Usage: source /path/to/command_logger.sh && vps_log_enable

__vps_json_escape() {
  python3 - <<'PY'
import json
import sys
sys.stdout.write(json.dumps(sys.stdin.read())[1:-1])
PY
}

__vps_trim_file_lines() {
  local file="$1"
  local max="${2:-${VPS_LOG_MAX_LINES:-100}}"
  awk -v max="$max" 'NR<=max {print} NR==max+1 {print "[...truncated...]"; exit}' "$file"
}

__vps_write_json_entry() {
  local ts cwd exit_status cmd stdin_data stdout_data stderr_data log_dir log_file
  ts="$1"
  cwd="$2"
  exit_status="$3"
  cmd="$4"
  stdin_data="$5"
  stdout_data="$6"
  stderr_data="$7"
  log_dir="${VPS_LOG_DIR:-$HOME/vps_checker_logs}"
  log_file="${log_dir}/command_${ts}_$$.json"

  mkdir -p "$log_dir"
  printf '{' > "$log_file"
  printf '"ts":"%s",' "$(__vps_json_escape <<<"$ts")" >> "$log_file"
  printf '"cwd":"%s",' "$(__vps_json_escape <<<"$cwd")" >> "$log_file"
  printf '"exit":%s,' "$exit_status" >> "$log_file"
  printf '"cmd":"%s",' "$(__vps_json_escape <<<"$cmd")" >> "$log_file"
  printf '"std_in":"%s",' "$(__vps_json_escape <<<"$stdin_data")" >> "$log_file"
  printf '"std_out":"%s",' "$(__vps_json_escape <<<"$stdout_data")" >> "$log_file"
  printf '"std_err":"%s"' "$(__vps_json_escape <<<"$stderr_data")" >> "$log_file"
  printf '}\n' >> "$log_file"
}

__vps_log_prompt_command() {
  local exit_status=$?
  local hist cmd ts cwd

  hist="$(history 1)"
  cmd="$(printf '%s' "$hist" | sed 's/^[ ]*[0-9]\+[ ]*//')"
  [[ -z "$cmd" ]] && return
  if [[ "${__VPS_LAST_CMD:-}" == "$cmd" ]]; then
    return
  fi
  __VPS_LAST_CMD="$cmd"

  ts="$(date +%Y%m%dT%H%M%S)"
  cwd="$PWD"
  __vps_write_json_entry "$ts" "$cwd" "$exit_status" "$cmd" "" "" ""
}

vps_log_enable() {
  if [[ "${VPS_LOGGING_ENABLED:-}" == "1" ]]; then
    return
  fi
  export VPS_LOGGING_ENABLED="1"

  if [[ -n "${PROMPT_COMMAND:-}" ]]; then
    PROMPT_COMMAND="__vps_log_prompt_command; ${PROMPT_COMMAND}"
  else
    PROMPT_COMMAND="__vps_log_prompt_command"
  fi
  export PROMPT_COMMAND
}

vps_run() {
  if [[ $# -eq 0 ]]; then
    echo "usage: vps_run <command> [args...]" >&2
    return 2
  fi

  local ts cwd exit_status stdin_file stdout_file stderr_file
  local stdin_data stdout_data stderr_data
  ts="$(date +%Y%m%dT%H%M%S)"
  cwd="$PWD"

  stdin_file="$(mktemp)"
  stdout_file="$(mktemp)"
  stderr_file="$(mktemp)"

  if [[ -t 0 ]]; then
    : > "$stdin_file"
  else
    cat > "$stdin_file"
  fi

  "$@" < "$stdin_file" > "$stdout_file" 2> "$stderr_file"
  exit_status=$?

  stdin_data="$(__vps_trim_file_lines "$stdin_file")"
  stdout_data="$(__vps_trim_file_lines "$stdout_file")"
  stderr_data="$(__vps_trim_file_lines "$stderr_file")"

  __vps_write_json_entry "$ts" "$cwd" "$exit_status" "$*" "$stdin_data" "$stdout_data" "$stderr_data"

  printf '%s' "$stdout_data"
  printf '%s' "$stderr_data" >&2

  rm -f "$stdin_file" "$stdout_file" "$stderr_file"
  return "$exit_status"
}

vps_session_start() {
  local log_dir log_file
  log_dir="${VPS_LOG_DIR:-$HOME/vps_checker_logs}"
  mkdir -p "$log_dir"
  log_file="${log_dir}/session_$(date +%Y%m%dT%H%M%S)_$$.log"

  echo "starting session log: $log_file" >&2
  exec script -q -f "$log_file"
}
