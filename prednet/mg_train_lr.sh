python ee_train.py
cp ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_6l_nt10_e150_lr001
python ee_train2.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_6l_nt10__e150_lr0025
