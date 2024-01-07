# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:08:58 2023
画石棉
两种插值方法 反距离插值 径向基函数（RBF）插值
@author: 14779
"""

import numpy as np
import pandas as pd


# In[1]:

sheet_names = ['石棉县', '汉源县', '雨城区', '什邡市', '万源市', '越西县', 
               '峨边彝族自治县', '梓潼县', '大邑县', '叙永县', '市中区', 
               '邛崃市', '普格县']    
sheet_en = ["shimian", "hanyuan", "yuchengqu", "shenfang", "wanyuan", "yuexi",
            "ebian", "zitong", "dayi", "xuyong", "leshanshizhongqu", 
            "qionglai", "puge"]
putfile = ["tem_min","tem_max","tem_avg","prcp","pres","RH","wind"]
var =['最低气温','最高气温','平均气温','20降水','平均气压','平均湿度','平均风速']
units = ["(℃)","(℃)","(℃)","(mm)","(hPa)", "(%)","(m/s)"]

i = 0 # 地区
for j in range(0,7):
    # j = 3 # 变量
    a0 = pd.read_table("D:\\job\\data\\deal\\"+sheet_en[i]+"_"+putfile[j]+".txt",
                              sep='\s+',na_values=32700)
    # 再去掉一些地名
    a0.loc[a0["站名"].isin(["大岗山营地", "王岗坪新华", "新民茨格达海" , "孟获收费站",
                          "安顺供水站", "美罗八佛山","美罗马富","美罗三明",
                          "坪阳","迎政红旗","龙头石", "新棉野猪坪","蟹螺猛种三组",
                          "马烈新华烂泥三湾","出路"]),"站名"] = " "
    
    
    # In[2]: # 站点数据插值到格点
    
    pre =a0[[var[j]]].values
    lon = a0['经度'].astype(float) # 这里不能用a0[['经度']].values 不然后面插值报错2D
    lat = a0['纬度'].astype(float)
    
    leftlon, rightlon, lowerlat, upperlat = (101.9,102.6,28.8,29.6) #!!!换县

     
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
            lon, lat, pre, lon_gridmesh, lat_gridmesh, r = 0.3, 
            min_neighbors = 0.05)
    else:
        pre_grid = inverse_distance_to_grid(
            lon, lat, pre, lon_gridmesh, lat_gridmesh, r = 0.2, 
            min_neighbors = 0.05)
    
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
    value_min = np.rint(float(np.nanmin(pre))) #四舍五入
    value_max = np.rint(float(np.nanmax(pre)))
    arr_min = np.nanmin(pre_grid)
    arr_max = np.nanmax(pre_grid)
    
    print("{} {}的站点最小值为：{}".format(j,var[j],value_min))
    print("{} {}的站点最大值为：{}".format(j,var[j],value_max))
    print("{} {}的格点最小值为：{}".format(j,var[j],arr_min))
    print("{} {}的格点最大值为：{}".format(j,var[j],arr_max))
    
    # 法一 给出数量，出等差数列
    # levels = np.linspace(value_min,value_max,nlevels)
    # levels1 = levels[10:-10]

    #法二给出间隔，出等差数列  #!!! 改  
    interval = [0.1, 0.1, 0.1, 5, 1, 0.01, 0.005]    
    if j == 3:
        value_min = 300 
        value_max = 1000
        levels = np.arange(value_min,value_max,interval[j])    
        levels1 = levels
    elif j == 4:
        value_min = 800
        value_max = 900
        levels = np.arange(value_min,value_max,interval[j])    
        levels1 = levels
    elif j == 5:
        value_min = 70
        value_max = 80
        levels = np.arange(value_min,value_max,interval[j])    
        levels1 = levels
    elif j == 6:
        value_min = 0.8
        value_max = 2.8
        levels = np.arange(value_min,value_max,interval[j])    
        levels1 = levels
    else:
        levels = np.arange(value_min,value_max,interval[j])    
        levels1 = levels[25:-25]
    
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
    
    a1.loc[:,'纬度'] = a1['纬度']+0.011
    a1.loc[:,'经度'] = a1['经度']+0.01        
    xy_sta = np.array(a1[['经度','纬度']])
    for k in range(len(a1)):
        ax.annotate(a1['站名'][k], xy=xy_sta[k], xytext=xy_sta[k],
                      horizontalalignment='center', verticalalignment='center',
                      fontsize = 10)
    
    # 保存
    pic_dir = r"D:/job/pic/"+sheet_en[i]+"/py/"+sheet_en[i]+str(j)+"_"+putfile[j]
    plt.savefig(pic_dir+'.jpg', dpi=1000, bbox_inches = 'tight')
    plt.show() #先保存才能plot.show

