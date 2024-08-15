import json
import os.path
import shutil

import yaml
import binascii
import random
import numpy as np
import tempfile


def get_pixel_data(texture_pixels: np.ndarray):
    ret = []
    for x in range(texture_pixels.shape[0]):
        for y in range(texture_pixels.shape[1]):
            for z in range(texture_pixels.shape[2]):
                for channel in range(texture_pixels.shape[3]):
                    ret.append(texture_pixels[x, y, z, channel])
    return ret


def serialize_3d_texture(texture_pixels: np.ndarray, name: str, saving_path) -> str:
    data_dict = {
        "name": name,
        "width": texture_pixels.shape[0],
        "height": texture_pixels.shape[1],
        "depth": texture_pixels.shape[2],
        "channels": texture_pixels.shape[3],
        "data": get_pixel_data(texture_pixels)
    }
    print(tempfile.gettempdir())
    temp_saving_path = os.path.join(tempfile.gettempdir(), name + ".sdf")
    saving_path = os.path.join(saving_path, name + ".sdf")
    with open(temp_saving_path, 'w') as f:
        f.write(json.dumps(data_dict))

    print("Created intermidiate file for unity processing")
    shutil.move(temp_saving_path, saving_path, )
    print("moved file to unity")
    return saving_path


def serialize_neural_compute(neural_network):
    pass


if __name__ == '__main__':
    saved_path = serialize_3d_texture(np.ones((128, 128, 128, 3), dtype=np.float32), "Texture3D", r"D:\Sergio\Projects\SDFBaker\Assets\SDFBaker\TestingEnv")




