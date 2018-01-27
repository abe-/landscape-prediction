# -*- coding: utf-8 -*--

import json
import random
from datetime import datetime
import numpy as np


# http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

def PixelsToLatLon(x, y, zoom):
	res = 180 / 256.0 / 2**zoom
	lat = x*res-180
	lon = y*res-90
	return lat, lon

def LatLonToPixels(lat, lon, zoom):
        "Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"
        res = 180 / 256.0 / 2**zoom
        x = (180 + lat) / res
        y = (90 + lon) / res
        return x, y


random.seed(datetime.now())

# Online tool to retrieve bbox lat/lon boundaries:
# http://bboxfinder.com

# mattogrosso
#lat0 = -14.721761
#lon0 = -59.677734
#lat1 = -10.033767
#lon1 = -54.371338

# ari1
#lat0 = -11.813588
#lon0 = -59.227295
#lat1 = -10.652510
#lon1 = -58.450012

# jiparana
lat0 = -12.576010
lon0 = -62.913208
lat1 = -8.939340
lon1 = -60.446777

key="ji"
zoom = 9

# coords transformed from EPSG:4326 (lat/lon) to EPSG:3857 (web mercator)

x0, y0 = LatLonToPixels(lat0, lon0, zoom)
x1, y1 = LatLonToPixels(lat1, lon1, zoom)

# we want to download tiles of 512x512 px

step = 512

# build the grid

x = np.arange(x0, x1, step)
y = np.arange(y0, y1, step)

print "Size of the grid: " + str(len(x)) + " x " + str(len(y)) 

data = []

iset = np.arange(len(x))
jset = np.arange(len(y))
np.random.shuffle(iset)
np.random.shuffle(jset)

for i in iset:
	for j in jset:
		centerx = x[i] + 256
		centery = y[j] + 256
		lat, lon = PixelsToLatLon(centerx, centery, zoom)
		point = {}
		point["id"] = key + "-" + "%03d" % (i,) + "-" + "%03d" % (j,)
		point["latitude"] = str(lat)
		point["longitude"] = str(lon)
		data.append(point)

with open("tmp.json", "w") as outfile:
	json.dump(data, outfile)


