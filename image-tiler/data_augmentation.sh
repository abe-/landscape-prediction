#!/bin/sh
if [ $# -eq 0 ]
  then
    echo "You need to supply a images directory"
    exit 1
fi

echo $1

# go to images dir
cd $1

# iterate through imgs dirs and flop them
for i in $( ls ); do
echo $i
cp -r $i $i"a"
cd $i"a"
ls|xargs -L1 -IX convert -flop X X
cd ..
done


# iterate through imgs dirs and rotate them 90 degrees clockwise
for k in $( ls -t ); do
echo $k
count=0
for j in `seq 0 3`; do
cp -r $k $k"r"$count
cd $k"r"$count
ls|xargs -L1 -IX convert -rotate 90 X X
cd ..
count=$((count+1))
done
done




# return to current dir
cd $PWD
