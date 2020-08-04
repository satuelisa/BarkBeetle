#!/bin/zsh
for file in `ls -1 cropped/*.png`; do
    dataset=`basename $file .png`
    echo Enhancing $dataset
    convert $file -separate -normalize -combine enhanced/normalized/$dataset.png
    convert -equalize enhanced/normalized/$dataset.png enhanced/equalized/$dataset.png
    # the script redist is from http://www.fmwconcepts.com/imagemagick/redist/n
    redist -s uniform enhanced/equalized/$dataset.png enhanced/uniform/$dataset.png
    # 80,230 makes too many greens to seem blue in aug90
    # 50,220 makes some yellows red
    # 70,230 distributes the errors among red and yellow but makes some yellow blue
    convert enhanced/uniform/$dataset.png -modulate 70,220 enhanced/modulated/$dataset.png 
    convert -transparent black enhanced/modulated/$dataset.png enhanced/$dataset.png
done
