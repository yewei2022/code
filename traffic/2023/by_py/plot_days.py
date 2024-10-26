# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:32:32 2023
换浓雾日数空间分布散点图
连续色条
@author: yewei
"""

import matplotlib.pyplot as plt
import numpy as np
import cartopy
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from cartopy.io import shapereader as shpreader
import os
#解决找不到proj.db文件
os.environ['GDAL_DATA'] = r'C:\Anaconda3\py39\Library\share\gdal'
os.environ['PROJ_LIB'] = r"C:\Anaconda3\envs\network37\Library\share\proj"


plt.rcParams['font.sans-serif'] = ['Arial'] # 图片统一字体
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题
plt.rcParams['font.size'] = 20 #字体统一大小

#读取数据pd.read_excel(excel格式的文件似乎不方便用contourf作图）
file_name = 'year_avg_days'
df = pd.read_table("D:\\YEWEI\\project\\traffic\\data\\"+file_name+".txt",sep = "\s+")

lat = df['lat']
lon = df['lon']
temps = df['days']
 
# ==========================建立画布开始绘图===================================

fig2 = plt.figure(figsize=(15, 15))

# 绘制地图
proj = ccrs.PlateCarree()
f2_ax1 = fig2.add_subplot(projection=proj)
# 在画布的绝对坐标建立子图
leftlon, rightlon, lowerlat, upperlat = (97, 109, 25, 35) 
#要显示的经纬度范围
f2_ax1.set_extent([leftlon, rightlon, lowerlat, upperlat],
                  crs=ccrs.PlateCarree())
 
# 以下6条语句是定义要显示的地理坐标标签
f2_ax1.set_xticks(np.arange(leftlon+1, rightlon, 1), crs=ccrs.PlateCarree())
#rightlon或是下面的upperlat应写大一个间隔，在这里就是+10
f2_ax1.set_yticks(np.arange(lowerlat, upperlat, 1), crs=ccrs.PlateCarree())
# # 设置坐标轴刻度的字体大小
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)

lon_formatter = LongitudeFormatter()
lat_formatter = LatitudeFormatter()
f2_ax1.xaxis.set_major_formatter(lon_formatter)
f2_ax1.yaxis.set_major_formatter(lat_formatter)
# f2_ax1.set_title('',loc='center', fontsize=15)
 
# 读取shp文件
Sichuan = shpreader.Reader("D:\\YEWEI\\project\\traffic\\data\\shp\\"+"city.shp").geometries()
# 绘制行政边界
f2_ax1.add_geometries(Sichuan, ccrs.PlateCarree(),
                      facecolor='none', edgecolor='black', zorder=1)
 
#绘制站点，颜色表示温度，cmap是选择一种colorbar的格式
f2 = f2_ax1.scatter(lon, lat, s=20, c=temps, cmap='gist_rainbow_r',
                    transform=ccrs.PlateCarree(),vmin = 0,vmax =175)


# #单独设置坐标轴以及刻度标签的字体
# f2_ax1.set_xlabel('Chinese Scores', fontname='Times New Roman')
# f2_ax1.set_ylabel('Math Scores / English Scores', fontname='Times New Roman')
# for tick in f2_ax1.get_xticklabels():
#     tick.set_fontname("Times New Roman")
# for tick in f2_ax1.get_yticklabels():
#     tick.set_fontname("Times New Roman")
    
#下面定义colorbar大小和位置
# colorbar 左 下 宽 高
l = 0.92
b = 0.25
w = 0.015
h = 0.5
 
# 对应 l,b,w,h；设置colorbar位置；
rect = [l, b, w, h]
cbar_ax = fig2.add_axes(rect)
cb = plt.colorbar(f2, cax=cbar_ax)
# #设置色标刻度字体大小
# cb.ax.tick_params(labelsize=18)  
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# font = {'family' : 'serif',
#         'color'  : 'darkred',
#         'weight' : 'normal',
#         'size'   : 18,
#         }
#图片保存
plt.savefig('D:\\YEWEI\\project\\traffic\\pic\\'+file_name+"1.jpg", dpi=300) #dpi越大越清晰
#要先save在show，不然show出来的是空白图片
plt.show()

