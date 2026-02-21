# Vizzy Commands Web Research (Juno: New Origins)

## Scope and method
- Primary source reviewed: `https://junoneworigins.fandom.com/wiki/Vizzy?action=raw`.
- Follow-up pages reviewed from links on the Vizzy page (instruction/expression/event pages).
- Scoped Google search attempted with `site:junoneworigins.fandom.com vizzy programming`, but automated access was blocked by Google anti-bot interstitial in this environment.

## High-confidence command families (from the Vizzy wiki page)
The Vizzy page groups commands into these categories:
- Program Flow
- Operators
- Craft Instructions
- Craft Information
- Events
- Variables
- Lists
- Custom Expressions
- Custom Instructions
- Multi Function Display

Source snippet (`Vizzy?action=raw`):
- `== Vizzy Elements ==`
- `=== Program Flow ===`
- `=== Operators ===`
- `=== Craft Instructions ===`
- `=== Craft Information ===`
- `=== Events ===`
- `=== Variables ===`
- `===Lists===`
- `===[[Custom Expressions]]===`
- `===[[Custom Instructions]]===`
- `===[[Multi Function Display]] ===`

## Command details captured from linked pages

### Set Input Instruction
- Syntax: `Set <Value> to <Number>`
- Available `<Value>` options listed:
  - Roll
  - Pitch
  - Yaw
  - Throttle
  - Break
  - Slider 1
  - Slider 2
  - Translate Forward
  - Translate Right
  - Translate Up
  - Translate Mode

Source: `https://junoneworigins.fandom.com/wiki/Set_Input_Instruction?action=raw`.

### Lock Heading Instruction
- Heading lock modes listed:
  - None (reset heading)
  - Prograde
  - Retrograde
  - Target
  - Burn Node
  - Current

Source: `https://junoneworigins.fandom.com/wiki/Lock_Heading_Instruction?action=raw`.

### Wait Instructions
- `Wait N Seconds`: pauses script for a time value.
- `Wait Until Condition`: pauses until a boolean expression becomes true.

Source: `https://junoneworigins.fandom.com/wiki/Wait_Instructions?action=raw`.

### Flow Instructions
- Available control-flow blocks listed:
  - `repeat`
  - `while`
  - `for`
  - `break`
  - `if`
  - `else if`
  - `else`

Source: `https://junoneworigins.fandom.com/wiki/Flow_Instructions?action=raw`.

### Set Camera Attribute Instruction
- Camera attributes/modes include:
  - X Rotation, Y Rotation, Tilt, Zoom
  - Camera Mode: Orbit (Planet Aligned), Orbit (Space Aligned), Chase View, Fly-By Cinematic, Fly-By Stationary, Camera Parts
  - Camera Index

Source: `https://junoneworigins.fandom.com/wiki/Set_Camera_Attribute_Instruction?action=raw`.

### Set Part Property Instruction
- Properties listed:
  - Activated
  - Focused
  - Name
  - Explode
  - Fuel Transfer
- `<value>` documented as `0 or 1`.

Source: `https://junoneworigins.fandom.com/wiki/Set_Part_Property_Instruction?action=raw`.

### Variables
- Variables must be created before use in the Vizzy editor.
- Core operations documented:
  - `set variable <var> to <value>`
  - `change variable <var> by <number>`

Source: `https://junoneworigins.fandom.com/wiki/Variables?action=raw`.

### List Variables
- List operations documented include add/insert/remove/set/sort/reverse/length/index lookup.
- Indexing is documented as 1-based.

Source: `https://junoneworigins.fandom.com/wiki/List_Variables?action=raw`.

### Craft information expressions (quick index pages)
The following pages provide short lists of available telemetry fields:
- Craft Nav Information Expression
- Craft Orbit Information Expression
- Craft Velocity Information Expression
- Craft Fuel Level Expression
- Craft Time Information Expression
- Miscellaneous Information Instruction
- Planet Information Expression

Sources:
- `https://junoneworigins.fandom.com/wiki/Craft_Nav_Information_Expression?action=raw`
- `https://junoneworigins.fandom.com/wiki/Craft_Orbit_Information_Expression?action=raw`
- `https://junoneworigins.fandom.com/wiki/Craft_Velocity_Information_Expression?action=raw`
- `https://junoneworigins.fandom.com/wiki/Craft_Fuel_Level_Expression?action=raw`
- `https://junoneworigins.fandom.com/wiki/Craft_Time_Information_Expression?action=raw`
- `https://junoneworigins.fandom.com/wiki/Miscellaneous_Information_Instruction?action=raw`
- `https://junoneworigins.fandom.com/wiki/Planet_Information_Expression?action=raw`

## Relevant link index for further documentation expansion
A broader set of Vizzy pages can be enumerated via MediaWiki category API:
- Endpoint used: `https://junoneworigins.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:Vizzy&cmlimit=200&format=json`
- Example pages from this list: `Activate Stage Instruction`, `Boolean Expressions`, `For Loop Instruction`, `Lock Heading Instruction`, `Set Input Instruction`, `Variables`, etc.

## UNVERIFIED / caution notes
- Some linked pages are sparse or empty in `action=raw` output (e.g., certain Event pages).
- Terminology inconsistencies exist in community docs (for example `Break` vs `Brake`, typos like `apoapis/perapis`).
- Use in-game block menus as final authority when naming exact options.
