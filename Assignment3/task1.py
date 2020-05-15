import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from sklearn import decomposition
from sklearn import datasets
from mpl_toolkits.mplot3d import Axes3D

class DIR(object):
    __slots__ = ()
    CHECKOUT = os.path.dirname(os.path.realpath('__file__'))
    RES = os.path.join(CHECKOUT, 'res')
    OUT = os.path.join(CHECKOUT, 'out')


DIR = DIR()
input_file = os.path.join(DIR.RES, 'breast-cancer-wisconsin.data')

# read data as 2D array of data type 'object'
data = np.loadtxt(input_file, dtype=np.str, comments='#', delimiter=',').T


data = np.where(data=="?", 0, data).astype(int)[1:11]

plt.plot(data.T[0:1])
plt.show()
arr = data
#
# def PCA(dims=2):
#     mean = np.mean(data, axis=0)
#
#     data = data - mean
#
#     covariance = np.cov(data.T)
#     values, vectors = np.linalg.eig(covariance)
#
#     ind = np.argpartition(values, -dims)[-dims:]  # Get id of dims max values
#
#     # Check vectors and values
#     for i in range(len(values)):
#         eigv = vectors[:, i].reshape(1, data_x.shape[1]).T
#         np.testing.assert_array_almost_equal(covariance.dot(eigv), values[i] * eigv,
#                                              decimal=6, err_msg='', verbose=True)
#     vectors = vectors.T  # But Why??
#     if dims == 2:
#         principals = np.array((vectors[ind[0]], vectors[ind[1]]))
#     else:
#         if dims == 3:
#             principals = np.array((-vectors[ind[0]], -vectors[ind[1]], vectors[ind[2]]))
#     transformed = principals.dot(data.T).real
#
#     # print(transformed)
#     if dims == 2:
#         plt.scatter(transformed[0, :], transformed[1, :], c="r")
#         plt.show()
#     else:
#         if dims == 3:
#             draw3D(transformed[0, :], transformed[1, :], transformed[2, :], 'b')
#     pass