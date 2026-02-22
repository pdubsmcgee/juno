# Notes from Steam Guide: "Advanced Data Structures in Vizzy"

Source reviewed: <https://steamcommunity.com/sharedfiles/filedetails/?id=3033402620>

## Core idea from the guide

Vizzy can be used to create **dynamic variables** by feeding a string expression into the variable slot of `set variable [] to []`.
That makes it possible to emulate map/struct-like layouts using naming conventions (for example, `craft1_pos`, `craft1_vel`, `craft1_state`) instead of predeclaring every variable as a green block.

## Why the guide recommends this pattern

- **List blocks can be cumbersome** in large programs (editor size/readability overhead).
- **FUNK integration is better for scalar/vector math**, and FUNK expressions can resolve dynamic variable names.
- **Variable-list clutter reduction**: fewer explicitly declared green variables in complex projects.
- **Nested grouping by name** is possible (for example, prefix-based pseudo "list-of-lists" / pseudo-struct grouping), which the author considers more flexible for some workflows.

## Practical mechanics distilled

1. **Write dynamically**
   - Construct a variable name string (often by joining a base name + index/suffix).
   - Assign into it with `set variable [dynamicName] to [value]`.

2. **Read dynamically with FUNK**
   - To fetch dynamic variables, pass the constructed variable token through FUNK so it is interpreted as a variable reference (not a literal string).

3. **Use stable naming conventions**
   - Treat prefixes as namespaces (e.g., `target3_...`, `stage2_...`).
   - Reserve consistent field suffixes (`_x`, `_y`, `_z`, `_mass`, `_mode`) to emulate struct fields.

4. **Wrap access in helper functions**
   - Build small helper instructions like `GetPos(prefix)`, `GetVel(prefix)`, `GetState(prefix)`.
   - Centralized helpers reduce naming bugs and simplify refactors.

## Important caveats called out in the guide

- This behavior is described as **undocumented** and may change in future game versions.
- FUNK behavior has type expectations:
  - **Strings are not directly usable through FUNK variable lookup** in the same way as numeric/vector workflows.
  - **Vectors require explicit vector interpretation** (guide indicates using `v:` prefixing when referencing vector variables in FUNK).
- If a variable is only dynamically created (no green block), access patterns must be deliberate (typically via FUNK/helper logic), otherwise it is easy to treat names as literals by mistake.

## Recommended guardrails for this repository

- Use dynamic-variable structures only in modules where list performance/readability is a real bottleneck.
- Keep a clear naming schema document near the code (prefixes, suffixes, lifecycle/cleanup expectations).
- Encapsulate dynamic reads/writes in helper instructions to avoid raw string-concatenation spread across many call sites.
- Add temporary logging for generated names during development, then remove or gate logs after validation.
- Treat this pattern as **advanced/optional**; prefer simpler explicit variables where scope is small.

## Example pseudo-pattern (conceptual)

- Base key: `craftId = "craft" + i`
- Fields:
  - `craftId + "_pos"` => vector
  - `craftId + "_vel"` => vector
  - `craftId + "_status"` => number
- Helpers:
  - `SetCraftPos(craftId, vec)`
  - `GetCraftPos(craftId)`
  - `SetCraftStatus(craftId, code)`
  - `GetCraftStatus(craftId)`

This gives struct-like access patterns while staying inside Vizzy's existing block set.
