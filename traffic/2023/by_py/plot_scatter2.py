# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 10:05:37 2023
浓雾日数空间分布散点图
色阶色条
@author: yewei
"""

import matplotlib.pyplot as plt
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from cartopy.io import shapereader as shpreader
import os
import cmaps #NCL绘图颜色
from matplotlib import colors, cm
from matplotlib.ticker import MultipleLocator

#解决找不到proj.db文件
os.environ['GDAL_DATA'] = r'C:\Anaconda3\py39\Library\share\gdal'
os.environ['PROJ_LIB'] = r"C:\Anaconda3\envs\network37\Library\share\proj"


plt.rcParams['font.sans-serif'] = ['Arial'] # 图片统一字体
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题
plt.rcParams['font.size'] = 15 #字体统一大小

#读取数据pd.read_excel(excel格式的文件似乎不方便用contourf作图）
file_name = 'year_avg_days'
df = pd.read_table("D:\\YEWEI\\project\\traffic\\data\\"+file_name+".txt",sep = "\s+")

lat = df['lat']
lon = df['lon']
rain = df['days']
 
# ==========================建立画布开始绘图===================================

# 设置colorbar刻度及区间色调
scales=[10,20,30,40,50,60,70,80,90,100,125,150,175]
cmap = cmaps.rainbow #cmap = cmaps.gist_rainbow 不行 只能用下面这个方法
# cmap = plt.get_cmap('jet')
boundaries=[0,10,20,30,40,50,60,70,80,90,100,125,150,175,500]#两边分别也要一个颜色啊
norm=colors.BoundaryNorm(boundaries,cmap.N)
mappable=cm.ScalarMappable(norm=norm,cmap=cmap)

# 设置散点标记的颜色区间
marker_colors= mappable.to_rgba(boundaries)

sizes= 20

plt_fig = plt.figure(figsize=(9, 6))
projection= ccrs.PlateCarree()
ax= plt.axes(projection=projection)
# 先在画布的绝对坐标建立子图
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

# 添加四川地图
shap=shpreader.Reader("D:\\YEWEI\\project\\traffic\\data\\shp\\"+"city.shp").geometries()
sichuan= cfeature.ShapelyFeature(shap,crs=ccrs.PlateCarree(),edgecolor='k', facecolor='none')
ax.add_feature(sichuan)

# Remove ticks on the top and right sides of the plot
ax.tick_params(axis='both', which='both', top=False, right=False)

# 绘制不同降水区间散点图
masked_lon= np.where(rain < scales[0], lon, np.nan)
masked_lat= np.where(rain < scales[0], lat, np.nan)
plt.scatter(masked_lon,masked_lat,s=sizes,color=marker_colors[0],zorder=1)

for x in range(1, len(scales)):
 masked_lon= np.where(rain >= scales[x - 1], lon, np.nan)
 masked_lon= np.where(rain < scales[x], masked_lon, np.nan)
 masked_lat= np.where(rain >= scales[x - 1], lat, np.nan)
 masked_lat= np.where(rain < scales[x], masked_lat, np.nan)
 plt.scatter(masked_lon,masked_lat,s=sizes,color=marker_colors[x],zorder=1)

masked_lon= np.where(rain >= scales[-1], lon, np.nan)
masked_lat= np.where(rain >= scales[-1], lat, np.nan)
plt.scatter(masked_lon,masked_lat,s=sizes,color=marker_colors[-1],zorder=1)


plt.colorbar(mappable=mappable,ax=ax,orientation='vertical',label='',
             drawedges=True,format='%.0f',
             ticks=scales) #extend 两头三角

#图片保存
plt.savefig('D:\\YEWEI\\project\\traffic\\pic\\'+file_name+"2.jpg", dpi=800) #dpi越大越清晰
#要先save在show，不然show出来的是空白图片
plt.show()

