WIDTH=96
HEIGHT=96

# Where data will be saved if you run process_ee.py
TRAIN_DIR = '../Data/Train-dams/'
VAL_DIR = '../Data/Val-dams/'
TEST_DIR = '../Data/Test-dams/'

# Where data will be saved if you run process_kitti.py
# If you directly download the processed data, change to the path of the data.
DATA_DIR = '../Data/prednet/Processed/dams/'

# Where model weights and config will be saved if you run kitti_train.py
# If you directly download the trained weights, change to appropriate path.
WEIGHTS_DIR = '../Data/prednet/Models/dams/'

# Where results (prediction plots and evaluation file) will be saved.
RESULTS_SAVE_DIR = '../Exports/prednet/ee_results-dams/'
