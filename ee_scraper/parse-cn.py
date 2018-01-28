# parser of geonames.org Chinese cities txt
# http://download.geonames.org/export/dump/readme.txt

import csv
import json

data = []

with open("CN.txt", "r") as f:
    reader = csv.reader(f, delimiter='\t')
    count = 0
    for row in reader:
        pop = int(row[14])
        lat = row[4]
        lon = row[5]
        if pop > 100000 and lat[::-1].find('.') > 3 and lon[::-1].find('.') > 3:
            point = {}
            point["id"] = "%04d" % (count,)
            point["latitude"] = row[4]
            point["longitude"] = row[5]
            data.append(point)
            count = count + 1
    print str(len(data)) + " cities"

with open("cn.json", "w") as outfile:
    json.dump(data, outfile)


