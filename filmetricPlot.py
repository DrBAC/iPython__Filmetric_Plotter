import pandas as pd
import sys
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import pylab
from scipy.interpolate import griddata

path = '../RAW DATA FILES FOR ANALYSIS/220316-BAC_ND1.fimap'

title = path.split('/')[-1]
rootpath = path.split('/')[:-1]

datafile = pd.read_csv(path,names=['Col1','Col2','Col3','Col4'])

#WaferW = kdf[kdf['Col1'].str.contains('Wafer Width')]
#SiteIndexing = kdf[kdf['Key'].str.contains('Site_')]

def Search(term):
    """
    Returns properties described by 'term'
    """
    item = datafile[datafile['Col1'].str.contains(term)] # allows search for term
    return item['Col1'].index

measuredPoints = Search('Measured Die')
dieSite = Search('Die x').values

firstSite = dieSite+1
lengthArray = datafile.iloc[measuredPoints,1].values[0]
lengthArrayNos = int(lengthArray)
#arrayEnd = (dieSite+1)+int(datafile.loc[measuredPoints,1].values[0])
arrayEnd = firstSite + lengthArrayNos
xyzValues = datafile.iloc[firstSite:arrayEnd,0:3]

Xobjs = xyzValues['Col1'].values
Yobjs = xyzValues['Col2'].values
Zobjs = xyzValues['Col3'].values

XInts = [int(float(x)) for x in Xobjs]
YInts = [int(float(y)) for y in Yobjs]
ZInts = [int(float(z)) for z in Zobjs]

df = pd.DataFrame()
df['x'] = XInts
df['y'] = YInts
df['z'] = ZInts

x=df['x']
y=df['y']
z=df['z']

x1 = np.linspace(df['x'].min(), df['x'].max(), 20)#len(df['x'].unique()))
y1 = np.linspace(df['y'].min(), df['y'].max(), 20)#len(df['y'].unique()))
x2, y2 = np.meshgrid(x1, y1)
#z2 = griddata((df['x'], df['y']), df['z'], (x2, y2), method='linear')
z2 = griddata((df['x'], df['y']), df['z'], (x2, y2), method='cubic')

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x2, y2, z2, rstride=1, cstride=1, cmap=cm.coolwarm,
    linewidth=0.05, antialiased=False)
ax.set_zlim(min(z)-200, max(z)+200)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=10)
plt.title(title)
# ~~~~ MODIFICATION TO EXAMPLE ENDS HERE ~~~~ #

plt.show()

# KICKS OUT THE GRAPH
# saves it to name of original input file but with pdf suffix
#pdf_name = os.path.splitext(path)[0]+'.pdf'
#pylab.savefig(pdf_name)