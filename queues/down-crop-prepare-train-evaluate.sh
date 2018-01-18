#!/bin/bash
LP_DIR=".."
cd $LP_DIR
python gee-scratcher.py aripuana
cd prednet
source bin/activate
python process_ee.py
python ee_train.py
python ee_evaluate.py
