; 填色 散点（色点 和 圆圈）叠加
; 利用shp 识别散点是否在shp内 以及mask格点数据
;注意 色标图例函数 undef("add_labelbar") 放在这个代码文件里会导致画不了填色
; 所以就用填色色标图例就好啦 ，反正都设置的同样色卡如果担心散点和填色的色标不一致
; 就单独运行 qionglai_dot.ncl 看一下 我看过了 一致的
;  ncl /mnt/d/job/code/by_ncl/zitong_spa.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "/mnt/d/job/code/by_ncl/shapefile_utils.ncl"


;根据降水量将经纬度数组分类
undef("mark_lat_lon")
  function mark_lat_lon(num_distinct_markers,R,levels,lat,lon,npts)
  local num_distinct_markers,R,levels,lat,lon,npts,i,indexes,\
  npts_range,lat_new,lon_new
  ; Create X and Y arrays to hold the points for each range and initialize
  ; them to missing values.  We want to use num_distinct_markers
  ; different colors, so we need num_distinct_markers sets of X and
  ; Y points.
  begin
  ; Group the points according to which range they fall in. At the
  ; same time, create the label that we will use later in the labelbar  
  lat_new = new((/num_distinct_markers,npts/),float,-999);设置成二维，标记*站点数
  lon_new = new((/num_distinct_markers,npts/),float,-999)
  do i = 0, num_distinct_markers-1
    if (i.eq.0) then ;第一个范围
      indexes = ind(R.lt.levels(0)) ;定位，且小于第一个level的点会画出来
    end if
    if (i.eq.num_distinct_markers-1) then ;最后一个范围
      indexes = ind(R.ge.max(levels))
    end if
    if (i.gt.0.and.i.lt.num_distinct_markers-1) then    ;中间的范围，因为格式不一样，要分别设置
      indexes = ind(R.ge.levels(i-1).and.R.lt.levels(i))
    end if
   ; Now that we have the set of indexes whose values fall within 
   ; the given range, take the corresponding lat/lon values and store
   ; them, so later we can color this set of markers with the appropriate color.
    if (.not.any(ismissing(indexes))) then 
      npts_range = dimsizes(indexes)   ; # of points in this range.
      lat_new(i,0:npts_range-1) = lat(indexes)
      lon_new(i,0:npts_range-1) = lon(indexes)
    end if
    delete(indexes)            ; Necessary b/c "indexes" may be a different
    ; size next time.
  end do

  return([/lat_new,lon_new/])
 end

undef("plot_rain_scatter")
  procedure plot_rain_scatter(wks,colors,num_distinct_markers,\
                        lat_new,lon_new,mapplot)
  local i,gsres,pmid
  begin
  pmid = new(num_distinct_markers,graphic)
  gsres               = True
  gsres@gsMarkerIndex = 16 ;
  gsres@gsMarkerSizeF      = 0.012
  gsres@gsMarkerThicknessF = 2 
  do i = 0, num_distinct_markers-1
    if (.not.ismissing(lat_new(i,0)))
      gsres@gsMarkerColor      = colors(i,:)
      pmid(i) = gsn_add_polymarker(wks,mapplot,lon_new(i,:),lat_new(i,:),gsres)      
    end if
  end do
  mapplot@$unique_string("pmid")$ = pmid
  end


; 画显著性
undef("plot_sig_scatter")
  procedure plot_sig_scatter(wks,lat_new,lon_new,map)
  local gsres,pmid
  begin

  gsres               = True
  gsres@gsMarkerThicknessF = 2 
  gsres@gsMarkerColor  = "black"
  gsres@gsMarkerIndex  = 4
  gsres@gsMarkerSizeF  = 0.012
  pmid = gsn_add_polymarker(wks,map,lon_new,lat_new,gsres)      
  map@$unique_string("pmid")$ = pmid
  end

;-----------------------------main code------------------------------------
begin

  county = "zitong"
  pic_dir = "/mnt/d/job/pic/"+county+"/ncl/"

; ;--------------------读站点数据----------------------------------
  var = (/"tem_min","tem_max","tem_avg","prcp","pres","RH","wind"/)

  do j = 0,6
  ; j = 4
  plot_district = (/104.8,105.6,31.3,32./)

  file_name := county + "_"+var(j)
  filepath := "/mnt/d/job/data/deal/"+file_name+".txt"  ;参数文件路径
  f       := asciiread(filepath,-1,"string")
  ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  lon     := stringtofloat(str_get_field(f(1:),3," ")) 
  lat     := stringtofloat(str_get_field(f(1:),4," ")) 
  pre_old := stringtofloat(str_get_field(f(1:),6," ")) 
  npts    := numAsciiRow(filepath)-1 ;获取行数-站点数
  ;注意：这里的txt文件最后一行数据下面需要空白行，才能读出文件的正确行数
  ;大多数txt文件都满足要求，但还是需要核实一下
  ;设置缺测值
  pre_old@_FillValue := 32700.

  ;---Open shapefile and read Mississippi River Basin lat/lon values.
  f1      = addfile("/mnt/d/ChinaMap/"+county+"/"+county+".shp", "r")
  mrb_lon = f1->x
  mrb_lat = f1->y
  ;---Start with data all missing
  pre := new(dimsizes(pre_old),typeof(pre_old),pre_old@_FillValue)
  do i=0,npts-1
    pre(i) = where(gc_inout(lat(i),lon(i),mrb_lat,mrb_lon), pre_old(i),pre_old@_FillValue)
  end do


;2. 数据处理 空间分布插值

  ;创建存放插值后生成数据的数组 在北纬0-50，东经70-130这个矩形框内插值
  nlons = toint((plot_district(1)-plot_district(0))/0.005)+1
  nlats = toint((plot_district(3)-plot_district(2))/0.005)+1
  olon = new(nlons,"float");
  olat = new(nlats,"float");
  data = new((/nlats,nlons/),"float")
  olon = fspan(plot_district(0), plot_district(1), nlons)
  olat = fspan(plot_district(2), plot_district(3), nlats)

  ;设置数组属性，为了符合netcdf规定的数据格式，使函数能够识别经纬度
  olon!0          = "lon"
  olon@long_name  = "lon"
  olon@units      = "degrees_east"
  olon&lon        = olon
  olat!0          = "lat"
  olat@long_name  = "lat"
  olat@units      = "degrees_north"
  olat&lat        = olat

  ;调用插值函数
  ; rscan = (/2,1,0.1/)   ;连续的有效半径大小，最大为10，依次递减
  rscan = (/2,1,0.2/)   ; j=4 开始 其实123也还行
 
  data  := obj_anal_ic_Wrap(lon,lat,pre,olon,olat,rscan, False)  ;Cressman插值


  ; mask掉区域以外的pw
  shp_filename  := "/mnt/d/ChinaMap/"+county+"/"+county+".shp" 
  mask1 := new(dimsizes(data),typeof(data),data@_FillValue)
  mask1 := shapefile_mask_data(data,shp_filename,True) 


  ; 定义色板间隔 设置颜色
  nlevels =  50
  levels = fspan(min(mask1), max(mask1), nlevels)
  ; 掐头去尾 因为颜色太深
  cmap  = read_colormap_file("wh-bl-gr-ye-re")
  interval = 160/nlevels
  id = ispan(20, 180, interval)
  cmap1 = cmap(id,:)
  colors  = span_color_rgba(cmap1,nlevels+1)


;===========================================================================
; Begin plotting section.
  wks = gsn_open_wks("eps",pic_dir+ county +tostring(j)+ "_"+\
                     var(j) + "_spa_mask")         

;---Set up some map resources.
  res                       = True
  ; res@gsnMaximize           = True             ; Maximize plot in frame.
  res@gsnDraw               = False            ; Will draw later
  res@gsnFrame              = False            ; Don't advance the frame
  res@gsnLeftString         = ""
  res@gsnRightString        = ""
  res@tmYROn                = False
  res@tmXTOn                = False
  ; res@gsnAddCyclic          = False
  ; res@tmEqualizeXYSizes     =True
  res@tmXBLabelFontHeightF  = 0.02
  ; res@gsnLeftString         ="P"+type
  ; res@gsnLeftStringFontHeightF=0.024
  ; res@gsnLeftStringOrthogonalPosF=0.024

  mpres                         =res
  mpres@mpMinLatF             = plot_district(2)
  mpres@mpMaxLatF             = plot_district(3)
  mpres@mpMinLonF             = plot_district(0)
  mpres@mpMaxLonF             = plot_district(1)

  ; mpres@mpMinLatF            = 25
  ; mpres@mpMaxLatF             = 40
  ; mpres@mpMinLonF             = 95
  ; mpres@mpMaxLonF             = 105
  mpres@pmTickMarkDisplayMode = "Always"
  ; mpres@gsnMajorLonSpacing    =1. 
  ; mpres@gsnMinorLonSpacing    =0.1   
  ; mpres@gsnMajorLatSpacing    =1. 
  ; mpres@gsnMinorLatSpacing    =0.1

  mpres@mpFillOn = False
  ; mpres@mpDataBaseVersion       = "MediumRes"
  ; mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
  ; mpres@mpOutlineSpecifiers     = (/"China:states"/)
  ;边界线
  ; mpres@mpOutlineBoundarySets   = "National"


  ;画等值线图
  temres = res
  temres@cnFillOn = True  ;cn means ContourPlot
  temres@cnLinesOn =   False

  ; temres@cnFillPalette = "WhBlGrYeRe" ;不需要了
  temres@cnLevelSelectionMode ="ExplicitLevels" 
  temres@cnLevels      = levels
  temres@cnFillColors  = colors
  ; temres@cnLevelSelectionMode = "ManualLevels" 
  ; temres@cnLevelSpacingF = 1

  temres@lbBoxLinesOn = False ; Label bar
  temres@lbLabelAutoStride     = True            ; let NCL determine label spacing
  temres@lbOrientation        = "Vertical"         ; vertical label bar 
  temres@pmLabelBarWidthF = 0.05     ;色标变窄
  ;temres@pmLabelBarHeightF = 0.02    ;色标变细
  temres@lbBoxEndCapStyle = "TriangleBothEnds"
  units = (/"(~S~o~N~C)","(~S~o~N~C)","(~S~o~N~C)","(mm)","(hPa)",\
           "(%)","(m/s)"/)
  temres@lbTitleString = units(j)
  temres@lbTitleJust        ="TopRight"
  temres@lbTitlePosition    ="Bottom"
  ; temres@cnLineLabelFormat ="3.3f" ;0@;*.2f
  temres@cnLineLabelFormat ="0@;*.2f" ;


;-----------------------------绘制填色图-------

  mask1 := smth9_Wrap(mask1,0.5,0.25,False)
  map := gsn_csm_map(wks,mpres)
  plot := gsn_csm_contour(wks,mask1,temres) 
  overlay(map,plot)


  ; -----------------------绘制散点图----------------------------------
  num_distinct_markers := nlevels+1        ; number of distinct markers
  ref   := mark_lat_lon(num_distinct_markers,pre,levels,lat,lon,npts)
  lat_new_total := ref[0]
  lon_new_total:= ref[1]

  plot_rain_scatter(wks,colors,num_distinct_markers,lat_new_total,\
                    lon_new_total,map)
  ; plot_sig_scatter(wks,lat,lon,map)


;轮廓线

  shp_line = "/mnt/d/ChinaMap/"+county+"/"+county+".shp" 
  lnres                  = True     
  lnres@gsLineColor      ="black"
  lnres@gsLineThicknessF = 4.0           
  shp_plot               := gsn_add_shapefile_polylines(wks,map,shp_line,\
                                                       lnres)


draw(map)
end do

end     
 
