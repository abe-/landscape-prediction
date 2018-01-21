python ee_train.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt10_e150_lr001
python ee_train2.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt10_e150_lr0025
python ee_train3.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt15_e150_lr0025
python ee_train4.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt15_extrap10_e150_lr0025

