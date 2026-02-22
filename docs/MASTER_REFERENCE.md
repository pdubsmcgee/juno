# Master Reference — Repository Documentation Map

This file is the canonical documentation index for the `juno` repository.
Use it as the first stop before opening other docs.

## 1) Quick navigation by audience

### Operators / players
1. `README.md` — high-level project overview and repository layout.
2. `USER_MANUAL.md` — how to run the flight program in-game.

### Maintainers / contributors
1. `docs/MAINTAINER_GUIDE.md` — editing policy, release/version checklist, and validation passes.
2. `agents.md` — repository-grounded verification contract and change-log process.
3. `PROJECT_STUBS.md` — implementation/resolution ledger for completed work items.

### Vizzy implementation references
1. `Reference.xml` — syntax atlas for block/tag/selector shapes (reference-only, non-operational, do-not-fly).
2. `vizzy_kb/verified_index.md` — repository-observed command/property inventory.
3. `docs/VIZZY_STATE_MACHINE_PATTERN.md` — standardized Broadcast/Receive state-machine pattern.

### Research and background notes
1. `vizzy_kb/vizzy_commands_web_research.md` — external command-family research notes.
2. `docs/FANDOM_VIZZY_WIKI_NOTES.md` — detailed wiki-page pass notes.
3. `docs/STEAM_GUIDE_*.md` — topic-focused Steam guide distillations.
4. `docs/QUADCOPTER_REVIEW_2026-02-22.md` — focused review notes for the quadcopter program.
5. `logic-table.md` — deep dive for the throttle/countdown interaction and fixes.

## 2) Organized documentation inventory

| Area | File | Role | Status |
|---|---|---|---|
| Root | `README.md` | Entry point and high-level map | Canonical |
| Root | `USER_MANUAL.md` | Operator-facing runtime procedures | Canonical |
| Root | `PROJECT_STUBS.md` | Historical implementation tracker | Canonical (history) |
| Root | `logic-table.md` | Incident analysis (launch/throttle deadlock) | Historical analysis |
| Root | `agents.md` | Repo operating contract and process guardrails | Canonical |
| Root | `agents.md.txt` | Legacy instruction/template content | Legacy reference |
| Root | `You are “DeltaVinci”.txt` | Legacy persona/process notes | Legacy reference |
| Docs | `docs/MAINTAINER_GUIDE.md` | Maintainer workflow and release policy | Canonical |
| Docs | `docs/VIZZY_STATE_MACHINE_PATTERN.md` | Reusable architecture pattern | Canonical pattern |
| Docs | `docs/FANDOM_VIZZY_WIKI_NOTES.md` | Source distillation notes | Research notes |
| Docs | `docs/STEAM_GUIDE_ADVANCED_DATA_STRUCTURES_NOTES.md` | Source distillation notes | Research notes |
| Docs | `docs/STEAM_GUIDE_INTRO_TO_VIZZY_LAUNCH_AUTOMATION_NOTES.md` | Source distillation notes | Research notes |
| Docs | `docs/STEAM_GUIDE_MFD_HUD_NOTES.md` | Source distillation notes | Research notes |
| Docs | `docs/STEAM_GUIDE_ORBITAL_MECHANICS_NOTES.md` | Source distillation notes | Research notes |
| Docs | `docs/STEAM_GUIDE_ORBITAL_TOOLKIT_INACCURACY_NOTES.md` | Source distillation notes | Research notes |
| Docs | `docs/STEAM_GUIDE_VECTORS_AND_PIDS_NOTES.md` | Source distillation notes | Research notes |
| Docs | `docs/QUADCOPTER_REVIEW_2026-02-22.md` | Program-specific review notes | Historical analysis |
| KB | `vizzy_kb/verified_index.md` | Evidence-grounded command/property index | Canonical reference |
| KB | `vizzy_kb/vizzy_commands_web_research.md` | External-source command taxonomy notes | Research notes |

## 3) Suggested reading sequence

When onboarding a new maintainer, follow this order:

1. `README.md`
2. `docs/MAINTAINER_GUIDE.md`
3. `agents.md`
4. `USER_MANUAL.md`
5. `vizzy_kb/verified_index.md`
6. `Reference.xml` (reference-only, non-operational, do-not-fly)

Then consume specialized analysis/research docs as needed.

## 4) Documentation hygiene rules

To keep this documentation set organized going forward:

1. **If behavior changes:** update `README.md`, `USER_MANUAL.md`, and `docs/MAINTAINER_GUIDE.md` in the same PR.
2. **If XML command surface changes:** update `vizzy_kb/verified_index.md`.
3. **If adding external research notes:** place in `docs/` with a source-attribution heading and clear scope section.
4. **If a note becomes process-critical:** promote its guidance into a canonical file (usually `README.md` or `docs/MAINTAINER_GUIDE.md`).
5. **Keep legacy files stable:** avoid editing `agents.md.txt` and `You are “DeltaVinci”.txt` unless explicitly doing historical cleanup.

## 5) Current organization result

The repository documentation is now grouped into five clear classes:

- Canonical user docs
- Canonical maintainer/process docs
- Canonical implementation references
- Research notes
- Historical/legacy artifacts

Use this file to determine where new documentation belongs before creating it.
