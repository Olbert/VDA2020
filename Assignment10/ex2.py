from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import pylab as pl
import scipy as sp
from itertools import chain
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.gca(projection='3d')

# draw cube
r = [0, 1]
for s, e in combinations(np.array(list(product(r, r, r))), 2):
    if np.sum(np.abs(s - e)) == r[1] - r[0]:
        ax.plot3D(*zip(s, e), color="b")

c_values = np.array((2, 2, -2, 1, 3, 2, 1, -2))
c = 0


def find_point(c, p1, v2, v1):
    return p1 + abs((c - v2) / (v2 - v1))


x1_1 = 0 + abs((c - c_values[3]) / (c_values[3] - c_values[2]))
y1_1 = 0
z1_1 = 1

x1_2 = 1
y1_2 = 0 + abs((c - c_values[6]) / (c_values[6] - c_values[2]))
z1_2 = 1

x1_3 = 1
y1_3 = 0
z1_3 = 0 + abs((c - c_values[1]) / (c_values[1] - c_values[2]))

x2_1 = 0
y2_1 = find_point(0, 1, c_values[3], c_values[7])
z2_1 = 1

x2_2 = find_point(0, 1, c_values[6], c_values[7])
y2_2 = 1
z2_2 = 1

x2_3 = 1
y2_3 = 1
z2_3 = find_point(0, 1, c_values[4], c_values[7])

c_points = np.array((
    [0, 0, 0],
    [1, 0, 0],
    [1, 0, 1],
    [0, 0, 1],

    [0, 1, 0],
    [1, 1, 0],
    [1, 1, 1],
    [0, 1, 1],
))


def find_point(c, p, v1, v2, v3):
    tri = np.zeros(3)
    tri[0] = c_points[p] + (c_points[p] - c_points[v1]) * ((c - c_values[p]) / (c_values[v1] - c_values[p]))
    tri[1] = c_points[p] + (c_points[p] - c_points[v2]) * ((c - c_values[p]) / (c_values[v2] - c_values[p]))
    tri[2] = c_points[p] + (c_points[p] - c_points[v3]) * ((c - c_values[p]) / (c_values[v3] - c_values[p]))

    return tri

tri = find_point(0,2,)
triangles = [
    ((x1_1, y1_1, z1_1), (x1_2, y1_2, z1_2), (x1_3, y1_3, z1_3)),

    ((x2_1, y2_1, z2_1), (x2_2, y2_2, z2_2), (x2_3, y2_3, z2_3)),

]
print((x1_1, y1_1, z1_1), (x1_2, y1_2, z1_2), (x1_3, y1_3, z1_3)),
print(((x2_1, y2_1, z2_1), (x2_2, y2_2, z2_2), (x2_3, y2_3, z2_3)))
tri_points = list(chain.from_iterable(triangles))
x, y, z = zip(*tri_points)
tri_idx = [(3 * i, 3 * i + 1, 3 * i + 2) for i in range(len(triangles))]
ax.plot_trisurf(x, y, z, triangles=tri_idx)

ax.scatter(x1_1, y1_1, z1_1)
ax.scatter(x1_2, y1_2, z1_2)
plt.show()

stop = True
