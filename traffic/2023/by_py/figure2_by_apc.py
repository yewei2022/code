from matplotlib.font_manager import FontProperties
import cartopy.mpl.ticker as cticker
from matplotlib.gridspec import GridSpec
proj = ccrs.PlateCarree()
# extent=[95.3,96.11,29.2,30.01]

level=np.arange(1000,6501,200)
fname=FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=10)
mkz=2.4
llw=1.2
font={'family' : 'Times New Roman', 'size'   :8}

plt.rc('font',family='Times New Roman')

fig=plt.figure(figsize=(12,4),dpi=800)
gs = GridSpec(1,3,  figure=fig)
# 第一个子图占有第一行的全部空间
ax1 = fig.add_subplot(gs[0, 0],projection = proj)
ax2 = fig.add_subplot(gs[0, 1],projection = proj)
ax3 = fig.add_subplot(gs[0, 2],projection = proj)

ax=[ax1,ax2,ax3]
path=['/mnt/h/TDK30s/wrfout_d04_2008-10-26_00_10_00','/mnt/g/TDK2m/wrfout_d04_2008-10-26_00_10_00','/mnt/g/TDK5m/wrfout_d04_2008-10-26_00_10_00']
path2=['/mnt/d/dixing/30s/','/mnt/d/dixing/2m/','/mnt/d/dixing/5m/']
bh=['(a) Topographic height of 30s (unit:m)','(b) Topographic height of 2m (unit:m)','(c) Topographic height of 5m (unit:m)']
# bl=[['8%','29%','25%','33%','4%'],['8%','12%','44%','4%','32%'],['24%','56%','8%','8%','4%']]
bl=[['8%','29%','25%','33%','4%'],['16%','44%','12%','24%','4%'],['27%','5%','41%','23%','5%']]

for i in range(0,3,1):

    ncfile = Dataset(path[i])
    HGT = getvar(ncfile, "HGT") 
    p = getvar(ncfile, "pressure") 
    lats, lons = latlon_coords(p)
    latt=lats[:,0]
    lonn=lons[0,:] 
    extent=[lonn.min(),lonn.max(),latt.min(),latt.max()]
    ax[i].set_extent(extent, crs=proj)
    c1=ax[i].contourf(lons, lats, HGT , cmap='terrain',alpha=1,levels=level, projection=proj,extend='both')
    ax[i].contour(lons, lats, HGT , levels=[3000], projection=proj,color='black')
    ax[i].scatter(91.95,27.9778,marker="o",s= 20)




    ax[i].set_xticks(np.arange(np.round(lonn.min(),1),np.round(lonn.max(),1),0.5), crs=proj)
    ax[i].set_yticks(np.arange(np.round(latt.min(),1),np.round(latt.max(),1),0.5), crs=proj)


    # ax[i].set_xticks(np.arange(95.3,96.11,0.2), crs=proj)
    # ax[i].set_yticks(np.arange(29.2,30.01,0.2), crs=proj)
    lon_formatter = cticker.LongitudeFormatter()
    lat_formatter = cticker.LatitudeFormatter()
    ax[i].xaxis.set_major_formatter(lon_formatter)
    ax[i].yaxis.set_major_formatter(lat_formatter)
    # ax[i].set_xlabel('Latitude', fontsize=8)# 
    # ax[i].set_ylabel('Longitude', fontsize=8)
    fname=FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=7)
    ax[i].legend(loc='upper left',markerscale=0.6,shadow=0,labelspacing=0.1,prop=fname)#{'family' : 'Times New Roman', 'size'   :8}
    ax[i].set_title(bh[i], fontsize=8,fontproperties=fname,loc='left')
    labels = ax[i].get_xticklabels() + ax[i].get_yticklabels()

    [label.set_fontproperties(FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=7)) for label in labels]



ax13=fig.add_axes([0.25,0.08,0.5,0.01])
cbar=fig.colorbar(c1,ax13,orientation='horizontal',shrink=0.8)

labels=cbar.ax.get_xticklabels()
# [label.set_fontname("/mnt/d/pythonjiaoben/font/Times.ttf") for label in labels]
[label.set_fontproperties(FontProperties(fname="/mnt/d/pythonjiaoben/font/Times.ttf", size=8)) for label in labels]
# plt.savefig('/mnt/d/OneDrive/论文程序实时更新版/积云对流方案对比/11.ps')
