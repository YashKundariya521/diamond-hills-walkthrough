
# ---------- appended to build.py when run in bake mode: light baking and glTF export ----------
import numpy as np,time
OUT=f'{HQ}/out';os.makedirs(OUT,exist_ok=True)
LM=int(ARGS[ARGS.index('bake')+1]);SMP=int(ARGS[ARGS.index('bake')+2])
LSCALE=8.0;VSCALE=8.0
t0=time.time()
deselect()
sc.cycles.use_denoising=False
all_shell=[o for o in col.objects if o.type=='MESH' and o.get('shell')==1]
noLM={'sheer','rustcurt','led','brass','cane','glass'}
for o in list(all_shell):
    nm=o.data.materials[0].name if o.data.materials else ''
    if nm in noLM:o['shell']=0;o['furn']=1;all_shell.remove(o)
for o in all_shell:o.select_set(True)
bpy.context.view_layer.objects.active=all_shell[0];bpy.ops.object.join();shell=bpy.context.view_layer.objects.active;shell.name='SHELL'
# planar world UVs stay on 'uv'; a second channel carries the lightmap
lm=shell.data.uv_layers.new(name='lm');shell.data.uv_layers.active=lm
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(60),island_margin=.0012,area_weight=0,correct_aspect=True,scale_to_bounds=False);bpy.ops.object.mode_set(mode='OBJECT')
print('UV done',round(time.time()-t0),'faces',len(shell.data.polygons))
img=bpy.data.images.new('LM',LM,LM,float_buffer=True,alpha=False);img.colorspace_settings.name='Non-Color'
for m in shell.data.materials:
    n=m.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.name='BAKE';t.image=img;t.interpolation='Linear';uvn=n.new('ShaderNodeUVMap');uvn.uv_map='lm';m.node_tree.links.new(uvn.outputs[0],t.inputs[0]);n.active=t
for o in col.objects:
    if o.get('glass'):o.hide_render=True
sc.cycles.samples=SMP;b=sc.render.bake;b.use_pass_direct=True;b.use_pass_indirect=True;b.use_pass_color=False;b.margin=6;b.target='IMAGE_TEXTURES';sc.cycles.bake_type='DIFFUSE'
deselect();shell.select_set(True);bpy.context.view_layer.objects.active=shell
bpy.ops.object.bake(type='DIFFUSE',pass_filter={'DIRECT','INDIRECT'},margin=6,use_clear=True)
print('shell baked',round(time.time()-t0))
# save raw light, denoise it with Open Image Denoise in a clean Blender process, then encode for the browser
import subprocess
img.filepath_raw=f'{OUT}/lm_raw.exr';img.file_format='OPEN_EXR';img.save()
subprocess.check_call([bpy.app.binary_path,'-b','--factory-startup','-P',f'{HQ}/denoise.py','--',f'{OUT}/lm_raw.exr',f'{OUT}/lm_dn.exr'],stdout=subprocess.DEVNULL)
dn=bpy.data.images.load(f'{OUT}/lm_dn.exr');dn.colorspace_settings.name='Non-Color';a=np.array(dn.pixels[:],dtype=np.float32).reshape(LM,LM,4)[:,:,:3]
print('denoised',round(time.time()-t0),'mean',float(a.mean()),'max',float(a.max()))
enc=np.sqrt(np.clip(a/LSCALE,0,1))
im2=bpy.data.images.new('LMOUT',LM,LM,alpha=False);im2.colorspace_settings.name='Non-Color';px=np.ones((LM,LM,4),dtype=np.float32);px[:,:,:3]=enc;im2.pixels.foreach_set(px.ravel());sc.render.image_settings.file_format='JPEG';sc.render.image_settings.quality=94;sc.render.image_settings.color_mode='RGB';sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;im2.save_render(f'{OUT}/lightmap.jpg',scene=sc)
for m in shell.data.materials:
    n=m.node_tree.nodes
    if 'BAKE' in n:n.remove(n['BAKE'])
    for nd in [x for x in n if x.type=='UVMAP']:n.remove(nd)
# ---------- furniture: bake light into vertices ----------
furn=[o for o in col.objects if o.type=='MESH' and o.get('furn')==1 and not o.hide_render]
print('furniture objects',len(furn))
for o in furn:
    deselect();o.select_set(True);bpy.context.view_layer.objects.active=o
    if o.data.users>1:o.data=o.data.copy()
    if not any(True for m in o.data.materials if m and m.name in('led',)):
        if len(o.data.polygons)<5000 and o.data.polygons:
            ss=o.modifiers.new('bakeSub','SUBSURF');ss.subdivision_type='SIMPLE';ss.levels=2 if len(o.data.polygons)>400 else 3
    for mod in list(o.modifiers):
        try:bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception as e:print('modfail',o.name,e);o.modifiers.remove(mod)
    ca=o.data.color_attributes.new('bake','FLOAT_COLOR','POINT');o.data.color_attributes.active_color=ca
    o.select_set(False)
deselect()
bakeset=[o for o in furn if o.data.polygons and not any(m and m.name=='led' for m in o.data.materials)]
for o in bakeset:o.select_set(True)
bpy.context.view_layer.objects.active=bakeset[0]
sc.cycles.samples=max(96,SMP//3);b.target='VERTEX_COLORS'
bpy.ops.object.bake(type='DIFFUSE',pass_filter={'DIRECT','INDIRECT'},target='VERTEX_COLORS',use_clear=True)
print('vertex baked',round(time.time()-t0))
for o in bakeset:
    ca=o.data.color_attributes['bake'];d=np.zeros(len(ca.data)*4,dtype=np.float32);ca.data.foreach_get('color',d);d=d.reshape(-1,4);d[:,:3]=np.sqrt(np.clip(d[:,:3]/VSCALE,0,1));d[:,3]=1;ca.data.foreach_set('color',d.ravel())
# ---------- per-room reflection panoramas ----------
for o in col.objects:
    if o.get('glass'):o.hide_render=False
sc.view_settings.view_transform='Standard'
cam=bpy.data.cameras.new('pano');cam.type='PANO';cam.panorama_type='EQUIRECTANGULAR';cob=bpy.data.objects.new('pano',cam);col.objects.link(cob);cob.rotation_euler=(math.pi/2,0,0);sc.camera=cob
sc.render.resolution_x,sc.render.resolution_y=768,384;sc.render.image_settings.file_format='HDR';sc.render.image_settings.color_mode='RGB';sc.cycles.samples=48;sc.cycles.use_denoising=True
for n_,r,f,s_ in ROOMS:
    px_,py_=(r[0]+r[2])/2,(r[1]+r[3])/2;cob.location=(X(px_),Y(py_),1.5);sc.render.filepath=f'{OUT}/env_{ROOMS.index((n_,r,f,s_))}.hdr';bpy.ops.render.render(write_still=True)
print('panos done',round(time.time()-t0))
# sky for the view outside
sky=bpy.data.images.load(f'{HQ}/hdri/kloofendal_48d_partly_cloudy_puresky.hdr');sky.scale(2048,1024);sc.render.image_settings.file_format='HDR';sky.save_render(f'{OUT}/sky.hdr',scene=sc)
# ---------- export ----------
for im in bpy.data.images:
    if not im.size[0] or im.name in('LM','LMOUT') or im.type!='IMAGE':continue
    mx=2048 if any(k in (im.filepath or '') for k in('marble_01','herringbone','mural','birds')) else 1024
    if max(im.size)>mx:
        k=mx/max(im.size);im.scale(int(im.size[0]*k),int(im.size[1]*k))
deselect()
for o in col.objects:
    if o.type=='MESH' and not o.hide_render:o.select_set(True)
bpy.context.view_layer.objects.active=shell
for o in bpy.context.selected_objects:
    if o is not shell:o.data.uv_layers.active=o.data.uv_layers[0] if o.data.uv_layers else None
bpy.ops.export_scene.gltf(filepath=f'{OUT}/scene.glb',export_format='GLB',use_selection=True,export_image_format='WEBP',export_image_quality=82,export_apply=False,export_yup=True,export_texcoords=True,export_normals=True,export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_lights=False,export_cameras=False,export_materials='EXPORT')
print('EXPORT DONE',round(time.time()-t0),os.path.getsize(f'{OUT}/scene.glb')/1e6,'MB')
json.dump(dict(colliders=colliders,items=ITEMS,rooms=[dict(n=n_,r=r,f=f,size=s_) for n_,r,f,s_ in ROOMS]),open(f'{OUT}/layout.json','w'))
