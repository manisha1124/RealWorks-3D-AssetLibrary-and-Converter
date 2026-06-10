import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "def setup_scene():" in line:
        new_lines.append("DEBUG_LOG = open('debug_log.txt', 'w')\n")
        new_lines.append("def my_print(*args):\n")
        new_lines.append("    msg = ' '.join(str(a) for a in args)\n")
        new_lines.append("    print(msg)\n")
        new_lines.append("    DEBUG_LOG.write(msg + '\\n')\n")
        new_lines.append("    DEBUG_LOG.flush()\n\n")
        new_lines.append(line)
    elif "    global DEBUG_LOG\n" == line or "    DEBUG_LOG = open('debug_log.txt', 'w')\n" == line or "    def my_print(*args):\n" == line or "        msg = ' '.join(str(a) for a in args)\n" == line or "        print(msg)\n" == line or "        DEBUG_LOG.write(msg + '\\n')\n" == line or "        DEBUG_LOG.flush()\n" == line:
        continue
    else:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
