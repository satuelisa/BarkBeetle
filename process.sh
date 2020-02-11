python3 radius.py
width=2000
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    echo Characterizing $dataset
    if [ ! -f ${dataset}_validation.png ]; then
	echo Validating $dataset
	python3 validate.py $dataset # check the annotation locations by class
    fi
    if [ ! -f ${dataset}_smaller.png ]; then # resize for efficiency
	echo Resizing to a width of $width pixels
	convert -resize ${width}x -transparent black $file ${dataset}_smaller.png # ensure RGBA with black transparent
	rm -f ${dataset}_enhanced.png # force the enhancement to be redone
    fi
    if [ ! -f ${dataset}_enhanced.png ]; then
	echo Enhancing $dataset
	python3 enhance.py ${dataset} >> offsets.txt # enhance color spectrum
	rm -f ${dataset}_histo.png # force the extraction to be redone
	rm -f ${dataset}_diff.png # force the analysis to be redone
    fi
    if [ ! -f ${dataset}_histo.png ]; then
	echo Analyzing $dataset
	python3 histogram.py ${dataset}
	for file in `ls -1 ${dataset}_orig_*.png`; do
	    convert -transparent black $file $file
	    convert -trim $file $file
	done
	convert -transparent black ${dataset}_green.png ${dataset}_green.png
	convert -transparent black ${dataset}_yellow.png ${dataset}_yellow.png
	convert -transparent black ${dataset}_red.png ${dataset}_red.png
	convert -transparent black ${dataset}_leafless.png ${dataset}_leafless.png
	convert -trim ${dataset}_green.png ${dataset}_green.png
	convert -trim ${dataset}_yellow.png ${dataset}_yellow.png
	convert -trim ${dataset}_red.png ${dataset}_red.png
	convert -trim ${dataset}_leafless.png ${dataset}_leafless.png
    fi
done
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
    python3 majority.py ${dataset}_thresholded.png > ${dataset}.log
done
python3 projections.py # update the 2D projections
python3 collages.py
bash figures.sh # update the manuscript figure files
