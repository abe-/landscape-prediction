import os
from shutil import copy2
import numpy as np
np.random.seed(123)
from six.moves import cPickle

from keras import backend as K
from keras.models import Model
from keras.layers import Input, Dense, Flatten, Reshape # @kikyou123
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.callbacks import LearningRateScheduler, ModelCheckpoint
from keras.optimizers import Adam
from keras import regularizers

from prednet import PredNet
from data_utils import SequenceGenerator
from ee_settings import *


save_model = True  # if weights will be saved
weights_file = os.path.join(WEIGHTS_DIR, 'prednet_ee_weights.hdf5')  # where weights will be saved
json_file = os.path.join(WEIGHTS_DIR, 'prednet_ee_model.json')

# Data files
train_file = os.path.join(DATA_DIR, 'X_train.hkl')
train_sources = os.path.join(DATA_DIR, 'sources_train.hkl')
val_file = os.path.join(DATA_DIR, 'X_val.hkl')
val_sources = os.path.join(DATA_DIR, 'sources_val.hkl')

# Training parameters
nb_epoch = 50 #orig:150 
batch_size =  4 #orig: 4
samples_per_epoch = 80 #orig: 500
N_seq_val = 32 # orig: 100 number of sequences to use for validation

# Model parameters
n_channels, im_height, im_width = (3, HEIGHT, WIDTH)
input_shape = (n_channels, im_height, im_width) if K.image_data_format() == 'channels_first' else (im_height, im_width, n_channels)
stack_sizes = (n_channels, 48, 96, 192) #orig: (n_c, 48, 96, 196)
R_stack_sizes = stack_sizes
A_filt_sizes = (3, 3, 3) 		#orig: (3, 3, 3)
Ahat_filt_sizes = (3, 3, 3, 3) 	#orig: (3, 3, 3, 3)
R_filt_sizes = (3, 3, 3, 3) 	#orig: (3, 3, 3, 3)
layer_loss_weights = np.array([1., 0., 0., 0.])  # weighting for each layer in final loss; "L_0" model:  [1, 0, 0, 0], "L_all": [1, 0.1, 0.1, 0.1]
layer_loss_weights = np.expand_dims(layer_loss_weights, 1)
nt = 10  # number of timesteps used for sequences in training # orig: 10
time_loss_weights = 1./ (nt - 1) * np.ones((nt,1))  # equally weight all timesteps except the first
time_loss_weights[0] = 0
lr = 0.001
extrap = None

prednet = PredNet(stack_sizes, R_stack_sizes,
                  A_filt_sizes, Ahat_filt_sizes, R_filt_sizes,
                  output_mode='error', extrap_start_time=extrap, return_sequences=True)

inputs = Input(shape=(nt,) + input_shape)
errors = prednet(inputs)  # errors will be (batch_size, nt, nb_layers)

errors_by_time = TimeDistributed(Dense(1, trainable=False), weights=[layer_loss_weights, np.zeros(1)], trainable=False)(errors)  # calculate weighted error by layer

# +regularizer (doesn't seem to produce annything interesting)
#errors_by_time = TimeDistributed(Dense(1, trainable=False, activity_regularizer=regularizers.l1(0.0001)), weights=[layer_loss_weights, np.zeros(1)], trainable=False)(errors)  # calculate weighted error by layer


errors_by_time = Flatten()(errors_by_time)  # will be (batch_size, nt)

# @kikyou123
#errors = Reshape((-1,4))(errors)
#errors_by_time = Dense(1, weights=[layer_loss_weights, np.zeros(1)], trainable=False)(errors)
#errors_by_time = Reshape((nt, ))(errors_by_time)

final_errors = Dense(1, weights=[time_loss_weights, np.zeros(1)], trainable=False)(errors_by_time)  # weight errors by time
model = Model(inputs=inputs, outputs=final_errors)
model.compile(loss='mean_absolute_error', optimizer='adam') #orig: adam

train_generator = SequenceGenerator(train_file, train_sources, nt, batch_size=batch_size, shuffle=True)
val_generator = SequenceGenerator(val_file, val_sources, nt, batch_size=batch_size, N_seq=N_seq_val)

lr_schedule = lambda epoch: lr if epoch < nb_epoch/2 else 0.1*lr    # start with lr of 0.001 and then drop to 0.0001 after 75 epochs

#lr_schedule = lambda epoch: lr * (1 -0.95*epoch/float(nb_epoch))  

callbacks = [LearningRateScheduler(lr_schedule)]


if save_model:
    if not os.path.exists(WEIGHTS_DIR): os.mkdir(WEIGHTS_DIR)
    callbacks.append(ModelCheckpoint(filepath=weights_file, monitor='val_loss', save_best_only=True)) # orig: save_best_only=True

history = model.fit_generator(train_generator, samples_per_epoch / batch_size, nb_epoch, callbacks=callbacks, validation_data=val_generator, validation_steps=N_seq_val / batch_size)

if save_model:
    json_string = model.to_json()
    with open(json_file, "w") as f:
        f.write(json_string)

if save_model:
    outputdir="nt"+str(nt)+"_b"+str(batch_size)+"_e"+str(nb_epoch)+"_s"+str(samples_per_epoch)+"_v"+str(N_seq_val)+"_lr"+str(lr)
    outputdir = os.path.join(WEIGHTS_DIR, outputdir)
    if not os.path.exists(outputdir): os.mkdir(outputdir)
    copy2(weights_file, outputdir)
    copy2(json_file, outputdir)

