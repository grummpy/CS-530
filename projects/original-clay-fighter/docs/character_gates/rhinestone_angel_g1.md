# Rhinestone Angel — character gate G1

## PAPM baseline

**Mission:** establish one original adult clay-style fighter whose visual identity, movement rules, attack logic, and export contract can scale into runtime sprites.  
**Player promise:** a confident stage-performer combatant who uses a harmless star guitar and compact wings for readable, theatrical movement.  
**Acceptance:** no recognizable real-person likeness; silhouette remains readable at 1280×720; the prop does not cover the face; all grounded poses retain a planted support foot; attack and block poses communicate a clear active/recovery state.

## Reconciled specialist review

| Lane | Decision |
|---|---|
| PAPM | Freeze the original-fiction identity before generating the pose set. |
| Leonardo / Visual Standards | Lock pink rhinestone suit, auburn bouffant, gold back wings, and purple star guitar. Keep guitar in right hand and wings behind the torso. |
| Super | Export fixed-pivot, left-facing frames. Gameplay needs idle, walk, run, jump, crouch, high/low block, light/medium/heavy, special, hit, knockdown, win, and loss. |
| Motion | Guitar attacks originate from shoulder/torso rotation; recovery restores a stable wide stance. Jump uses compression → rise → apex → fall → two-foot landing. |
| Adult anatomy review | Character is an adult and is costumed for a non-sexualized all-ages fighting game. Joints stay within believable ranges; no exposed underwear, forced pose, or erotic framing. |
| Quality | Key art is an identity concept only. It is not yet a transparent sprite sheet, animation, collision asset, or in-game-tested render. |

## Combat contract

| Action | Pose / gameplay intent |
|---|---|
| Walk / run | Guitar stays low on the outside of the stride; wings stay folded. |
| Jump | Wings flutter decoratively only; no flight or collision advantage. |
| High block | Guitar neck angled upward to shield head and shoulder. |
| Low block | Knees flex; guitar body protects lead thigh. |
| Light / medium / heavy | Palm jab, horizontal guitar sweep, overhead guitar sweep. |
| Special: Star Chord | Two-handed guitar strike creates a short, non-graphic sparkle shockwave. |

## Required production exports after approval

- Editable Blender scene, rig, and material files.
- 1024×1024 transparent PNG frames with a ground pivot under the lead foot.
- Named clips: idle (8–12), walk, run, crouch, jump rise/apex/fall/land, high/low block, three normals, special, hit, knockdown/wake, intro, win, loss.
- Sprite atlas, clip manifest, frame event notes, hit/hurt/push boxes, and runtime import test.
- Optional finisher only after the match-state timeline, skip behavior, and results cleanup are implemented.

## Evidence and open work

`art_source/characters/rhinestone_angel/key_art_v2.png` is the current reviewed key art. It has a non-transparent background despite the generation request, so the runtime displays it as an opaque portrait render. `assets/characters/rhinestone_angel/manifest.json` makes that limitation explicit. The first-player match wiring now loads this portrait; multi-frame animation and a transparent sprite atlas remain the next production gate.
