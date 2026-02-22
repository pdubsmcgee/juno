# Steam Guide Notes: MFD HUD Construction (Guide `id=2954199325`)

## Source and scope
- Source guide title: **"Creating a Heads Up Display using a MFD Panel"**.
- Scope of these notes: distill practical build + Vizzy patterns for SimpleRockets 2 / Juno HUDs rendered through a Multi-Function Display (MFD).
- These are implementation notes, not a canonical API spec.

## Distilled workflow
1. **Create a transparent MFD surface**
   - Add an MFD to the craft.
   - In paint mode, switch paint target to **All** (not Primary).
   - Apply a transparent-ish glass material/color so the panel itself is effectively invisible in the camera view.

2. **Set up camera geometry**
   - Mount a camera (or piloted chair/Drood viewpoint) aimed through the MFD center.
   - Alignment matters more than exact parts: keep camera axis centered through panel center for stable HUD overlay behavior.

3. **Enable MFD Vizzy program**
   - Set MFD Program to **Custom** so the MFD exposes the MFD-specific Vizzy block category.
   - Rename parts clearly (single-word identifiers help when wiring part-variable paths).

4. **Author HUD primitives as widgets**
   - Treat MFD objects as widget instances (rectangle, sprite, line, text, etc.).
   - Create once, then update each physics tick instead of recreating each frame.
   - Use parent-child widget hierarchy to move/scale/rotate grouped elements with fewer operations.

5. **Implement hollow reticles/boxes**
   - A default rectangle is filled; for HUD reticles, use either:
     - a rectangle + 4 line children, or
     - a border sprite/icon style (author-recommended shortcut).

6. **Drive screen-space positioning from world-space targets**
   - Compute/track target position in world frame (PCI in the guide).
   - Convert target direction into camera-local offset.
   - Write resulting 2D offset into widget position each tick.

7. **Optional: mechanically gimbal the camera/MFD rig**
   - Add yaw + pitch motor stack to keep camera pointed at tracked target.
   - Balance assembly and use counterweight if required.
   - Route motor inputs from HUD/MFD Vizzy variables.

## "Special language" takeaways (MFD Vizzy dialect)
These are the practical semantics emphasized in the guide's MFD programming style:

- **Typed widget model**
  - Objects are broadly manipulable as `Widget`.
  - Many objects also support subtype blocks (e.g., sprite-specific setters/getters).

- **Scene graph style composition**
  - `Parent` relationships turn individual widgets into transformable groups.
  - Group transforms are preferred for performance and maintainability.

- **MFD coordinate space**
  - Origin is centered on the display (`0,0` at center, not top-left).
  - Coordinates are fine-grained and accept fractional values.

- **Tick-driven update model**
  - Recompute and set HUD element transforms/properties each physics frame for moving targets.

- **Color pipeline**
  - Hex color values are directly usable for widget color blocks.

## Practical guidance for this repository
- Prefer this MFD HUD method when you need custom reticles/overlays tightly coupled to a specific camera view.
- If your only goal is "mark a world position", evaluate native target-node reticle features first; the guide author notes that newer target-node support can replace parts of this custom HUD approach.
- Keep any new Vizzy blocks added to flight XML grounded in locally verified block names/fields before operationalizing.

## Caveats from guide discussion
- Guide comments indicate transparent MFD behavior may vary by game version.
- The guide itself notes that native target-node reticles can supersede parts of this workflow, with trade-offs (jitter/update-frequency sensitivity).
