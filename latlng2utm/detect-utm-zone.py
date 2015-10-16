# modified code from https://pcjericks.github.io/py-gdalogr-cookbook/
# vector_layers.html

import os
from osgeo import ogr
from sys import argv
import math

script, daShapefile = argv

# /Users/jbranigan/Documents/phila-city_limits_shp

def check_latlng(bbox):
    for i in bbox:
        if i < -180 or i > 180:
            failure('This file is already projected.')
        
def check_width(bbox):
    width = bbox[1] - bbox[0]
    if width > 3:
        failure('This file is too many degrees wide for UTM')

def get_zone(coord):
    # print 'zone function on ', coord
    # There are 60 longitudinal projection zones numbered 1 to 60 starting at 180W
    # So that's -180 = 1, -174 = 2, -168 = 3
    zone = ((coord - -180) / 6.0)
    return math.ceil(zone)

def get_bbox(daShapefile):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    dataSource = driver.Open(daShapefile, 0) # 0 means read, 1 means write
    
    # Check to see if shapefile is found.
    if dataSource is None:
        print 'Could not open %s' % (daShapefile)
    else:
        print 'Opened %s' % (daShapefile)
        layer = dataSource.GetLayer()
        bbox = layer.GetExtent()
        return bbox
        
def failure(why):
    print why
    raise SystemExit

bbox = get_bbox(daShapefile)
latlng = check_latlng(bbox)
width = check_width(bbox)

bbox_center = ((bbox[1] - bbox[0]) / 2) + bbox[0]
utmzone = get_zone(bbox_center)
print 'The UTM zone is: %d' % utmzone