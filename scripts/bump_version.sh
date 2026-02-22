#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 {major|minor|patch}" >&2
  exit 1
fi

kind="$1"
version_file="VERSION"

if [[ ! -f "$version_file" ]]; then
  echo "ERROR: VERSION file not found at repo root." >&2
  exit 1
fi

current_raw="$(tr -d '[:space:]' < "$version_file")"
if [[ ! "$current_raw" =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
  echo "ERROR: VERSION must be in MAJOR.MINOR.PATCH format." >&2
  exit 1
fi

major="${BASH_REMATCH[1]}"
minor="${BASH_REMATCH[2]}"
patch="${BASH_REMATCH[3]}"

case "$kind" in
  major)
    major=$((major + 1))
    minor=0
    patch=0
    ;;
  minor)
    minor=$((minor + 1))
    patch=0
    ;;
  patch)
    patch=$((patch + 1))
    ;;
  *)
    echo "ERROR: Unsupported bump type '$kind'. Use major|minor|patch." >&2
    exit 1
    ;;
esac

next="${major}.${minor}.${patch}"
printf '%s\n' "$next" > "$version_file"

echo "Version bumped: ${current_raw} -> ${next}"
echo "Next steps:"
echo "  1) Update XML Program name/file label if release-worthy."
echo "  2) Add a changelog entry in agents.md section 8."
echo "  3) Commit VERSION (and any related docs/XML updates)."
