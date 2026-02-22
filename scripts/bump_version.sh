#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 {change|major}" >&2
  exit 1
fi

kind="$1"
version_file="VERSION"

if [[ ! -f "$version_file" ]]; then
  echo "ERROR: VERSION file not found at repo root." >&2
  exit 1
fi

current_raw="$(tr -d '[:space:]' < "$version_file")"

major=""
revision=""

if [[ "$current_raw" =~ ^([0-9]+)\.([0-9]+)$ ]]; then
  major="${BASH_REMATCH[1]}"
  revision="${BASH_REMATCH[2]}"
elif [[ "$current_raw" =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
  # Migration path from legacy MAJOR.MINOR.PATCH to MAJOR.REVISION.
  # 3.0.1 normalizes to 3.1 and then the selected bump is applied.
  major="${BASH_REMATCH[1]}"
  revision="${BASH_REMATCH[2]}${BASH_REMATCH[3]}"
else
  echo "ERROR: VERSION must be MAJOR.REVISION (or legacy MAJOR.MINOR.PATCH for migration)." >&2
  exit 1
fi

case "$kind" in
  major)
    major=$((major + 1))
    revision=0
    ;;
  change)
    revision=$((revision + 1))
    ;;
  *)
    echo "ERROR: Unsupported bump type '$kind'. Use change|major." >&2
    exit 1
    ;;
esac

next="${major}.${revision}"
printf '%s\n' "$next" > "$version_file"

echo "Version bumped: ${current_raw} -> ${next}"
echo "Next steps:"
echo "  1) Update XML Program name/file label if release-worthy."
echo "  2) Add a changelog entry in agents.md section 8."
echo "  3) Commit VERSION (and any related docs/XML updates)."
