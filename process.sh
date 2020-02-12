width=2000
date > start_time.txt
python3 radius.py > radius.dat
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    if [ ! -f ${dataset}.map ]; then    
	python3 overlap.py ${dataset} > ${dataset}.map
    fi
    if [ ! -f ${dataset}_validation.png ]; then
	echo "Validating $dataset"
	python3 validate.py $dataset # check the annotation locations by class
    fi
    python3 closeup.py ${dataset} # individual samples
    python3 extract.py ${dataset}        
    echo GREEN
    ls -lh *_green_t*.png | wc -l
    echo YELLOW
    ls -lh *_yellow_t*.png | wc -l
    echo RED
    ls -lh *_red_t*.png | wc -l
    echo LEAFLESS
    ls -lh *_leafless_t*.png | wc -l 
    if [ ! -f ${dataset}_smaller.png ]; then # resize for efficiency
	echo "Resizing to a width of $width pixels"
	convert -resize ${width}x -transparent black $file ${dataset}_smaller.png # ensure RGBA with black transparent
	rm -f ${dataset}_enhanced.png # force the enhancement to be redone
    fi
    if [ ! -f ${dataset}_enhanced.png ]; then
	echo "Enhancing $dataset"
	python3 enhance.py ${dataset} >> offsets.txt # enhance color spectrum
	rm -f ${dataset}_histo.png # force the extraction to be redone
	rm -f ${dataset}_diff.png # force the analysis to be redone
	rm -f ${dataset}_thresholded.png # force the processing to be redone
	python3 grayscale.py ${dataset} # a figure for the manuscript
    fi

    if [ ! -f ${dataset}_histo.png ]; then
	echo "Analyzing $dataset"
	python3 histogram.py ${dataset}
    fi
done
python3 examples.py 
for file in `ls -1 *.tiff`; do 
    dataset=`basename $file .tiff`
    if [ ! -f ${dataset}_diff.png ]; then
	echo "Additional characterization for $dataset"
	python3 chandiff.py ${dataset}
    fi
done
python3 projections.py # update the 2D projections
echo 'Characterization concluded'
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    if [ ! -f ${dataset}_thresholded.png ]; then
	echo "Thresholding $dataset"
	python3 threshold.py ${dataset}
	rm ${dataset}.log 
    fi
    if [ ! -f ${dataset}.log ]; then
	python3 automaton.py ${dataset}_thresholded.png > ${dataset}.log
    fi
done
python3 collages.py # update the pixel collages
echo "Evaluating the results"
python3 test.py > results.txt
python3 confusion.py results.txt # just to see
python3 confusion.py results.txt tex > results.tex # redo the reesults in LaTeX
gnuplot changes.plot
fgrep "\\\\" results.tex > conf.tex
fgrep "$" results.tex | sed 's/$/ \\\\/' > perf.tex
bash figures.sh # update the manuscript figure files
date > end_time.txt

