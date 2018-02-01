'''
This file merges together prepare_ and _evaluate
TODO: refactor into usable objects across the platform
'''


import os
import sys, argparse
from shutil import copy2
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
from scipy.misc import imsave
from scipy.misc import imresize
from scipy.ndimage import imread
import hickle as hkl

from settings import *



batch_size = BATCH_SIZE
nt = NT
numtests = 1
extrap = None

parser = argparse.ArgumentParser()
parser.add_argument('-ft', help="fine-tune multistep: number of the first predicted frame")
parser.add_argument('dir', metavar="DIR", type=str, nargs=1, help="dir of the input images")
args=parser.parse_args()


# Model files and image directories
weights_file = os.path.join(MODELS_DIR, 'prednet_ee_weights.hdf5')
json_file = os.path.join(MODELS_DIR, 'prednet_ee_model.json')
test_file = os.path.join(DATA_DIR, 'X_single.hkl')
test_sources = os.path.join(DATA_DIR, 'sources_single.hkl')

if args.ft is not None:
	extrap = int(args.ft)
	weights_file = os.path.join(MODELS_DIR, 'prednet_ee_weights-extrapfinetuned.hdf5')
	json_file = os.path.join(MODELS_DIR, 'prednet_ee_model-extrapfinetuned.json')
	nt = extrap+32

if args.dir is not None:
	inputdir = args.dir[0]


# Create tmpdir if it does not exist
if not os.path.exists("tmp"): os.mkdir("tmp")
tmpdir = os.path.join("tmp")

# remove the files within tmp
for f in os.listdir(tmpdir):
	file_path = os.path.join(tmpdir,f)
	try:
		if os.path.isfile(file_path):
			os.unlink(file_path)
	except Exception as e:
		print(e)




# Move input files to tmp dir
def copy_to_tmp():
	print "[DEBUG] Input dir: " + inputdir
	for root, _, files in os.walk(inputdir):
		for f in files:
			name = os.path.join(root,f)
			copy2(name, tmpdir)

	for root, _, files in os.walk(tmpdir):
		file_count = len(files)
		last = files[-1]
		for i in range(file_count, nt):
			name1 = os.path.join(tmpdir,last)
			name2 = os.path.join(tmpdir,"extra-"+"%02d" % i+",png")
			copy2(name1, name2)




# Create image datasets.
def process_data():
	desired_im_sz = (HEIGHT, WIDTH)
	categories = ['all']

	next_recordings = []
	next_recordings.append(('all', tmpdir))

	splits = {s: [] for s in ['single']}
	splits['single'] = next_recordings
	for split in splits:
		im_list = []
		source_list = []  # corresponds to recording that image came from
	for category, folder in splits[split]:
		im_dir = os.path.join(folder + '/')
		#im_dir = folder
		_, _, files = os.walk(im_dir).next()
		im_list += [im_dir + f for f in sorted(files)]
		source_list += [category + '-' + folder] * len(files)

		print 'Creating ' + split + ' data: ' + str(len(im_list)) + ' images'
		X = np.zeros((len(im_list),) + desired_im_sz + (3,), np.uint8)

		for i, im_file in enumerate(im_list):
			im = imread(im_file, mode='RGB')
			X[i] = process_im(im, desired_im_sz)

		hkl.dump(X, os.path.join(DATA_DIR, 'X_' + split + '.hkl'))
		hkl.dump(source_list, os.path.join(DATA_DIR, 'sources_' + split + '.hkl'))




# resize and crop image
def process_im(im, desired_sz):
	target_ds = float(desired_sz[0])/im.shape[0]
	im = imresize(im, (desired_sz[0], int(np.round(target_ds * im.shape[1]))))
	d = int((im.shape[1] - desired_sz[1]) / 2)
	im = im[:, d:d+desired_sz[1]]
	return im




# Execute a test with the files in the folder
def execute_test():

	# Load trained model
	f = open(json_file, 'r')
	json_string = f.read()
	f.close()
	train_model = model_from_json(json_string, custom_objects = {'PredNet': PredNet})
	train_model.load_weights(weights_file)

	# Create testing model (to output predictions)
	layer_config = train_model.layers[1].get_config()
	layer_config['output_mode'] = 'prediction' #'prediction'
	layer_config['extrap_start_time'] = extrap;
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

	# Compare MSE of PredNet predictions vs. using last frame.  Write results to prediction_scores.txt
	mse_model = np.mean( (X_test[:, 1:] - X_hat[:, 1:])**2 )  # look at all timesteps except the first
	mse_prev = np.mean( (X_test[:, :-1] - X_test[:, 1:])**2 )
	if not os.path.exists(RESULTS_SAVE_DIR): os.mkdir(RESULTS_SAVE_DIR)
	f = open(RESULTS_SAVE_DIR + 'prediction_scores.txt', 'w')
	f.write("Model MSE: %f\n" % mse_model)
	f.write("Previous Frame MSE: %f" % mse_prev)
	f.close()

	# Plot some predictions
	aspect_ratio = float(X_hat.shape[2]) / X_hat.shape[3]
	plt.figure(figsize = (nt, 2*aspect_ratio))
	gs = gridspec.GridSpec(2, nt)
	gs.update(wspace=0., hspace=0.)
	plot_save_dir = os.path.join(RESULTS_SAVE_DIR, 'prediction_plots/')
	if not os.path.exists(plot_save_dir): os.mkdir(plot_save_dir)

	# Output the sequence of all the predicted images
	for test in range(numtests):
	    testdir = "tile-" + str(test)
	    testdir = os.path.join(plot_save_dir, testdir)
	    if not os.path.exists( testdir ) : os.mkdir( testdir )
	    for t in range(nt):
		imsave( testdir + "/pred-%02d.png" % (t,), X_hat[test,t] )
		imsave( testdir + "/orig-%02d.png" % (t,), X_test[test,t])




# main loop
if __name__ == '__main__':
	copy_to_tmp()
	process_data()
	execute_test()
