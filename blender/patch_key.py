import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    content = f.read()

# Replace function signature
content = content.replace("def heuristic_texture_linking(input_dir, dest_folder, asset_dir):", "def heuristic_texture_linking(input_dir, dest_folder, asset_dir, gemini_key=''):")

# Replace function call
content = content.replace("heuristic_count = heuristic_texture_linking(os.path.dirname(os.path.abspath(input_file)), textures_dir, asset_dir)", "heuristic_count = heuristic_texture_linking(os.path.dirname(os.path.abspath(input_file)), textures_dir, asset_dir, gemini_api_key)")

# Replace the sys.argv[-1] logic
old_gemini_logic = """    # Check if we should generate the map dynamically using Gemini
    gemini_key = sys.argv[-1] if len(sys.argv) > 5 else ""
    if len(gemini_key) > 30 and found_textures:"""

new_gemini_logic = """    # Check if we should generate the map dynamically using Gemini
    my_print(f"DEBUG: AI CHECK - gemini_key length: {len(gemini_key)}, found_textures count: {len(found_textures)}")
    if len(gemini_key) > 30 and found_textures:"""

content = content.replace(old_gemini_logic, new_gemini_logic)

with open(file_path, "w") as f:
    f.write(content)
