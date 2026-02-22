#!/usr/bin/env bash
set -euo pipefail

expected_program='Vizzy Syntax Atlas (REFERENCE ONLY)'
required_phrase='reference-only, non-operational, do-not-fly'

if ! grep -Fq "<Program name=\"${expected_program}\">" Reference.xml; then
  echo "FAIL: Reference.xml root Program name must be '${expected_program}'." >&2
  exit 1
fi

for doc in README.md docs/MASTER_REFERENCE.md; do
  if ! grep -Fq "${required_phrase}" "$doc"; then
    echo "FAIL: ${doc} must contain phrase '${required_phrase}'." >&2
    exit 1
  fi
done

echo "PASS: Reference.xml and documentation guardrails are in place."
