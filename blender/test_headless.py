import bpy
try:
    bpy.context.scene.display.shading.color_type = 'MATERIAL'
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
