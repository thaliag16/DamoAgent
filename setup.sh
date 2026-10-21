#!/usr/bin/env bash
# damostack installer — links the skills and agent into Claude Code.
#
#   ./setup.sh            install (symlinks; edits to this repo take effect immediately)
#   ./setup.sh --copy     install by copying instead of symlinking
#   ./setup.sh --uninstall
#
# Installs:
#   ~/.claude/skills/damostack        -> this repo (knowledge/ and bin/ live here)
#   ~/.claude/skills/dam, dam-*       -> each skill
#   ~/.claude/agents/damodaran.md     -> the subagent
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS="$HOME/.claude/skills"
AGENTS="$HOME/.claude/agents"
MODE="link"
[[ "${1:-}" == "--copy" ]] && MODE="copy"

skill_names() { for d in "$REPO"/skills/*/; do basename "$d"; done; }

place() { # place <src> <dst>
  local src="$1" dst="$2"
  if [[ -e "$dst" || -L "$dst" ]]; then
    if [[ -L "$dst" ]] || [[ -f "$dst/.damostack-owned" ]] || [[ -f "$dst.damostack-owned" ]]; then
      rm -rf "$dst"
    else
      echo "  ! $dst exists and isn't managed by damostack; skipping" >&2
      return
    fi
  fi
  if [[ "$MODE" == "copy" ]]; then
    cp -R "$src" "$dst"
    if [[ -d "$dst" ]]; then touch "$dst/.damostack-owned"; else touch "$dst.damostack-owned"; fi
  else
    ln -s "$src" "$dst"
  fi
  echo "  + $dst"
}

if [[ "${1:-}" == "--uninstall" ]]; then
  for n in damostack $(skill_names); do
    t="$SKILLS/$n"
    if [[ -L "$t" || -f "$t/.damostack-owned" ]]; then rm -rf "$t"; echo "  - $t"; fi
  done
  a="$AGENTS/damodaran.md"
  if [[ -L "$a" || -f "$a.damostack-owned" ]]; then rm -f "$a" "$a.damostack-owned"; echo "  - $a"; fi
  echo "damostack uninstalled. Your saved valuations in ~/.damostack were left alone."
  exit 0
fi

mkdir -p "$SKILLS" "$AGENTS" "$HOME/.damostack/valuations"
chmod +x "$REPO"/bin/*.py

echo "Installing damostack ($MODE) from $REPO"
place "$REPO" "$SKILLS/damostack"
for n in $(skill_names); do place "$REPO/skills/$n" "$SKILLS/$n"; done
place "$REPO/agents/damodaran.md" "$AGENTS/damodaran.md"

echo
echo "Done. Restart Claude Code, then try:"
echo "  /dam-value <company>   full story-to-value valuation"
echo "  /dam                   ask anything; routes to the right skill"
