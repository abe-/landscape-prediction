'''
Evaluate trained PredNet
Calculates mean-squared error and plots predictions.
'''

import os
import sys, argparse
import numpy as np
from six.moves import cPickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from keras import backend as K
from keras.models import Model, model_from_json
from keras.layers import Input, Dense, Flatten

from prednet import PredNet
from data_utils import SequenceGenerator
from ee_settings_mg import *

from scipy.misc import imsave

n_plot = 40
batch_size = 10
nt = 10
numtests = 1
startF = 0

parser = argparse.ArgumentParser()
parser.add_argument('-m', help="path of the dir with the model files")
parser.add_argument('-l', help="nt: number of training frames")
parser.add_argument('-i', help="starting sequence frame number")
args=parser.parse_args()

if args.m is not None:
	WEIGHTS_DIR = os.path.join(WEIGHTS_DIR,args.m)
if args.l is not None:
	nt = int(args.l)
if args.i is not None:
	startF = int(args.i)

NEXT_SAVE_DIR = 'next/'

weights_file = os.path.join(WEIGHTS_DIR, 'prednet_ee_weights.hdf5')
json_file = os.path.join(WEIGHTS_DIR, 'prednet_ee_model.json')
test_file = os.path.join(DATA_DIR, 'X_next.hkl')
test_sources = os.path.join(DATA_DIR, 'sources_next.hkl')

# Load trained model
f = open(json_file, 'r')
json_string = f.read()
f.close()
train_model = model_from_json(json_string, custom_objects = {'PredNet': PredNet})
train_model.load_weights(weights_file)

# Create testing model (to output predictions)
layer_config = train_model.layers[1].get_config()
layer_config['output_mode'] = 'prediction'
data_format = layer_config['data_format'] if 'data_format' in layer_config else layer_config['dim_ordering']
test_prednet = PredNet(weights=train_model.layers[1].get_weights(), **layer_config)
input_shape = list(train_model.layers[0].batch_input_shape[1:])
input_shape[0] = nt
inputs = Input(shape=tuple(input_shape))
predictions = test_prednet(inputs)
test_model = Model(inputs=inputs, outputs=predictions)

test_generator = SequenceGenerator(test_file, test_sources, nt, sequence_start_mode='unique', data_format=data_format) # orig: unique
X_test = test_generator.create_all()
X_hat = test_model.predict(X_test, batch_size)
if data_format == 'channels_first':
    X_test = np.transpose(X_test, (0, 1, 3, 4, 2))
    X_hat = np.transpose(X_hat, (0, 1, 3, 4, 2))


for test in range(numtests):
    testdir = os.path.join(NEXT_SAVE_DIR)
    if not os.path.exists( testdir ) : os.mkdir( testdir )
    for t in range(startF,startF+nt):
	if t > startF and t < startF+nt:
		imsave( testdir + "/%03d.png" % (t-1,), X_test[test,t-startF])
    imsave( testdir + "/%03d.png" % (startF+nt-1,), X_hat[test,nt-1])
