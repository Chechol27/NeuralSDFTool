import bpy
import numpy
import numpy as np
import os
from mathutils import Vector
from progress.bar import Bar



def get_min_and_max_vertex_coords(mesh_data) -> ((float,float,float), (float, float, float)):
    firstVertex = mesh_data.vertices[0].co
    minX, minY, minZ = firstVertex[0], firstVertex[1], firstVertex[2]
    maxX, maxY, maxZ = 0, 0, 0
    for v in mesh_data.vertices:
        minX = min(minX, v.co[0])
        minY = min(minY, v.co[1])
        minZ = min(minZ, v.co[2])

        maxX = max(maxX, v.co[0])
        maxY = max(maxY, v.co[1])
        maxZ = max(maxZ, v.co[2])

    return (minX, minY, minZ), (maxX, maxY, maxZ)


def apply_object_transforms(target_object):
    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.transform_apply(scale=True, rotation=True)


def simple_lerp(a, b , t):
    return a * t + b * (1-t)


def bake_sdf_3d_from_mesh(path_to_3d_model: str, domain_shape: (int, int, int, int)) -> np.ndarray:
    bpy.ops.import_scene.fbx(filepath=path_to_3d_model)
    model_name = os.path.splitext(os.path.basename(path_to_3d_model))[0]
    imported_object = bpy.data.objects[model_name]
    apply_object_transforms(imported_object)
    res = np.zeros(domain_shape)
    minV, maxV = get_min_and_max_vertex_coords(imported_object.data)
    bar = Bar('Computing SDF', max=domain_shape[0] * domain_shape[1] * domain_shape[2])
    for x in range(domain_shape[0]):
        for y in range(domain_shape[1]):
            for z in range(domain_shape[2]):
                nco = (x / domain_shape[0], y/domain_shape[1], z/domain_shape[2])
                object_space_coord = (simple_lerp(minV[0], maxV[0], nco[0]),
                                      simple_lerp(minV[1], maxV[1], nco[1]),
                                      simple_lerp(minV[2], maxV[2], nco[2])
                                      )
                found, location, normal, index = imported_object.closest_point_on_mesh(object_space_coord)
                v_loc_os = Vector(object_space_coord)
                normalized_location: Vector = (v_loc_os - location).normalized()
                dot = normal.dot(normalized_location)
                distance = (v_loc_os - location).length * 1 if dot >= 0 else -1
                pixel = []
                distance = distance * 0.5 + 0.5
                for c in range(domain_shape[3]):
                    pixel.append(distance)
                res[x, y, z] = numpy.array(pixel)
                bar.next()
    bar.finish()
    return res

