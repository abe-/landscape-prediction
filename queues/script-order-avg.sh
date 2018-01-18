#!/bin/bash
for i in .clips-m20*; do mv $i .clips-m20; done
cd .clips-m20;
for i in .clips*; do eval "mv \"$i\" \"`echo "$i" | sed 's/^\.clips-m20//g'`\""; done
cd ..;
cd Adversarial_Video_Generation/Code/;
python avg_runner.py -t ../../Test-hm/ -r 4 -s 500000 -n m20;
