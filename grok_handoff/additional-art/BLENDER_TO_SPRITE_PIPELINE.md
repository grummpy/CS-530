# Blender-to-Sprite Art Pipeline Prompt

```text
Create an original tactile claymation-inspired art pipeline for the six fighters. Model in Blender with matte polymer-clay materials, visible fingerprints/seams, simple bead-like eyes, large readable hands, and asymmetrical silhouettes. Use original geometry and materials only. Work in 3/4 view with an orthographic fighting camera; preserve a common lead-foot ground pivot, body scale, outline treatment, and warm key/cool rim/soft contact-shadow light rig.

For each fighter create editable .blend scenes for model, rig, materials, animation, camera, and light rig. Render transparent PNG sprite sequences at 1024x1024 per frame, 24 fps source cadence, sRGB, premultiplied alpha. Export atlas JSON containing frame rect, duration, event names, ground pivot, facing, and source checksum. Pack core, special, and VFX atlases independently with 4 px margin and 8 px alpha extrusion. Validate no seam, halo, pivot drift, color-space shift, or accidental mirrored handedness.

Author animation as readable combat poses: anticipation, active silhouette, impact hold, recovery. Use stop-motion-like pose offsets sparingly and never let render timing determine collision. Attach named events such as FOOTSTEP, WHOOSH, HIT_LIGHT, HIT_HEAVY, SPAWN_PROJECTILE, SUPER_FLASH, and FINISHER_CUE. Create one graybox turnaround and silhouette readability check before detailing each character.
```
