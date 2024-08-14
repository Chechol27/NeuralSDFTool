import numpy as np

import sdf_baker
import matplotlib.pyplot as plt


def plot_sdf(sdf: np.ndarray):
    x = np.indices(sdf.shape)[0]
    y = np.indices(sdf.shape)[1]
    z = np.indices(sdf.shape)[2]
    col = sdf.flatten()

    fig = plt.figure()
    ax3D = fig.add_subplot(projection='3d')
    cm = plt.colormaps['brg']
    p3d = ax3D.scatter(x,y,z, c=col, cmap=cm)
    plt.colorbar(p3d)
    plt.show()


if __name__ == '__main__':
    sdf = sdf_baker.bake_sdf_3d_from_mesh(r"D:\Sergio\PycharmProjects\NeuralSDFTool\NeuralSDFTool\data\testing_files\Suzanne.fbx", (64, 64, 64))
    plot_sdf(sdf)