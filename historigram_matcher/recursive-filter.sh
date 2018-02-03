cd Data;
cd Train;
for i in $( ls -d */ ); do
echo "Entering dir " $i;
cd $i;
first=`ls|head -n1`
echo "Changing the colour levels of" $first
convert $first -level 25% $first;
echo "Adjusting the rest of histograms to " $first
for j in $( ls|tail -n32 );
do bash ../../../histmatch.sh $first $j $j;
done;
cd ..;
done;
cd ..;
cd ..;
