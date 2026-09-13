# Mr. President — character gate G1

## Identity and combat contract

Mr. President is an original, fictional elderly real-estate-showman fighter. His readable silhouette is a broad navy suit, neon-orange clay skin, brilliant white eyes, sandy-blond curled pompadour, and a navy-and-brass briefcase. The concept sheet is `art_source/characters/mr_president/visual_bible_v1.png`.

| Action | Visual and play intent |
| --- | --- |
| Walk / run | Broad suit silhouette stays stable; briefcase remains low and outside the stride. |
| Jump | Compression, rise, apex, fall, and stable two-foot landing are represented by the named clip. |
| High / low block | Briefcase and shoulders create a readable high guard; knees compress for low guard. |
| Light / medium / heavy | Short hand jab, longer shoulder check, and committed briefcase arc. |
| Special: Hostile Takeover | A planted briefcase swing with a non-graphic paperwork burst. |

## Production package

- 29 transparent 512×512 runtime frames with an explicit 256×480 ground pivot.
- Editable deterministic source at `art_source/characters/mr_president/build_sprite_library.py`.
- Fighter profile, move timing, hit/hurt/push boxes, HUD portrait, sprite manifest, roster entry, and renderer routing.
- A Blender `.blend` export remains pending: the host currently has no discoverable Blender executable. The source preserves clip names and pivot for a later Blender replacement.
- Finisher remains deferred until the roster-wide finisher state, camera, skip, and guaranteed results cleanup exist.

## Acceptance notes

The character uses clearly fictional neon-orange clay skin, an original face and hair silhouette, generic unmarked banknotes, and no real-person references, logos, slogans, or currency markings. Grounded frames retain a support footprint and frame alpha is transparent outside the character.
