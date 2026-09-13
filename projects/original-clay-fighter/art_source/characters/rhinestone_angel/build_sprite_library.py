"""Render an original clay fighter's editable Blender pose library.

Run from the project root:
Blender --background --python art_source/characters/rhinestone_angel/build_sprite_library.py
"""
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets/characters/rhinestone_angel/sprites"
OUT.mkdir(parents=True, exist_ok=True)

def material(name, rgb, metallic=0):
    m=bpy.data.materials.new(name); m.use_nodes=True; m.diffuse_color=(*rgb,1); m.metallic=metallic; m.roughness=.62
    bsdf=m.node_tree.nodes.get("Principled BSDF"); bsdf.inputs["Base Color"].default_value=(*rgb,1); bsdf.inputs["Metallic"].default_value=metallic; bsdf.inputs["Roughness"].default_value=.62
    return m
PINK=material("rhinestone pink",(.75,.03,.30)); SILVER=material("silver denim",(.38,.42,.51),.55); GOLD=material("gold wings",(.72,.42,.08),.5); BLONDE=material("blonde wig",(.96,.65,.25)); PURPLE=material("star guitar",(.31,.03,.62),.25); SKIN=material("clay skin",(.74,.34,.20)); BLACK=material("boots",(.04,.03,.06))

parts={}; base={}
def add(name, kind, loc, scale, mat):
    if kind=="sphere": bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=loc)
    elif kind=="cone": bpy.ops.mesh.primitive_cone_add(vertices=8, location=loc)
    else: bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel=o.modifiers.new("soft clay", "BEVEL"); bevel.width=.12; bevel.segments=3; o.data.materials.append(mat); parts[name]=o; base[name]=(o.location.copy(), o.rotation_euler.copy()); return o

def reset():
    for n,o in parts.items(): o.location, o.rotation_euler = base[n][0].copy(), base[n][1].copy()

def build():
    # Blender armature is retained for production handoff; rigid pose pieces keep these renders inexpensive.
    bpy.ops.object.armature_add(location=(0,0,0)); rig=bpy.context.object; rig.name="RhinestoneAngel_PoseRig"
    rig["bones"]="root, spine, head, upper_arm_L, upper_arm_R, thigh_L, thigh_R, wing_L, wing_R, guitar"
    add("torso","cone",(0,0,4.5),(1.15,.55,1.55),PINK); add("head","sphere",(0,0,6.4),(.72,.58,.78),SKIN)
    add("wig","sphere",(-.05,.05,7.15),(1.25,.65,1.20),BLONDE)
    add("leg_L","cone",(-.52,0,2.3),(.42,.40,1.7),SILVER); add("leg_R","cone",(.52,0,2.3),(.42,.40,1.7),SILVER)
    add("boot_L","cube",(-.62,-.12,.75),(.55,.68,.30),BLACK); add("boot_R","cube",(.62,-.12,.75),(.55,.68,.30),BLACK)
    add("arm_L","cone",(-1.25,0,4.75),(.28,.30,1.25),PINK); add("arm_R","cone",(1.25,0,4.75),(.28,.30,1.25),PINK)
    add("wing_L","sphere",(-1.25,.35,5.15),(.65,.16,1.25),GOLD); add("wing_R","sphere",(1.25,.35,5.15),(.65,.16,1.25),GOLD)
    guitar=add("guitar","cone",(.92,-.55,3.6),(.70,.14,1.75),PURPLE); guitar.rotation_euler[1]=-.75; base["guitar"]=(guitar.location.copy(), guitar.rotation_euler.copy())

def pose(name, index):
    reset(); phase=index/3
    if name in {"walk","run"}:
        stride=.38 if name=="walk" else .62
        parts["leg_L"].rotation_euler[1]=stride*(-1 if index%2 else 1); parts["leg_R"].rotation_euler[1]=-parts["leg_L"].rotation_euler[1]
        parts["arm_L"].rotation_euler[1]=-parts["leg_L"].rotation_euler[1]; parts["arm_R"].rotation_euler[1]=parts["leg_L"].rotation_euler[1]
    elif name=="jump":
        parts["torso"].location.z+=.6+index*.12; parts["head"].location.z+=.6+index*.12; parts["wig"].location.z+=.6+index*.12
        for n in ("leg_L","leg_R","boot_L","boot_R","arm_L","arm_R","wing_L","wing_R","guitar"): parts[n].location.z+=.6+index*.12
        parts["wing_L"].rotation_euler[1]=-.6; parts["wing_R"].rotation_euler[1]=.6
    elif name=="crouch":
        for n in ("torso","head","wig","arm_L","arm_R","wing_L","wing_R","guitar"): parts[n].location.z-=.65
        parts["leg_L"].rotation_euler[1]=.5; parts["leg_R"].rotation_euler[1]=-.5
    elif name=="block_high":
        parts["guitar"].rotation_euler[1]=-1.65; parts["guitar"].location.z+=1.2
    elif name=="block_low":
        pose("crouch",0); parts["guitar"].rotation_euler[1]=-.25; parts["guitar"].location.z-=.4
    elif name in {"light","medium","heavy","star_chord"}:
        swing={"light":.45,"medium":.85,"heavy":1.15,"star_chord":1.4}[name]
        parts["guitar"].rotation_euler[1]=-swing; parts["guitar"].location.x+=.5; parts["arm_R"].rotation_euler[1]=-swing*.55
        if name=="star_chord": parts["wing_L"].rotation_euler[1]=-.35; parts["wing_R"].rotation_euler[1]=.35
    elif name=="hit": parts["torso"].rotation_euler[1]=-.18; parts["head"].rotation_euler[1]=-.22
    elif name=="knockdown":
        for o in parts.values(): o.rotation_euler[1]=1.35; o.location.z=.85
    elif name=="win":
        parts["guitar"].rotation_euler[1]=-.1; parts["guitar"].location.z+=1.5; parts["arm_R"].rotation_euler[1]=-.8
    elif name=="lose": parts["head"].rotation_euler[1]=.45; parts["guitar"].location.z-=.5

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False); build()
bpy.ops.object.camera_add(location=(0,-22,5)); cam=bpy.context.object; cam.data.lens=58; cam.rotation_euler=(Vector((0,0,4))-cam.location).to_track_quat('-Z','Y').to_euler(); bpy.context.scene.camera=cam
bpy.ops.object.light_add(type="AREA", location=(-5,-6,9)); bpy.context.object.data.energy=1100; bpy.context.object.data.shape="DISK"; bpy.context.object.data.size=5
bpy.ops.object.light_add(type="AREA", location=(5,1,7)); bpy.context.object.data.energy=700; bpy.context.object.data.color=(1,.25,.55); bpy.context.object.data.size=4
s=bpy.context.scene; s.render.engine="BLENDER_EEVEE"; s.render.resolution_x=512; s.render.resolution_y=512; s.render.resolution_percentage=100; s.render.image_settings.file_format="PNG"; s.render.film_transparent=True
clips={"idle":4,"walk":4,"run":4,"jump":4,"crouch":1,"block_high":1,"block_low":1,"light":1,"medium":1,"heavy":1,"star_chord":1,"hit":1,"knockdown":1,"wake":1,"intro":1,"win":1,"lose":1}
for clip,count in clips.items():
    for i in range(count):
        pose(clip if clip != "wake" else "idle", i); s.render.filepath=str(OUT/f"{clip}_{i:02}.png"); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/"art_source/characters/rhinestone_angel/rhinestone_angel.blend"))
