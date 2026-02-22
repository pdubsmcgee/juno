# Maintainer Guide

This guide describes how to safely maintain this repository's Vizzy XML program and documentation set.

## 1) Source of truth

- Primary executable artifact: `Flight Program R V3.0.xml`.
- Repository version marker: `VERSION` (semantic version).
- Version bump helper: `scripts/bump_version.sh`.
- Verification policy and guardrails: `agents.md`.
- Repo-extracted command/property inventory: `vizzy_kb/verified_index.md`.

## 2) Editing policy

When changing flight logic:

- Prefer minimal diffs.
- Preserve existing variable names unless there is an explicit migration reason.
- Preserve behavior outside the target change.
- Keep repo evidence for any new command/property usage.

## 3) Version bump workflow

- Choose bump type: `patch` (small safe changes), `minor` (new behavior/features), `major` (breaking behavior/contract shift).
- Run `scripts/bump_version.sh <patch|minor|major>`.
- If doing a formal release, align XML program naming/file naming to the new version.
- Add/update the corresponding entry in `agents.md` change log.

## 4) Documentation update checklist

After changing behavior, update at least:

- `PROJECT_STUBS.md` (resolution notes / work log).
- `USER_MANUAL.md` (operator-facing behavior changes).
- `README.md` (high-level summary if scope changed).
- `vizzy_kb/verified_index.md` if command/property surface changed.

## 5) Suggested validation passes

- XML well-formedness check.
- Quick scan for newly introduced command/property nodes.
- Sanity read of startup prompts, mode transitions, and fault paths.

## 6) Repository conventions

- Keep claims repository-grounded.
- Mark unknowns as **UNVERIFIED** rather than guessing.
- Keep manuals concise but complete enough for a new operator.
