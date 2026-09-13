"""Build an editable Mr. President Blender master scene.

Run with:
  /Applications/Blender.app/Contents/MacOS/Blender --background --python \
    art_source/characters/mr_president/build_blender_model.py
"""
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "art_source" / "characters" / "mr_president" / "mr_president.blend"

def material(name, color, metallic=0.0):
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    node = mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1.0)
    node.inputs["Roughness"].default_value = 0.58
    node.inputs["Metallic"].default_value = metallic
    return mat

NAVY = material("Navy suit", (0.03, 0.10, 0.32))
ORANGE = material("Neon orange clay", (1.0, 0.15, 0.0))
HAIR = material("Sandy blonde hair", (0.92, 0.62, 0.16))
WHITE = material("White shirt", (0.93, 0.93, 0.88))
CORAL = material("Coral patterned tie", (0.92, 0.16, 0.12))
BLACK = material("Shoes and ink", (0.015, 0.02, 0.04), 0.15)
BRASS = material("Briefcase brass", (0.56, 0.30, 0.05), 0.5)
GREEN = material("Generic banknotes", (0.20, 0.62, 0.18))

def piece(name, primitive, loc, scale, mat, rotation=(0, 0, 0)):
    if primitive == "sphere": bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=loc, rotation=rotation)
    elif primitive == "cone": bpy.ops.mesh.primitive_cone_add(vertices=12, location=loc, rotation=rotation)
    else: bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rotation)
    obj = bpy.context.object; obj.name = name; obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = obj.modifiers.new("Soft clay bevel", "BEVEL"); bevel.width = 0.10; bevel.segments = 3
    obj.data.materials.append(mat)
    return obj

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
# Editable rig contract for later animation/skin refinement.
bpy.ops.object.armature_add(location=(0, 0, 0)); rig = bpy.context.object; rig.name = "MrPresident_PoseRig"
rig["bones"] = "root, spine, head, arm_L, arm_R, thigh_L, thigh_R, briefcase"
rig["clip_contract"] = "idle, walk, run, jump, crouch, block_high, block_low, light, medium, heavy, hostile_takeover, hit, knockdown, wake, intro, win, lose"

# The model uses discrete, named clay components so each can be replaced or parented during rigging.
piece("torso_suit", "cone", (0, 0, 4.3), (1.30, 0.62, 1.52), NAVY)
piece("shirt_front", "cube", (0, -0.58, 4.48), (0.34, 0.08, 0.72), WHITE)
piece("tie", "cone", (0, -0.72, 4.10), (0.20, 0.08, 0.85), CORAL, (0.0, 0.0, 3.14))
piece("head", "sphere", (0, 0, 6.35), (0.86, 0.68, 0.90), ORANGE)
piece("hair_cap", "sphere", (0, 0.05, 7.03), (1.04, 0.70, 0.50), HAIR)
piece("hair_curl", "sphere", (0.38, -0.13, 7.38), (0.44, 0.30, 0.34), HAIR)
for side in (-1, 1):
    piece(f"eye_{side}", "sphere", (side * 0.30, -0.61, 6.42), (0.25, 0.10, 0.29), WHITE)
    piece(f"pupil_{side}", "sphere", (side * 0.30, -0.72, 6.42), (0.075, 0.04, 0.10), BLACK)
    piece(f"brow_{side}", "cube", (side * 0.30, -0.68, 6.76), (0.32, 0.06, 0.075), BLACK, (0.0, side * 0.28, side * 0.16))
piece("mouth", "sphere", (0, -0.69, 6.02), (0.30, 0.06, 0.14), BLACK)
piece("leg_L", "cone", (-0.54, 0, 2.28), (0.46, 0.45, 1.72), NAVY)
piece("leg_R", "cone", (0.54, 0, 2.28), (0.46, 0.45, 1.72), NAVY)
piece("shoe_L", "cube", (-0.62, -0.18, 0.75), (0.60, 0.76, 0.28), BLACK)
piece("shoe_R", "cube", (0.62, -0.18, 0.75), (0.60, 0.76, 0.28), BLACK)
piece("arm_L", "cone", (-1.38, 0, 4.56), (0.32, 0.34, 1.22), NAVY)
piece("arm_R", "cone", (1.38, 0, 4.56), (0.32, 0.34, 1.22), NAVY)
piece("briefcase", "cube", (1.88, -0.16, 3.35), (0.82, 0.20, 0.68), NAVY)
for x in (1.22, 2.54):
    piece(f"briefcase_corner_{x}", "sphere", (x, -0.39, 3.35), (0.11, 0.05, 0.11), BRASS)
piece("banknote_stack", "cube", (1.88, -0.38, 3.92), (0.56, 0.05, 0.18), GREEN)

# Retain a camera and studio lights so opening the file yields a legible reference render.
bpy.ops.object.camera_add(location=(0, -22, 5.0)); camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, 4.0)) - camera.location).to_track_quat("-Z", "Y").to_euler(); bpy.context.scene.camera = camera
for location, energy, color in [((-5, -6, 9), 1000, (1, 1, 1)), ((5, 1, 7), 650, (1.0, 0.38, 0.18))]:
    bpy.ops.object.light_add(type="AREA", location=location); light = bpy.context.object; light.data.energy = energy; light.data.color = color; light.data.shape = "DISK"; light.data.size = 5
scene = bpy.context.scene; scene.render.engine = "BLENDER_EEVEE"; scene.render.resolution_x = 512; scene.render.resolution_y = 512; scene.render.resolution_percentage = 100; scene.render.film_transparent = True
scene["asset_id"] = "mr_president"; scene["source_of_truth"] = "visual_bible_v1.png"
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
