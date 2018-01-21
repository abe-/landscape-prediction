python ee_train.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/aripuana/64_nt10_e150_lr002_0002
python ee_train2.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/aripuana/64_nt10_e150_lr001_00025
python ee_train3.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/aripuana/64_nt10_e150_lr0015_00015
python ee_train4.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/aripuana/64_nt10_e150_lr0035

