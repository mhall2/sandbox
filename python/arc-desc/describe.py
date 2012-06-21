# Create a report with some layer information for a mxd file.
# Need to print out name, source name etc.
import sys, os, arcpy

def parseMXD(mxd):
  dataFrames = arcpy.mapping.ListDataFrames(mxd)
  out = {}
  for df in dataFrames:
    # print "dataframe =>" , df.name
    layers = arcpy.mapping.ListLayers(mxd, "", df)
    goodLayers = []
    for x in range(len(layers)):
      # discard group layers, it turns out that the 'leaf' layers will print  group1\group2\group3\feature etc.  that is nice....
      if not(layers[x].isGroupLayer):
        goodLayers.append(layers[x])
    out[df.name] = goodLayers
  return out
  
def main(args):
  # exit if the user did not provide the right number of args
  if len(args) <> 3:
    print "call the script passing in the following format ==> describe.py 'C:\your\mxd\here.mxd' 'c:\youroutput\here\out.csv'"
    sys.exit()
  fileName = args[1]
  outfile = args[2]
  print "REPORTING ON ====>" , fileName, "<===="
  
  # open the mxd.
  mxd = arcpy.mapping.MapDocument(fileName)
   
  # get the list of layers that we need to document. 
  # the layers are lists that are indexed by dataframe name.
  listing = parseMXD(mxd)
  
  print "WRITING TO ====>", outfile , "<===="
  file = open(outfile, 'w')
  
  # the output file will be .csv format containing the following information.
  file.write( "DataFrame,Order,GroupPrefix,LayerName,FeatureClassName,DataType,LayerType,Source,Location\n")
  for dataFrameKey in listing.keys():
    
    # 'x' is used as a counter for the report.
    x=1 
    for lyr in listing[dataFrameKey]:
      # set some variables used in the report.
      groupPrefix = ''  # any groups the layer is under seperated by '/'
      datasetName = ''  # layers datasetName if it is supported.
      serviceType = ''  # what kind of layer is this ShapeFile, SDE, etc.
      location = ''  # path to the file, or some kind of connection info, maybe a URL for the layer
      dspart = ''
      shapetype ='unknown'
      
      # longName for layers in a group looks like group1/group2/layer 
      # remove the '/layer' part.      
      if lyr.longName <> lyr.name:
        groupPrefix = lyr.longName[:0-(len(lyr.name) + 1)]
      
      if lyr.supports('datasetName'):
        datasetName = lyr.datasetName
      
      # try to determine the service type for layers that support serviceProperties.
      if lyr.supports('serviceProperties'):
        serviceType = lyr.serviceProperties['ServiceType']
        if serviceType == 'SDE':
          if len(lyr.serviceProperties['Database']) > 0:
            location = lyr.serviceProperties['Database'] +'@'+ lyr.serviceProperties['Server']
          else:
            location = lyr.serviceProperties['Server'] + ':' + lyr.serviceProperties['Service']
        else:
          location = lyr.serviceProperties['URL']
      
      # try to determine location for layers that support workspace path.
      ws = ''
      if lyr.supports('workspacePath'):
        ws = lyr.workspacePath
        if ws[-4:] == '.gdb':
          location = ws
          serviceType = 'FileGeoDatabase'
        if ws[-4:] == '.mdb':
          location = ws
          serviceType = 'PersonalGeoDatabase'
      
      # try to determine shape type and possibly location for layers that support dataSource
      if lyr.supports('dataSource'):
        dspart = lyr.dataSource
        if dspart[-4:] == '.shp':
          location = dspart
          serviceType = 'ShapeFile'
        # try to find shape Type for layer with valid datasource
        try:
          desc = arcpy.Describe(lyr.dataSource)
          #if desc.hasattr('datasettype'):
          #if desc.hasattr('dataType'):
          if hasattr(desc, 'shapeType'):
            shapeType = desc.shapeType
        except:
          print 'Failed to detect Shape, ?Broken DataSource for layer ', lyr.longName
          shapeType = 'unknown(broken data source)'
          
      # try to find something to use as location if one hasn't been set yet    
      if len(location) == 0:
        if len(dspart) > 0:
          location = dspart
          serviceType = 'UNKNOWN_DS'
        else:
          if len(ws) > 0:
            location = ws
            serviceType = 'UNKNOWN_WS'
      
      
      # report row structure
      output = []
      output.append(dataFrameKey)           # dataframe
      output.append(str(x))    # counter
      output.append(groupPrefix.replace(",", "_"))   # groupname group1/group2/etc.
      output.append(lyr.name.replace(",", "_"))     # layer display name (TOC)
      output.append(datasetName)   # layer data name
      output.append(shapeType)     # type of shape, if layer is not broken
      output.append(serviceType)   # shapefile, sde, etc.
      output.append('???')         # placeholder to fit in target output format.
      output.append(location)      # path to data
  
      file.write( ','.join(output) + '\n')
      x = x + 1
    
    # clean up  
    del mxd
    file.close()
    

main(sys.argv)



 
 
