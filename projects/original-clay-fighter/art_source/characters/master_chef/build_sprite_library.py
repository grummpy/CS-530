"""Build Master Chef's editable Blender master and transparent runtime clips."""
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3]; CHAR=ROOT/"art_source"/"characters"/"master_chef"; OUT=ROOT/"assets"/"characters"/"master_chef"/"sprites"; OUT.mkdir(parents=True,exist_ok=True)
def mat(n,c,me=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;b=m.node_tree.nodes.get("Principled BSDF");b.inputs["Base Color"].default_value=(*c,1);b.inputs["Roughness"].default_value=.58;b.inputs["Metallic"].default_value=me;return m
WHITE=mat("chef white",(.88,.84,.74));PANTS=mat("charcoal trousers",(.06,.055,.05));SKIN=mat("clay skin",(.62,.31,.18));HAIR=mat("golden blonde",(.82,.48,.10));BLACK=mat("clogs",(.015,.015,.018),.2);STEEL=mat("knife steel",(.40,.43,.45),.7);SALMON=mat("salmon",(.78,.22,.12));FIN=mat("salmon fins",(.10,.16,.20));
parts={};base={}
def add(n,k,loc,scale,ma):
 if k=="sphere":bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=loc)
 elif k=="cone":bpy.ops.mesh.primitive_cone_add(vertices=10,location=loc)
 else:bpy.ops.mesh.primitive_cube_add(location=loc)
 o=bpy.context.object;o.name=n;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);q=o.modifiers.new("soft clay bevel","BEVEL");q.width=.1;q.segments=3;o.data.materials.append(ma);parts[n]=o;base[n]=(o.location.copy(),o.rotation_euler.copy());return o
def reset():
 for n,o in parts.items():o.location,o.rotation_euler=base[n][0].copy(),base[n][1].copy()
def build():
 bpy.ops.object.armature_add(location=(0,0,0));r=bpy.context.object;r.name="MasterChef_PoseRig";r["bones"]="root,spine,head,arm_L,arm_R,thigh_L,thigh_R,knife,salmon";r["special"]="Kitchen Rush: chef knife and intact salmon dual-wielded as non-graphic cooking tools"
 add("torso","cone",(0,0,4.4),(1.15,.58,1.52),WHITE);add("head","sphere",(0,0,6.38),(.74,.57,.80),SKIN);add("hair","sphere",(0,.03,7.13),(1.02,.65,.55),HAIR);add("brow_L","cube",(-.28,-.58,6.68),(.28,.06,.07),PANTS);add("brow_R","cube",(.28,-.58,6.68),(.28,.06,.07),PANTS);add("mouth","sphere",(0,-.60,6.03),(.31,.05,.14),PANTS)
 add("leg_L","cone",(-.50,0,2.25),(.42,.40,1.72),PANTS);add("leg_R","cone",(.50,0,2.25),(.42,.40,1.72),PANTS);add("clog_L","cube",(-.62,-.14,.72),(.56,.70,.28),BLACK);add("clog_R","cube",(.62,-.14,.72),(.56,.70,.28),BLACK)
 add("arm_L","cone",(-1.30,0,4.72),(.30,.31,1.20),WHITE);add("arm_R","cone",(1.30,0,4.72),(.30,.31,1.20),WHITE);knife=add("knife","cone",(1.66,-.35,3.75),(.20,.06,1.20),STEEL);knife.rotation_euler[1]=-.55;base["knife"]=(knife.location.copy(),knife.rotation_euler.copy());fish=add("salmon","sphere",(-1.62,-.24,3.72),(.35,.17,1.14),SALMON);add("salmon_tail","cone",(-1.62,-.24,4.78),(.36,.10,.38),FIN)
build();bpy.ops.object.camera_add(location=(0,-22,5));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,4))-cam.location).to_track_quat("-Z","Y").to_euler();bpy.context.scene.camera=cam
for loc,en,col in [((-5,-6,9),1100,(1,1,1)),((5,1,7),650,(1,.65,.22))]:bpy.ops.object.light_add(type="AREA",location=loc);o=bpy.context.object;o.data.energy=en;o.data.color=col;o.data.size=5
s=bpy.context.scene;s.render.engine="BLENDER_EEVEE";s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.render.image_settings.file_format="PNG";s.render.film_transparent=True;s["asset_id"]="master_chef"
def pose(c,i):
 reset()
 if c in {"walk","run"}:
  a=.40 if c=="walk" else .65;parts["leg_L"].rotation_euler[1]=a*(1 if i%2 else -1);parts["leg_R"].rotation_euler[1]=-parts["leg_L"].rotation_euler[1]
 elif c=="jump":
  for o in parts.values():o.location.z+=.55+i*.10
 elif c=="crouch":
  for n in ("torso","head","hair","arm_L","arm_R","knife","salmon","salmon_tail"):parts[n].location.z-=.55
 elif c in {"light","medium","heavy","kitchen_rush"}:
  a={"light":.45,"medium":.75,"heavy":1.0,"kitchen_rush":1.35}[c];parts["arm_R"].rotation_euler[1]=-a;parts["knife"].rotation_euler[1]=-a;parts["knife"].location.x+=.45;parts["arm_L"].rotation_euler[1]=a*.7;parts["salmon"].rotation_euler[1]=a*.8;parts["salmon_tail"].rotation_euler[1]=a*.8
 elif c=="hit":parts["torso"].rotation_euler[1]=-.2;parts["head"].rotation_euler[1]=-.2
 elif c=="knockdown":
  for o in parts.values():o.rotation_euler[1]=1.35;o.location.z=.82
 elif c=="win":parts["knife"].location.z+=1.2;parts["salmon"].location.z+=1.2
CLIPS={"idle":4,"walk":4,"run":4,"jump":4,"crouch":1,"block_high":1,"block_low":1,"light":1,"medium":1,"heavy":1,"kitchen_rush":1,"hit":1,"knockdown":1,"wake":1,"intro":1,"win":1,"lose":1}
for c,count in CLIPS.items():
 for i in range(count):
  target=OUT/f"{c}_{i:02}.png"
  if not target.exists():
   pose(c,i);s.render.filepath=str(target);bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(CHAR/"master_chef.blend"))
