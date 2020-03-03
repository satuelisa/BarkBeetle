# the script redist is from http://www.fmwconcepts.com/imagemagick/redist/n
for file in `ls -1 cropped/*.png`; do
    dataset=`basename $file .png`
    echo Enhancing $dataset
    convert $file -separate -normalize -combine enhanced/normalized/$dataset.png
    convert -equalize enhanced/normalized/$dataset.png enhanced/equalized/$dataset.png
    redist -s uniform enhanced/equalized/$dataset.png enhanced/uniform/$dataset.png
    convert enhanced/uniform/$dataset.png -modulate 60,245 enhanced/modulated/$dataset.png 
    convert -transparent black enhanced/modulated/$dataset.png enhanced/$dataset.png
done
