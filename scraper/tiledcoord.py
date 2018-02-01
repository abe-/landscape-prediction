# -*- coding: utf-8 -*--

import json
import random
from datetime import datetime
import numpy as np
from settings import *

#
# Helper functions
#

# http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
# COORDS transformed from EPSG:4326 (lat/lon) to EPSG:3857 (web mercator)

def PixelsToLatLon(x, y, ZOOM):
	res = 180 / 256.0 / 2**ZOOM
	lon = x*res-180
	lat = y*res-90
	return lat, lon

def LatLonToPixels(lat, lon, ZOOM):
        "Converts lat/lon to pixel coordinates in given ZOOM of the EPSG:4326 pyramid"
        res = 180 / 256.0 / 2**ZOOM
        x = (180 + lon) / (res)
        y = (90 + lat) / res
        return x, y




#
# json producer
#

data = []
random.seed(datetime.now())

count = 0
for cds in COORDS:

    lat0, lon0, lat1, lon1 = cds[0], cds[1], cds[2], cds[3]

    x0, y0 = LatLonToPixels(lat0, lon0, ZOOM)
    x1, y1 = LatLonToPixels(lat1, lon1, ZOOM)

    # we want to download tiles of 512x512 px

    step = 512

    # build the grid

    x = np.arange(x0, x1, step)
    y = np.arange(y0, y1, step)

    print "Size of the grid: " + str(len(x)) + " x " + str(len(y)) + ". Tiles: " + str(len(x)*len(y))

    iset = np.arange(len(x))
    jset = np.arange(len(y))
    np.random.shuffle(iset)
    np.random.shuffle(jset)

    for i in iset:
        for j in jset:
                centerx = x[i] + 256
                centery = y[j] + 256
                lat, lon = PixelsToLatLon(centerx, centery, ZOOM)
                point = {}
                point["id"] = KEY + str(count) + "-" + "%03d" % (i,) + "-" + "%03d" % (j,)
                point["latitude"] = str(lat)
                point["longitude"] = str(lon)
                data.append(point)

    count = count + 1

print "Writing points to json file"
with open(KEY+".json", "w") as outfile:
	json.dump(data, outfile)
