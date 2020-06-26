cat ~/Downloads/annotations* aug100.raw | grep 'aug100' > temp; mv temp aug100.raw
cat ~/Downloads/annotations* aug90.raw | grep 'aug90' > temp; mv temp aug90.raw 
cat ~/Downloads/annotations* jul90.raw | grep 'jul90' > temp; mv temp jul90.raw
cat ~/Downloads/annotations* jul100.raw | grep 'jul100' > temp; mv temp jul100.raw
cat ~/Downloads/annotations* jun60.raw | grep 'jun60' > temp; mv temp jun60.raw
rm ~/Downloads/annotations*.txt
cat *.raw | grep -v '#' | awk '{print $1" "$2}' | sort | uniq -c
