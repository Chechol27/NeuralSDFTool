import bpy
import numpy as np
import os


def bake_sdf_3d_from_mesh(path_to_3d_model: str) -> np.ndarray:
    bpy.ops.import_scene.fbx(filepath=path_to_3d_model)
    model_name = os.path.splitext(os.path.basename(path_to_3d_model))[0]
    imported_object = bpy.data.objects[model_name]
    #TODO
    #Define SDF Volume
    #Calculate distance foreach discreet point in volume
    #Return NDArray
    pass
