mkdir -p enhanced/normalized
mkdir -p enhanced/equalized
mkdir -p enhanced/uniform
mkdir -p enhanced/modulated
date > timestamps/enhancement_start_time.txt
for file in `ls -1 complete/*.png`; do
    dataset=`basename $file .png`
    echo Enhancing $dataset
    convert $file -separate -normalize -combine enhanced/normalized/$dataset.png
    convert -equalize enhanced/normalized/$dataset.png enhanced/equalized/$dataset.png
    # the following script is from http://www.fmwconcepts.com/imagemagick/redist/n
    redist -s uniform enhanced/equalized/$dataset.png enhanced/uniform/$dataset.png
    convert enhanced/uniform/$dataset.png -modulate 60,250 enhanced/modulated/$dataset.png
    convert -transparent black enhanced/modulated/$dataset.png enhanced/$dataset.png
done
date > timestamps/enhancement_end_time.txt
