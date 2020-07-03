cp *.raw backup/
cat ~/Downloads/annotations*.txt aug100.raw | grep 'aug100' | sort | uniq > temp; mv temp aug100.raw
cat ~/Downloads/annotations*.txt aug90.raw | grep 'aug90' | sort | uniq > temp; mv temp aug90.raw 
cat ~/Downloads/annotations*.txt jul90.raw | grep 'jul90' | sort | uniq > temp; mv temp jul90.raw
cat ~/Downloads/annotations*.txt jul100.raw | grep 'jul100' | sort | uniq > temp; mv temp jul100.raw
cat ~/Downloads/annotations*.txt jun60.raw | grep 'jun60' | sort | uniq > temp; mv temp jun60.raw
rm ~/Downloads/annotations*.*
cat *.raw | grep -v '#' | awk '{print $1" "$2}' | sort | uniq -c
