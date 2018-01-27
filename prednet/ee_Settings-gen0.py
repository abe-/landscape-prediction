WIDTH=64
HEIGHT=64

# Where data will be saved if you run process_ee.py
TRAIN_DIR = '../Data/Train-gen0/'
VAL_DIR = '../Data/Val-gen0/'
TEST_DIR = '../Data/Test-gen0/'

# Where data will be saved if you run process_kitti.py
# If you directly download the processed data, change to the path of the data.
DATA_DIR = '../Data/prednet/Processed/gen0/'

# Where model weights and config will be saved if you run kitti_train.py
# If you directly download the trained weights, change to appropriate path.
WEIGHTS_DIR = '../Data/prednet/Models/gen0/'

# Where results (prediction plots and evaluation file) will be saved.
RESULTS_SAVE_DIR = '../Exports/prednet/ee_results-gen0/'
