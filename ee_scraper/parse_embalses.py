import csv
import json
from pyproj import Proj, transform

# Spanish SNCZI database comes with EPSG:25830 coords
# http://sig.mapama.es/snczi/ayuda/intro.html
inProj = Proj( init='epsg:25830' )

# Google EarthEngine urls need WSG84 EPSG:4326 (GPS) coords
outProj = Proj( init='epsg:4326' )

# Data to be written in the json file
data=[]

with open("embalses.csv", "r") as f:
    reader = csv.reader(f)
    count = 0
    for row in reader:
        if count > 0:
            x = int(row[9])
            y = int(row[10])
            lon,lat=transform( inProj, outProj, x, y)
           
            surface = int(row[14].replace(',', ''))
            
            if surface > 35000:
            
                # json entry
                point = {}
                point["id"] = "%04d" % count
                point["latitude"] = str(lat)
                point["longitude"] = str(lon)

                data.append(point)
        count = count + 1

print len(data)

with open("dams.json", "w") as outfile:
    json.dump(data, outfile)
