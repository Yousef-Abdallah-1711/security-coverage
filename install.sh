#!/usr/bin/env bash
set -euo pipefail

PLUGIN_NAME="security-coverage"
COMMANDS=(security-assess security-plan security-implement)
COMMAND_SKILLS=(security-assess security-plan security-implement)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL=0
UNINSTALL=0
CLAUDE=0
CODEX=0
EXPLICIT_AGENT=0

usage() {
  cat <<'USAGE'
security-coverage installer

Usage:
  ./install.sh [options]

Options:
  --claude       install Claude commands and skill only
  --codex        install Codex commands, skill, and plugin files only
  --local        install into the current project (./.claude and/or ./.codex)
  --uninstall    remove installed files
  --help         show this help

Default:
  ./install.sh installs globally for both Claude and Codex.
USAGE
}

while (($#)); do
  case "$1" in
    --claude)
      CLAUDE=1
      EXPLICIT_AGENT=1
      ;;
    --codex)
      CODEX=1
      EXPLICIT_AGENT=1
      ;;
    --local)
      LOCAL=1
      ;;
    --uninstall)
      UNINSTALL=1
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ "$EXPLICIT_AGENT" -eq 0 ]]; then
  CLAUDE=1
  CODEX=1
fi

copy_dir_replace() {
  local src="$1"
  local dst="$2"
  rm -rf "$dst"
  mkdir -p "$(dirname "$dst")"
  cp -R "$src" "$dst"
}

copy_plugin_replace() {
  local dst="$1"
  rm -rf "$dst"
  mkdir -p "$dst"
  mkdir -p "$dst/.codex-plugin" "$dst/commands" "$dst/skills"
  cp "$ROOT_DIR/.codex-plugin/plugin.json" "$dst/.codex-plugin/plugin.json"
  cp "$ROOT_DIR/README.md" "$ROOT_DIR/LICENSE" "$ROOT_DIR/.gitignore" "$ROOT_DIR/.gitattributes" "$ROOT_DIR/install.sh" "$ROOT_DIR/install.ps1" "$ROOT_DIR/package.json" "$dst/"
  cp -R "$ROOT_DIR/commands/." "$dst/commands/"
  cp -R "$ROOT_DIR/skills/." "$dst/skills/"
  cp -R "$ROOT_DIR/security-assess" "$ROOT_DIR/security-plan" "$ROOT_DIR/security-implement" "$dst/"
}

install_commands() {
  local target="$1"
  mkdir -p "$target"
  for cmd in "${COMMANDS[@]}"; do
    cp "$ROOT_DIR/commands/${cmd}.md" "$target/${cmd}.md"
  done
}

verify_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "Missing expected file: $file" >&2
    exit 1
  fi
}

verify_dir() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    echo "Missing expected directory: $dir" >&2
    exit 1
  fi
}

install_claude() {
  local base
  if [[ "$LOCAL" -eq 1 ]]; then
    base="$PWD/.claude"
  else
    base="$HOME/.claude"
  fi

  if [[ "$UNINSTALL" -eq 1 ]]; then
    rm -rf "$base/skills/$PLUGIN_NAME"
    for skill in "${COMMAND_SKILLS[@]}"; do
      rm -rf "$base/skills/$skill"
    done
    for cmd in "${COMMANDS[@]}"; do
      rm -f "$base/commands/${cmd}.md"
    done
    echo "Removed Claude install from $base"
    return
  fi

  copy_dir_replace "$ROOT_DIR/skills/$PLUGIN_NAME" "$base/skills/$PLUGIN_NAME"
  for skill in "${COMMAND_SKILLS[@]}"; do
    copy_dir_replace "$ROOT_DIR/$skill" "$base/skills/$skill"
  done
  install_commands "$base/commands"

  verify_dir "$base/skills/$PLUGIN_NAME"
  verify_file "$base/skills/$PLUGIN_NAME/SKILL.md"
  for skill in "${COMMAND_SKILLS[@]}"; do
    verify_file "$base/skills/$skill/SKILL.md"
  done
  for cmd in "${COMMANDS[@]}"; do
    verify_file "$base/commands/${cmd}.md"
  done
  echo "Installed Claude files to $base"
}

install_codex() {
  local base
  if [[ "$LOCAL" -eq 1 ]]; then
    base="$PWD/.codex"
  else
    base="${CODEX_HOME:-$HOME/.codex}"
  fi

  if [[ "$UNINSTALL" -eq 1 ]]; then
    rm -rf "$base/skills/$PLUGIN_NAME" "$base/plugins/$PLUGIN_NAME"
    for skill in "${COMMAND_SKILLS[@]}"; do
      rm -rf "$base/skills/$skill"
    done
    for cmd in "${COMMANDS[@]}"; do
      rm -f "$base/commands/${cmd}.md"
    done
    echo "Removed Codex install from $base"
    return
  fi

  copy_dir_replace "$ROOT_DIR/skills/$PLUGIN_NAME" "$base/skills/$PLUGIN_NAME"
  for skill in "${COMMAND_SKILLS[@]}"; do
    copy_dir_replace "$ROOT_DIR/$skill" "$base/skills/$skill"
  done
  copy_plugin_replace "$base/plugins/$PLUGIN_NAME"
  install_commands "$base/commands"

  verify_dir "$base/skills/$PLUGIN_NAME"
  verify_file "$base/skills/$PLUGIN_NAME/SKILL.md"
  for skill in "${COMMAND_SKILLS[@]}"; do
    verify_file "$base/skills/$skill/SKILL.md"
  done
  verify_file "$base/plugins/$PLUGIN_NAME/.codex-plugin/plugin.json"
  for cmd in "${COMMANDS[@]}"; do
    verify_file "$base/commands/${cmd}.md"
  done
  echo "Installed Codex files to $base"
}

if [[ "$CLAUDE" -eq 1 ]]; then
  install_claude
fi

if [[ "$CODEX" -eq 1 ]]; then
  install_codex
fi

if [[ "$UNINSTALL" -eq 1 ]]; then
  echo "Uninstall complete."
else
  echo "Install complete."
fi
