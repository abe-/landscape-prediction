import os
import sys, argparse
from shutil import copy2
from string import Template

LANDPREDS_DIR = os.path.join("LandPreds")

parser = argparse.ArgumentParser()
parser.add_argument('KEY', metavar='key', type=str, nargs=1,
                    help='codename of the project')

args = parser.parse_args()
key = args.KEY[0]


print "Creating project folders:"

PROJECT_DIR = os.path.join(LANDPREDS_DIR, key)
if not os.path.exists(PROJECT_DIR): os.makedirs(PROJECT_DIR)

print "- Data"

DATA_DIR = os.path.join(PROJECT_DIR, "Data")
if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

print "- Models"

MODELS_DIR = os.path.join(PROJECT_DIR, "Models")
if not os.path.exists(MODELS_DIR): os.makedirs(MODELS_DIR)

print "- Exports"

EXPORTS_DIR = os.path.join(PROJECT_DIR, "Exports")
if not os.path.exists(EXPORTS_DIR): os.makedirs(EXPORTS_DIR)

d={ 'width':128,
    'height':128,
    'nt':10,
    'extrap':5,
    'nb_epoch': 100,
    'samples_per_epoch': 125,
    'n_seq_val': 32,
    'batch_size': 4,
    'lr': 0.002,
    'num_tests':18,
    'num_plots':10,
    'zoom': 12.2,
    'key': key }


print "Creating settings file"

settingsTemplate = open(os.path.join('prednet', '_settings.py'), 'r')
src = Template( settingsTemplate.read() )
new_settings = src.substitute( d )

with open( os.path.join(PROJECT_DIR, 'settings.py'), 'w') as f:
    f.write( new_settings )



print "Copying PredNet files..."
copy2(os.path.join('prednet', 'data_utils.py'), PROJECT_DIR)
copy2(os.path.join('prednet', 'evaluate_future.py'), PROJECT_DIR)
copy2(os.path.join('prednet', 'evaluate.py'), PROJECT_DIR)
copy2(os.path.join('prednet', 'extrap_finetune.py'), PROJECT_DIR)
copy2(os.path.join('prednet', 'keras_utils.py'), PROJECT_DIR)
copy2(os.path.join('prednet', 'prednet.py'), PROJECT_DIR)
copy2(os.path.join('prednet', 'process_data.py'), PROJECT_DIR)
copy2(os.path.join('prednet', 'train.py'), PROJECT_DIR)
print "Copying scraper files..."
copy2(os.path.join('scraper', 'tiledcoord.py'), PROJECT_DIR)
copy2(os.path.join('scraper', 'scraper-tiled.py'), PROJECT_DIR)
copy2(os.path.join('scraper', 'scraper-chrome.py'), PROJECT_DIR)
print "Copying utils files..."
copy2(os.path.join('prednet', 'random_distributor.py'), PROJECT_DIR)
copy2(os.path.join('historigram_matcher', 'histmatch.sh'), PROJECT_DIR)
copy2(os.path.join('historigram_matcher', 'recursive-filter.sh'), PROJECT_DIR)
copy2(os.path.join('image-tiler', 'data_augmentation.sh'), PROJECT_DIR)
