import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    content = f.read()

old_vlm_render = """            mat_objects = list(set([m for o in bpy.context.scene.objects if o.type == 'MESH' for m in o.data.materials if m]))
            color_legend = []
            orig_colors = {}
            for idx_c, mat in enumerate(mat_objects):
                orig_colors[mat] = tuple(mat.diffuse_color)
                r, g, b, a, name = palette[idx_c % len(palette)]
                mat.diffuse_color = (r, g, b, a)
                color_legend.append(f"Material '{mat.name}' is painted {name}")
                
            mask_path = os.path.join(input_dir, "vlm_mask.jpg")
            cam_data = bpy.data.cameras.new('VLMCam')
            cam_data.clip_end = 50000.0
            cam_obj = bpy.data.objects.new('VLMCam', cam_data)
            bpy.context.scene.collection.objects.link(cam_obj)
            bpy.context.scene.camera = cam_obj
            
            min_co, max_co = [float('inf')]*3, [float('-inf')]*3
            has_mesh = False
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH':
                    has_mesh = True
                    for point in obj.bound_box:
                        world_point = obj.matrix_world @ mathutils.Vector(point)
                        for idx_c in range(3):
                            min_co[idx_c] = min(min_co[idx_c], world_point[idx_c])
                            max_co[idx_c] = max(max_co[idx_c], world_point[idx_c])
                            
            if has_mesh:
                center = [(max_co[idx_c] + min_co[idx_c]) / 2 for idx_c in range(3)]
                size = max(max_co[idx_c] - min_co[idx_c] for idx_c in range(3)) if max_co[0] != float('-inf') else 10
                cam_obj.location = (center[0], center[1] - size * 1.5, center[2] + size * 0.5)
                direction = mathutils.Vector(center) - cam_obj.location
                cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
            
            prev_engine = bpy.context.scene.render.engine
            bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
            bpy.context.scene.display.shading.color_type = 'MATERIAL'
            bpy.context.scene.display.shading.light = 'FLAT'
            bpy.context.scene.render.resolution_x = 512
            bpy.context.scene.render.resolution_y = 512
            bpy.context.scene.render.filepath = mask_path
            bpy.context.scene.render.image_settings.file_format = 'JPEG'
            
            bpy.ops.render.render(write_still=True)
            bpy.context.scene.render.engine = prev_engine
            
            # RESTORE ORIGINAL COLORS
            for mat, orig_col in orig_colors.items():
                mat.diffuse_color = orig_col"""


new_vlm_render = """            mat_objects = list(set([m for o in bpy.context.scene.objects if o.type == 'MESH' for m in o.data.materials if m]))
            color_legend = []
            
            # Create Emission Materials
            neon_materials = {}
            for idx_c, mat in enumerate(mat_objects):
                r, g, b, a, name = palette[idx_c % len(palette)]
                
                # Create a perfectly flat, unshaded emission material for Eevee
                neon = bpy.data.materials.new(name=f"VLM_Neon_{mat.name}")
                neon.use_nodes = True
                neon.node_tree.nodes.clear()
                emission = neon.node_tree.nodes.new('ShaderNodeEmission')
                emission.inputs['Color'].default_value = (r, g, b, 1.0)
                output = neon.node_tree.nodes.new('ShaderNodeOutputMaterial')
                neon.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                neon_materials[mat.name] = neon
                color_legend.append(f"Material '{mat.name}' is painted {name}")
                
            # Swap mesh slots
            orig_slots = []
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH':
                    for i, slot in enumerate(obj.material_slots):
                        if slot.material and slot.material.name in neon_materials:
                            orig_slots.append((obj, i, slot.material))
                            slot.material = neon_materials[slot.material.name]
                
            mask_path = os.path.join(input_dir, "vlm_mask.jpg")
            cam_data = bpy.data.cameras.new('VLMCam')
            cam_data.clip_end = 50000.0
            cam_obj = bpy.data.objects.new('VLMCam', cam_data)
            bpy.context.scene.collection.objects.link(cam_obj)
            bpy.context.scene.camera = cam_obj
            
            min_co, max_co = [float('inf')]*3, [float('-inf')]*3
            has_mesh = False
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH':
                    has_mesh = True
                    for point in obj.bound_box:
                        world_point = obj.matrix_world @ mathutils.Vector(point)
                        for idx_c in range(3):
                            min_co[idx_c] = min(min_co[idx_c], world_point[idx_c])
                            max_co[idx_c] = max(max_co[idx_c], world_point[idx_c])
                            
            if has_mesh:
                center = [(max_co[idx_c] + min_co[idx_c]) / 2 for idx_c in range(3)]
                size = max(max_co[idx_c] - min_co[idx_c] for idx_c in range(3)) if max_co[0] != float('-inf') else 10
                cam_obj.location = (center[0], center[1] - size * 1.5, center[2] + size * 0.5)
                direction = mathutils.Vector(center) - cam_obj.location
                cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
            
            prev_engine = bpy.context.scene.render.engine
            bpy.context.scene.render.engine = 'BLENDER_EEVEE' # Use EEVEE to avoid Workbench headless crash!
            bpy.context.scene.render.resolution_x = 512
            bpy.context.scene.render.resolution_y = 512
            bpy.context.scene.render.filepath = mask_path
            bpy.context.scene.render.image_settings.file_format = 'JPEG'
            
            try:
                bpy.ops.render.render(write_still=True)
            except Exception as e:
                print(f"DEBUG: VLM Render failed: {e}")
                
            bpy.context.scene.render.engine = prev_engine
            
            # RESTORE ORIGINAL MATERIALS
            for obj, idx_c, mat in orig_slots:
                obj.material_slots[idx_c].material = mat
                
            # Cleanup neon materials
            for neon in neon_materials.values():
                bpy.data.materials.remove(neon)"""


# Note: The replace is sensitive. 
# Let's do a more robust string replacement by doing regex or replacing line by line.
import re
# We'll just replace the block starting at `mat_objects = list(set([m for o in bpy.context.scene.objects`
# up to `# RESTORE ORIGINAL COLORS\n            for mat, orig_col in orig_colors.items():\n                mat.diffuse_color = orig_col`
start_str = "mat_objects = list(set([m for o in bpy.context.scene.objects if o.type == 'MESH' for m in o.data.materials if m]))"
end_str = "mat.diffuse_color = orig_col"

if start_str in content and end_str in content:
    start_idx = content.find(start_str)
    end_idx = content.find(end_str) + len(end_str)
    
    new_content = content[:start_idx] + new_vlm_render.lstrip() + content[end_idx:]
    with open(file_path, "w") as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("FAILED TO FIND BLOCK")
