for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    echo Processing $dataset
    if [ ! -f ${dataset}_smaller.png ]; then
	echo Resizing to a width of 1000 pixels
	convert -resize 1000x -transparent black $file ${dataset}_smaller.png
	
    fi
    if [ ! -f ${dataset}_smaller_enhanced.png ]; then    
	python3 enhance.py ${dataset}_smaller.png
    fi
    python3 histogram.py ${dataset}_smaller_enhanced.png
done

