""" 
Start code from code in project 1 description on github
"""
import numpy as np
from random import random, seed
#
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


#   /////// Functions   /////// 
def Frankefunction(x, y):
    term1   =   0.75  *np.exp(    -0.25*(9*x - 2)**2  -   0.25*(9*y - 2)**2   )
    term2   =   0.75  *np.exp(    -(9*x + 1)**2/49.   -   0.1*(9*y - 1)       )
    term3   =   0.5   *np.exp(    -0.25*(9*x - 7)**2  -   0.25*(9*y - 3)**2   )
    term4   =  -0.2   *np.exp(    -(9*x - 4)**2       -   (9*y - 7)**2        )
    return term1 + term2 + term3 + term4

def Designmatrix(x, y, n=5):
    """ 
    create a design matrix dependent on the polynomial grade you want, with a base of 3.
    want the collumns of X to be [1, x, y, x^2, xy, y^2, x^3, x^2y, xy^2, y^3]
    and so on. 
    """
    if len(x.shape) > 1:
        x = np.ravel(x)
        y = np.ravel(y)

    N = len(x)
    l = int( (n+1)*(n+2)/2 )    # nr. of elements in beta
    X = np.ones((N,l))

    for i in range(1, n+1):
        q = int( (i)*(i+1)/2 )
        for k in range(i+1):
            X[:, q+k] = x**(i-k) * y**k
    
    return X

def confidence(beta, confidence=1.96):
    weight = confidence*np.var(beta)
    betamin = beta - weight
    betamax = beta + weight
    return betamin, betamax

def rsquared(y, y_pred):
    return 1 - ( np.sum( (y - y_pred)**2 )/np.sum( (y - np.mean(y))**2 ) )
#   ///////     /////// 


#   ///////   make data   ///////   
row             =   np.arange(0, 1, 0.05)
col             =   np.arange(0, 1, 0.05)
x_plot, y_plot  =   np.meshgrid(row,col)
#   Noise
noiseSTR = .05
noise           =   np.random.randn(len(row), len(col))
#
z_plot          =   Frankefunction(x_plot, y_plot) + (noiseSTR * noise)
#   ///////     /////// 
#   ///////   make random data   ///////   
nrow = 100
ncol = 200
rand_row        =       np.random.uniform(0, 1, size=nrow)
rand_col        =       np.random.uniform(0, 1, size=ncol)

sortrowindex    =       np.argsort(rand_row)
sortcolindex    =       np.argsort(rand_col)

rowsort         =       rand_row[sortrowindex]
colsort         =       rand_col[sortcolindex]

colmat, rowmat  =       np.meshgrid(colsort, rowsort)

noiseSTR        =       .05
noise           =       np.random.randn(nrow, ncol)

zmat            =       Frankefunction(rowmat, colmat) + noiseSTR*noise
#   ///////     /////// 

#   ///////   flatten   ///////   
rowarr          =       rowmat.ravel()
colarr          =       colmat.ravel()
zarr            =       zmat.ravel()
#   ///////     /////// 

#   ///////   design matrix   ///////   
n               =       5
X               =       Designmatrix(rowarr, colarr, n)
#   ///////     /////// 

#   ///////    Linear regression   ///////   
beta            =       np.linalg.inv( X.T @ X ) @ X.T @ zarr
CImin, CImax    =       confidence(beta)
z_pred          =       X @ beta
z_pred_plot     =       z_pred.reshape(nrow, ncol)
#   ///////     /////// 

#   ///////   Error   ///////   
MSE             =       1/len(z_pred) * np.linalg.norm( zarr - z_pred )**2
print( "MSE is: ", MSE )
#   ///////     /////// 

#   ///////   Plot   ///////   
fig = plt.figure()

ax      =   fig.add_subplot(1, 2, 1, projection='3d')
surf    =   ax.plot_surface(
            rowmat, colmat, zmat, cmap=cm.coolwarm, linewidth=0, antialiased=False   )
fig.colorbar(surf, shrink=0.5, aspect=5)
#plt.title('Franke')
plt.title('Measurement')

ax      =   fig.add_subplot(1, 2, 2, projection='3d')
surf    =   ax.plot_surface(
            rowmat, colmat, z_pred_plot, cmap=cm.coolwarm, linewidth=0, antialiased=False   )
fig.colorbar(surf, shrink=0.5, aspect=5)
#plt.title('Fitted Franke')
plt.title('OLS fit')

plt.show()
#   ///////     /////// 
