#!/bin/bash

SIZE=64
INITIAL=0
NT=10
MODEL="./"

while getopts s:i:l:m: option
do
case "${option}"
in
s) SIZE=${OPTARG};;
i) INITIAL=${OPTARG};;
l) NT=${OPTARG};;
m) MODEL=${OPTARG};
esac
done

FINAL=$(($INITIAL+$NT))
LAST=$(($FINAL-1))

echo "PROCESSING t FRAME"
python process_next.py -s $SIZE 2> next.log
echo ""
echo "GENERATING t+1 FRAME"
python evaluate_next.py -m $MODEL -l $NT
echo ""
echo "ADDING t+1 FRAME TO THE SEQUENCE"
NUM=$( ls pred|wc -l )
NEXT=$(($NUM+1))

cp next/$(printf "%03d" $LAST).png pred/$(printf "%03d" $NUM).png
#ls pred | wc -l | xargs -L1 -IX cp next/$LASTFR.png  pred/0X.png

echo "------------------------"
