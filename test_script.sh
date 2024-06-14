
clear

# to generate render:
python cmd_script.py --blender-path BLENDER_EXE --scene-path BLEND_FILES_SUBDIR --scene-name SCENE

# to compare generated render with ground truth/actual
python compare_render.py --scene SCENE --ground_truth GROUND_TRUTH_SUBDIR --render RENDER_SUBDIR
