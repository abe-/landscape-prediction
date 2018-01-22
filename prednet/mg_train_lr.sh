#python ee_train.py
#cp ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt10_e150_lr001
python ee_train2.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt15_extrap10_ft_e150_lr001
python ee_train3.py
cp ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt10_e150_lr0025
python ee_train4.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt15_extrap10_ft_e150_lr0025
python ee_train5.py
cp ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt5_e150_lr001
python ee_train6.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt5_e150_lr0025
python ee_train7.py
cp ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt10_extra5_ft_e150_lr001
python ee_train8.py
mv ../Data/prednet/Models/prednet* ../Data/prednet/Models/mg/64_nt10_extra5_ft_e150_lr0025

