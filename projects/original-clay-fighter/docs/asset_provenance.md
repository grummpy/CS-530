# Asset provenance

## Title screen key art

`assets/ui/title/title_hero_v1.png` was generated for this project on
2026-09-13 using the four committed character design sheets as references. It
is original project artwork with no third-party game logos or television-show
branding. Pygame renders the title, tagline, menu labels, focus borders, and
navigation hint separately so the interface remains readable and interactive.
The selection screen derives cached fighter-card crops from the same key art
and pairs them with the three committed arena images. Names, player colors,
focus borders, stage labels, and the begin-match control remain live UI.

Runtime presentation uses the approved stage concept art in `assets/stages/*_concept.png`, created with the built-in image generator on 2026-09-13 and reviewed by the project owner. The accompanying Blender blockouts and the procedural source script are retained as editable stage foundations. Rhinestone Angel’s visual bible, Blender source, and transparent runtime frames are recorded under `art_source/characters/rhinestone_angel/` and `assets/characters/rhinestone_angel/`.

Mr. President’s original, fictional neon-orange clay character sheet was generated with the built-in image generator on 2026-09-13 and retained at `art_source/characters/mr_president/visual_bible_v1.png`; the same approved sheet supplies the HUD portrait. Its transparent runtime-frame library is deterministically generated from `art_source/characters/mr_president/build_sprite_library.py`. The editable Blender master `art_source/characters/mr_president/mr_president.blend` was built and rendered with Blender 5.2.1 from the adjacent `build_blender_model.py` source.

The Tech Billionaire’s visual bible and armored combat reference were generated with the built-in image generator on 2026-09-13 and retained under `art_source/characters/tech_billionaire/`. The native master and transparent clip library were built with Blender 5.2.1 from `build_sprite_library.py`; the project retains the Blender master, source script, manifests, and generated runtime frames together.

Master Chef’s approved asset sheet was generated with the built-in image generator on 2026-09-13 and retained under `art_source/characters/master_chef/`. His native master and transparent clip library were built with Blender 5.2.1 from the adjacent `build_sprite_library.py` source.

Current tracked inventory includes four Blender character masters, four character
frame libraries, 12 MP4 finisher previews, 360 PNG finisher frames, three stage
concept images, and five runtime PCM WAV tracks. The previously claimed 51
synthesized placeholder WAV files and one graybox turnaround are not present.
The per-file release manifest, hashes, and export-version checks remain Cycle 2
work.
