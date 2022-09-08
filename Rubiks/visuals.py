import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np
from itertools import product, combinations
import copy

fig = plt.figure()


def showCube(cube, rotation, moveAm):
    ax = fig.gca(projection='3d')
    ax.set_aspect("auto")
    ax.set_autoscale_on(True)
    mult = 2

    r = [mult*-1.5, mult*1.5]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            ax.plot3D(*zip(s, e), color="black")

    colors = ['g', 'y', 'orange', 'w', 'r', 'b']
    dim = ['z', 'y', 'x']
    sides = [1, 6, 4, 2, 5, 3]

    cartCube = copy.deepcopy(cube)
    cartCube[5] = np.flip(cartCube[5], 0)
    cartCube[2] = np.flip(cartCube[2], 1)
    cartCube[3] = np.flip(cartCube[3], 1)

    for i, (zdir, z, row, col) in enumerate(product([0, 1, 2], [0,1], [0, 1, 2], [0, 1, 2])):
        curColor = colors[cartCube[sides[2*zdir + z]-1, row, col]]
        square = Rectangle(((col-1.5)*mult, (.5-row)*mult), mult, mult, facecolor=curColor, edgecolor='black')
        ax.add_patch(square)
        art3d.pathpatch_2d_to_3d(square, z=(.5-z)*3*mult, zdir=dim[zdir])

    plt.grid(False)
    plt.axis('off')
    plt.title('Generation: ' + str(rotation)+ '\n Move: ' + str(moveAm))

    plt.show(block=False)
    plt.pause(.05)
    plt.clf()