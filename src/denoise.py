import bpy,sys
a=sys.argv[sys.argv.index('--')+1:];src,dst=a[0],a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene;img=bpy.data.images.load(src);img.colorspace_settings.name='Non-Color'
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x,sc.render.resolution_y=img.size;sc.render.resolution_percentage=100
cam=bpy.data.objects.new('c',bpy.data.cameras.new('c'));sc.collection.objects.link(cam);sc.camera=cam
nt=bpy.data.node_groups.new('cmp','CompositorNodeTree');sc.compositing_node_group=nt
i=nt.nodes.new('CompositorNodeImage');i.image=img;d=nt.nodes.new('CompositorNodeDenoise');o=nt.nodes.new('NodeGroupOutput');nt.interface.new_socket('Image',in_out='OUTPUT',socket_type='NodeSocketColor')
nt.links.new(i.outputs[0],d.inputs['Image']);nt.links.new(d.outputs[0],o.inputs[0])
sc.render.use_compositing=True;sc.view_settings.view_transform='Raw' if False else 'Standard';sc.view_settings.look='None';sc.render.image_settings.file_format='OPEN_EXR';sc.render.image_settings.color_mode='RGB';sc.render.image_settings.color_depth='32';sc.render.filepath=dst
bpy.ops.render.render(write_still=True);print('DENOISED',dst)
