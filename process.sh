width=2000
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    echo Processing $dataset
    if [ ! -f ${dataset}_validation.png ]; then    
	python3 validate.py $file # check the annotation locations by class
    fi
    if [ ! -f ${dataset}_smaller.png ]; then # resize for efficiency
	echo Resizing to a width of $width pixels
	convert -resize ${width}x -transparent black $file ${dataset}_smaller.png 
	
    fi
    if [ ! -f ${dataset}_smaller_enhanced.png ]; then    
	python3 enhance.py ${dataset}_smaller.png # enhance color spectrum
    fi
    python3 histogram.py ${dataset}_smaller_enhanced.png # analyze isolated class samples
done

