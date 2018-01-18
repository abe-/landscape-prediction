#!/bin/bash
SEQ="0209-1"
SIZE=64
INITIAL=23
NT=10
MODEL="aripuana/64-bueno"
FUTURE=10
while getopts n:s:i:l:m:f: option
do
case "${option}"
in
n) SEQ=${OPTARG};;
s) SIZE=${OPTARG};;
i) INITIAL=${OPTARG};;
l) NT=${OPTARG};;
m) MODEL=${OPTARG};;
f) FUTURE=${OPTARG};;
esac
done

FINAL=$(($INITIAL+$NT))

echo "SEQUENCE: "     $SEQ
echo "SIZE: "         $SIZE "x" $SIZE
echo "INITIAL FRAME: "$INITIAL
echo "FINAL FRAME:   "$FINAL

rm next/*
cd pred
rm *

for i in $( ls ../../Data/$SEQ/*|head -n $FINAL); do
cp $i .
done

for i in $( ls ); do convert -resize $SIZEx$SIZE $i $i; done

cp `ls|tail -n $NT` ../next
cd ..

for i in `seq 0 $(($FUTURE-1))`; do sh pred_next.sh -s $SIZE -i $INITIAL -l $NT -m $MODEL; done
