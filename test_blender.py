import os
import subprocess
import argparse

def set_output_path(base_path, subdir_name):
    # Create a subdirectory if it does not exist
    output_dir = os.path.join(base_path, subdir_name)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        except OSError as e:
            print(f"Failed to create directory {output_dir}: {e}")
            return None
    return output_dir

def render_final_image(blender_path, blend_file, output_file):
    blender_command = [
        blender_path,
        "--background",
        blend_file,
        "--render-output",
        output_file,
        "--render-frame",
        "1"
    ]
    print(f"Rendering final image with command: {' '.join(blender_command)}")
    subprocess.run(blender_command)
    print(f"Final render saved to: {output_file}")

def render_viewport_image(blender_path, scene_path, scene_name):
    viewport_script = os.path.join(scene_path, "viewport_render.py")
    viewport_command = [
        blender_path,
        "--python",
        viewport_script,
        "--",
        scene_path,
        scene_name
    ]
    print(f"Rendering viewport image with command: {' '.join(viewport_command)}")
    subprocess.run(viewport_command)

def main(blender_path, scene_path, scene_name):
    # Set the base directory name to the scene name
    output_dir = set_output_path(scene_path, scene_name)
    
    # Define file names
    final_filename = f"{scene_name}_final.png"
    viewport_filename = f"{scene_name}_viewport.png"
    
    # Define full paths
    final_output_file = os.path.join(output_dir, final_filename)
    blend_file = os.path.join(scene_path, f"{scene_name}.blend")
    
    # Render the final image
    render_final_image(blender_path, blend_file, final_output_file)
    
    # Render the viewport image
    render_viewport_image(blender_path, scene_path, scene_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render final and viewport images using Blender.")
    parser.add_argument("--blender-path", type=str, required=True, help="The path to the Blender executable.")
    parser.add_argument("--scene-path", type=str, required=True, help="The path to the directory containing the Blender scene.")
    parser.add_argument("--scene-name", type=str, required=True, help="The name of the Blender scene file without the .blend extension.")
    
    args = parser.parse_args()
    
    main(args.blender_path, args.scene_path, args.scene_name)
