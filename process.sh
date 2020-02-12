width=2000
date > start_time.txt
python3 radius.py
for file in `ls -1 *.tiff`; do
    dataset=`basename $file .tiff`
    if [ ! -f ${dataset}.map ]; then    
	python3 overlap.py ${dataset} > ${dataset}.map
    fi
    if [ ! -f ${dataset}_validation.png ]; then
	echo "Validating $dataset"
	python3 validate.py $dataset # check the annotation locations by class
    fi
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
echo 'SAMPLE COUNTS'
cat *.map | awk '{if ($1 > 30) {print $2}}' | sort | uniq -c
for file in `ls -1 *.tiff`; do 
    dataset=`basename $file .tiff`
    if [ ! -f ${dataset}_diff.png ]; then
	echo "Additional characterization for $dataset"
	python3 chandiff.py ${dataset}
    fi
done
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
echo "Evaluating the results"
python3 test.py > results.txt
python3 confusion.py results.txt # just to see
echo "Updating figures for the manuscript"
python3 projections.py # update the 2D projections
python3 collages.py # update the pixel collages
python3 confusion.py results.txt tex > results.tex # redo the reesults in LaTeX
gnuplot changes.plot
fgrep "\\\\" results.tex > conf.tex
fgrep "$" results.tex | sed 's/$/ \\\\/' > perf.tex
bash figures.sh # update the manuscript figure files
wc -l *.map # how many non-overlapping annotations there were
date > end_time.txt

