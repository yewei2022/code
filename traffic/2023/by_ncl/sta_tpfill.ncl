;绘制高原站点位置和高原地形填图
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;散点图参考 http://www.ncl.ucar.edu/Applications/polyg.shtml polyg_8_lbar.ncl
;  ncl /mnt/d/YEWEI/project/traffic/code/by_ncl/sta_tpfill.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "//mnt/d/YEWEI/project/traffic/code/by_ncl/shapefile_utils.ncl"



begin

  filepath = "/mnt/d/YEWEI/project/traffic/data/"  ;参数文件路径
  name="sta_info"
  pic_path="/mnt/d/YEWEI/project/traffic/pic/"
  f       = asciiread(filepath+name+".txt",-1,"string")
  ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  lon     = stringtofloat(str_get_field(f(1:),5,",")) 
  lat     = stringtofloat(str_get_field(f(1:),4,",")) 
  npts = numAsciiRow(filepath+name+".txt")-1 ;获取行数-1=站点数

;读地形文件
  topo        = addfile("/mnt/d/YEWEI/project/traffic/data/ETOPO2v2c_f4.nc", "r")
  elev        = topo->z({24:35},{96:110}) 
  ; printVarSummary(elev)
  ; exit 
  lon_topo    = topo->x({96:110}) 
  lat_topo    = topo->y({24:35}) 
  lat_topo!0     = "lat"
  lon_topo!0     = "lon"
  lat_topo@units = "degrees_north"
  lon_topo@units = "degrees_east"
  lat_topo&lat   = lat_topo
  lon_topo&lon   = lon_topo

  ;---Attach the coordinate arrays
  elev!0    = "lat"
  elev!1    = "lon"
  elev&lat  = lat_topo
  elev&lon  = lon_topo

  polyshp  = filepath +"shp/province.shp" 
  elev_mask1 = new(dimsizes(elev),typeof(elev),elev@_FillValue) ;用于后面mask高原以外
  elev_mask1 =shapefile_mask_data(elev,polyshp,True) 

;===========================================================================
; Begin plotting section.
  wks = gsn_open_wks("eps",pic_path + "sta_tpfill")              ; send graphics to PNG file

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
  mpres@mpMinLatF             = 25.
  mpres@mpMaxLatF             = 35.
  mpres@mpMinLonF             = 97
  mpres@mpMaxLonF             = 109
  mpres@gsnMajorLonSpacing    =5. 
  mpres@gsnMinorLonSpacing    =1.    
  mpres@gsnMajorLatSpacing    =5. 
  mpres@gsnMinorLatSpacing    =1

  mpres@mpFillOn=False
  mpres@mpDataBaseVersion       = "MediumRes"
  mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
  ; mpres@mpOutlineSpecifiers     = (/"China:states"/)
  ; ;边界线
  ; mpres@mpOutlineBoundarySets   = "National"
  ; mpres@mpNationalLineColor     = "black"
  ; mpres@mpProvincialLineColor   = "black"
  ; mpres@mpGeophysicalLineColor  = "black"
  ; mpres@mpNationalLineThicknessF  =2.5
  ; mpres@mpProvincialLineThicknessF  =2.5
  ; mpres@mpGeophysicalLineThicknessF = 2.5



  ;---高原地形填图
  topores                    = res
  topores@cnFillOn           = True             ; turn off contour fill
  topores@cnFillPalette      = "OceanLakeLandSnow" ;topo_15lev OceanLakeLandSnow MPL_Greys
  topores@cnLinesOn          = False
  topores@cnLevelSelectionMode="ManualLevels" 
  topores@cnLevelSpacingF    = 250
  topores@cnMinLevelValF     = 0
  topores@cnMaxLevelValF     =5000            
  topores@cnFillMode         = "RasterFill"     ; much faster than AreaFill
  topores@lbBoxLinesOn       = True ; Label bar
  ; topores@lbLabelAutoStride  = True            ; let NCL determine label spacing
  topores@lbLabelStride  = 2            ; let NCL determine label spacing

  topores@cnLineLabelsOn     = False            ; turn off line labels
  topores@cnInfoLabelOn      = False            ; turn off info label
  topores@pmLabelBarHeightF  = 0.12
  topores@lbBoxEndCapStyle   ="TriangleBothEnds"
  topores@pmLabelBarOrthogonalPosF  = 0.1 ;色标离图的距离
  topores@lbTitleString                  ="elevation(m)"
  topores@lbTitleJust                    ="BottomRight"
  topores@lbTitlePosition                ="Bottom"
  topores@lbLabelFontHeightF = 0.01
  topores@lbTitleFontHeightF = 0.01


;绘制地形图
  map = gsn_csm_map(wks,mpres)
  topo_plot = gsn_csm_contour(wks,elev_mask1,topores)
  overlay(map, topo_plot)

  ;高原轮廓线
  shp_line = filepath +"shp/city.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="black"
  lnres@gsLineThicknessF = 3.0           ; 6x thickness 
  plot_topoline = gsn_add_shapefile_polylines(wks,map,shp_line,lnres) 

; 绘制散点
  gsres               = True
  gsres@gsMarkerIndex = 16
  gsres@gsMarkerSizeF      = 0.005  
  gsres@gsMarkerColor      = "red"
  gsres@gsMarkerThicknessF = 2.0
  pmid = gsn_add_polymarker(wks,map,lon,lat,gsres)      

  ; ;公路 
  ; lnres                  = True     
  ; lnres@gsLineColor      ="Blue"
  ; lnres@gsLineThicknessF = 6.0           ; 6x thickness 
  ; plot_road = new(4,graphic)
  ; road = (/"G42","G65","G75","G76"/)
  ; do i = 0,3
  ; shp_line1 := filepath +"road_each/"+ road(i) +"/"+road(i) +".shp" 
  ; print(shp_line1)
  ; plot_road(i) = gsn_add_shapefile_polylines(wks,map,shp_line1,lnres)
  ; end do 


draw(map)
frame(wks)

end     
 


 

