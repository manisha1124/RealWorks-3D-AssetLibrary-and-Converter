import os
file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    lines = f.readlines()
new_lines = []
for line in lines:
    if "traceback.print_exc()" in line:
        new_lines.append(line)
        new_lines.append("        with open('crash_log.txt', 'w') as crashf:\n")
        new_lines.append("            crashf.write(traceback.format_exc())\n")
    else:
        new_lines.append(line)
with open(file_path, "w") as f:
    f.writelines(new_lines)
