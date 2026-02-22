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

updated_xml=0
for xml_file in *.xml; do
  [[ -f "$xml_file" ]] || continue

  current_name="$(sed -n 's/.*<Program name="\([^"]*\)".*/\1/p' "$xml_file" | head -n 1)"

  if [[ "$current_name" =~ ^(.*[[:space:]]V)([0-9]+)(\.[0-9]+)?$ ]]; then
    base_name="${BASH_REMATCH[1]}"
    new_name="${base_name}${next}"

    if [[ "$new_name" != "$current_name" ]]; then
      OLD_NAME="$current_name" NEW_NAME="$new_name" perl -0pi -e 's/(<Program\s+name=")([^"]+)(")/${1} . ($2 eq $ENV{OLD_NAME} ? $ENV{NEW_NAME} : $2) . $3/e' "$xml_file"
      echo "Updated XML program name: ${xml_file} -> ${new_name}"
      updated_xml=1
    fi
  fi
done

echo "Version bumped: ${current_raw} -> ${next}"
echo "Next steps:"
if [[ "$updated_xml" -eq 0 ]]; then
  echo "  1) No version-tagged XML program names were auto-updated."
else
  echo "  1) Confirm auto-updated XML Program names using version suffix V${next}."
fi
echo "  2) Add a changelog entry in agents.md section 8."
echo "  3) Commit VERSION (and any related docs/XML updates)."
