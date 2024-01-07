;读取，画彩色散点图
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;散点图参考 http://www.ncl.ucar.edu/Applications/polyg.shtml polyg_8_lbar.ncl
;  ncl /mnt/d/job/code/by_ncl/shimian_dot.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"



; 一张图的色标图例 
undef("add_labelbar")
  procedure add_labelbar(wks,levels,colors)
  local lbres, labels
  begin
  nlevels = dimsizes(levels)
  ; Draw a labelbar
  lbres                    = True
  lbres@vpWidthF           = 0.5           ; width
  lbres@vpHeightF          = 0.06           ; height
  lbres@lbPerimOn          = False            ; Turn off perimeter.
  lbres@lbOrientation      = "Horizontal"     ; Default is vertical.
  lbres@lbLabelAlignment   = "InteriorEdges"  ; Default is "BoxCenters",标签如何与标签栏对齐
  lbres@lbFillColors       = colors           ; Colors for boxes.
  lbres@lbMonoFillPattern  = True             ; Fill them all solid.
  lbres@lbLabelFontHeightF = 0.02            ; label font height
  lbres@lbBoxLinesOn       =True
  lbres@lbBoxEndCapStyle   = "TriangleBothEnds"
  lbres@lbTitleString      ="(~S~o~N~C)"
  lbres@lbTitleFontHeightF = 0.02
  lbres@lbTitleJust        ="BottomRight"
  lbres@lbTitlePosition    ="Bottom"
  lbres@lbLabelStride      =1

  labels = sprintf("%2.1f",levels)

  gsn_labelbar_ndc(wks,nlevels+1,labels,0.25,0.15,lbres)
  frame(wks)                                   ; now advance the frame

  end


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

;-----------------------------main code------------------------------------
begin

  pic_dir = "/mnt/d/job/pic/tem_min/"

;--------------------读站点数据----------------------------------
  file_name="shimian_tem_min"
  filepath = "/mnt/d/job/data/"+file_name+".txt"  ;参数文件路径
  f       = asciiread(filepath,-1,"string")
  ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  lon     = stringtofloat(str_get_field(f(1:),3," ")) 
  lat     = stringtofloat(str_get_field(f(1:),4," ")) 
  pre     = stringtofloat(str_get_field(f(1:),6," ")) 
  npts    = numAsciiRow(filepath)-1 ;获取行数-站点数
  ;注意：这里的txt文件最后一行数据下面需要空白行，才能读出文件的正确行数
  ;大多数txt文件都满足要求，但还是需要核实一下
  ;设置缺测值
  pre@_FillValue = 32700.
  ; print(lon)

  ; 定义颜色 颜色设置
  levels = fspan(0, 13, 14)
  nlevels = dimsizes(levels)
  ; 掐头去尾 因为颜色太深
  cmap  = read_colormap_file("WhBlGrYeRe")
  id = ispan(10, 94,6)
  cmap1 = cmap(id,:)
  colors  = span_color_rgba(cmap1,nlevels+1)
  
; 1. 数据处理 散点画图
  num_distinct_markers = nlevels+1        ; number of distinct markers
  ref   = mark_lat_lon(num_distinct_markers,pre,levels,lat,lon,npts)
  lat_new_total=ref[0]
  lon_new_total=ref[1]



;===========================================================================
; Begin plotting section.
  wks = gsn_open_wks("eps",pic_dir+file_name)              ; send graphics to PNG file

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

  mpres                       =res
  mpres@mpMinLatF             = 28.8
  mpres@mpMaxLatF             = 29.8
  mpres@mpMinLonF             = 101.8
  mpres@mpMaxLonF             = 102.6
  mpres@pmTickMarkDisplayMode = "Always"
  ; mpres@gsnMajorLonSpacing    =1. 
  ; mpres@gsnMinorLonSpacing    =0.1   
  ; mpres@gsnMajorLatSpacing    =1. 
  ; mpres@gsnMinorLatSpacing    =0.1

  mpres@mpFillOn = False
  mpres@mpDataBaseVersion       = "MediumRes"
  mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
  mpres@mpOutlineSpecifiers     = (/"China:states"/)
  ;边界线
  ; mpres@mpOutlineBoundarySets   = "National"


;-----------------------------绘制散点图-------

  map = gsn_csm_map(wks,mpres)
  plot_rain_scatter(wks,colors,num_distinct_markers,lat_new_total,\
                    lon_new_total,map)


;轮廓线
  shp_line = "/mnt/d/ChinaMap/China_counties/counties_china.shp" 
  lnres                  = True     
  lnres@gsLineColor      ="black"
  lnres@gsLineThicknessF = 4.0           
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,\
                                                       lnres)


draw(map)

;色标图例
add_labelbar(wks,levels,colors) 
; frame(wks)
end     
 


 

