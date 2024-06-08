import os
import subprocess
import argparse
from elevate import elevate


def main(blender_path, scene_path, scene_name):
    script_path = os.path.join(os.path.dirname(__file__), "render_script.py")
    blend_file = os.path.join(scene_path, f"{scene_name}.blend")
    
    # Ensure the blend file exists
    if not os.path.exists(blend_file):
        print(f"Blend file not found: {blend_file}")
        return
    
    # Final render in background
    command = [blender_path, "--background", "--python", script_path, blend_file, scene_name, "final"]
    subprocess.run(command)
    
    # Open Blender for viewport render with elevated privileges
    elevate()
    command = [blender_path, blend_file, "--python", script_path, blend_file, scene_name, "viewport"]
    subprocess.run(command)

    # # Open Blender for viewport render with elevated privileges
    # elevate_command = [
    #     'runas', '/user:Administrator',
    #     f'"{blender_path}" "{blend_file}" --python "{script_path}" {blend_file} {scene_name} viewport'
    # ]
    # subprocess.run(' '.join(elevate_command), shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render final and viewport images using Blender.")
    parser.add_argument("--blender-path", type=str, required=True, help="The path to the Blender executable.")
    parser.add_argument("--scene-path", type=str, required=True, help="The path to the directory containing the Blender scene.")
    parser.add_argument("--scene-name", type=str, required=True, help="The name of the Blender scene file without the .blend extension.")
    
    args = parser.parse_args()
    
    main(args.blender_path, args.scene_path, args.scene_name)
