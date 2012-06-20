#Print out some layer information for a mxd file.
#Need to print out name, source name etc.

import os, arcpy

filename = r"C:\Users\matthew.hall\Desktop\Test_StationFeatures.mxd"

mxd = arcpy.mapping.MapDocument(filename)


def describe(layer):
  if layer.supports('datasource'):
    return layer.name + "," +  layer.dataSource
  else:
    return layer.name + ","+  '-> does not support datasource'


for df in arcpy.mapping.ListDataFrames(mxd):
  print "DATA_FRAME[" , df.name , "]"
  for lyr in arcpy.mapping.ListLayers(mxd, "", df):
    #check for group layer
    
    if lyr.isGroupLayer:
      print 'GROUP_Layer[' + lyr.name + ']', len(arcpy.mapping.ListLayers(lyr))
      
    else:
      s = describe(lyr)
      print s
  
    
 #   print lyr.name
 #   if lyr.supports('dataSource'):
 #     print lyr.dataSource
 #   else:
 #     print "layer does not support datasource"
