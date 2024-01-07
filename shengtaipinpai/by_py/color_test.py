# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:37:03 2023
截取colors部分颜色
@author: 14779
"""

from cartopy.mpl.patch import geos_to_path
import matplotlib.pyplot as plt
from matplotlib.path import Path
import cartopy.crs as ccrs
import cmaps
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter 
import numpy as np


import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list("trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),cmap(np.linspace(minval, maxval, n)),)
    return new_cmap
arr = np.linspace(0, 50, 100).reshape((10, 10))
fig, ax = plt.subplots(ncols=2)
cmap = plt.get_cmap("Spectral")
trunc_cmap = truncate_colormap(cmap, 0.2, 0.8)
ax[0].imshow(arr, interpolation="nearest", cmap=cmap)
ax[1].imshow(arr, interpolation="nearest", cmap=trunc_cmap)
plt.show()