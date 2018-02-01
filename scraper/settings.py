
#
# PredNet settings
#


# Size of the training images
WIDTH=64
HEIGHT=64

# Hyperparameters
NT=10
EXTRAP=5
NB_EPOCH=100
SAMPLES_PER_EPOCH=125
N_SEQ_VAL=32
BATCH_SIZE=4
LR=0.002


# Where data will be saved if you run process_data.py
TRAIN_DIR = '../Data/Train-edson2/'
VAL_DIR = '../Data/Val-edson2/'
TEST_DIR = '../Data/Test-edson2/'

# Where data will be saved if you run process_data.py
DATA_DIR = '../Data/prednet/Processed/edson2/'

# Where model weights and config will be saved if you run train.py
WEIGHTS_DIR = '../Data/prednet/Models/edson2/'

# Where results (prediction plots and evaluation file) will be saved.
RESULTS_SAVE_DIR = '../Exports/prednet/ee_results-edson2/'


#
# Scraper settings
#

# Online tool to retrieve bbox lat/lon boundaries:
#
#           DON'T FORGET TO CHOOSE THE
#      CORRECT ORDER OF COORDINATES Lat/Lng
#   (corner at the bottom right of the window)
#
# http://bboxfinder.com


COORDS = []

# edson2, kansas (irrigation agriculture)
COORDS.append( [ 40.165757,-101.698380,40.239178,-101.553497 ] )
ZOOM = 12.2
KEY = "edson2"




# mg (mattogrosso)
#-14.721761, -59.677734, -10.033767, -54.371338

# aripuana
#-11.813588, -59.227295, -10.652510, -58.450012
#ZOOM=8

#Yuzhni Island (Russia) + Groenland
#key="ice"
#ZOOM=8
#COORDS.append( [71.635993,53.162842,73.131322,55.458984]  )
#COORDS.append( [73.201317,54.843750,74.116047,56.997070]  )
#COORDS.append( [74.132576,55.728149,74.849236,59.891968]  )

# Kansas
#lat0,lon0,lat1,lon1=[38.975425,-99.091187,39.757880,-97.800293]
#key="crops"
#ZOOM = 12.2

# Max ZOOM in Earth Engine:
ZOOM = min(ZOOM, 12.2)
