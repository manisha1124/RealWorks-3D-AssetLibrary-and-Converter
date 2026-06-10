import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "def main():" in line:
        new_lines.append(line)
        new_lines.append("    global DEBUG_LOG\n")
        new_lines.append("    DEBUG_LOG = open('debug_log.txt', 'w')\n")
        new_lines.append("    def my_print(*args):\n")
        new_lines.append("        msg = ' '.join(str(a) for a in args)\n")
        new_lines.append("        print(msg)\n")
        new_lines.append("        DEBUG_LOG.write(msg + '\\n')\n")
        new_lines.append("        DEBUG_LOG.flush()\n")
        continue
        
    if "print(" in line and "traceback.print_exc" not in line and "def my_print" not in line:
        # replace print( with my_print(
        new_lines.append(line.replace("print(", "my_print("))
    else:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
