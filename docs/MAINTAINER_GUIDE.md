# Maintainer Guide

This guide describes how to safely maintain this repository's Vizzy XML program and documentation set.

## 1) Source of truth

- Primary executable artifact: `Flight Program R V3.0.xml`.
- Repository version marker: `VERSION` (`MAJOR.REVISION` version).
- Version bump helper: `scripts/bump_version.sh`.
- Verification policy and guardrails: `agents.md`.
- Repo-extracted command/property inventory: `vizzy_kb/verified_index.md`.
- Syntax reference catalog: `Reference.xml` (reference-only, non-operational, do-not-fly).

## 2) Editing policy

When changing flight logic:

- Prefer minimal diffs.
- Preserve existing variable names unless there is an explicit migration reason.
- Preserve behavior outside the target change.
- Keep repo evidence for any new command/property usage.

Before introducing a new XML pattern, check `Reference.xml` for an existing block form and attribute shape (reference-only, non-operational, do-not-fly).

## 2.1) Using `Reference.xml` correctly

- Treat `Reference.xml` as a syntax atlas, not a runnable flight profile.
- **Policy:** Do not modify `Reference.xml` during normal feature work unless the task is specifically syntax-catalog maintenance.
- Reuse verified tag/attribute/value patterns from the reference when composing new program XML.
- For dropdown-style blocks, copy the exact selector attribute names/values shown in the reference (for example `input="..."`, `mode="..."`, `indicatorType="..."`, `property="..."`).
- Keep executable program behavior changes isolated to the intended flight program file; do not convert `Reference.xml` into mission logic.

## 3) Version bump workflow

- Choose bump type: `change` (all non-major updates, minimum `+0.01` equivalent) or `major` (breaking behavior/contract shift).
- Run `scripts/bump_version.sh <change|major>`.
- If doing a formal release, align XML program naming/file naming to the new version.
- Add/update the corresponding entry in `agents.md` change log.

## 4) Documentation update checklist

After changing behavior, update at least:

- `PROJECT_STUBS.md` (resolution notes / work log).
- `USER_MANUAL.md` (operator-facing behavior changes).
- `README.md` (high-level summary if scope changed).
- `vizzy_kb/verified_index.md` if command/property surface changed.
- `Reference.xml` if new block families or selector variants are discovered and manually cataloged.
- `scripts/check_reference_guardrails.sh` to confirm guardrails around `Reference.xml` naming and documentation wording remain intact.

## 5) Suggested validation passes

- XML well-formedness check.
- Run `scripts/check_reference_guardrails.sh` and require a pass before merging PRs that touch XML/docs.
- Quick scan for newly introduced command/property nodes.
- Sanity read of startup prompts, mode transitions, and fault paths.

## 6) Repository conventions

- Keep claims repository-grounded.
- Mark unknowns as **UNVERIFIED** rather than guessing.
- Keep manuals concise but complete enough for a new operator.
