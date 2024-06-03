import ogr
shp = ogr.Open('comuni_join.shp')
'''There are 110 provincia'''
prov_ids = range(1,111)
drv = ogr.GetDriverByName('ESRI Shapefile')
srs = ogr.osr.SpatialReference()
srs.ImportFromEPSG(4326)
srs.MorphToESRI()  
for prov in prov_ids:
    lyr = shp.GetLayer()
    prov = str(prov)
    lyr.SetAttributeFilter("comuni_4_2 = '%s'" %(prov))
    output_file = "comuni_%s.shp" %(prov)
    output_shp = drv.CreateDataSource(output_file)
    outlyr = output_shp.CopyLayer(lyr, 'comuni_%s' %(prov)) 
    file = open("comuni_%s.prj" %(prov), 'w')   
    file.write(srs.ExportToWkt())   
    file.close() 
    del lyr, output_file, outlyr, output_shp