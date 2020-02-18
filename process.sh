reqs=$@
declare -a classes=("green" "yellow" "red" "leafless")
mkdir -p timestamps
mkdir -p validation
for arg in "$reqs"
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
for arg in "$reqs" 
do
    if [ "$arg" == "valid" ] # if locations change
    then
	echo Validating
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
for arg in "$reqs" 
do
    if [ "$arg" == "char" ] 
    then
	echo Characterizing
	mkdir -p individual/squares
	mkdir -p individual/circles
	mkdir -p histograms
	mkdir -p composite/enhanced
	mkdir -p composite/original
	mkdir -p projections
	date > timestamps/characterization_start_time.py
	for file in `ls -1 orthomosaics/*.tiff`; do
	    echo "Characterizing $dataset"
	    dataset=`basename $file .tiff`
	    python3 extract.py ${dataset} # individual samples in individual files
	    convert -background none individual/circles/${dataset}_*.png +append composite/enhanced/${dataset}.png
	    convert -background none individual/original/${dataset}_*.png +append composite/original/${dataset}.png	
	    for kind in "${classes[@]}"
	    do
		convert -background none individual/circles/*_${kind}_*.png +append composite/enhanced/${kind}.png
		convert -background none individual/original/*_${kind}_*.png +append composite/original/${kind}.png
		convert -background none individual/circles/${dataset}_${kind}_*.png +append composite/enhanced/${dataset}_${kind}.png
		convert -background none individual/original/${dataset}_${kind}_*.png +append composite/original/${dataset}_${kind}.png
	    done
	    python3 histogram.py ${dataset} # the channel histograms for the manuscript
	    python3 chandiff.py ${dataset} # the channel-difference histograms for the manuscript
	done
	date > timestamps/characterization_end_time.py
	for kind in "${classes[@]}"
	do
	    echo $kind
	    ls -lh individual/circles/*_${kind}_*.png | wc -l
	done
	python3 projections.py # illustrations for the manuscript
	break
    fi
done
width=1000
for arg in "$reqs" 
do
    if [ "$arg" == "scale" ] 
    then
	echo Rescaling
	mkdir -p scaled/enhanced
	mkdir -p scaled/original
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`	
	    convert -resize ${width}x orthomosaics/$dataset.png scaled/original/$dataset.png	
	    convert -resize ${width}x enhanced/$dataset.png scaled/enhanced/$dataset.png
	done
    fi
    break
done
mkdir -p thresholded
mkdir -p automaton/frames
mkdir -p output/automaton
mkdir -p output/original
rm results.txt # redo the result file
touch results.txt
date > timestamps/processing_start_time.py
for file in `ls -1 orthomosaics/*.tiff`
do
    dataset=`basename $file .tiff`
    echo "Processing $dataset"
    python3 threshold.py $dataset
    python3 automaton.py $dataset > automaton/${dataset}.log
    python3 test.py $dataset >> results.txt # compute the results
done
echo "Evaluating the results"
python3 confusion.py results.txt # view the results
date > timestamps/processing_end_time.py
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
python3 collages.py # update the pixel collages for the manuscript
mkdir -p examples/squares
mkdir -p examples/enhanced
mkdir -p examples/original
python3 examples.py # update the examples of the samples for the manuscript
python3 confusion.py results.txt tex > results.tex # format the results in LaTeX
gnuplot changes.plot # update the convergence figure for the manuscript
fgrep "\\\\" results.tex > conf.tex
fgrep "$" results.tex | sed 's/$/ \\\\/' > perf.tex
bash figures.sh # update the manuscript figure files based on the results
