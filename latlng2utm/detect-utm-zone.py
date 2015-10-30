''' Accepts a polygon shapefile in WGS84 and finds the UTM zone '''
# modified code from https://pcjericks.github.io/py-gdalogr-cookbook/
# vector_layers.html

from osgeo import ogr
import math
import argparse

PARSER = argparse.ArgumentParser()
PARSER.add_argument("filename", help="the path to the input shapefile")
ARGS = PARSER.parse_args()

# /Users/jbranigan/Documents/phila-city_limits_shp

def check_latlng(check_bbox):
    ''' Checks to see if the file coordinates are in lat/lng '''
    for i in check_bbox:
        if i < -180 or i > 180:
            failure('This file is already projected.')
    return True

def check_width(check_bbox):
    ''' Checsk to see if the bounding box fits in a UTM zone '''
    wide = check_bbox[1] - check_bbox[0]
    if wide > 3:
        failure('This file is too many degrees wide for UTM')
    return True

def get_zone(coord):
    ''' Finds the UTM zone of the coordinate '''
    # print 'zone function on ', coord
    # There are 60 longitudinal projection zones numbered 1 to 60 starting at 180W
    # So that's -180 = 1, -174 = 2, -168 = 3
    zone = ((coord - -180) / 6.0)
    return math.ceil(zone)

def get_bbox(shapefile):
    ''' Gets the bounding box of a shapefile input '''
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(shapefile, 0) # 0 means read, 1 means write
    # Check to see if shapefile is found.
    if data_source is None:
        print 'Could not open %s' % (shapefile)
    else:
        print 'Opened %s' % (shapefile)
        layer = data_source.GetLayer()
        shape_bbox = layer.GetExtent()
        return shape_bbox

def failure(why):
    ''' Quits the script with an exit message '''
    print why
    raise SystemExit

BBOX = get_bbox(ARGS.filename)
LATLNG = check_latlng(BBOX)
LNG_EXTENT = check_width(BBOX)

BBOX_CENTER = ((BBOX[1] - BBOX[0]) / 2) + BBOX[0]
UTMZONE = get_zone(BBOX_CENTER)
print 'The UTM zone is: %d' % UTMZONE
