# Landscape Prediction

Next Frame Prediction names the experimental set of Machine Learning techniques aimed to algorithmically produce the frame that follows a video stream of images. This approach to video-prediction makes use of convolutional neural networks that, relying on large databases of videos, are able to identify temporal patterns and behaviours within a sequence of frames. This analysis provides them with the capacity of generating future movement and, in consequence, of extending videos with plausible futures.

This project is conceived as a platform to research on the application of techniques of video prediction to sequences of historical satellital data. Starting from the available timelapses of archived arial images, this platform aims to generate future visions of the surfaces of the Earth where, flattened as video sequences, terraforming activities such as deforestation or urbanisation might be scrutinised as visual feeders for predictive algorithms.

The platform wraps and merges together the ConvLSTM [PredNet network](https://github.com/coxlab/prednet) together with tools to work with images (downloading / cleaning / augmenting and enhacing) coming from the timelapses of Google's Earth Engine project. 

It is a project elaborated initially by Abelardo Gil-Fournier as part of the AMT workshop "Surface Value and Landscape Prediction" that took place in Transmediale 18.

# Samples

- Timelapse viewer (movements on the surface):

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/grid-viewer.gif" width=768px>

- Video prediction:

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/gen0-irregular.gif" width=768px>

- First attemps, with a GAN:

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/landscape-prediction-gan-t0.gif" width=384px>

- Tests with PredNet:

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/compared-0353-0.gif" width=768px>

- First results:

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/0353-0.gif" width=384px><img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/0353-1.gif" width=384px>

- ~1 hour (GPU-based) trainings:

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/dams-e100.gif" width=768px>

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/irrigation-crops.gif" width=768px>

- The importance of data:

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/cn-orig-pred.gif" width=768px>

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/cn-pred-pred.gif" width=768px>





## Installation

### 1. Get the platform

This is a project that relies on python2.7, pip, virtualenv and git:

#### python 2.7 + pip + virtualenv

Linuxes and MacOSX have python 2.7 as preinstalled language. You only need to get pip and virtual env. In case of Debian/Ubuntu, this is achived with:
```
sudo apt-get install python-pip
sudo pip install virtualenv
```
In case of MacOSX:
```
sudo easy_install pip
sudo pip install virtualenv
```

In case of Windows, a good guide to install this platform [can be reached here](http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/).

#### git as code and documentation repository

[here's a quick installation guide for Linux/Mac/Win](https://www.atlassian.com/git/tutorials/install-git#linux)

### 2. Clone the project and create its virtual environment
To retrieve the updated version of this project you need to clone this repository:
```
git clone https://github.com/abe-/landscape-prediction.git
```
Enter then in its folder and create a python environment for it:
```
cd landscape-prediction
virtualenv -p /usr/bin/python2.7 env
source env/bin/activate
```

### 3. Scraping tools

To download the sequences of images provided by GEE we are temporarily relying on a scraping approach. That is, we setup and automated web-browser to visit and fetch from GEE's Timelapse the temporal images. To do that, we need a headless browser:

If MAC OS X:
```
brew install chromedriver
brew install Caskroom/versions/google-chrome-canary
```
If WINDOWS: 
```
install google-chrome-canary
```
If LINUX (instructions for Ubuntu only):
```
sudo apt-get install xvfb
pip install pyvirtualdisplay
```
Then, we install python's scraping library:
```
pip install selenium
pip install numpy
```
Once the images are downloaded, they are resized (and eventually cropped). This is performed by the swiss-knife of image manipulation, the open source tool imagemagick:

If LINUX:
```
sudo apt-get install imagemagick
```
If WINDOWS of MACOSX, see the [installation instructions here](https://legacy.imagemagick.org/script/binary-releases.php)

### 4. The Machine Learning part: installing Tensorflow and Keras

The PredNet video-predicting network is built on top of the Machine Learning platforms Keras (v2.0.6) and Tensorflow (v1.2.1).

Tensorflow installation steps can be found [here](https://www.tensorflow.org/versions/r1.2/install/install_linux#the_url_of_the_tensorflow_python_package). Summarized:

If LINUX with CPU only:
```
pip install - -upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.2.1-cp27-none-linux_x86_64.whl
```
If LINUX with GPU:
```
pip install - -upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.2.1-cp27-none-linux_x86_64.whl
```
If MAC with CPU only:
```
pip install - -upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.2.1-py2-none-any.whl
```
if MAC with GPU: (tensor flow v. 1.1 !!)
```
pip install - -upgrade https://storage.googleapis.com/tensorflow/mac/gpu/tensorflow_gpu-1.1.0-py2-none-any.whl
```
Now we proceed with the installation of Keras (and other dependencies that will be installed as well):
```
pip install keras==2.0.6
pip install hickle
pip install matplotlib
pip install pillow
```
### 5. Finally, rsync to transfer files between computers

rsync is one of the fastests way to transfer files among computers:

If LINUX:
```
sudo apt-get install rsync
```
If MACOSX:
```
brew install rsync
```
If WINDOWS:
Follow the instructions [here](https://itefix.net/cwrsync)


## First step: Initialize a project

The basic entity of this Landscape Prediction platform is the landpred project. A landpred project is a structure of files and folders aimed to ease the creation of landscape predictions. It encapsulates both the datasets and the neural network within a single directory so that it can be easily transfered to remote training computers and obtain back their results.

To create a landpred the only you need to give a name. Then, inslde the project's main folder, you run:
```
python create_landpred.py LANDPREDNAME
```
Each landpred is a directory initially stored inside the folder "LandPreds". It contains all the necessary files to be trained on a properly configured machine. They are placed dierctly inside this main directory. Additionally, each landpred contains three folders:
```
Data/
Models/
Exports/
```
where the datasets, the obtained models and the prediction results will be stored, respectively.

## Second step: prepare a set of sample data

The folder "sample-data" contains a dataset of images of a procedurally animated animation. The source code of the generator, written in Processing, is also available.

To train a model with this data, you need to copy these 3 directories (Train, Test, Val) to the Data directory of your landpred. For instance, if the project is named "gen0" and we are inside its main folder, we would run:
```
cp -r ../../sample-data/* Data/
```
Now we might adjust some settings of our training process. This can be done by editing the settings.py file. For instance, in our case we want the model to work with files of size 64z64px (default is 128x128) and with a learning rate LR of 0.001 (default is 0.002). We edit settings.py and change the corresponding lines:
```
WIDTH=64
HEIGHT= 64
...
LR=0.001
```
Now we need to prepare the data to be analyzed by the neural network. To do this, we run the command:
```
python process_data.py
```
It will transform the images into matrices of numbers that will be conveniently store insided the Data folder as well.

## Third step: 

Now we are able to train a model with these data:
```
python train.py
```
The process will display some useful information about how the learning evolves. When finished, it will have created a model inside the Models folder, and made a copy of it inside a separate folder.

This model will have being trained to produce the t+1 frame of a sequence of frames. As we are interested in longer predictions, we need to train a bit more the model (to finetune it) so that is can extrapolate several future frames:
```
python  extrap_finetune.py
```
This will create two additional Model files, the ones corresponding to the finetuned model.

## Fourth step: evaluate the model:

Finally, we need to test the model. To evaluate what the neural network has learnt we need to run:
```
python evaluate.py -ft EXTRAP_FRAME
```
where EXTRAP_FRAME is the frame number from where extrapolation will start to be produced. 

This will produce a set of tests and plots displaying the prediction against the actual frames (the so-called "ground truth").

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/plot-4.png">

The tests can be reviewed with a simple processing tool, "tests_viewer", that will animate the results:

<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/gen0.gif" width="768">

To export either the visualisations of this tool or the tiles themselves as a gif we have the nice convert tool provided by imagemagick:
```
convert g???.png  -set delay 25  cn-orig-pred.gif
```

## Fifth step: produce a longer extrapolation of the prediction

A final script will allow us to produce with the extrap_finetuned model a longar extrapolation:
```
python evaluate_future.py Data/Test/0270 -ft 32
```
<img src="https://github.com/abe-/landscape-prediction/raw/master/gifs/gen0-extrapolated.gif" width="256">

SI HAGO EJEMPLO EDSON:
With downloaded data, after scraper -> random-distributor
settings : nt 1 batch 1 nseqval 1 samples 1






Host gnd1
	HostName croopier.ddns.net
	Port 1180
	User tm
	IdentityFile ~/.ssh/tm

Host gnd2
	HostName 35.195.172.252
	User tm
	IdentityFile ~/.ssh/tm

Host gnd3
	HostName 35.189.226.77
	User tm
	IdentityFile ~/.ssh/tm


Host gnd4
	HostName 35.195.99.125
	User tm
	IdentityFile ~/.ssh/tm

