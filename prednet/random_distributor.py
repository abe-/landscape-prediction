#! /usr/bin/python

# --------------------
# LANDSCAPE PREDICTION
# --------------------
#
# random_distributor.py
#
# Distributes randomly the sequences among
# TRAIN_DIR, VAL_DIR and TEST_DIR
#

import os
import random as random
from shutil import move
from datetime import datetime
from settings import *

random.seed(datetime.now())

root, folders, files = os.walk( TRAIN_DIR ).next()

# Define number of sequences in each of the main dirs

tot = len(folders)
num_val = max(1,int(tot*0.15))
num_test = max(1,min(18,tot*0.1));

# Create the folders if needed

if not os.path.exists(VAL_DIR):  os.mkdir(VAL_DIR)
if not os.path.exists(TEST_DIR): os.mkdir(TEST_DIR)

# Move sequences to folders

random.shuffle(folders)
move_to_val = folders[0:num_val]
move_to_test = folders[num_val:num_val+num_test]

print "Moving " + str(num_val) + " sequences to " + VAL_DIR
print "Moving " + str(num_test) + " sequences to " + TEST_DIR
print "Left   " + str(tot-num_val-num_test) + " sequences in " + TRAIN_DIR

for folder in folders:
	if folder in move_to_val:
		folder = os.path.join(TRAIN_DIR, folder)
		move(folder, VAL_DIR)
	if folder in move_to_test:
		folder = os.path.join(TRAIN_DIR, folder)
		move(folder, TEST_DIR)
