import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import sklearn
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import datasets
from pandas.plotting import scatter_matrix
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd


class DIR(object):
    __slots__ = ()
    CHECKOUT = os.path.dirname(os.path.realpath('__file__'))
    RES = os.path.join(CHECKOUT, 'res')
    OUT = os.path.join(CHECKOUT, 'out')


DIR = DIR()
input_file = os.path.join(DIR.RES, 'breast-cancer-wisconsin.data')

"""
#  Attribute                     Domain
   -- -----------------------------------------
   1. Sample code number            id number
   2. Clump Thickness               1 - 10
   3. Uniformity of Cell Size       1 - 10
   4. Uniformity of Cell Shape      1 - 10
   5. Marginal Adhesion             1 - 10
   6. Single Epithelial Cell Size   1 - 10
   7. Bare Nuclei                   1 - 10
   8. Bland Chromatin               1 - 10
   9. Normal Nucleoli               1 - 10
  10. Mitoses                       1 - 10
  11. Class:                        (2 for benign, 4 for malignant)
"""


"""         Task A          """
# read data as collection of string
mix_data = np.loadtxt(input_file, dtype=np.str, comments='#', delimiter=',').T

mix_data = np.where(mix_data== '?', np.nan, mix_data).astype(np.float)

# change all missing instances to average value

avgs = np.nanmean(mix_data.astype(np.float),axis=1)
col_mean = np.nanmean(mix_data, axis=1)

#Find indices that you need to replace
inds = np.where(np.isnan(mix_data))

#Place column means in the indices. Align the arrays using take
mix_data[inds] = np.take(col_mean,inds[0])
data = np.where(mix_data == np.nan, 0, mix_data).astype(int)


"""
All missing data was replaced by mean value to cause minimal noise in correlation matrix 
"""

"""         Task B          """
# Aplly PCA
pca = PCA()
principalComponents_breast = pca.fit_transform(data[1:10].T)
# Make some plots
plt.scatter(np.arange(data[1:10].shape[0]) + 1, pca.explained_variance_)
plt.xlabel('components')
plt.ylabel('variance')
plt.show()

plt.scatter(np.arange(data[1:10].shape[0]) + 1, pca.explained_variance_ratio_)
plt.ylim(0, 1)
plt.xlabel('components')
plt.ylabel('variance ratio')
plt.show()
# Last plot summarizes cumulative variance ratio
total_vars = [sum(pca.explained_variance_ratio_[0: current]) for current in
              range(1, len(pca.explained_variance_ratio_) + 1, 1)]
plt.scatter(np.arange(data[1:10].shape[0]) + 1, total_vars)
plt.axhline(0.9, label='90% threshold')
plt.legend()
plt.ylim(0, 1)
plt.xlabel('components')
plt.ylabel('total variance ratio')
plt.show()

""" 
To cross 90% threshold we need at least 5 first components
"""





"""         Task C          """

pca = PCA(n_components=5)

principalComponents_breast = pca.fit_transform(data[1:10].T)
# Adding class column to data
target = data[10:None].T
principalComponents_breast = np.hstack((principalComponents_breast, target))

principal_breast_Df = pd.DataFrame(data=principalComponents_breast,
                                   columns=['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'target'])
principal_breast_Df.tail()
# Here seaborn is used to make scatter plot matrix
g = sns.pairplot(principal_breast_Df, hue="target",vars=['pc1', 'pc2', 'pc3', 'pc4', 'pc5'])

# New legend added because original one is badly located
handles = g._legend_data.values()
labels = ['Benign', 'Malignant']
g.fig.legend(handles=handles, labels=labels, loc='lower center', ncol=3)
plt.show()






"""         Task D          """
pca = PCA()

principalComponents_breast = pca.fit_transform(data[1:10].T)
# number of components
n_pcs= pca.components_.shape[0]

# get the index of the most important feature on each component
most_important = [np.abs(pca.components_[i]).argmax() for i in range(n_pcs)]

# using just numbers of features
initial_feature_names = ['2','3','4','5', '6', '7', '8', '9', '10']
# get the names
most_important_names = [initial_feature_names[most_important[i]] for i in range(n_pcs)]

# LIST COMPREHENSION HERE AGAIN
dic = {'PC{}'.format(i): most_important_names[i] for i in range(n_pcs)}

df = pd.DataFrame(dic.items())
print("Sorted features from most to least important \n")
print (df)

""" 
As Written in the output:
    the most important feature is 7 (Bare Nuclei) 
    the least important feature is 3 (Uniformity of Cell Size) 
"""




"""         Task E          """

"""Not done"""



"""         Task F          """
"""
Since PCA is based on the correlation matrix, it is better to scale the data before processing. 
Without pre-processing huge variance in one variable can affect correlation matrix.
To avoid it, we have to scale all the variables to zero mean and variance of 1
"""




"""         Task G          """

lda = LinearDiscriminantAnalysis(n_components=1)
mm = lda.fit(data[1:10].T, data[10].T).transform(data[1:10].T)
colors = ['green', 'red']
lw = 2
plt.figure()

for color, i, target_name in zip(colors, [2,4], labels):
    plt.scatter(mm[data[10] == i, 0], principal_breast_Df["pc1"].where(data[10] == i).dropna(), alpha=.8, color=color,
                label=target_name)
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('1D-LDA vs PC1 of PCA')
plt.show()

""" 
1. It is not possible to make 5D embedding of the data because 
    original LDA can return only num_classes-1 projection.

2. As we can see on the plot, there are some outliers in comparison of LDA and PCA, 
    but overall both algorithms shows almost the same result
    In general, if data is normally distributed both algorithms should return almost the same result.
        
"""