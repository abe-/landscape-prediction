for i in $( ls -d */ ); do 
echo "Entering dir " $i; 
cd $i; 
echo "Changing the colour levels of 000.png"
convert 000.png -level 25% 000.png; 
echo "Adjusting the rest of histograms to 000.png"
for j in $( ls|tail -n32 ); 
do bash ../histmatch.sh 000.png $j $j; 
done; 
cd ..; 
done;

