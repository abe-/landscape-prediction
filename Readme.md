git
python2.7
python-pip
virtualenv

entorno python:

:
git clone https://github.com/abe-/landscape-prediction.git

cd landscape-prediction

virtualenv -p /usr/bin/python2.7 env
source env/bin/activate

** SCRAPER INSTALLATION **

we need a headless browser:

if MAC OS X:
brew install chromedriver
brew install Caskroom/versions/google-chrome-canary

if WINDOWS: 
install google-chrome-canary

if LINUX:
sudo apt-get install xvfb
pip install pyvirtualdisplay

we’ll make use of ImageMagick

if LINUX:
sudo apt-get install imagemagick

then:
pip install selenium
pip install numpy


** TENSORFLOW and KERAS INSTALLATION **

we will work with tensor flow v  and keras version 2.0.6

tensorflow
(https://www.tensorflow.org/versions/r1.2/install/install_linux#the_url_of_the_tensorflow_python_package)

if LINUX with CPU only:
pip install - -upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.2.1-cp27-none-linux_x86_64.whl

if LINUX with GPU:
pip install - -upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.2.1-cp27-none-linux_x86_64.whl

if MAC with CPU only:
pip install - -upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.2.1-py2-none-any.whl

if MAC with GPU: (tensor flow v. 1.1 !!)
pip install - -upgrade https://storage.googleapis.com/tensorflow/mac/gpu/tensorflow_gpu-1.1.0-py2-none-any.whl


then keras: (and other dependencies will be installed as well)

pip install keras==2.0.6
pip install hickle
pip install matplotlib
pip install pillow


We need to have an initial dataset to test the installation. Cuestión del “name” (key or code) of the project:

cp -r sample_data/* Data/

we edit config/settings.py and replace the existing name with gen0
- WIDTH, HEIGHT 64
- NB_EPOCH 3

then:

python process_data.py

it will create:
../Data/prednet/Processed/gen0


then we train a model with these data:

python train.py


It will create a Model here:

../Data/prednet/Models/gen0/


python  extrap_finetune.py

this creates two additional Model files, extrap_finetuned

To evaluate what the neural network has learnt, we have then:

python evaluate.py




SI HAGO EJEMPLO EDSON:
With downloaded data, after scraper -> random-distributor
settings : nt 1 batch 1 nseqval 1 samples 1


convert g???.png  -set delay 25  cn-orig-pred.gif


Even when the NN seems to be doing nothing, it has the capacity to clean the datasets, as these images show:

cn-orig-pred.gif
cn-pred-pred.gif

file:///Users/agfm1n14/Documents/Processing/tests_viewer/cn-pred-pred.gif


Host gnd1
	HostName croopier.ddns.net
	Port 1180
	User tm
	IdentityFile ~/.ssh/tm


Host gnd2
	HostName 35.195.172.252
	User tm
	IdentityFile ~/.ssh/tm


