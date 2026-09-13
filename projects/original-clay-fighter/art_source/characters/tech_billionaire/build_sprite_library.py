"""Build the editable Blender master and transparent runtime clips for The Tech Billionaire."""
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
CHAR = ROOT / "art_source" / "characters" / "tech_billionaire"
OUT = ROOT / "assets" / "characters" / "tech_billionaire" / "sprites"; OUT.mkdir(parents=True, exist_ok=True)

def mat(name, rgb, metal=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes.get("Principled BSDF"); b.inputs["Base Color"].default_value=(*rgb,1); b.inputs["Roughness"].default_value=.55; b.inputs["Metallic"].default_value=metal; return m
SKIN=mat("warm clay skin",(.64,.35,.22)); HAIR=mat("dark brown hair",(.07,.035,.02)); BLACK=mat("black shirt",(.018,.018,.022)); GRAY=mat("gray undershirt",(.20,.20,.23)); JEANS=mat("indigo jeans",(.025,.05,.13)); SHOE=mat("black shoes",(.012,.015,.02),.15); GRAPHITE=mat("graphite armor",(.08,.10,.12),.35); BRASS=mat("brass armor",(.50,.28,.05),.6); TEAL=mat("teal core",(0,.75,.78),.2); GLASSES=mat("smoked glasses",(.03,.04,.06),.5)
parts={}; base={}; armor=[]
def add(name, kind, loc, scale, material, armored=False):
    if kind=="sphere": bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=loc)
    elif kind=="cone": bpy.ops.mesh.primitive_cone_add(vertices=10, location=loc)
    else: bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); be=o.modifiers.new("soft clay bevel","BEVEL"); be.width=.10; be.segments=3; o.data.materials.append(material); parts[name]=o; base[name]=(o.location.copy(),o.rotation_euler.copy());
    if armored: armor.append(o)
    return o
def reset():
    for n,o in parts.items(): o.location,o.rotation_euler=base[n][0].copy(),base[n][1].copy(); o.hide_render=False
    for o in armor: o.hide_render=True
def build():
    bpy.ops.object.armature_add(location=(0,0,0)); rig=bpy.context.object; rig.name="TechBillionaire_PoseRig"; rig["bones"]="root,spine,head,arm_L,arm_R,thigh_L,thigh_R,wrist_controller,armor"; rig["armor_mode"]="Charge 210 damage; special activates 600 ticks; attacks gain +3 damage"
    add("torso","cone",(0,0,4.35),(1.10,.56,1.48),BLACK); add("undershirt","cube",(0,-.46,4.05),(.90,.10,.86),GRAY); add("head","sphere",(0,0,6.35),(.72,.56,.76),SKIN); add("hair","sphere",(0,.04,7.02),(.82,.58,.44),HAIR); add("bald_spot","sphere",(0,.30,7.16),(.27,.18,.08),SKIN)
    add("glasses","cube",(0,-.56,6.40),(.60,.055,.18),GLASSES); add("arm_L","cone",(-1.18,0,4.62),(.28,.30,1.18),GRAY); add("arm_R","cone",(1.18,0,4.62),(.28,.30,1.18),GRAY); add("wrist_controller","cube",(1.58,-.20,3.82),(.32,.22,.36),GRAPHITE); add("controller_core","sphere",(1.58,-.43,3.82),(.15,.05,.15),TEAL)
    add("leg_L","cone",(-.46,0,2.25),(.40,.38,1.70),JEANS); add("leg_R","cone",(.46,0,2.25),(.40,.38,1.70),JEANS); add("shoe_L","cube",(-.58,-.13,.72),(.52,.66,.28),SHOE); add("shoe_R","cube",(.58,-.13,.72),(.52,.66,.28),SHOE)
    for n,loc,scale,ma in [("armor_chest",(0,-.20,4.62),(1.25,.26,1.22),GRAPHITE),("armor_core",(0,-.48,4.70),(.28,.08,.28),TEAL),("armor_shoulder_L",(-1.24,0,5.28),(.53,.45,.40),BRASS),("armor_shoulder_R",(1.24,0,5.28),(.53,.45,.40),BRASS),("armor_boot_L",(-.55,-.10,1.24),(.60,.54,.70),GRAPHITE),("armor_boot_R",(.55,-.10,1.24),(.60,.54,.70),GRAPHITE),("armor_gauntlet_L",(-1.50,-.10,3.95),(.38,.32,.58),GRAPHITE),("armor_gauntlet_R",(1.50,-.10,3.95),(.38,.32,.58),GRAPHITE)]: add(n,"cube",loc,scale,ma,True)
def pose(clip,i):
    reset(); armed=clip.startswith("armor_") or clip=="exosuit_call"
    if armed:
        for o in armor:o.hide_render=False
    mode=clip.removeprefix("armor_")
    if mode in {"walk","run"}:
        stride=.38 if mode=="walk" else .62; parts["leg_L"].rotation_euler[1]=stride*(1 if i%2 else -1); parts["leg_R"].rotation_euler[1]=-parts["leg_L"].rotation_euler[1]
    elif mode=="jump":
        for o in parts.values(): o.location.z+=.55+i*.10
    elif mode=="crouch":
        for n in ("torso","undershirt","head","hair","glasses","arm_L","arm_R","wrist_controller","controller_core"):parts[n].location.z-=.55
    elif mode in {"light","medium","heavy","punch","kick"}:
        swing={"light":.45,"medium":.75,"heavy":1.0,"punch":1.15,"kick":.75}[mode]; parts["arm_R"].rotation_euler[1]=-swing; parts["wrist_controller"].location.x+=.55; parts["controller_core"].location.x+=.55
        if mode in {"kick"}:parts["leg_R"].rotation_euler[1]=-1.18; parts["shoe_R"].location.z+=.85; parts["shoe_R"].location.x+=.75
    elif mode=="exosuit_call":
        for o in armor:o.hide_render=False; o.location.z+=.45
    elif mode=="hit": parts["torso"].rotation_euler[1]=-.20;parts["head"].rotation_euler[1]=-.20
    elif mode=="knockdown":
        for o in parts.values():o.rotation_euler[1]=1.35;o.location.z=.82
    elif mode=="win":parts["arm_R"].rotation_euler[1]=-.9

bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False);build()
bpy.ops.object.camera_add(location=(0,-22,5));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,4))-cam.location).to_track_quat("-Z","Y").to_euler();bpy.context.scene.camera=cam
for loc,energy,color in [((-5,-6,9),1100,(1,1,1)),((5,1,7),700,(0,.8,1))]:bpy.ops.object.light_add(type="AREA",location=loc);o=bpy.context.object;o.data.energy=energy;o.data.color=color;o.data.size=5
s=bpy.context.scene;s.render.engine="BLENDER_EEVEE";s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.render.image_settings.file_format="PNG";s.render.film_transparent=True;s["asset_id"]="tech_billionaire";s["armor_mode"]="210 charge / 600 ticks / +3 damage"
CLIPS={"idle":4,"walk":4,"run":4,"jump":4,"crouch":1,"block_high":1,"block_low":1,"light":1,"medium":1,"heavy":1,"exosuit_call":1,"armor_idle":4,"armor_punch":1,"armor_kick":1,"hit":1,"knockdown":1,"wake":1,"intro":1,"win":1,"lose":1}
for clip,count in CLIPS.items():
    for i in range(count):pose(clip,i);s.render.filepath=str(OUT/f"{clip}_{i:02}.png");bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(CHAR/"tech_billionaire.blend"))
