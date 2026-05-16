#!/bin/zsh
set -euo pipefail
setopt null_glob

STATE_ROOT="${HOME}/.local/state/dev-browser-profile-chrome"

usage() {
  cat <<'EOF'
Usage:
  launch-profile-debug-chrome.sh --list
  launch-profile-debug-chrome.sh --cleanup [profile]
  launch-profile-debug-chrome.sh --cleanup-owner <owner>
  launch-profile-debug-chrome.sh --cleanup-all
  launch-profile-debug-chrome.sh <personal|exampleco|gmr|example-agency> [url]

Behavior:
  - Reuses one isolated debug Chrome per profile when possible.
  - Persists state under ~/.local/state/dev-browser-profile-chrome
  - Cleans up stale state automatically on launch.
EOF
}

list_profiles() {
  cat <<'EOF'
personal	Profile 1	the user
exampleco	Profile 10	ExampleCo.com
gmr	Profile 15	ReviewCo
example-agency	Profile 3	example.com
EOF
}

resolve_profile() {
  local key="${1:-}"
  case "$key" in
    personal)
      profile_dir="Profile 1"
      profile_label="Personal"
      ;;
    exampleco)
      profile_dir="Profile 10"
      profile_label="ExampleCo"
      ;;
    gmr)
      profile_dir="Profile 15"
      profile_label="ReviewCo"
      ;;
    example-agency)
      profile_dir="Profile 3"
      profile_label="Example Agency"
      ;;
    *)
      return 1
      ;;
  esac
}

state_path() {
  local key="${1:-}"
  printf '%s/%s.json\n' "$STATE_ROOT" "$key"
}

port_ready() {
  local port="${1:-}"
  [[ -n "$port" ]] || return 1
  /usr/bin/curl -fsS "http://127.0.0.1:${port}/json/version" >/dev/null 2>&1
}

pid_alive() {
  local pid="${1:-}"
  [[ -n "$pid" ]] || return 1
  kill -0 "$pid" >/dev/null 2>&1
}

cleanup_tmp_dir() {
  local dir="${1:-}"
  [[ -n "$dir" ]] || return 0
  rm -rf "$dir" 2>/dev/null || true
}

cleanup_state_file() {
  local file="${1:-}"
  [[ -n "$file" ]] || return 0
  rm -f "$file" 2>/dev/null || true
}

cleanup_instance() {
  local key="${1:-}"
  local file
  file="$(state_path "$key")"

  if [[ ! -f "$file" ]]; then
    return 0
  fi

  local pid tmp_dir port
  pid="$(jq -r '.pid // empty' "$file" 2>/dev/null || true)"
  tmp_dir="$(jq -r '.tmp_dir // empty' "$file" 2>/dev/null || true)"
  port="$(jq -r '.port // empty' "$file" 2>/dev/null || true)"

  if pid_alive "$pid"; then
    kill "$pid" >/dev/null 2>&1 || true
    sleep 1
    if pid_alive "$pid"; then
      kill -9 "$pid" >/dev/null 2>&1 || true
    fi
  fi

  if [[ -n "$port" ]]; then
    pkill -f -- "--remote-debugging-port=${port}" >/dev/null 2>&1 || true
  fi

  cleanup_tmp_dir "$tmp_dir"
  cleanup_state_file "$file"
}

cleanup_owner() {
  local owner="${1:-}"
  [[ -n "$owner" ]] || return 0

  mkdir -p "$STATE_ROOT"
  local file
  for file in "$STATE_ROOT"/*.json; do
    [[ -f "$file" ]] || continue
    local recorded_owner
    recorded_owner="$(jq -r '.owner // empty' "$file" 2>/dev/null || true)"
    [[ "$recorded_owner" == "$owner" ]] || continue
    cleanup_instance "${file:t:r}"
  done
}

cleanup_legacy_instances() {
  local matched=0

  for dir in /tmp/dev-browser-profile-*; do
    [[ -d "$dir" ]] || continue
    matched=1

    local pids=""
    pids="$(pgrep -f -- "--user-data-dir=${dir}" || true)"
    if [[ -n "$pids" ]]; then
      while IFS= read -r pid; do
        [[ -n "$pid" ]] || continue
        kill "$pid" >/dev/null 2>&1 || true
        sleep 0.2
        if kill -0 "$pid" >/dev/null 2>&1; then
          kill -9 "$pid" >/dev/null 2>&1 || true
        fi
      done <<< "$pids"
    fi

    rm -rf "$dir" 2>/dev/null || true
  done

  return 0
}

cleanup_stale_states() {
  mkdir -p "$STATE_ROOT"
  local file
  for file in "$STATE_ROOT"/*.json; do
    [[ -f "$file" ]] || continue
    local pid port tmp_dir
    pid="$(jq -r '.pid // empty' "$file" 2>/dev/null || true)"
    port="$(jq -r '.port // empty' "$file" 2>/dev/null || true)"
    tmp_dir="$(jq -r '.tmp_dir // empty' "$file" 2>/dev/null || true)"

    if pid_alive "$pid" && port_ready "$port"; then
      continue
    fi

    if pid_alive "$pid"; then
      kill "$pid" >/dev/null 2>&1 || true
      sleep 0.2
      if kill -0 "$pid" >/dev/null 2>&1; then
        kill -9 "$pid" >/dev/null 2>&1 || true
      fi
    fi

    cleanup_tmp_dir "$tmp_dir"
    cleanup_state_file "$file"
  done
}

read_existing_state() {
  local key="${1:-}"
  local file
  file="$(state_path "$key")"
  [[ -f "$file" ]] || return 1

  local pid port
  pid="$(jq -r '.pid // empty' "$file")"
  port="$(jq -r '.port // empty' "$file")"
  if pid_alive "$pid" && port_ready "$port"; then
    cat "$file"
    return 0
  fi

  local tmp_dir
  tmp_dir="$(jq -r '.tmp_dir // empty' "$file" 2>/dev/null || true)"
  cleanup_tmp_dir "$tmp_dir"
  cleanup_state_file "$file"
  return 1
}

find_open_port() {
  local candidate
  for candidate in $(jot 50 9310 9359 2>/dev/null || seq 9310 9359); do
    if ! lsof -nP -iTCP:"$candidate" -sTCP:LISTEN >/dev/null 2>&1; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

open_new_tab_best_effort() {
  local port="${1:-}"
  local url="${2:-}"
  [[ -n "$port" && -n "$url" && "$url" != "about:blank" ]] || return 0
  /usr/bin/curl -fsS -X PUT "http://127.0.0.1:${port}/json/new?${url}" >/dev/null 2>&1 || true
}

emit_state_json() {
  local file="${1:-}"
  jq -c '.' "$file"
}

launch_instance() {
  local key="${1:-}"
  local start_url="${2:-about:blank}"

  if ! resolve_profile "$key"; then
    echo "Unknown profile: $key" >&2
    exit 1
  fi

  local chrome_root="${HOME}/Library/Application Support/Google/Chrome"
  local source_profile="${chrome_root}/${profile_dir}"
  if [[ ! -d "$source_profile" ]]; then
    echo "Profile directory not found: $source_profile" >&2
    exit 1
  fi

  mkdir -p "$STATE_ROOT"

  if existing_json="$(read_existing_state "$key" 2>/dev/null)"; then
    local port
    port="$(printf '%s\n' "$existing_json" | jq -r '.port')"
    open_new_tab_best_effort "$port" "$start_url"
    printf '%s\n' "$existing_json" | jq -c --argjson reused true --arg requested_url "$start_url" \
      '. + {reused_existing: $reused, requested_url: $requested_url}'
    return 0
  fi

  local tmp_dir
  tmp_dir="$(mktemp -d "/tmp/dev-browser-profile-${key}.XXXXXX")"
  mkdir -p "${tmp_dir}/Default"

  cp "${chrome_root}/Local State" "${tmp_dir}/Local State"
  local name
  for name in "Cookies" "Preferences" "Secure Preferences"; do
    if [[ -e "${source_profile}/${name}" ]]; then
      cp -R "${source_profile}/${name}" "${tmp_dir}/Default/"
    fi
  done

  local port
  if ! port="$(find_open_port)"; then
    echo "Could not find an open debugging port in 9310-9359" >&2
    cleanup_tmp_dir "$tmp_dir"
    exit 1
  fi

  local log_file="${tmp_dir}/chrome.log"
  /usr/bin/open -g -na "Google Chrome" --args \
    --user-data-dir="${tmp_dir}" \
    --profile-directory="Default" \
    --remote-debugging-port="${port}" \
    --no-first-run \
    --no-default-browser-check \
    "${start_url}" \
    >"${log_file}" 2>&1

  local ready=0
  local _
  for _ in $(seq 1 40); do
    if port_ready "$port"; then
      ready=1
      break
    fi
    sleep 0.5
  done

  if [[ "$ready" -ne 1 ]]; then
    echo "Chrome debug endpoint did not come up on port ${port}" >&2
    echo "log: ${log_file}" >&2
    cleanup_tmp_dir "$tmp_dir"
    exit 1
  fi

  local ws_endpoint chrome_pid file
  local owner="${LIFE_BACKLOG_BROWSER_OWNER:-}"
  ws_endpoint="$(
    /usr/bin/curl -sS "http://127.0.0.1:${port}/json/version" | jq -r '.webSocketDebuggerUrl'
  )"
  chrome_pid="$(lsof -nP -t -iTCP:"${port}" -sTCP:LISTEN | head -n 1)"
  file="$(state_path "$key")"

  jq -n \
    --arg profile "$profile_label" \
    --arg profile_key "$key" \
    --arg profile_dir "$profile_dir" \
    --arg tmp_dir "$tmp_dir" \
    --arg log_file "$log_file" \
    --arg ws_endpoint "$ws_endpoint" \
    --arg start_url "$start_url" \
    --arg owner "$owner" \
    --arg created_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --argjson port "$port" \
    --argjson pid "$chrome_pid" \
    '{
      profile: $profile,
      profile_key: $profile_key,
      profile_dir: $profile_dir,
      port: $port,
      endpoint: ("http://127.0.0.1:" + ($port|tostring)),
      ws_endpoint: $ws_endpoint,
      pid: $pid,
      tmp_dir: $tmp_dir,
      log_file: $log_file,
      start_url: $start_url,
      owner: $owner,
      created_at: $created_at
    }' > "$file"

  jq -c --argjson reused false '. + {reused_existing: $reused}' "$file"
}

mkdir -p "$STATE_ROOT"
cleanup_stale_states

case "${1:-}" in
  --list)
    list_profiles
    exit 0
    ;;
  --cleanup-all)
    cleanup_stale_states
    cleanup_legacy_instances
    for key in personal exampleco gmr example-agency; do
      cleanup_instance "$key"
    done
    printf '%s\n' '{"success":true,"cleaned":"all"}'
    exit 0
    ;;
  --cleanup)
    cleanup_stale_states
    cleanup_legacy_instances
    if [[ -n "${2:-}" ]]; then
      cleanup_instance "$2"
      printf '%s\n' "$(jq -n --arg profile "$2" '{success:true, cleaned:$profile}')"
    else
      for key in personal exampleco gmr example-agency; do
        cleanup_instance "$key"
      done
      printf '%s\n' '{"success":true,"cleaned":"known-profiles"}'
    fi
    exit 0
    ;;
  --cleanup-owner)
    cleanup_owner "${2:-}"
    printf '%s\n' "$(jq -n --arg owner "${2:-}" '{success:true, cleaned_owner:$owner}')"
    exit 0
    ;;
  ""|-h|--help)
    usage
    exit 0
    ;;
esac

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage >&2
  exit 1
fi

launch_instance "$1" "${2:-about:blank}"
