# --------------------
# LANDSCAPE PREDICTION
# --------------------
#
# augment.py
#
# Augments the sequences in TRAIN
# random rotation, mirror and flip
#

import os
import math
import random as random
from shutil import move
from settings import *
from PIL import Image
from PIL import ImageOps
from random import random

for root, folders, _ in os.walk( TRAIN_DIR ):
	for folder in folders:
		imgdir = os.path.join( root, folder )
		newdir = os.path.join( root, folder+"-aug")
		if not os.path.exists(newdir):
			os.mkdir( newdir )
		angle = random() * 360
		rnd = random()

		for f in os.listdir( imgdir ):
			img = Image.open( os.path.join(imgdir, f)  )
			width, height = img.size
		
			# Mirror / Flip 
			if rnd > 0.66:
				img = ImageOps.mirror(img)
			elif rnd > 0.33:
				img = ImageOps.flip(img)
			
			# Rotate
			sc = math.sqrt(2)
			img = img.resize( (int(width*sc),int(height*sc)), Image.BICUBIC )
			img = img.rotate(angle)
		
			# Crop
			nw, nh = img.size
			dx = (nw-width)/2
			dy = (nh-height)/2
			bbox = (dx, dy, dx+width, dy+height)
			img = img.crop(bbox)
			
			# Save it
			newname = os.path.join( newdir, f )
			img.save( newname )
