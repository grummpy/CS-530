# The Tech Billionaire — character gate G1

## Identity and combat contract

The Tech Billionaire is an original fictional tech-magnate fighter: layered black-and-gray casual executive clothing, indigo jeans, asymmetric glasses, a controlled smirk, styled dark-brown undercut, and a graphite/brass cybernetic wrist controller. The approved visual reference is `art_source/characters/tech_billionaire/visual_bible_v1.png`; armored punch/kick reference is `armor_combat_v1.png`.

| System | Contract |
| --- | --- |
| Charge | Damage received adds to the controller charge, capped at 210. |
| Activation | Press Special when fully charged to summon the original Patriot Prototype Exosuit. |
| Duration | Armor Mode lasts 600 simulation ticks, or 10 seconds at 60 Hz. |
| Benefit | Each attack hit gains exactly +3 damage during Armor Mode. |
| Visual state | Base clips switch to armor idle/punch/kick clips while `armor_ticks` is positive. |

The Exosuit uses original graphite panels, brass trim, and teal energy seams. It contains no franchise, brand, or logo elements.

## Production exports

- Native Blender 5.2.1 master: `tech_billionaire.blend`, with named parts and `TechBillionaire_PoseRig` contract.
- 35 transparent Blender-rendered runtime frames, including base and Armor Mode clips.
- Sprite manifest, profile, move timing, collision boxes, deterministic Armor Mode state, renderer routing, HUD portrait, and roster entry.
- Finisher remains deferred until the shared multi-character finisher system exists.
