# -*- coding: utf-8 -*--

import json
import random
from datetime import datetime
import numpy as np

random.seed(datetime.now())

# Online tool to retrieve bbox lat/lon boundaries:
# http://bboxfinder.com

lat0 = -11.813588
lon0 = -59.227295
lat1 = -10.652510
lon1 = -58.450012

# num of points

npoints = 300

data = []

for i in range(npoints):
	lat = np.random.uniform(lat0, lat1)
	lon = np.random.uniform(lon1, lon0)
	point = {}
	point["id"] = str(i+480)
	point["latitude"] = str(lat)
	point["longitude"] = str(lon)
	data.append(point)

with open("tmp.json", "w") as outfile:
	json.dump(data, outfile)

