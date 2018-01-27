import os
import sys, argparse
import numpy as np
from scipy.misc import imresize
from scipy.ndimage import imread
import hickle as hkl
from ee_settings import *
from random import randint

desired_im_sz = (64,64)
categories = ['all']

parser = argparse.ArgumentParser()
parser.add_argument('-s', help="size of the test tiles")
args = parser.parse_args()

if args.s is not None:
	sz = int(args.s)	
	desired_im_sz = (sz,sz)

next_recordings = []
next_recordings.append(('all', os.path.join(TRAIN_DIR,"..", 'SingleTest')))

# Create image datasets.
def process_data():
    splits = {s: [] for s in ['single']}
    splits['single'] = next_recordings
    for split in splits:
        im_list = []
        source_list = []  # corresponds to recording that image came from
        for category, folder in splits[split]:
            im_dir = os.path.join(folder + '/')
            #im_dir = folder
	    print im_dir
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


if __name__ == '__main__':
    process_data()
