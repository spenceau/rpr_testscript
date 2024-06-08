import os
import bpy
import sys
import time

def create_output_dir(scene_name):
    # Set the path to the output directory based on the scene_name
    output_dir = os.path.abspath(scene_name)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        except OSError as e:
            print(f"Failed to create directory {output_dir}: {e}")
            return None
    return output_dir

def render_final_image(output_file):
    # Set the render engine to Radeon ProRender
    bpy.context.scene.render.engine = 'RPR'
    bpy.context.scene.render.filepath = output_file
    bpy.ops.render.render(write_still=True)
    print(f"Final render saved to: {output_file}")

def render_viewport_image(output_dir, filename):
    # Set the viewport shading to 'RENDERED' and use Radeon ProRender
    for area in bpy.context.window_manager.windows[0].screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'
                    break
            break

    # Wait for the viewport to update
    time.sleep(10)

    # Take a screenshot of the viewport
    screenshot_path = os.path.join(output_dir, filename)
    bpy.ops.screen.screenshot(filepath=screenshot_path)
    print(f"Viewport render saved to: {screenshot_path}")

def main():
    blend_file = sys.argv[-3]
    scene_name = sys.argv[-2]
    mode = sys.argv[-1]

    if mode == "final":
        # Load the Blender file
        bpy.ops.wm.open_mainfile(filepath=blend_file)
        
        # Create the output directory based on the scene name
        output_dir = create_output_dir(scene_name)
        if not output_dir:
            print("Failed to create output directory. Exiting.")
            return
        
        # Define file names
        final_filename = f"{scene_name}_final.png"
        
        # Define full paths
        final_output_file = os.path.join(output_dir, final_filename)
        
        # Render the final image
        render_final_image(final_output_file)
    elif mode == "viewport":
        # Load the Blender file
        bpy.ops.wm.open_mainfile(filepath=blend_file)
        
        # Create the output directory based on the scene name
        output_dir = create_output_dir(scene_name)
        if not output_dir:
            print("Failed to create output directory. Exiting.")
            return
        
        # Define file names
        viewport_filename = f"{scene_name}_viewport.png"
        
        # Render the viewport image
        render_viewport_image(output_dir, viewport_filename)

if __name__ == "__main__":
    main()
