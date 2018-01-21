#! /bin/bash
mkdir "$1-tiles";
cd "$1-tiles";

for i in $( ls ../$1 ); do
	for j in `seq 0 1`; do
		mkdir "$i-$j";
	done
done

cd ..;
cd $1;

for i in $( ls ); do
		echo "$1/$i";
		cd $i;
		count=0
		var=0
		for j in $( ls ); do
			#let "var = (count - 1) % 6"
			#if [ $var -eq 0 ]; then
			#if [ $count -gt 0 ]; then
			convert -resize 128x64 -crop 2x1@ +repage +adjoin $j ../../"$1-tiles"/"$i-%01d"/$j;
			#fi
			#let "count = count + 1"
		done
		cd ..;
done
