# Asset provenance

Runtime presentation uses the approved stage concept art in `assets/stages/*_concept.png`, created with the built-in image generator on 2026-09-13 and reviewed by the project owner. The accompanying Blender blockouts and the procedural source script are retained as editable stage foundations. Rhinestone Angel’s visual bible, Blender source, and transparent runtime frames are recorded under `art_source/characters/rhinestone_angel/` and `assets/characters/rhinestone_angel/`.

Mr. President’s original, fictional neon-orange clay character sheet was generated with the built-in image generator on 2026-09-13 and retained at `art_source/characters/mr_president/visual_bible_v1.png`; the same approved sheet supplies the HUD portrait. Its transparent runtime-frame library is deterministically generated from `art_source/characters/mr_president/build_sprite_library.py`. The editable Blender master `art_source/characters/mr_president/mr_president.blend` was built and rendered with Blender 5.2.1 from the adjacent `build_blender_model.py` source.

The Tech Billionaire’s visual bible and armored combat reference were generated with the built-in image generator on 2026-09-13 and retained under `art_source/characters/tech_billionaire/`. The native master and transparent clip library were built with Blender 5.2.1 from `build_sprite_library.py`; the project retains the Blender master, source script, manifests, and generated runtime frames together.

The handoff claimed 51 synthesized placeholder WAV files and one graybox turnaround image, but neither is present in this repository tree after reconciliation. Character sprites, HUD/button art, and finisher video files remain separate production work.
