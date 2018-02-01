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

# Data dir
DATA_DIR = '$data_dir'

# Where data will be saved if you run process_data.py
TRAIN_DIR = '$train_dir'
VAL_DIR = '$val_dir'
TEST_DIR = '$test_dir'


# Where model weights and config will be saved if you run train.py or extrap
MODELS_DIR = '$models_dir'

# Where results (prediction plots and evaluation file) will be saved.
RESULTS_DIR = '$results_dir'


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

#COORDS.append(  )

ZOOM = $zoom
KEY = '$key'


# Max ZOOM in Earth Engine:
ZOOM = min(ZOOM, 12.2)
