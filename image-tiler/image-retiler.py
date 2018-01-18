import os
from scipy.misc import imread

TRAIN_256 = "/home/abe/Software/landscape-prediction-db/Train-256"

for _, dirs, _ in os.walk(TRAIN_256):
    ts256 = [None]*len(dirs)
    for dir in dirs:
        id, t256 = os.path.basename(dir).split("-")
        id = int(id)
        t256 = int(t256)
        ts256[id] = [None]*8
        ts256[id][t256] = [None]*32
        for file in os.listdir(os.path.join(TRAIN_256,dir)):
            fr = int(os.path.splitext(file)[0])-1
            ts256[id][t256][fr] = file
            print ts256[0][0][0]

print ts256
