import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    content = f.read()

# PATCH 1: Asset ID Duplication
old_id_block = """    asset_id = str(uuid.uuid4())
    filename = os.path.basename(input_file)
    asset_name = os.path.splitext(filename)[0]
    source_format = os.path.splitext(filename)[1].lower().replace(".", "")
    
    my_print(f"Starting conversion for: {input_file}")
    
    # Create output directory
    asset_dir = os.path.join(output_dir, category, asset_name)
    os.makedirs(asset_dir, exist_ok=True)
    textures_dir = os.path.join(asset_dir, "textures")"""

new_id_block = """    filename = os.path.basename(input_file)
    asset_name = os.path.splitext(filename)[0]
    source_format = os.path.splitext(filename)[1].lower().replace(".", "")
    
    my_print(f"Starting conversion for: {input_file}")
    
    # Create output directory
    asset_dir = os.path.join(output_dir, category, asset_name)
    os.makedirs(asset_dir, exist_ok=True)
    textures_dir = os.path.join(asset_dir, "textures")
    
    asset_id = str(uuid.uuid4())
    metadata_path = os.path.join(asset_dir, "metadata.json")
    if os.path.exists(metadata_path):
        import json
        try:
            with open(metadata_path, 'r') as f:
                existing_meta = json.load(f)
                if "id" in existing_meta:
                    asset_id = existing_meta["id"]
                    my_print(f"DEBUG: Preserving existing asset ID {asset_id}")
        except Exception:
            pass"""

content = content.replace(old_id_block, new_id_block)


# PATCH 2: Rename Improper Textures
old_rename_block = """                        img = next((i for name, i in images.items() if i.name == tex_filename or os.path.basename(i.filepath) == tex_filename), None)
                        if img:
                            is_color = socket_name in ['Base Color', 'Emission']
                            tex_node = add_mapped_texture(img, is_color=is_color)"""

new_rename_block = """                        img = next((i for name, i in images.items() if i.name == tex_filename or os.path.basename(i.filepath) == tex_filename), None)
                        if img:
                            # Rename improper images if they haven't been renamed yet
                            old_filepath = bpy.path.abspath(img.filepath)
                            if "tex_renamed" not in img.keys():
                                new_name = f"{mat.name}_{socket_name.replace(' ', '')}{os.path.splitext(old_filepath)[1]}"
                                new_name = "".join(c for c in new_name if c.isalnum() or c in "._- ")
                                new_filepath = os.path.join(os.path.dirname(old_filepath), new_name)
                                
                                if old_filepath != new_filepath and os.path.exists(old_filepath):
                                    try:
                                        os.rename(old_filepath, new_filepath)
                                        # Rename copied version in dest_folder
                                        copied_old = os.path.join(dest_folder, os.path.basename(old_filepath))
                                        copied_new = os.path.join(dest_folder, new_name)
                                        if os.path.exists(copied_old):
                                            os.rename(copied_old, copied_new)
                                        img.filepath = new_filepath
                                        img.name = new_name
                                        img["tex_renamed"] = 1
                                        my_print(f"DEBUG: Renamed texture to {new_name}")
                                    except Exception as e:
                                        my_print(f"DEBUG: Failed to rename texture: {e}")
                                        
                            is_color = socket_name in ['Base Color', 'Emission']
                            tex_node = add_mapped_texture(img, is_color=is_color)"""

content = content.replace(old_rename_block, new_rename_block)

with open(file_path, "w") as f:
    f.write(content)
