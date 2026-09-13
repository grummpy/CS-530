"""Build original clay-style stage previews in Blender 5.2.

Run: Blender --background --python create_stage_previews.py -- <stage> <output.png>
"""
import bpy
import math
import sys
from pathlib import Path
from mathutils import Vector

stage, output = sys.argv[sys.argv.index("--") + 1:][:2]

def mat(name, color, metallic=0.0):
    m = bpy.data.materials.new(name); m.diffuse_color = (*color, 1)
    m.metallic = metallic; m.roughness = 0.68
    return m

CLAY = mat("warm clay", (0.50, 0.18, 0.11)); DARK = mat("charcoal clay", (0.035, 0.045, 0.07))
CREAM = mat("cream clay", (0.82, 0.72, 0.52)); STEEL = mat("brushed steel", (0.18, 0.26, 0.35), .65)
CYAN = mat("cool neon clay", (0.04, 0.48, 0.70)); ASPHALT = mat("asphalt clay", (0.12, 0.13, 0.16))
GREEN = mat("lawn clay", (0.14, 0.34, 0.16)); RED = mat("red clay", (0.62, 0.05, 0.035))

def cube(name, loc, scale, material, bevel=.12):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod=o.modifiers.new("soft clay edges", "BEVEL"); mod.width=bevel; mod.segments=3
    o.data.materials.append(material); return o

def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=loc); o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(material); return o

def spectator(x, z, color):
    sphere("cheering adult spectator", (x, 0.2, z+1.12), (.28,.18,.28), color)
    cube("spectator torso", (x,.2,z+.55), (.22,.16,.52), color, .18)
    # Raised arms distinguish the crowd while retaining a non-specific adult silhouette.
    for side in (-1,1):
        arm=cube("raised arm", (x+side*.26,.2,z+.92), (.07,.09,.38), color,.07); arm.rotation_euler[1]=side*.55

def light(loc, energy, color, size=5):
    bpy.ops.object.light_add(type="AREA", location=loc); o=bpy.context.object; o.data.energy=energy; o.data.color=color; o.data.shape="DISK"; o.data.size=size
    direction = Vector((0,0,1.5)) - o.location; o.rotation_euler = direction.to_track_quat('-Z','Y').to_euler()

def truckstop():
    cube("concrete fighting lot", (0,0,0), (8,2.5,.3), ASPHALT,.18)
    cube("truck stop building", (0,2.1,2.5), (5,.5,2), CREAM,.25)
    for x in (-5.8,5.8):
        cube("tractor trailer edge", (x,1.2,2.3), (1.8,.9,1.8), STEEL,.25)
        cube("trailer stripe", (x,0.25,2.4), (1.84,.05,.16), RED,.04)
    for x in (-6,-4.8,4.8,6): spectator(x,2.8,DARK if x<0 else CLAY)
    for x in (-2.8,2.8): cube("fuel canopy", (x,1.0,4.6), (1.6,.45,.12), CREAM,.08)
    for x in (-2.8,2.8): cube("fuel post", (x,1.0,2.8), (.12,.12,1.8), RED,.06)
    light((-5,-4,8),1200,(1,.46,.16)); light((5,-2,6),900,(.25,.55,1))

def residence():
    cube("front lawn fighting ground", (0,0,0), (8,2.5,.28), GREEN,.18)
    cube("neoclassical executive residence", (0,2.3,2.9), (5.4,.55,2.5), CREAM,.22)
    cube("central portico", (0,1.6,2.3), (2.0,.45,1.6), CREAM,.15)
    for x in (-1.4,-.7,0,.7,1.4): cube("portico column", (x,1.05,1.8), (.13,.16,1.7), CREAM,.08)
    cube("roof", (0,2.0,5.5), (5.8,.75,.25), STEEL,.08)
    for x in (-6,-4.9,4.9,6): spectator(x,2.5,STEEL)
    for x in (-7,7): sphere("topiary",(x,1.8,1.2),(.65,.5,.8),GREEN)
    light((-5,-4,8),1100,(1,.60,.28)); light((4,-2,6),700,(.25,.45,1))

def factory():
    cube("factory fight platform", (0,0,0), (8,2.5,.3), CREAM,.18)
    cube("assembly hall rear wall", (0,2.6,3), (8,.4,3.2), STEEL,.25)
    for x in (-5.5,-2.75,0,2.75,5.5):
        sphere("robot spectator head",(x,1.7,2.2),(.45,.35,.45),STEEL)
        cube("robot spectator body",(x,1.7,1.3),(.4,.28,.65),DARK,.14)
        cube("cyan status visor",(x,1.32,2.2),(.27,.04,.08),CYAN,.02)
    for x in (-6.5,6.5): cube("assembly robot arm base",(x,1.1,1.2),(.65,.55,1.2),DARK,.2)
    for x in (-6.5,6.5):
        arm=cube("assembly robot arm",(x,1.05,3),(.18,.25,1.6),STEEL,.12); arm.rotation_euler[1]=(-.55 if x<0 else .55)
    for x in (-4,0,4): cube("ceiling strip",(x,1.1,5.7),(1.25,.09,.08),CYAN,.03)
    light((-4,-4,8),900,(.16,.65,1)); light((5,-3,7),950,(.85,.95,1))

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
bpy.context.scene.world.color=(.015,.02,.04)
{"roadside_truck_stop": truckstop, "executive_lawn": residence, "electric_assembly_hall": factory}[stage]()
bpy.ops.object.camera_add(location=(0,-30,6)); cam=bpy.context.object; cam.data.lens=52
cam.rotation_euler=(Vector((0,1.5,2.1))-cam.location).to_track_quat('-Z','Y').to_euler(); bpy.context.scene.camera=cam
scene=bpy.context.scene; scene.render.engine="BLENDER_EEVEE"; scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"; scene.render.filepath=str(Path(output).resolve()); scene.render.film_transparent=False
scene.view_settings.look="AgX - Medium High Contrast"; bpy.ops.wm.save_as_mainfile(filepath=str(Path(output).with_suffix('.blend').resolve()))
bpy.ops.render.render(write_still=True)
