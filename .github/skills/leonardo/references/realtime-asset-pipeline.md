# Real-time asset pipeline

Use this reference for engine-bound 3D assets, materials, rigs, animations, or interchange validation.

## Contract before craft

Get the target engine/version, platform, camera distance, world units, coordinate convention, skeleton, animation rate, material model, texture channels, compression, and budgets before final production. If no budget exists, provide a proposed budget as an estimate and validate it in a representative scene.

Keep editable masters separate from derived exports. The engine-ready file is a build artifact unless the project deliberately authors in that format.

## Geometry and transforms

- Establish scale, forward/up axes, origin, pivot, naming, hierarchy, and transform-freeze policy before rigging or animation.
- Use topology appropriate to deformation and silhouette. Polygon count alone is not a quality metric; evaluate vertices after splits, material sections, overdraw, skinning cost, and screen size.
- Provide intentional normals and tangents. Test mirrored UVs, hard edges, negative scale, triangulation, and normal-map orientation in the target engine.
- Create collision and LODs according to gameplay and camera needs, then check transitions in motion.

## UVs, textures, and materials

- Keep consistent texel density where the art direction requires it; reserve unique density for focal assets intentionally.
- Treat base color/emissive as color data and normal, roughness, metallic, occlusion, masks, and height as non-color data unless the target pipeline specifies otherwise.
- Test mipmaps, compression, alpha mode, edge padding, tiling seams, and channel packing after engine import.
- Do not assume material-node graphs transfer between tools. Exchange textures and supported PBR parameters, then rebuild engine-specific shading as needed.

## Rigs and animation

- Confirm bone names, hierarchy, rest pose, deform-only export, influence limit, root-motion policy, and clip boundaries.
- Check skin weights at extreme poses, scale changes, looping seams, foot contact, root drift, and animation events.
- Bake procedural constraints only when the target cannot reproduce them, and retain the editable constrained rig in the master file.

## glTF exchange

glTF 2.0 uses meters and a right-handed coordinate system with +Y up and +Z forward. Its common material model is metallic-roughness PBR. Validate `.gltf` and `.glb` deliverables with Khronos glTF Validator, then still import them into the target engine because a specification-valid asset can violate project conventions or budgets.

## Acceptance check

Open the exported asset on a clean machine or clean checkout when practical. Confirm missing-file behavior, scale, pivot, hierarchy, materials, textures, alpha, normals, skeleton, clips, collision, LODs, bounds, and runtime cost. Capture import warnings and do not claim engine readiness from a DCC render alone.

## Authoritative starting points

- Khronos glTF 2.0 specification: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- Khronos glTF Validator: https://github.com/KhronosGroup/glTF-Validator
- Godot 3D import configuration: https://github.com/godotengine/godot-docs/blob/master/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.rst
- Blender manual: https://docs.blender.org/manual/en/latest/

Verify current exporter and engine support before relying on optional extensions.
