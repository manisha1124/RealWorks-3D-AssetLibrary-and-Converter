import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.startswith("def heuristic_texture_linking(input_dir, textures_dir):"):
        new_lines.append("def heuristic_texture_linking(input_dir, textures_dir, asset_dir):\n")
        continue
        
    if "gemini_key = sys.argv[-1] if len(sys.argv) > 5 else" in line:
        # Start replacing from here
        skip = True
        
        new_code = """    gemini_key = sys.argv[-1] if len(sys.argv) > 5 else ""
    if len(gemini_key) > 30 and found_textures:
        import urllib.request, urllib.error, json, time, os
        
        def call_gemini(payload):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}", data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                        llm_text = res_data['candidates'][0]['content']['parts'][0]['text']
                        llm_text = llm_text.replace('```json', '').replace('```', '').strip()
                        return json.loads(llm_text), llm_text
                except urllib.error.HTTPError as e:
                    if e.code == 429 and attempt < max_retries - 1:
                        time.sleep(10)
                    else:
                        print(f"DEBUG: Gemini HTTP Error {e.code}: {e.read().decode('utf-8')}")
                        break
                except Exception as e:
                    print(f"DEBUG: Gemini API failed: {e}")
                    break
            return None, ""

        print("DEBUG: Asking Gemini Text-LLM to map textures...")
        mat_names = list(set([m.name for o in bpy.context.scene.objects if o.type == 'MESH' for m in o.data.materials if m]))
        tex_names = [os.path.basename(t) for t in found_textures]
        
        prompt_stage1 = f\"\"\"You are a 3D asset pipeline assistant.
Materials: {mat_names}
Textures: {tex_names}
Return a JSON object where keys are the exact Material names, and values are objects mapping socket names ('Base Color', 'Roughness', 'Metallic', 'Normal', 'Alpha', 'Emission') to exact Texture filenames. Do not use markdown.
CRITICAL: If the names are completely arbitrary and meaningless (e.g. 'Mat_001' and 'IMG_123.jpg') and you cannot semantically map them with absolute confidence, DO NOT GUESS. Instead, return exactly: {{"REQUIRE_VLM": true}}\"\"\"

        llm_map, raw_text = call_gemini({"contents": [{"parts": [{"text": prompt_stage1}]}], "generationConfig": {"responseMimeType": "application/json"}})
        
        if llm_map and llm_map.get("REQUIRE_VLM"):
            print("DEBUG: Text-LLM requested VLM Fallback. Initializing Multimodal Vision LLM...")
            import base64, math, mathutils, uuid
            palette = [
                (1, 0, 0, 1, "Red"), (0, 1, 0, 1, "Green"), (0, 0, 1, 1, "Blue"), 
                (1, 1, 0, 1, "Yellow"), (1, 0, 1, 1, "Magenta"), (0, 1, 1, 1, "Cyan"), 
                (1, 0.5, 0, 1, "Orange"), (0.5, 0, 1, 1, "Purple"), (1, 0.75, 0.8, 1, "Pink"), 
                (0.5, 1, 0, 1, "Lime"), (0, 0.5, 1, 1, "Light Blue"), (0.5, 0, 0, 1, "Maroon"), 
                (0, 0.5, 0, 1, "Dark Green"), (0, 0, 0.5, 1, "Navy"), (0.5, 0.5, 0.5, 1, "Gray"), 
                (1, 1, 1, 1, "White")
            ]
            
            mat_objects = list(set([m for o in bpy.context.scene.objects if o.type == 'MESH' for m in o.data.materials if m]))
            color_legend = []
            orig_colors = {}
            for i, mat in enumerate(mat_objects):
                orig_colors[mat] = tuple(mat.diffuse_color)
                r, g, b, a, name = palette[i % len(palette)]
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
                        for idx in range(3):
                            min_co[idx] = min(min_co[idx], world_point[idx])
                            max_co[idx] = max(max_co[idx], world_point[idx])
                            
            if has_mesh:
                center = [(max_co[idx] + min_co[idx]) / 2 for idx in range(3)]
                size = max(max_co[idx] - min_co[idx] for idx in range(3)) if max_co[0] != float('-inf') else 10
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
                mat.diffuse_color = orig_col
                
            parts = []
            legend_text = "\\n".join(color_legend)
            prompt_vlm = f\"\"\"You are a 3D asset pipeline vision assistant.
Here is a color-coded render of the 3D model:
{legend_text}

I will also provide the texture images found in the folder.
Return a JSON object where keys are the exact Material names, and values are objects mapping socket names ('Base Color', 'Roughness', 'Metallic', 'Normal', 'Alpha', 'Emission') to exact Texture filenames. Do not use markdown.\"\"\"
            parts.append({"text": prompt_vlm})
            
            if os.path.exists(mask_path):
                with open(mask_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})
                    
            for tex in found_textures:
                parts.append({"text": f"Texture filename: {os.path.basename(tex)}"})
                try:
                    img = bpy.data.images.load(tex)
                    temp_img = img.copy()
                    temp_img.scale(512, 512)
                    temp_tex = os.path.join(input_dir, f"vlm_temp_{uuid.uuid4().hex[:6]}.jpg")
                    temp_img.filepath_raw = temp_tex
                    temp_img.file_format = 'JPEG'
                    temp_img.save()
                    with open(temp_tex, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode('utf-8')
                        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})
                    os.remove(temp_tex)
                    bpy.data.images.remove(temp_img)
                    bpy.data.images.remove(img)
                except Exception as e:
                    pass
                    
            bpy.data.objects.remove(cam_obj)
            if os.path.exists(mask_path):
                os.remove(mask_path)
                
            llm_map, raw_text = call_gemini({"contents": [{"parts": parts}], "generationConfig": {"responseMimeType": "application/json"}})
            
        if llm_map and not llm_map.get("REQUIRE_VLM"):
            try:
                raw_path = os.path.join(asset_dir, "texture_map_raw.txt")
                with open(raw_path, 'w') as f: f.write(raw_text)
                
                texture_map_path = os.path.join(asset_dir, "texture_map.json")
                with open(texture_map_path, 'w') as f: json.dump(llm_map, f, indent=2)
                print(f"DEBUG: Saved final texture_map.json to {texture_map_path}")
            except Exception as e: 
                print(f"DEBUG: Error saving map: {e}")
"""
        new_lines.append(new_code)
        continue
        
    if skip:
        if "for obj in bpy.context.scene.objects:" in line:
            # We reached the rest of the function! Wait, the loop over objects is after the LLM logic!
            # Let's find the exact end of the old LLM block.
            # The old block ends right before the fuzzy logic starts.
            pass
        if "# Helper for fuzzy scoring" in line:
            # Reached the end of the LLM block
            skip = False
            # We must append the line that defines `mesh_count` which we skipped
            new_lines.append("    mesh_count = len([o for o in bpy.context.scene.objects if o.type == 'MESH'])\n")
            new_lines.append(line)
            continue
        
        # Another line we need to make sure we didn't skip: the `if llm_map and mat.name in llm_map:` logic!
        # Wait, the LLM application loop is inside the `for mat in obj.data.materials` loop!
        continue
        
    if "heuristic_count = heuristic_texture_linking(" in line:
        # Patch the function call in main
        line = line.replace("heuristic_texture_linking(os.path.dirname(os.path.abspath(input_file)), textures_dir)", "heuristic_texture_linking(os.path.dirname(os.path.abspath(input_file)), textures_dir, asset_dir)")
        
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
