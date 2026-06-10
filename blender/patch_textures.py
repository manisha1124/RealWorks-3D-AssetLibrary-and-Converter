import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    content = f.read()

old_func = """def find_loose_textures(input_dir):
    found_textures = []
    dirs_to_search = [
        input_dir, 
        os.path.join(input_dir, 'Textures'), 
        os.path.join(input_dir, 'textures'),
        os.path.join(input_dir, 'Maps'),
        os.path.join(input_dir, 'maps'),
        os.path.join(input_dir, 'Images'),
        os.path.join(input_dir, 'images')
    ]
    for d in dirs_to_search:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.tga', '.exr')):
                    found_textures.append(os.path.join(d, f))
    return list(set(found_textures))"""

new_func = """def find_loose_textures(input_dir):
    found_textures = []
    # Recursively search all subdirectories within input_dir
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.tga', '.exr')):
                found_textures.append(os.path.join(root, f))
    return list(set(found_textures))"""

content = content.replace(old_func, new_func)

with open(file_path, "w") as f:
    f.write(content)
