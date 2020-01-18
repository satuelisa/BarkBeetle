width=2000
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    echo Characterizing $dataset
    if [ ! -f ${dataset}_validation.png ]; then    
	python3 validate.py $file # check the annotation locations by class
    fi
    if [ ! -f ${dataset}_smaller.png ]; then # resize for efficiency
	echo Resizing to a width of $width pixels
	convert -resize ${width}x -transparent black $file ${dataset}_smaller.png # ensure RGBA with black transparent
    fi
    if [ ! -f ${dataset}_smaller_enhanced.png ]; then    
	python3 enhance.py ${dataset} # enhance color spectrum
    fi
    if [ ! -f ${dataset}_circ_histo.png ]; then        
	python3 histogram.py ${dataset} # extract and analyze isolated class samples
	# ensure that black is transparent in the extractions
	for file in `ls -1 ${dataset}_*_circ.png`; do 
	    convert -transparent black $file $file
	done
    fi
done
# analyze isolated sample color differences
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    if [ ! -f ${dataset}_diff.png ]; then
	echo Additional characterization for $dataset	
	python3 chandiff.py ${dataset} 
    fi
done
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`    
    echo Processing $dataset
    python3 threshold.py ${dataset}    
done

