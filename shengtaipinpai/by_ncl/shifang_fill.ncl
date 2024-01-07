;绘制高原站点位置和高原地形填图
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;散点图参考 http://www.ncl.ucar.edu/Applications/polyg.shtml polyg_8_lbar.ncl
;  ncl /mnt/d/job/code/by_ncl/shifang_fill.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "/mnt/d/job/code/by_ncl/shapefile_utils.ncl"



begin

  name="shifang"
  plot_district = (/103.7,104.4,30.9,31.7/)
  pic_path="/mnt/d/job/pic/"+name+"/"
  ; filepath = "/mnt/d/job/data/"  ;参数文件路径
  ; f       = asciiread(filepath+name+".txt",-1,"string")
  ; ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  ; lon     = stringtofloat(str_get_field(f(1:),2," ")) 
  ; lat     = stringtofloat(str_get_field(f(1:),3," ")) 
  ; npts = numAsciiRow(filepath+name+".txt")-1 ;获取行数-1=站点数


;读地形文件
  topo_path="/mnt/d/ChinaMap/ETOPO_2022_v1_15s_N45E090_surface.nc"
  topo     = addfile(topo_path, "r")
  elev     = topo->z({plot_district(2):plot_district(3)},{plot_district(0):plot_district(1)}) 

  ; mask掉区域以外的pw
  shp_filename  = "/mnt/d/ChinaMap/"+name+"/"+name+".shp"
  mask1 = new(dimsizes(elev),typeof(elev),elev@_FillValue)
  mask1 = shapefile_mask_data(elev,shp_filename,True)
  print(min(mask1))
  print(max(mask1))


;=======================================================================
; Begin plotting section.
  wks = gsn_open_wks("eps",pic_path + name+"_topo")              

;---Set up some map resources.
  res                       = True
  ; res@gsnMaximize           = True             ; Maximize plot in frame.
  res@gsnDraw               = False            ; Will draw later
  res@gsnFrame              = False            ; Don't advance the frame
  res@gsnLeftString         = ""
  res@gsnRightString        = ""
  res@tmYROn                =False
  res@tmXTOn                =False

  ; res@vpWidthF=1.0
  ; res@vpHeightF=0.6

  ;-----------地图属性-----------------
  mpres                       =res
  mpres@mpMinLatF             = plot_district(2)
  mpres@mpMaxLatF             = plot_district(3)
  mpres@mpMinLonF             = plot_district(0)
  mpres@mpMaxLonF             = plot_district(1)
  mpres@pmTickMarkDisplayMode = "Always"
  mpres@mpFillOn =False


  ;---地形填图
  topores                    = res
  topores@cnFillOn           = True             ; turn off contour fill

    ; 掐头去尾 因为颜色太深
  cmap  = read_colormap_file("cmocean_gray")
  id = ispan(0, 255, 1)
  cmap1 = cmap(id(::-1),:)
  colors  = span_color_rgba(cmap1,256)
  topores@cnFillPalette      = colors
  topores@cnLinesOn          = False
  topores@cnLevelSelectionMode="ManualLevels" 
  topores@cnLevelSpacingF    = 25
  topores@cnMinLevelValF     = 400
  topores@cnMaxLevelValF     = 4500           
  ; topores@cnFillMode         = "RasterFill"     ; much faster than AreaFill
  topores@lbBoxLinesOn       = False ; Label bar
  ; topores@lbLabelAutoStride  = True            
  topores@lbLabelStride  = 2            

  topores@cnLineLabelsOn     = False            ; turn off line labels
  topores@cnInfoLabelOn      = False            ; turn off info label
  topores@pmLabelBarHeightF  = 0.12
  ; topores@lbBoxEndCapStyle   ="TriangleBothEnds"
  topores@pmLabelBarOrthogonalPosF  = 0.015 ;色标离图的距离
  topores@pmLabelBarParallelPosF  = 0.51

  topores@lbTitleString                  ="(m)"
  topores@lbTitleJust                    ="BottomRight"
  topores@lbTitlePosition                ="Bottom"
  topores@lbLabelFontHeightF = 0.012
  topores@lbTitleFontHeightF = 0.015


;绘制地地形图
  map = gsn_csm_map(wks,mpres)
  topo_plot = gsn_csm_contour(wks,mask1,topores)
  overlay(map, topo_plot)

  ;轮廓线
  shp_line = "/mnt/d/ChinaMap/"+name+"/"+name+".shp"
  lnres                  = True     
  lnres@gsLineColor      ="black"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness 
  plot_topoline= gsn_add_shapefile_polylines(wks,map,shp_line,lnres) 

; ; 绘制散点
;   gsres               = True
;   gsres@gsMarkerIndex = 4
;   gsres@gsMarkerSizeF      = 0.012  
;   gsres@gsMarkerColor      = "black"
;   gsres@gsMarkerThicknessF = 3.0
;   pmid = gsn_add_polymarker(wks,map,lon,lat,gsres)      


draw(map)
frame(wks)
end     
 
