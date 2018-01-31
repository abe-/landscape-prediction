WIDTH=128
HEIGHT=128

# Hyperparameters
NT=10
EXTRAP=5
NB_EPOCH=100
SAMPLES_PER_EPOCH=125
N_SEQ_VAL=32
BATCH_SIZE=4
LR=0.002


# Where data will be saved if you run process_ee.py
TRAIN_DIR = '../Data/Train-cn/'
VAL_DIR = '../Data/Val-cn/'
TEST_DIR = '../Data/Test-cn/'

# Where data will be saved if you run process_kitti.py
# If you directly download the processed data, change to the path of the data.
DATA_DIR = '../Data/prednet/Processed/cn/'

# Where model weights and config will be saved if you run kitti_train.py
# If you directly download the trained weights, change to appropriate path.
WEIGHTS_DIR = '../Data/prednet/Models/cn/'

# Where results (prediction plots and evaluation file) will be saved.
RESULTS_SAVE_DIR = '../Exports/prednet/ee_results-cn/'
