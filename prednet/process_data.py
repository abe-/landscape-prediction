import os
import numpy as np
from scipy.misc import imresize
from scipy.ndimage import imread
import hickle as hkl
from settings import *
from random import randint
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

desired_im_sz = (HEIGHT,WIDTH)
categories = ['all']

if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

# VALIDATION SEQUENCES

val_recordings = []
try:
	_, folders, _ = os.walk(VAL_DIR).next()
	for f in folders:
		val_recordings.append(('all', os.path.join(VAL_DIR, f)))
except StopIteration:
	pass
 #for i in range(80):
 #	randomtile = "%04d" % randint(119, 559) + "-0"
 #	val_recordings.append(('all', randomtile))





# TEST SEQUENCES

test_recordings = []
try:
	_, folders, _ = os.walk(TEST_DIR).next()
	for f in folders:
		test_recordings.append(('all', os.path.join(TEST_DIR, f)))
except StopIteration:
	pass

#for i in range(8):
#	randomtile = "%04d" % randint(119,559)
#        randomtile0 = randomtile + "-0"
#        randomtile1 = randomtile + "-1"
#        test_recordings.append(('all', randomtile0))
#        test_recordings.append(('all', randomtile1))




# TRAIN SEQUENCIES and image datasets

# Create image datasets.
# Processes images and saves them in train, val, test splits.
def process_data():
    splits = {s: [] for s in ['train', 'test', 'val']}
    splits['val'] = val_recordings
    splits['test'] = test_recordings
    not_train = splits['val'] + splits['test']
    for c in categories:  # Randomly assign recordings to training and testing. Cross-validation done across entire recordings.
        c_dir = TRAIN_DIR
        try:
		_, folders, _ = os.walk(c_dir).next()
        	splits['train'] += [(c, os.path.join(TRAIN_DIR,f)) for f in folders if (c, f) not in not_train]
	except StopIteration:
		pass
    for split in splits:
        im_list = []
        source_list = []  # corresponds to recording that image came from
        for category, folder in splits[split]:
            im_dir = os.path.join(folder + '/')
            try:
		_, _, files = os.walk(im_dir).next()
            	im_list += [im_dir + f for f in sorted(files)]
            	source_list += [category + '-' + folder] * len(files)
	    except StopIteration:
		pass
        print 'Creating ' + split + ' data: ' + str(len(im_list)) + ' images'
        X = np.zeros((len(im_list),) + desired_im_sz + (3,), np.uint8)
        fileOK = True
	for i, im_file in enumerate(im_list):
	    try:
            	im = imread(im_file, mode='RGB')
            	X[i] = process_im(im, desired_im_sz)
	    except IOError:
		fileOK = False
		pass
	if fileOK:
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
