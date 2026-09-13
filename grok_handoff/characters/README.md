# Character Prompt Rules

Each subfolder describes a wholly original satirical fighter. Use it as a creative target, not a template for a public figure. Do not add a real name, familiar face, imitation voice, signature hairstyle/clothes, catchphrase, party/campaign mark, biography, or reference to a real event.

For each character, Grok must create:

```text
art_source/characters/<id>/{model,rig,textures,animation,reference}/
assets/characters/<id>/{sprites,portraits,vfx,audio}/
data/fighters/<id>.yaml
data/moves/<id>.yaml
data/finishers/<id>.yaml
docs/moves/<id>.md
```

Every package includes: a silhouette sheet, color/material guide, Blender master and export settings, turntable/reference render, atlas metadata, ground pivot, animation/event mapping, move sheet, provenance entry, and originality review. Runtime sprites use 1024x1024 cells, a lead-foot ground pivot, sRGB premultiplied alpha, 4 px atlas padding, and 8 px alpha extrusion. Author at 24 fps and map intentional combat timing to 60 Hz simulation frames.
