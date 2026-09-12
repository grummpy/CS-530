---
name: leonardo
description: Visual-art and game-asset workflow for art direction, graphics software, concept art, illustration, UI, 2D sprites, pixel art, 3D modeling, sculpting, materials, rigging, animation, lighting, VFX, rendering, and engine-ready asset pipelines. Use when the requested outcome is primarily visual or requires creating, editing, evaluating, or integrating artistic assets.
---

# Leonardo

Create coherent, production-ready visual work that serves the intended mood, gameplay, medium, and technical budget.

## Art-production loop

1. Establish the subject, purpose, audience, visual hierarchy, style, references, deliverable, dimensions, viewing distance, platform, and technical limits.
2. Inspect existing art, brand or game style, source files, palettes, topology, rigs, naming, licenses, and export conventions before producing replacements.
3. Set an art direction with concrete shape language, value structure, color, materials, lighting, camera, scale, and consistency rules. Distinguish inspiration from direct imitation.
4. Produce the cheapest useful proof first: thumbnails, silhouettes, palette studies, blockouts, grayboxes, or low-resolution sprite tests. Resolve composition and readability before detail.
5. Build the requested asset with editable sources and a non-destructive workflow where the software supports it.
6. Verify the result at its real display size and in its target context. Check silhouette, contrast, animation, seams, normals, UVs, alpha, compression, scale, pivots, naming, and import behavior as applicable.
7. Deliver source and export formats, dimensions, color space, asset dependencies, import settings, and any remaining artistic or technical limitations.

## Domain coverage

- 2D: drawing, painting, illustration, vector graphics, icons, typography, layouts, textures, sprites, tile sets, atlases, parallax layers, and frame animation.
- Pixel art: deliberate pixel placement, restricted palettes, cluster quality, clean silhouettes, consistent pixel density, nearest-neighbor scaling, tileability, and readable animation timing.
- 3D: reference and blockout, hard-surface and organic modeling, sculpting, retopology, UVs, baking, PBR materials, procedural texturing, rigging, skinning, animation, lighting, cameras, and rendering.
- Real-time art: LODs, collision, pivots, texel density, draw calls, batching, material count, shader cost, overdraw, skeletal budgets, VFX, UI, and engine import/export.
- Tools: Photoshop, Illustrator, Blender, Maya, 3ds Max, ZBrush, Substance 3D, Krita, Aseprite, Affinity, Houdini, Unreal, Unity, Godot, and suitable open formats.

## Specialist references

- For meshes, rigs, materials, texture color space, glTF exchange, engine import, validation, and runtime budgets, read [references/realtime-asset-pipeline.md](references/realtime-asset-pipeline.md).
- For pixel density, palettes, animation tags, sprite sheets, tiles, filtering, and automated export, read [references/pixel-art-pipeline.md](references/pixel-art-pipeline.md).
- Read only the reference relevant to the requested asset; do not load 3D guidance for an ordinary illustration.

## Collaboration and quality rules

- Use the Super approach when the primary outcome is game mechanics, engine code, runtime systems, performance implementation, or a playable build. Supply Super with explicit asset budgets and import requirements.
- Match the project's established visual language before introducing a new one. Keep characters, props, environments, UI, lighting, and VFX visually related.
- Optimize for the final medium, not the authoring viewport. Preserve editable master files and derive runtime exports from them.
- Use image-generation or editing tools when they fit the requested raster outcome; use native vector, 3D, or engine workflows when editability and exact structure matter.
- Never claim that generated work is hand-drawn, scanned, modeled, licensed, or tested in-engine when it is not.
- Respect copyrights, trademarks, likeness rights, fonts, stock licenses, and third-party asset terms. Create original work instead of copying a living artist's signature style.
