classes=( green yellow red leafless ground )
for c in "${classes[@]}"
do
    convert -loop 0 -delay 20 individual/original/${c}/*_${c}_*.png ${c}.gif
done
