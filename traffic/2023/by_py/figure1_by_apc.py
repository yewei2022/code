

from netCDF4 import Dataset
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import xarray as xr
import pandas as pd
import cartopy
import matplotlib
from netCDF4 import Dataset
from cartopy.feature import NaturalEarthFeature, COLORS
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from cartopy.feature import NaturalEarthFeature
from matplotlib.colors import from_levels_and_colors
from netCDF4 import Dataset
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader as shpreader
import matplotlib.ticker as mticker
import matplotlib.lines as mlines
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
import warnings
import re
import os, glob
import pandas as pd
from matplotlib.image import imread
from matplotlib.animation import FuncAnimation
import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
import cartopy.io.img_tiles as cimgt
from PIL import Image
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
import cartopy
import matplotlib
from netCDF4 import Dataset
from xarray import DataArray
from cartopy.feature import NaturalEarthFeature, COLORS
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from cartopy.feature import NaturalEarthFeature
from matplotlib.colors import from_levels_and_colors
from netCDF4 import Dataset
from xarray import DataArray
from wrf import smooth2d,interpline, getvar, interplevel, vertcross,vinterp, ALL_TIMES, CoordPair, xy_to_ll, ll_to_xy, to_np, get_cartopy, latlon_coords, cartopy_xlim, cartopy_ylim
from matplotlib.animation import FuncAnimation
import wrf
from IPython.display import HTML
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader as shpreader
import matplotlib.ticker as mticker
import matplotlib.lines as mlines
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
import warnings
import re
import os, glob
import pandas as pd
from matplotlib.image import imread
from matplotlib.animation import FuncAnimation
import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
import cartopy.io.img_tiles as cimgt
from PIL import Image
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from xgrads import CtlDescriptor
from xgrads import open_CtlDataset
import xarray as xr
#处理警告和中文
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

import cartopy.mpl.ticker as cticker
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.path as mpath
from matplotlib.font_manager import FontProperties
import numpy as np
import matplotlib as mpl
Simsun = FontProperties(fname="/mnt/d/pythonjiaoben/font/SimSun.ttf")
Times = FontProperties(fname="./mnt/d/pythonjiaoben/font/Times.ttf")
fname=FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=8)

proj = ccrs.PlateCarree()
prj =proj 

Chinese_land_territory_path = r'/mnt/d/keyan/pyconda/DataAl/daodaima/CMABSTdata/China_land_territory/China_land_territory.shp'
Chinese_10dash_line_path = r'/mnt/d/keyan/pyconda/DataAl/daodaima/CMABSTdata/China_10-dash_line/China_10-dash_line.shp'
world_countries_path = r'/mnt/d/keyan/pyconda/DataAl/daodaima/CMABSTdata/world_countries/world_countries.shp'
Chinese_Pr_Path = r'/mnt/d/keyan/pyconda/DataAl/daodaima/CMABSTdata/China_provinces/China_provinces.shp'
# 绘制中国陆地领土边界
Chinese_land_territory = shpreader(Chinese_land_territory_path).geometries()
Chinese_land_territory = cfeat.ShapelyFeature(Chinese_land_territory,prj, edgecolor='k',facecolor='none')
Chinese_Pr = shpreader(Chinese_Pr_Path).geometries()
Chinese_Pr = cfeat.ShapelyFeature(Chinese_Pr,prj, edgecolor='k',facecolor='none')
# 绘制中国十段线
Chinese_10dash_line = shpreader(Chinese_10dash_line_path).geometries()
Chinese_10dash_line = cfeat.ShapelyFeature(Chinese_10dash_line,prj, edgecolor='r')

# 绘制世界各国领土边界
world_countries = shpreader(world_countries_path).geometries()
world_countries = cfeat.ShapelyFeature(world_countries,prj, edgecolor='k', facecolor='none')


Gaoyuan=r'/mnt/d/Shuju/DBATP/DBATP_Line.shp'


Gaoyuan1= shpreader(Gaoyuan).geometries()
Gaoyuan1 = cfeat.ShapelyFeature(Gaoyuan1,
                                       prj, edgecolor='blue', 
                                       facecolor='none')




fig=plt.figure(figsize=(12,3.5))
gs = GridSpec(1,4,  figure=fig)
# 第一个子图占有第一行的全部空间
ax1 = fig.add_subplot(gs[0, 0],projection = proj)
ax2 = fig.add_subplot(gs[0, 1],projection = proj)
ax3 = fig.add_subplot(gs[0, 2],projection = proj)
ax4 = fig.add_subplot(gs[0, 3],projection = proj)

ax=[ax1,ax2,ax3,ax4]


cmap =  [[145,20,24],[ 210,30,39],
[245,106,41],[249,231,91],[ 72,181,70],[ 0,255,0] ,[ 71,142,201],[157,217,247],[255,255,255]]#       
cmap = np.array(cmap)/255.0  


import matplotlib.path as mpath
def get_hurricane():
    u = np.array([ [2.444,7.553],
    [0.513,7.046],
    [-1.243,5.433],
    [-2.353,2.975],
    [-2.578,0.092],
    [-2.075,-1.795],
    [-0.336,-2.870],
    [2.609,-2.016] ])
    u[:,0] -= 0.098
    codes = [1] + [2]*(len(u)-2) + [2]
    u = np.append(u, -u[::-1], axis=0)
    codes += codes
    return mpath.Path(3*u, codes, closed=False)

lon_t=[89.6,90.4,90.6,90.6]
lat_t=[21,23.4,25,25]


bq=['(a)','(b)','(c)','(d)']
ti=['TBB2618', 'TBB2700','TBB2706', 'TBB2712']




ctl1 = open_CtlDataset('/mnt/d/data/2.ctl')
# open_CtlDataset('f:/data/1.ctl').to_netcdf('f:/data/out.nc')
value1=ctl1.TBB.values[0,0]
lat1=ctl1.lat
lon1=ctl1.lon

ctl2 = open_CtlDataset('/mnt/d/data/3.ctl')
# open_CtlDataset('f:/data/1.ctl').to_netcdf('f:/data/out.nc')
value2=ctl2.TBB.values[0,0]
lat2=ctl2.lat
lon2=ctl2.lon

ctl3 = open_CtlDataset('/mnt/d/data/4.ctl')
# open_CtlDataset('f:/data/1.ctl').to_netcdf('f:/data/out.nc')
value3=ctl3.TBB.values[0,0]
lat3=ctl3.lat
lon3=ctl3.lon

ctl4 = open_CtlDataset('/mnt/d/data/5.ctl')
# open_CtlDataset('f:/data/1.ctl').to_netcdf('f:/data/out.nc')
value4=ctl4.TBB.values[0,0]
lat4=ctl4.lat
lon4=ctl4.lon



i=0
ff=xr.open_dataset('/mnt/d/era5nc/era5.u_component_of_wind.20081026.nc')
uwi=ff.u[18,15,92:201,40:141]
ff1=xr.open_dataset('/mnt/d/era5nc/era5.v_component_of_wind.20081026.nc')
vwi=ff1.v[18,15,92:201,40:141]
level=[value1.min(),-80, -70, -60, -50, -40, -30, -20, -10,   0]
ax[i].contourf(lon1,lat1,value1,transform=ccrs.PlateCarree(),levels=level,extend='both',colors=cmap)
ax[i].scatter(lon_t[i],lat_t[i], s=100, marker=get_hurricane(),transform=ccrs.PlateCarree(),
    edgecolors="black", linewidth=2.5,zorder=3)
lon=uwi.longitude
lat=uwi.latitude
inte=3
q=ax[i].quiver(lon[::inte], lat[::inte],uwi[::inte,::inte],vwi[::inte,::inte],
            width=0.0025, scale=270, color='k', headwidth=5,pivot='mid',transform=ccrs.PlateCarree(),
            alpha=1) 
ax[i].quiverkey(q, 0.5, 1.05, 10, r'$10 \frac{m}{s}$', labelpos='W',coordinates='axes',fontproperties=fname)
extent = [80,105,10,37]
ax[i].set_extent(extent, crs=prj)
ax[i].add_feature(Chinese_land_territory, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_Pr, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_10dash_line, linewidth=2)
ax[i].add_feature(world_countries, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Gaoyuan1, linewidth=1.2,alpha=0.8)
ax[i].set_xticks([ 80,  85,  90,  95, 100,105], crs=proj)
ax[i].set_yticks(np.arange(10,37,5), crs=proj)
fname=FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=8)
ax[i].set_title(bq[0],fontproperties=fname,loc='left')
ax[i].set_title(ti[0],fontproperties=fname,loc='right')

lon_formatter = cticker.LongitudeFormatter()
lat_formatter = cticker.LatitudeFormatter()
ax[i].xaxis.set_major_formatter(lon_formatter)
ax[i].yaxis.set_major_formatter(lat_formatter)
# ax[i].set_xlabel('Latitude', fontsize=8)# 
# ax[i].set_ylabel('Longitude', fontsize=8)
labels = ax[i].get_xticklabels() + ax[i].get_yticklabels()
[label.set_fontproperties(FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=7)) for label in labels]
gl = ax[i].gridlines(linestyle='-', alpha=0.5,linewidth=0.5)




i=1
ff=xr.open_dataset('/mnt/d/era5nc/era5.u_component_of_wind.20081027.nc')
uwi=ff.u[0,15,92:201,40:141]
ff1=xr.open_dataset('/mnt/d/era5nc/era5.v_component_of_wind.20081027.nc')
vwi=ff1.v[0,15,92:201,40:141]
level=[value2.min(),-80, -70, -60, -50, -40, -30, -20, -10,   0]
c1=ax[i].contourf(lon2,lat2,value2,transform=ccrs.PlateCarree(),levels=level,extend='both',colors=cmap)
ax[i].scatter(lon_t[i],lat_t[i], s=100, marker=get_hurricane(),transform=ccrs.PlateCarree(),
    edgecolors="black", linewidth=2.5,zorder=3)
lon=uwi.longitude
lat=uwi.latitude
inte=3
q=ax[i].quiver(lon[::inte], lat[::inte],uwi[::inte,::inte],vwi[::inte,::inte],
            width=0.0025, scale=270, color='k', headwidth=5,pivot='mid',transform=ccrs.PlateCarree(),
            alpha=1) 
ax[i].quiverkey(q, 0.5, 1.05, 10, r'$10 \frac{m}{s}$', labelpos='W',coordinates='axes',fontproperties=fname)

extent = [80,105,10,37]
ax[i].set_extent(extent, crs=prj)

ax[i].add_feature(Chinese_land_territory, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_Pr, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_10dash_line, linewidth=2)
ax[i].add_feature(world_countries, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Gaoyuan1, linewidth=1.2,alpha=0.8)

ax[i].set_xticks([ 80,  85,  90,  95, 100,105], crs=proj)
ax[i].set_yticks(np.arange(10,37,5), crs=proj)
fname=FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=8)
ax[i].set_title(bq[1],fontproperties=fname,loc='left')
ax[i].set_title(ti[1],fontproperties=fname,loc='right')

lon_formatter = cticker.LongitudeFormatter()
lat_formatter = cticker.LatitudeFormatter()
ax[i].xaxis.set_major_formatter(lon_formatter)
ax[i].yaxis.set_major_formatter(lat_formatter)
# ax[i].set_xlabel('Latitude', fontsize=8)# 
# ax[i].set_ylabel('Longitude', fontsize=8)
labels = ax[i].get_xticklabels() + ax[i].get_yticklabels()
[label.set_fontproperties(FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=7)) for label in labels]
gl = ax[i].gridlines(linestyle='-', alpha=0.5,linewidth=0.5)




i=2

ff=xr.open_dataset('/mnt/d/era5nc/era5.u_component_of_wind.20081027.nc')
uwi=ff.u[6,15,92:201,40:141]
ff1=xr.open_dataset('/mnt/d/era5nc/era5.v_component_of_wind.20081027.nc')
vwi=ff1.v[6,15,92:201,40:141]

level=[value1.min(),-80, -70, -60, -50, -40, -30, -20, -10,   0]
ax[i].contourf(lon1,lat1,value3,transform=ccrs.PlateCarree(),levels=level,extend='both',colors=cmap)
ax[i].scatter(lon_t[i],lat_t[i], s=100, marker=get_hurricane(),transform=ccrs.PlateCarree(),
    edgecolors="black", linewidth=2.5,zorder=3)

lon=uwi.longitude
lat=uwi.latitude

inte=3
q=ax[i].quiver(lon[::inte], lat[::inte],uwi[::inte,::inte],vwi[::inte,::inte],
            width=0.0025, scale=270,  color='k', headwidth=5,pivot='mid',transform=ccrs.PlateCarree(),
            alpha=1) 
ax[i].quiverkey(q, 0.5, 1.05, 10, r'$10 \frac{m}{s}$', labelpos='W',coordinates='axes',fontproperties=fname)

extent = [80,105,10,37]
ax[i].set_extent(extent, crs=prj)

ax[i].add_feature(Chinese_land_territory, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_Pr, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_10dash_line, linewidth=2)
ax[i].add_feature(world_countries, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Gaoyuan1, linewidth=1.2,alpha=0.8)


ax[i].set_xticks([ 80,  85,  90,  95, 100,105], crs=proj)
ax[i].set_yticks(np.arange(10,37,5), crs=proj)
fname=FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=8)
ax[i].set_title(bq[2],fontproperties=fname,loc='left')
ax[i].set_title(ti[2],fontproperties=fname,loc='right')


lon_formatter = cticker.LongitudeFormatter()
lat_formatter = cticker.LatitudeFormatter()
ax[i].xaxis.set_major_formatter(lon_formatter)
ax[i].yaxis.set_major_formatter(lat_formatter)
# ax[i].set_xlabel('Latitude', fontsize=8)# 
# ax[i].set_ylabel('Longitude', fontsize=8)
labels = ax[i].get_xticklabels() + ax[i].get_yticklabels()
[label.set_fontproperties(FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=7)) for label in labels]
gl = ax[i].gridlines(linestyle='-', alpha=0.5,linewidth=0.5)



i=3
ff=xr.open_dataset('/mnt/d/era5nc/era5.u_component_of_wind.20081027.nc')
uwi=ff.u[12,15,92:201,40:141]
ff1=xr.open_dataset('/mnt/d/era5nc/era5.v_component_of_wind.20081027.nc')
vwi=ff1.v[12,15,92:201,40:141]
level=[value2.min(),-80, -70, -60, -50, -40, -30, -20, -10,   0]
c1=ax[i].contourf(lon2,lat2,value4,transform=ccrs.PlateCarree(),levels=level,extend='both',colors=cmap)
ax[i].scatter(lon_t[i],lat_t[i], s=100, marker=get_hurricane(),transform=ccrs.PlateCarree(),
    edgecolors="black", linewidth=2.5,zorder=3)
lon=uwi.longitude
lat=uwi.latitude
inte=3
q=ax[i].quiver(lon[::inte], lat[::inte],uwi[::inte,::inte],vwi[::inte,::inte],
            width=0.0025, scale=270, color='k', headwidth=5,pivot='mid',transform=ccrs.PlateCarree(),
            alpha=1) 
ax[i].quiverkey(q, 0.5, 1.05, 10, r'$10 \frac{m}{s}$', labelpos='W',coordinates='axes',fontproperties=fname)

extent = [80,105,10,37]
ax[i].set_extent(extent, crs=prj)

ax[i].add_feature(Chinese_land_territory, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_Pr, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Chinese_10dash_line, linewidth=2)
ax[i].add_feature(world_countries, linewidth=0.3,alpha=0.8)
ax[i].add_feature(Gaoyuan1, linewidth=1.2,alpha=0.8)
ax[i].set_xticks([ 80,  85,  90,  95, 100,105], crs=proj)
ax[i].set_yticks(np.arange(10,37,5), crs=proj)
fname=FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=8)
ax[i].set_title(bq[3],fontproperties=fname,loc='left')
ax[i].set_title(ti[3],fontproperties=fname,loc='right')
lon_formatter = cticker.LongitudeFormatter()
lat_formatter = cticker.LatitudeFormatter()
ax[i].xaxis.set_major_formatter(lon_formatter)
ax[i].yaxis.set_major_formatter(lat_formatter)
# ax[i].set_xlabel('Latitude', fontsize=8)# 
# ax[i].set_ylabel('Longitude', fontsize=8)
labels = ax[i].get_xticklabels() + ax[i].get_yticklabels()
[label.set_fontproperties(FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=7)) for label in labels]
gl = ax[i].gridlines(linestyle='-', alpha=0.5,linewidth=0.5)


ax13=fig.add_axes([0.25,0.08,0.5,0.01])
cbar=fig.colorbar(c1,ax13,orientation='horizontal',shrink=0.8)#,ticks=[' ','-80','-70','-60','-50','-40','-30','-20','-10',' ']
# ax5.set_title('mm',fontsize=7)
# cbar.ax.tick_params(labelsize=1,width=0.5,length=0.5)
ax13.set_xticklabels([' ','−80','−70','−60','−50','−40','−30','−20','−10',' '])
labels=cbar.ax.get_xticklabels()
# [label.set_fontname("/mnt/d/pythonjiaoben/font/Times.ttf") for label in labels]
[label.set_fontproperties(FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=8.5)) for label in labels]


plt.savefig('/mnt/d/积云对流最终/tbb.png',dpi=1000)
plt.savefig('/mnt/d/积云对流最终/tbb.ps')
plt.savefig('/mnt/d/积云对流最终/tbb.eps')