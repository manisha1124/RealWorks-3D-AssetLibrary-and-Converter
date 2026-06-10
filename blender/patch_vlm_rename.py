import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    content = f.read()

# PATCH 1: Set VLM flag when VLM returns a map
old_vlm_call = """            llm_map, raw_text = call_gemini({"contents": [{"parts": parts}], "generationConfig": {"responseMimeType": "application/json"}})"""

new_vlm_call = """            llm_map, raw_text = call_gemini({"contents": [{"parts": parts}], "generationConfig": {"responseMimeType": "application/json"}})
            if llm_map:
                llm_map["_WAS_VLM_GENERATED"] = True"""

content = content.replace(old_vlm_call, new_vlm_call)

# PATCH 2: Only rename if VLM generated it
old_rename_cond = """                            # Rename improper images if they haven't been renamed yet
                            old_filepath = bpy.path.abspath(img.filepath)
                            if "tex_renamed" not in img.keys():"""

new_rename_cond = """                            # Rename improper images ONLY if VLM mapped them
                            old_filepath = bpy.path.abspath(img.filepath)
                            if "tex_renamed" not in img.keys() and llm_map.get("_WAS_VLM_GENERATED", False):"""

content = content.replace(old_rename_cond, new_rename_cond)

with open(file_path, "w") as f:
    f.write(content)
