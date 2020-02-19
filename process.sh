declare -a classes=("green" "yellow" "red" "leafless")
echo Stages requested
for arg in "$@"
do
    echo "* " $arg
done
mkdir -p timestamps
for arg in "$@"
do
    if [ "$arg" == "enhance" ] 
    then
	echo Enhancing
	bash enhance.sh
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`	
	    python3 grayscale.py $dataset # figure for the manuscript
	done
	break
    fi
done
# these are separate loops to ensure correct order if multiple are chosen
for arg in "$@" 
do
    if [ "$arg" == "valid" ] # if locations change
    then
	echo Validating
	mkdir -p validation
	python3 radius.py > radius.dat
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`	
	    python3 overlap.py $dataset 
	    python3 validate.py $dataset
	done
	break
    fi
done
for arg in "$@" 
do
    if [ "$arg" == "char" ] 
    then
	echo Characterizing
	mkdir -p individual/squares
	mkdir -p individual/original
	mkdir -p individual/enhanced
	mkdir -p histograms
	mkdir -p composite/enhanced
	mkdir -p composite/original
	mkdir -p projections
	date > timestamps/characterization_start_time.py
	for file in `ls -1 orthomosaics/*.tiff`; do
	    echo "Characterizing $dataset"
	    dataset=`basename $file .tiff`
	    python3 extract.py ${dataset} # individual samples in individual files
	    convert -background none individual/enhanced/${dataset}_*.png +append composite/enhanced/${dataset}.png
	    convert -background none individual/original/${dataset}_*.png +append composite/original/${dataset}.png	
	    for kind in "${classes[@]}"
	    do
		convert -background none individual/original/*_${kind}_*.png +append composite/original/${kind}.png
		convert -background none individual/enhanced/*_${kind}_*.png +append composite/enhanced/${kind}.png
		convert -background none individual/original/${dataset}_${kind}_*.png +append composite/original/${dataset}_${kind}.png
		convert -background none individual/enhanced/${dataset}_${kind}_*.png +append composite/enhanced/${dataset}_${kind}.png
	    done
	    python3 histogram.py ${dataset} # the channel histograms for the manuscript
	    python3 chandiff.py ${dataset} # the channel-difference histograms for the manuscript
	done
	date > timestamps/characterization_end_time.py
	for kind in "${classes[@]}"
	do
	    echo $kind
	    ls -lh individual/enhanced/*_${kind}_*.png | wc -l
	done
	python3 projections.py # illustrations for the manuscript
	break
    fi
done
width=2000 # to which width to scale down the processing 
for arg in "$@" 
do
    if [ "$arg" == "scale" ] 
    then
	echo Scaling
	mkdir -p scaled/enhanced
	mkdir -p scaled/original
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`	
	    convert -resize ${width}x orthomosaics/$dataset.png scaled/original/$dataset.png	
	    convert -resize ${width}x enhanced/$dataset.png scaled/enhanced/$dataset.png
	done
	break
    fi
done
mkdir -p thresholded
for arg in "$@" 
do
    if [ "$arg" == "proc" ] 
    then
	echo Processing
	date > timestamps/processing_start_time.py
	rm -rf automaton/frames # force clear so as not to affect the GIF
	mkdir -p automaton/frames
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`
	    echo "Processing $dataset"
	    python3 threshold.py $dataset
	    python3 automaton.py $dataset > automaton/${dataset}.log
	    wc -l automaton/${dataset}.log
	done
	date > timestamps/processing_end_time.py	
	break
    fi
done
for arg in "$@" 
do
    if [ "$arg" == "eval" ] 
    then
	mkdir -p output/air/original
	mkdir -p output/air/automaton
	mkdir -p output/air/thresholded
	rm results.txt # redo the result file
	touch results.txt
	date > timestamps/eval_start_time.py
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`
	    echo "Evaluating $dataset"
	    python3 test.py $dataset >> results.txt 
	done
	date > timestamps/eval_end_time.py	
	python3 confusion.py results.txt 
	break
    fi
done
for arg in "$@" 
do
    if [ "$arg" == "forecast" ] 
    then
	mkdir -p output/ground/original
	mkdir -p output/ground/automaton
	mkdir -p output/ground/thresholded
	rm ground.txt # redo the forecast result file
	touch ground.txt
	date > timestamps/forecast_start_time.py
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`
	    echo "Forecasting $dataset"
	    python3 test.py $dataset ground >> ground.txt 
	done
	date > timestamps/forecast_end_time.py	
	break
    fi
done

for arg in "$@" 
do
    if [ "$arg" == "update" ] # update the manuscript
    then
	mkdir -p individual/thresholded
	mkdir -p individual/automaton
	for file in `ls -1 orthomosaics/*.tiff`
	do # update the individual samples to include the thresholded and the automata versions
	    dataset=`basename $file .tiff`  
	    python3 extract.py ${dataset} post 
	done
	# extractions for the comparative illustrations in the manuscript
	mkdir -p composite/thresholded
	mkdir -p composite/automaton
	for kind in "${classes[@]}"
	do
	    convert -background none -transparent black individual/thresholded/*_${kind}_*.png +append composite/thresholded/${kind}.png
	    convert -background none -transparent black individual/automaton/*_${kind}_*.png +append composite/automaton/${kind}.png
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		convert -background none -transparent black individual/thresholded/${dataset}_${kind}_*.png +append composite/thresholded/${dataset}_${kind}.png
		convert -background none -transparent black individual/automaton/${dataset}_${kind}_*.png +append composite/automaton/${dataset}_${kind}.png
	    done
	done
	mkdir -p collages/original
	mkdir -p collages/enhanced
	mkdir -p collages/thresholded
	python3 collages.py # the pixel collages for the manuscript
	mkdir -p examples/squares
	mkdir -p examples/enhanced
	mkdir -p examples/original
	mkdir -p examples/thresholded
	mkdir -p examples/automaton
	python3 examples.py # the examples of the samples for the manuscript
	python3 confusion.py results.txt tex > results.tex # format the results in LaTeX
	gnuplot changes.plot # update the convergence figure for the manuscript
	fgrep "\\\\" results.tex > conf.tex
	fgrep "$" results.tex | sed 's/$/ \\\\/' > perf.tex
	bash figures.sh # update the manuscript figure files based on the results
	break
    fi
done
