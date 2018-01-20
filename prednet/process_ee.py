import os
import numpy as np
from scipy.misc import imresize
from scipy.ndimage import imread
import hickle as hkl
from ee_settings import *
from random import randint

desired_im_sz = (64,64)
categories = ['all']

# Recordings used for validation and testing.
# Were initially chosen randomly such that one of the city recordings was used for validation and one of each category was used for testing.

val_recordings = []
for i in range(80):
	randomtile = "%04d" % randint(119, 559) + "-0"
	val_recordings.append(('all', randomtile))

test_recordings = []
for i in range(8):
	randomtile = "%04d" % randint(119,559)
        randomtile0 = randomtile + "-0"
        randomtile1 = randomtile + "-1"
        test_recordings.append(('all', randomtile0))
        test_recordings.append(('all', randomtile1))

#val_recordings = [('all', '0101-0'),('all', '0101-1'),('all', '0101-2'),('all', '0101-3'),('all', '0101-4'),('all', '0101-5'),('all', '0101-6'),('all', '0101-7'), ('all', '0101-8'),('all', '0101-9'),('all', '0101-10'),('all', '0101-11'),('all', '0101-12'),('all', '0101-13'),('all', '0101-14'),('all', '0101-15'),('all', '0101-16'),('all', '0101-17'),('all', '0101-18'),('all', '0101-19'),('all', '0101-20'),('all', '0101-21'),('all', '0101-22'),('all', '0101-23'),('all', '0101-24'),('all', '0101-25'),('all', '0101-26'),('all', '0101-27'),('all', '0101-28'),('all', '0101-29'),('all', '0101-30'),('all', '0101-31')]
#test_recordings = [('all', '0102-0'),('all', '0102-1'),('all', '0102-2'),('all', '0102-3'),('all', '0102-4'),('all', '0102-5'),('all', '0102-6'),('all', '0102-7'), ('all', '0102-8'),('all', '0102-9'),('all', '0102-10'),('all', '0102-11'),('all', '0102-12'),('all', '0102-13'),('all', '0102-14'),('all', '0102-15'),('all', '0102-16'),('all', '0102-17'),('all', '0102-18'),('all', '0102-19'),('all', '0102-20'),('all', '0102-21'),('all', '0102-22'),('all', '0102-23'),('all', '0102-24'),('all', '0102-25'),('all', '0102-26'),('all', '0102-27'),('all', '0102-28'),('all', '0102-29'),('all', '0102-30'),('all', '0102-31')]


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
        	splits['train'] += [(c, f) for f in folders if (c, f) not in not_train]
	except StopIteration:
		pass
    for split in splits:
        im_list = []
        source_list = []  # corresponds to recording that image came from
        for category, folder in splits[split]:
            im_dir = os.path.join(TRAIN_DIR, folder + '/')
            try:
		_, _, files = os.walk(im_dir).next()
            	im_list += [im_dir + f for f in sorted(files)]
            	source_list += [category + '-' + folder] * len(files)
	    except StopIteration:
		pass
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
