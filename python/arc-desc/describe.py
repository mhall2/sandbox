#Print out some layer information for a mxd file.
#Need to print out name, source name etc.

import sys, os, arcpy

def parseMXD(mxd):
  dataFrames = arcpy.mapping.ListDataFrames(mxd)
  out = {}
  for df in dataFrames:
    #print "dataframe =>" , df.name
    layers = arcpy.mapping.ListLayers(mxd, "", df)
    goodLayers = []
    for x in range(len(layers)):
      #discard group layers, it turns out that the 'leaf' layers will print  group1\group2\group3\feature etc.  that is nice....
      if not(layers[x].isGroupLayer):
        goodLayers.append(layers[x])
    out[df.name] = goodLayers
  return out
  
def main(args):
  #exit if the user did not provide a file to look at.
  if len(args) <= 1:
    print "pass in the path to the .mxd file to report on."
    sys.exit()
  fileName = args[1]
  #print "REPORTING ON ====>" , fileName, "<===="
  #open the mxd.
  mxd = arcpy.mapping.MapDocument(fileName)
  listing = parseMXD(mxd)
  
  #format the output to console for now alot of this stuff needs to be moved around.
  #creates a csv style output that can be piped and opend in excel
  print "DataFrame,Order,GroupPrefix,LayerName,FeatureClassName,DataType,LayerType,Source,Location"
  for key in listing.keys():
    for x in range(len(listing[key])):
      lyr = listing[key][x]
      #print lyr.longName, lyr.name
      groupPrefix = ''
      if lyr.longName <> lyr.name:
        # group name looks like group1/group2/layer slice the string to remove the '/layer' part
        groupPrefix = lyr.longName[0:len(lyr.longName) - (len(lyr.name) + 1)]
      datasetName = ''
      if lyr.supports('datasetName'):
        datasetName = lyr.datasetName
      #determine the service type.. SDE , WMS, ShapeFile etc.
      serviceType = ''
      location = ''
      if lyr.supports('serviceProperties'):
        serviceType = lyr.serviceProperties['ServiceType']
        if serviceType == 'SDE':
          location = lyr.serviceProperties['Database'] +'@'+ lyr.serviceProperties['Server'] 
        else:
          location = lyr.serviceProperties['URL']
      dspart = ''
      if lyr.supports('dataSource'):
        dspart = lyr.dataSource
      ws = ''
      if lyr.supports('workspacePath'):
        ws = lyr.workspacePath
      #determine if a shapefile/filegeodb/pgdb is used.
      if len(dspart) > 4:
        if dspart[-4:] == '.shp':
          location = dspart
          serviceType = 'ShapeFile'
      if len(ws) > 4:
        if ws[-4:] == '.gdb':
          location = ws
          serviceType = 'FileGeoDatabase'
      if len(ws) > 4:
        if ws[-4:] == '.mdb':
          location = ws
          serviceType = 'PersonalGeoDatabase'
      
      shapeType = 'UNKNOWN!'
      if len(dspart) > 0:    
        desc = arcpy.Describe(dspart)
        if hasattr(desc, 'shapeType'):
          shapeType = desc.shapeType
      print key + ','+ str(x+1) + ','+ groupPrefix + ','+ lyr.name + ',' + datasetName + ',' + shapeType + ',' + serviceType + ',' + '???' + ',' + location


main(sys.argv)



 
 
