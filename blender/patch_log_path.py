import os

file_path = "d:/RealWorks/Animation Preset Lib/ASSET LIB APP/blender/convert.py"
with open(file_path, "r") as f:
    content = f.read()

# PATCH 1: debug_log.txt location
old_log = """DEBUG_LOG = open('debug_log.txt', 'w')"""
new_log = """import os
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug_log.txt')
DEBUG_LOG = open(log_path, 'w')"""
content = content.replace(old_log, new_log)

# PATCH 2: crash_log.txt location
old_crash = """        with open('crash_log.txt', 'w') as crashf:"""
new_crash = """        crash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crash_log.txt')
        with open(crash_path, 'w') as crashf:"""
content = content.replace(old_crash, new_crash)

with open(file_path, "w") as f:
    f.write(content)
