#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: ./examples/install-one-skill.sh <skill-name> <claude|codex>"
  exit 1
fi

skill_name="$1"
target_app="$2"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/$skill_name"

case "$target_app" in
  claude)
    target_root="$HOME/.claude/skills"
    ;;
  codex)
    target_root="$HOME/.codex/skills"
    ;;
  *)
    echo "Target must be claude or codex."
    exit 1
    ;;
esac

if [ ! -d "$source_dir" ]; then
  echo "Skill not found: $source_dir"
  exit 1
fi

mkdir -p "$target_root"
rm -rf "$target_root/$skill_name"
cp -R "$source_dir" "$target_root/$skill_name"
echo "Installed $skill_name to $target_root/$skill_name"
