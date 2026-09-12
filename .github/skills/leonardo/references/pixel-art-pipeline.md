# Pixel-art pipeline

Use this reference for sprites, tiles, pixel animation, atlases, or automated Aseprite exports.

## Pixel contract

Define the base canvas, pixels per world unit, target display scale, palette policy, tile dimensions, sprite anchor, collision reference, outline rule, light direction, animation frame rate, and engine filtering before production. Integer scaling and consistent pixel density matter more than the authoring zoom level.

## Drawing and animation

- Judge sprites at 1× and in-game scale. Build silhouette, value grouping, and clusters before surface detail.
- Avoid accidental single-pixel noise, stair-step inconsistency, mixed outline logic, and subpixel-looking motion unless stylistically deliberate.
- Use animation tags for named states and slices or agreed markers for pivots, hitboxes, sockets, and nine-slice regions.
- Animate keys and readable extremes first. Add anticipation, impact, recovery, secondary motion, and in-betweens only where they improve the intended feel.
- For tiles, test every required adjacency, corner, edge, variation, animated tile, and collision case in an actual map—not only as an atlas.

## Export contract

Preserve the layered `.aseprite` or equivalent master. Export lossless PNG plus structured metadata when the engine workflow supports it. Specify frame rectangles, durations, tags, trimming, rotation, padding/extrusion, origin, and whether empty frames are retained.

Use nearest-neighbor filtering for intentionally crisp pixels, disable inappropriate resampling, and check texture compression and mip behavior on the target platform. Atlas padding should prevent neighboring sprites from bleeding when sampled.

Aseprite’s command-line interface can batch-export sprite sheets and JSON metadata. Before automating, detect the installed executable/version and derive the command from the project’s existing convention. Do not overwrite master files, and remember that Aseprite source and official binaries have their own EULA rather than a blanket permissive license.

## Acceptance check

Verify palette, transparency, dimensions, scale, pivots, frame order, timing, loop seams, tags, texture bleeding, tile seams, and import settings in the game engine. Test at every supported window scale or camera zoom that can expose uneven pixels.

## Authoritative starting points

- Aseprite official repository and license summary: https://github.com/aseprite/aseprite
- Aseprite CLI documentation: https://github.com/aseprite/docs/blob/main/cli.md
- Aseprite sprite-sheet documentation: https://github.com/aseprite/docs/blob/main/sprite-sheet.md

Check the installed version before using CLI flags because export capabilities can change.
