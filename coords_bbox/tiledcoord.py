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

# yuzhni island (Russia)(1)
#lat0,lon0,lat1,lon1=[71.635993,53.162842,73.131322,55.458984]
#zoom = 10
#key="yu"

# yuzhni island (Russia)(2)
#lat0,lon0,lat1,lon1=[73.201317,54.843750,74.116047,56.997070]
#key="yu1"
#zoom=10

# yu2
lat0,lon0,lat1,lon1=[74.132576,55.728149,74.849236,59.891968]
key="yu2"
zoom=10

# yu3
lat0,lon0,lat1,lon1=[74.873624,56.343384,75.336721,60.842285]
key="yu3"
zoom=10

# jiparana
#lat0,lon0,lat1,lon1=[-12.343831,-62.641296,-10.734638,-61.042786]
#zoom = 11
#key = "ji"

# crops
#39.056111,-98.536389,39.156111,-98.436389
#lat0,lon0,lat1,lon1=[38.975425,-99.091187,39.757880,-97.800293]
#key="crops"
#zoom = 13

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


