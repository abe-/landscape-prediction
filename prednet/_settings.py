import os

# Dims of images to train the model
WIDTH=$width
HEIGHT=$height

# Hyperparameters
NT=$nt
EXTRAP=$extrap
NB_EPOCH=$nb_epoch
SAMPLES_PER_EPOCH=$samples_per_epoch
N_SEQ_VAL=$n_seq_val
BATCH_SIZE=$batch_size
LR=$lr

# For the evaluation stage, number of tests and plots:
NUM_TESTS=$NUM_TESTS
NUM_PLOTS=$NUM_PLOTS

# Get dir where file is
current = os.path.dirname(os.path.realpath(__file__))

# Data dir
DATA_DIR = os.path.join(current, 'Data')

# Where data will be saved if you run process_data.py
TRAIN_DIR = os.path.join( DATA_DIR, 'Train')
VAL_DIR = os.path.join( DATA_DIR, 'Val')
TEST_DIR = os.path.join( DATA_DIR, 'Test')


# Where model weights and config will be saved if you run train.py or extrap
MODELS_DIR = os.path.join(current, 'Models')

# Where results (prediction plots and evaluation file) will be saved.
RESULTS_DIR = os.path.join(current, 'Exports')


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

# Add the BBOX coordinates as in the following line,
# which corresponds to an irrigation area close to Edson, Kansas:
# (important: Lan/Lon order)
#COORDS.append( [ 40.165757,-101.840515,40.238654,-101.553497 ] )

ZOOM = $zoom
KEY = '$key'


# Max ZOOM in Earth Engine:
ZOOM = min(ZOOM, 12.2)
