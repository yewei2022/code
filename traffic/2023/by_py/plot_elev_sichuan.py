# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 14:55:57 2023
白化地图
一个shp 一个地区
@author: yewei
"""

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import matplotlib as mpl
import pandas as pd
import matplotlib.patheffects as path_effects
import os
import cartopy.crs as ccrs
os.environ['GDAL_DATA'] = r'C:\Anaconda3\py39\Library\share\gdal'
os.environ['PROJ_LIB'] = r"C:\Anaconda3\envs\network37\Library\share\proj"

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=128):
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name,
                                            a=minval, b=maxval),cmap(np.linspace(minval, maxval, n)))
    return new_cmap
data_dir = "D:\\YEWEI\\project\\traffic\\data\\"
pic_dir ='D:\\YEWEI\\project\\traffic\\pic\\'
data=nc.Dataset(data_dir+ "ETOPO2v2c_f4.nc")
print(data)
topo=data.variables['z'][2600:,5400:]
lat=data.variables['y'][2600:]
lon=data.variables['x'][5400:]
lon_grid, lat_grid = np.meshgrid(lon,lat) #经纬度2维化

#站点数据
sta = pd.read_table(data_dir+ "sta_info.txt", sep = ",")
sta_name_160 = sta['name']
sta_id_160 = sta['sta']
lo_160= sta['lon'].to_numpy()
la_160 = sta['lat'].to_numpy()



#%%

import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import pandas as pd
import os
from matplotlib.ticker import MultipleLocator


#开始画图
plt.rcParams['font.sans-serif'] = ['Arial'] # 图片统一字体
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题
plt.rcParams['font.size'] = 15 #字体统一大小
fig = plt.figure(figsize=(12, 8))
projection= ccrs.PlateCarree()
ax = fig.add_subplot(projection=projection)

leftlon, rightlon, lowerlat, upperlat = (97, 109, 25, 35) 
ax.set_extent([leftlon, rightlon, lowerlat, upperlat], crs=projection)
# 自定义坐标轴主刻度
ax.set_xticks(np.arange(leftlon+1, rightlon, 4), crs=ccrs.PlateCarree())
#rightlon或是下面的upperlat应写大一个间隔，在这里就是+10
ax.set_yticks(np.arange(lowerlat, upperlat, 2), crs=ccrs.PlateCarree())
# # 设置坐标轴刻度的字体大小
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
#坐标设置成经纬度
lon_formatter = LongitudeFormatter()
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
# ax.set_title('',loc='center', fontsize=15)
#设置次刻度间隔
ax.xaxis.set_minor_locator(MultipleLocator(1))##把x轴的刻度间隔设置为1
ax.yaxis.set_minor_locator(MultipleLocator(1))
# 显示主副刻度线
ax.tick_params(axis="both", which="major", direction="out", width=1, length=6)
ax.tick_params(axis="both", which="minor", direction="out", width=1, length=3)


cmap_new = truncate_colormap(plt.cm.terrain, 0.23, 1.0) #截取colormap，要绿色以上的（>=0.23）
cmap_new.set_under([198/255,234/255,250/255]) #低于0的填色为海蓝
lev=np.arange(0,5600,50)
norm3 = mpl.colors.BoundaryNorm(lev, cmap_new.N) #标准化level，映射色标
ac = ax.contourf(lon_grid, lat_grid, topo,transform=projection, 
                  levels= lev, norm = norm3, extend='neither',cmap=cmap_new,
                  alpha=0.8, antialiased = True)#alpha透明度 antialiased 等值线浅

# 添加四川市级地图
shp = shpreader.Reader(data_dir + "shp\\city.shp").geometries()
sichuan= cfeature.ShapelyFeature(shp,crs=ccrs.PlateCarree(),edgecolor='k', facecolor='none')
ax.add_feature(sichuan)

# 填色图色条
cb=plt.colorbar(ac, ax=ax,drawedges = False,pad=0.02,
                orientation='vertical') #pa-色标与图形间距
# cb.ax.tick_params(labelsize=10,pad=2,direction='in') #单独设置色标字体大小
cb.set_label('(m)') 
# cb.ax.set_title("(m)",x= 1.4,y= -0.1,fontsize=20)

# 站点
ax.scatter(lo_160, la_160, color="red", s=15, marker="^",transform=projection, 
            label='station')

#白化中国以外区域
import cartopy.io.shapereader as shpreader
from cartopy.mpl.patch import geos_to_path
import matplotlib.pyplot as plt
from matplotlib.path import Path
import cartopy.crs as ccrs
import geopandas as gpd

shp_clip = gpd.read_file(data_dir + "shp\\province.shp")
path_clip = Path.make_compound_path(*geos_to_path(shp_clip['geometry'].tolist()))
codes = path_clip.codes
 
path_clip = Path(projection.transform_points(ccrs.PlateCarree(),
                                       path_clip.vertices[:,0], 
                                       path_clip.vertices[:,1])[:,0:2],codes=codes)

for col in ac.collections:
    col.set_clip_path(path_clip, transform=ax.transData) 
  
plt.savefig(pic_dir + "elev_sichuan.jpg",dpi=300,bbox_inches='tight') #存图
plt.show()