
import numpy as np
import matplotlib.pyplot as plt
import os
import sklearn
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import datasets
from pandas.plotting import scatter_matrix
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
from sklearn.impute import SimpleImputer

from matplotlib.ticker import NullFormatter
from sklearn import manifold, datasets
from time import time

import pandas as pd
from sklearn.manifold import Isomap

np.random.seed(0)

class DIR(object):
    __slots__ = ()
    CHECKOUT = os.path.dirname(os.path.realpath('__file__'))
    RES = os.path.join(CHECKOUT, 'res')
    OUT = os.path.join(CHECKOUT, 'out')


DIR = DIR()
input_file = os.path.join(DIR.RES, 'breast-cancer-wisconsin.data')

# read data as collection of string
# mix_data = np.loadtxt(input_file, dtype=np.str, comments='#', delimiter=',').T

