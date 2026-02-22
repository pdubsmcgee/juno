# Juno: New Origins Fandom Wiki Notes — Vizzy (Recursive Pass)

Primary seed page: <https://junoneworigins.fandom.com/wiki/Vizzy>

## Scope and method

- Started from the Vizzy wiki page and followed relevant in-wiki links recursively (depth ≤ 2) focused on Vizzy instructions, expressions, variables, and craft-control pages.
- Read 49 relevant pages in total (including the seed page) during this pass.
- Important caveat from the seed page: the wiki itself flags the Vizzy page as needing cleanup because it is "Outdate, incomplete, insufficient information." Treat these notes as a helpful external overview, not a ground-truth spec.

## What the wiki says about Vizzy at a high level

- Vizzy is the game's visual scripting language for automating craft behavior.
- The ecosystem described on the wiki is broad and includes:
  - control-flow blocks,
  - arithmetic/boolean/text/vector expressions,
  - craft-control instructions,
  - telemetry/property expressions,
  - variable systems (including lists), and
  - advanced text expressions via FUNK.

## Distilled findings by topic

### 1) Flow control and execution pacing

- **Flow Instructions** are described as the branching/loop core (repeat, while, for, and conditional logic).
- **For Loop** is documented as fixed-count iteration with an index variable and explicit start/end/increment inputs.
- **Wait Instructions** pause execution either for a duration or until a condition is true, making them key for pacing loops and avoiding over-tight polling.

### 2) Messaging and debugging primitives

- **Display** writes text at the top-center HUD area and is overwritten on each update.
- **Log** writes to the flight program log panel (useful for historical debugging).
- **Comment** is non-executing annotation for readability/maintenance.

### 3) Core expression families

- Arithmetic, comparison, boolean, and function expressions are framed as the mathematical basis for decision/control logic.
- Documented text operations include concatenation, length, character retrieval, substring, contains, and format.
- Vector operations are broken into creation, unary operations (for example length/normalization), and binary operations (for example dot/cross/angle/projection-style utilities).

### 4) Craft-control instructions highlighted by linked pages

- **Activate Stage** triggers the next stage.
- **Set Input** supports direct control-channel writes (e.g., roll/pitch/yaw/throttle, sliders, translation channels).
- **Set Axis** and **Lock Heading** provide orientation/attitude targeting tools.
- **Set Camera Attribute** and **Set Part Property** expose non-flight-control craft interactions (camera and part state/property operations).

### 5) Telemetry/data expressions highlighted by linked pages

The linked expression pages describe read access to multiple data groups used by automation logic, including:

- altitude fields,
- orbit descriptors,
- atmosphere data,
- performance/fuel information,
- navigation/velocity/input values,
- craft time,
- node/planet/part information,
- local vector conversions for part/craft contexts.

### 6) Variables and data structures

- The Vizzy link graph includes **Variables**, **User Input Variable Expression**, and **List Variables**, indicating support for scalar and list-oriented program state.
- This aligns with common patterns where flight logic uses persistent variables plus loops/conditions for stateful automation.

### 7) FUNK expression (advanced text expression path)

- The FUNK page describes a text-based expression evaluator introduced in an older version line (noted there as 0.9.700).
- It is positioned as a way to evaluate expressions from text and access additional properties, making it an advanced/dynamic path versus plain visual blocks.

## Practical usage guidance for this repository

- Use these wiki notes as a discovery map for capabilities and terminology.
- Before changing repository XML programs, continue validating concrete command/property availability against in-repo evidence (for example `Reference.xml` and existing operational program patterns), since the wiki explicitly warns about incompleteness/outdated content.

## Link set reviewed (seed + relevant recursive links)

- Seed: `https://junoneworigins.fandom.com/wiki/Vizzy`
- Key linked pages reviewed during recursion include:
  - `Wait_Instructions`
  - `Flow_Instructions`
  - `For_Loop_Instruction`
  - `Display_Instruction`
  - `Log_Instruction`
  - `Comment_Instruction`
  - `Arithmetic_Expressions`
  - `Boolean_Expressions`
  - `Comparison_Expressions`
  - `Math_Function_Expression`
  - `Text_*` expression pages
  - `Vector_*` expression pages
  - `FUNk_expression`
  - `Activate_Stage_Instruction`
  - `Set_Input_Instruction`
  - `Set_Axis_Instruction`
  - `Lock_Heading_Instruction`
  - `Set_Camera_Attribute_Instruction`
  - `Set_Part_Property_Instruction`
  - `Craft_*` telemetry/info expression pages
  - `Atmosphere_Information_Expression`
  - `Variables`
  - `List_Variables`
