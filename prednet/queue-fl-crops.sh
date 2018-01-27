cp ee_settings-fl.py ee_settings.py

python ee_train.py # ft 15 extrap 10
python ee_evaluate.py


rm /home/abe/Software/landscape-prediction-db/Data/prednet/Models/fl/prednet_*
python ee_train2.py # 5l

cp ee_settings-crops.py ee_settings.py

python ee_train.py  # ft 15 extrap 10
python ee_evaluate.py  

rm /home/abe/Software/landscape-prediction-db/Data/prednet/Models/crops/prednet_*
python ee_train2.py  # 5l


# QUEDARA POR HACER LOS EVALUATES DE LOS 5l



