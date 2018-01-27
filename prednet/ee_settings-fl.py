WIDTH=64
HEIGHT=64

# Where data will be saved if you run process_ee.py
TRAIN_DIR = '../Data/Train-fl/'
VAL_DIR = '../Data/Val-fl/'
TEST_DIR = '../Data/Test-fl/'

# Where data will be saved if you run process_kitti.py
# If you directly download the processed data, change to the path of the data.
DATA_DIR = '../Data/prednet/Processed/fl/'

# Where model weights and config will be saved if you run kitti_train.py
# If you directly download the trained weights, change to appropriate path.
WEIGHTS_DIR = '../Data/prednet/Models/fl/'

# Where results (prediction plots and evaluation file) will be saved.
RESULTS_SAVE_DIR = '../Exports/prednet/ee_results-fl/'
