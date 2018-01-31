# -*- coding: utf-8 -*--

import json
import random
from datetime import datetime
import numpy as np

# Online tool to retrieve bbox lat/lon boundaries:
# 
#           DON'T FORGET TO CHOOSE THE 
#      CORRECT ORDER OF COORDINATES Lat/Lng 
#   (corner at the bottom right of the window)
#
# http://bboxfinder.com

coords = []


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
#zoom = 8
#key="ice0"

# yuzhni island (Russia)(2)
#lat0,lon0,lat1,lon1=[73.201317,54.843750,74.116047,56.997070]
#key="ice1"
#zoom=8

# yu2
#lat0,lon0,lat1,lon1=[74.132576,55.728149,74.849236,59.891968]
#key="ice2"
#zoom=8

# yu3
#lat0,lon0,lat1,lon1=[74.873624,56.343384,75.336721,60.842285]
#key="ice3"
#zoom=8

#yu + groed
#key="ice"
#zoom=8
#coords.append( [71.635993,53.162842,73.131322,55.458984]  )
#coords.append( [73.201317,54.843750,74.116047,56.997070]  )
#coords.append( [74.132576,55.728149,74.849236,59.891968]  )
#coords.append( [74.873624,56.343384,75.336721,60.842285] )
#coords.append( [69.710489,-29.003906,74.164085,-21.093750] )
#coords.append( [74.188052,-23.071289,77.851100,-18.105469] )
#coords.append( [63.074866,-53.876953,68.942607,-47.548828] )
#coords.append( [68.997802,-55.942383,72.154890,-49.614258] )
#coords.append( [68.366801,-70.971680,70.801366,-67.170410] )
#coords.append( [70.510241,-73.366699,71.667119,-70.400391] )
#coords.append( [71.052665,-76.245117,72.143102,-73.108521] )
#coords.append( [71.732662,-78.332520,72.711903,-74.904785] )

# jiparana
#lat0,lon0,lat1,lon1=[-12.343831,-62.641296,-10.734638,-61.042786]
#zoom = 11
#key = "ji"

# crops
#39.056111,-98.536389,39.156111,-98.436389
#lat0,lon0,lat1,lon1=[38.975425,-99.091187,39.757880,-97.800293]
#key="crops"
#zoom = 12.2

# edson, kansas (irrigation agriculture)
coords.append( [ 40.165757,-101.698380,40.239178,-101.553497 ] )
zoom = 12.2
key = "edson"


# Max zoom in Earth Engine:

zoom = min(zoom, 12.2)

# helper functions
# http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
# coords transformed from EPSG:4326 (lat/lon) to EPSG:3857 (web mercator)

def PixelsToLatLon(x, y, zoom):
	res = 180 / 256.0 / 2**zoom
	lon = x*res-180
	lat = y*res-90
	return lat, lon

def LatLonToPixels(lat, lon, zoom):
        "Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"
        res = 180 / 256.0 / 2**zoom
        x = (180 + lon) / (res)
        y = (90 + lat) / res
        return x, y






# json producer


data = []
random.seed(datetime.now())

count = 0
for cds in coords:

    lat0, lon0, lat1, lon1 = cds[0], cds[1], cds[2], cds[3]

    x0, y0 = LatLonToPixels(lat0, lon0, zoom)
    x1, y1 = LatLonToPixels(lat1, lon1, zoom)

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
                lat, lon = PixelsToLatLon(centerx, centery, zoom)
                point = {}
                point["id"] = key + str(count) + "-" + "%03d" % (i,) + "-" + "%03d" % (j,)
                point["latitude"] = str(lat)
                point["longitude"] = str(lon)
                data.append(point)
                
    count = count + 1


with open(key+".json", "w") as outfile:
	json.dump(data, outfile)


