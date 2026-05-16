#!/bin/zsh
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  chrome-live.sh list-profiles
  chrome-live.sh active-tab
  chrome-live.sh list-tabs
  chrome-live.sh activate-tab [--focus] <needle>
  chrome-live.sh open-profile [--focus] <profile> [url]
  chrome-live.sh exec-js [--focus] [js]
  chrome-live.sh body-text [--focus] [chars]

Notes:
  - exec-js reads JavaScript from the first argument or stdin.
  - body-text returns the first N characters of document.body.innerText.
  - Commands stay in the background by default; pass --focus to bring Chrome forward.
EOF
}

frontmost_app() {
  osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null || true
}

restore_frontmost_app() {
  local app_name="${1:-}"
  if [[ -z "$app_name" || "$app_name" == "Google Chrome" ]]; then
    return 0
  fi

  osascript - "$app_name" <<'EOF' >/dev/null 2>&1 || true
on run argv
  tell application (item 1 of argv) to activate
end run
EOF
}

resolve_profile() {
  local key="${1:-}"
  case "$key" in
    personal)
      printf '%s\t%s\n' "Profile 1" "the user"
      ;;
    exampleco)
      printf '%s\t%s\n' "Profile 10" "ExampleCo.com"
      ;;
    gmr)
      printf '%s\t%s\n' "Profile 15" "ReviewCo"
      ;;
    example-agency)
      printf '%s\t%s\n' "Profile 3" "example.com"
      ;;
    *)
      return 1
      ;;
  esac
}

list_profiles() {
  cat <<'EOF'
personal	Profile 1	the user
exampleco	Profile 10	ExampleCo.com
gmr	Profile 15	ReviewCo
example-agency	Profile 3	example.com
EOF
}

active_tab() {
  osascript -e 'tell application "Google Chrome" to get {title of active tab of front window, URL of active tab of front window}'
}

list_tabs() {
  osascript <<'EOF'
tell application "Google Chrome"
  set rows to {}
  repeat with w from 1 to count of windows
    set winRef to window w
    set tabIndex to 0
    repeat with t in tabs of winRef
      set tabIndex to tabIndex + 1
      set tabTitle to ""
      set tabURL to ""
      try
        set tabTitle to (title of t) as text
      end try
      try
        set tabURL to (URL of t) as text
      end try
      set rowText to "window=" & w & " tab=" & tabIndex & " title=" & quoted form of tabTitle & " url=" & quoted form of tabURL
      set end of rows to rowText
    end repeat
  end repeat
  set {oldTID, AppleScript's text item delimiters} to {AppleScript's text item delimiters, linefeed}
  set outputText to rows as text
  set AppleScript's text item delimiters to oldTID
  return outputText
end tell
EOF
}

activate_tab() {
  local focus=0
  if [[ "${1:-}" == "--focus" ]]; then
    focus=1
    shift
  fi

  local needle="${1:-}"
  if [[ -z "$needle" ]]; then
    echo "activate-tab requires a title or URL substring" >&2
    exit 1
  fi

  osascript - "$needle" "$focus" <<'EOF'
on run argv
  set needle to item 1 of argv
  set shouldFocus to (item 2 of argv) is "1"
  tell application "Google Chrome"
    repeat with w from 1 to count of windows
      set winRef to window w
      set tabIndex to 0
      repeat with t in tabs of winRef
        set tabIndex to tabIndex + 1
        set tabTitle to title of t
        set tabURL to URL of t
        if tabTitle contains needle or tabURL contains needle then
          set active tab index of winRef to tabIndex
          set index of winRef to 1
          if shouldFocus then activate
          return {tabTitle, tabURL}
        end if
      end repeat
    end repeat
  end tell
  error "No Chrome tab matched: " & needle
end run
EOF
}

open_profile() {
  local focus=0
  if [[ "${1:-}" == "--focus" ]]; then
    focus=1
    shift
  fi

  local key="${1:-}"
  local url="${2:-about:blank}"
  local profile_info profile_dir profile_label
  local previous_app=""

  if [[ -z "$key" ]]; then
    echo "open-profile requires a profile key" >&2
    exit 1
  fi

  if ! profile_info="$(resolve_profile "$key")"; then
    echo "Unknown profile: $key" >&2
    exit 1
  fi

  profile_dir="${profile_info%%$'\t'*}"
  profile_label="${profile_info#*$'\t'}"

  if (( ! focus )); then
    previous_app="$(frontmost_app)"
  fi

  # Reuse an existing matching tab when possible instead of spawning a fresh window.
  if [[ "$url" != "about:blank" ]]; then
    if activate_tab "$url" >/dev/null 2>&1; then
      if (( ! focus )); then
        restore_frontmost_app "$previous_app"
      fi
      active_tab
      printf '\nprofile=%s profile_dir=%s reused_existing_tab=1\n' "$profile_label" "$profile_dir"
      return 0
    fi
  fi

  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --profile-directory="$profile_dir" \
    "$url" \
    >/dev/null 2>&1 &

  for _ in {1..20}; do
    if activate_tab "$url" >/dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done

  if (( ! focus )); then
    restore_frontmost_app "$previous_app"
  fi

  active_tab
  printf '\nprofile=%s profile_dir=%s reused_existing_tab=0\n' "$profile_label" "$profile_dir"
}

exec_js() {
  local focus=0
  if [[ "${1:-}" == "--focus" ]]; then
    focus=1
    shift
  fi

  local js
  if [[ $# -gt 0 ]]; then
    js="$1"
  else
    js="$(cat)"
  fi

  if [[ -z "$js" ]]; then
    echo "exec-js requires JavaScript via argument or stdin" >&2
    exit 1
  fi

  osascript - "$js" "$focus" <<'EOF'
on run argv
  set js to item 1 of argv
  set shouldFocus to (item 2 of argv) is "1"
  tell application "Google Chrome"
    if shouldFocus then activate
    return execute active tab of front window javascript js
  end tell
end run
EOF
}

body_text() {
  local focus=0
  if [[ "${1:-}" == "--focus" ]]; then
    focus=1
    shift
  fi

  local chars="${1:-4000}"
  if (( focus )); then
    exec_js --focus "(() => (document.body.innerText || '').slice(0, ${chars}))();"
  else
    exec_js "(() => (document.body.innerText || '').slice(0, ${chars}))();"
  fi
}

cmd="${1:-}"
case "$cmd" in
  list-profiles)
    list_profiles
    ;;
  active-tab)
    active_tab
    ;;
  list-tabs)
    list_tabs
    ;;
  activate-tab)
    shift
    activate_tab "${1:-}"
    ;;
  open-profile)
    shift
    open_profile "${1:-}" "${2:-about:blank}"
    ;;
  exec-js)
    shift
    exec_js "$@"
    ;;
  body-text)
    shift
    body_text "${1:-4000}"
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
