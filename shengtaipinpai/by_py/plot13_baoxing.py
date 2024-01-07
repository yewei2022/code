# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 16:42:00 2023

@author: 14779
"""

import pandas as pd
import numpy as np

# excel表格中“县级”那栏下的名称 用于读取每个表中需要的县（有些表可能混杂其他县
sheet_names = ['宝兴县', '古蔺县']
sheet_en = ["baoxing", "gulin"]
data_dir = "D:\\project\\shengtaipinpai\\data\\"
pic_dir = "D:\\project\\shengtaipinpai\\pic\\"

#%% branch3 站点插值成格点并绘图 


putfile = ["tem_min","tem_max","tem_avg","prcp","pres","RH","wind"]
var =['最低气温','最高气温','平均气温','20降水','平均气压','平均湿度','平均风速']
units = ["(℃)","(℃)","(℃)","(mm)","(hPa)", "(%)","(m/s)"]

i = 0 # 地区
for j in range(0,7):
    # j = 3 # 变量
    a0 = pd.read_table(data_dir+"deal\\"+sheet_en[i]+"_"+putfile[j]+".txt",
                              sep='\s+',na_values=32700)
    # 再去掉一些地名
    a0.loc[a0["站名"].isin(["两河口", "泽根", "嘎日" , "硗碛",
                          "中岗12组", "大池沟民和","教场沟口","冷木沟顶",
                          "烟溪口","新华", "陇东","灵关河口",
                          "灵关大沟","邓池沟和平"]),"站名"] = " "
    
    
    # In[2]: # 站点数据插值到格点
    
    pre =a0[[var[j]]].values
    lon = a0['经度'].astype(float) # 这里不能用a0[['经度']].values 不然后面插值报错2D
    lat = a0['纬度'].astype(float)
    
    leftlon, rightlon, lowerlat, upperlat = (102.3,103.1,30.1,31) #!!!宝兴
    # leftlon, rightlon, lowerlat, upperlat = (101.9,102.6,28.8,29.6) #!!!换县
    

     
    # 根据上下限确定范围，至少为10°
    lon_grid = np.arange(leftlon, rightlon, 0.005)
    lat_grid = np.arange(lowerlat, upperlat, 0.005)
    lon_gridmesh, lat_gridmesh = np.meshgrid(lon_grid, lat_grid)
    
    # 站点数据插值到格点 反距离插值
    from metpy.interpolate import inverse_distance_to_grid
    if j==4 or j==5 :
        pre_grid = inverse_distance_to_grid(
            lon, lat, pre, lon_gridmesh, lat_gridmesh, r = 0.5, 
            min_neighbors = 0.05)
    elif j==6 :
        pre_grid = inverse_distance_to_grid(
            lon, lat, pre, lon_gridmesh, lat_gridmesh, r = 0.6, 
            min_neighbors = 0.05)
    else:
        pre_grid = inverse_distance_to_grid(
            lon, lat, pre, lon_gridmesh, lat_gridmesh, r = 0.3, 
            min_neighbors = 0.025)
    
    # # 站点数据插值到格点 Rbf 插值
    # from scipy.interpolate import Rbf
    # # 插值处理,‘linear’，‘nearest’，‘cubic’
    # # cubic, gaussian, inverse_multiquadric, linear, multiquadric, quintic, thin_plate
    # # rain_data_new = griddata((lon,lat), data, (olon,olat), method='linear')
    # func1 = Rbf(lon,lat,pre,function='linear', smooth = 1) #Gaussian linear
    # pre_grid = func1(lon_gridmesh,lat_gridmesh)

    # In[3]:
    # 画图
    import cartopy.io.shapereader as shpreader
    from cartopy.mpl.patch import geos_to_path
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    import cartopy.crs as ccrs
    import cmaps
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter  
                                                                 
    cmap=cmaps.MPL_rainbow                                                 
    
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题
    
    # 读取shp文件
    shp_path = r"D:/ChinaMap/"+sheet_en[i]+"/"+sheet_en[i]+".shp"
    shp = shpreader.Reader(shp_path)
    geo_list = list(shp.geometries())
    proj = ccrs.PlateCarree()
    poly = geo_list[0] # 248代表中国
    path = Path.make_compound_path(*geos_to_path(poly))
    # 开始画图
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(projection=ccrs.PlateCarree())
    #必须设置地图范围 不然经纬度会错误对应
    ax.set_extent([leftlon, rightlon, lowerlat, upperlat], crs=ccrs.PlateCarree())
    value_min = np.rint(float(np.nanmin(pre))) #四舍五入
    value_max = np.rint(float(np.nanmax(pre)))
    arr_min = np.nanmin(pre_grid)
    arr_max = np.nanmax(pre_grid)
    
    print("{} {}的站点最小值为：{}".format(j,var[j],value_min))
    print("{} {}的站点最大值为：{}".format(j,var[j],value_max))
    print("{} {}的格点最小值为：{}".format(j,var[j],arr_min))
    print("{} {}的格点最大值为：{}".format(j,var[j],arr_max))
    
    # 法一 给出数量，出等差数列
    nlevels = 80
    levels = np.linspace(float(arr_min),float(arr_max),nlevels)
    #相对湿度
    if j == 5:
        value_min = 83 
        value_max = 86
        levels = np.arange(value_min,value_max,0.01)    
        levels1 = levels
    else:
        levels1 = levels[10:-10]

    # #法二给出间隔，出等差数列  #!!! 改  
    # interval = [0.1, 0.1, 0.1, 5, 1, 0.01, 0.005]    
    # if j == 3:
    #     value_min = 700 
    #     value_max = 1400
    #     levels = np.arange(value_min,value_max,interval[j])    
    #     levels1 = levels
    # elif j == 4:
    #     value_min = 800
    #     value_max = 900
    #     levels = np.arange(value_min,value_max,interval[j])    
    #     levels1 = levels
    # elif j == 5:
    #     value_min = 84
    #     value_max = 86
    #     levels = np.arange(value_min,value_max,interval[j])    
    #     levels1 = levels
    # elif j == 6:
    #     value_min = 1
    #     value_max = 2.5
    #     levels = np.arange(value_min,value_max,interval[j])    
    #     levels1 = levels
    # else:
    #     levels = np.arange(value_min,value_max,interval[j])    
    #     levels1 = levels[5:-35]
    
    ac = ax.contourf(lon_grid, lat_grid, pre_grid,transform=proj, 
                     levels= levels1, extend='both',cmap=cmap,
                     alpha=0.8, antialiased = True)#alpha透明度 antialiased 等值线浅
    # 中国轮廓线
    ax.add_geometries([poly], proj, facecolor='none', edgecolor='k') 
    # 等值线
    # ad = ax.contour(ac, colors='k')
    # 站点
    ax.scatter(lon, lat, color="k", s=10, marker="o",transform=proj, label='station')
    
    # # 添加网格
    # gl = ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle=':',
    #                   xlocs=np.arange(70, 140, 5), ylocs=np.arange(16.0, 56.0, 5.0))
    # gl.right_labels = False
    # gl.top_labels = False
    # gl.down_labels = True
    # 
    # 白化中国以外的填色
    for col in ac.collections:
        col.set_clip_path(path, transform=ax.transData)
    # 白化中国以外的散点
    for col in ax.collections:
        col.set_clip_path(path, transform=ax.transData)
        
    # 白化等值线线条
    # for col in ad.collections:
    #     col.set_clip_path(path, transform=ax.transData)
    
    # plt.legend(fontsize=15) ;站点图例
    # 色标 
    cb = plt.colorbar(ac, orientation='vertical', shrink=0.6)
    cb.ax.set_title(units[j],x= 1.4,y= -0.18,fontsize=20)
    from matplotlib.ticker import FormatStrFormatter
    cb.ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    
    # 以下6条语句是定义地理坐标标签格式
    ax.set_xticks(np.arange(leftlon+0.1, rightlon, 0.2),crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(lowerlat+0.1, upperlat, 0.2),crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter()
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    
    cb.ax.tick_params(labelsize=16)  #设置色标刻度字体大小。
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    font = {'family' : 'serif',
            'color'  : 'darkred',
            'weight' : 'normal',
            'size'   : 16,
            }
    # cb.set_label('降水量',fontdict=font,loc='bottom') #设置colorbar的标签字体

    # 去掉站名有以下字符的行
    a0 = a0[~a0['站名'].isin(['新民集镇'])]
    # 添加站点名    
    a1 =a0.reset_index(inplace = False)
    
    a1.loc[:,'纬度'] = a1['纬度']+0.015
    a1.loc[:,'经度'] = a1['经度']+0.01        
    xy_sta = np.array(a1[['经度','纬度']])
    for k in range(len(a1)):
        ax.annotate(a1['站名'][k], xy=xy_sta[k], xytext=xy_sta[k],
                      horizontalalignment='center', verticalalignment='center',
                      fontsize = 12)
    
    # 保存
    plt.savefig(pic_dir+sheet_en[i]+"\\py\\"+sheet_en[i]+str(j)
                +"_"+putfile[j]+'.jpg', dpi=1000, bbox_inches = 'tight')
    plt.show() #先保存才能plot.show