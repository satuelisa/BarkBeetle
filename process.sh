#!/bin/zsh
timestamps=false
if [ "$timestamps" = true ]
then
    echo Storing timestamps
    fastReplicas=30 
    slowReplicas=3
else
    echo Performing a single execution per step
    fastReplicas=1
    slowReplicas=1
fi
width=1000 
declare -a classes=( "green" "yellow" "red" "leafless" )
declare -A rgb=( ["dry"]="0x999999" ["green"]="0x00ff00" ["infested"]="0xa5ff00" ["leafless"]="0x0000ff" ["orange"]="0xffa500" ["yellow"]="0xffff00" ["red"]="0xff0000" )
req=($(echo $@ | tr ' ' '\n'))
all=$(grep "\$arg" process.sh | grep -v "process" | grep -v "all" | grep '=' | cut -c 20-30 | awk -F '"' '{print $1}')
echo Available $all
for arg in $req
do
    if [ "$arg" = "all" ] 
    then
	req=($(echo $all | tr ' ' '\n'))
	break
    fi    
done
echo Requested:
for arg in $req
do
    echo "+" $arg
done
if [ "$timestamps" = true ]
then
    mkdir -p timestamps
fi
for arg in $req
do
    if [ "$arg" = "crop" ] 
    then
	mkdir -p cropped
	rm -rf cropped/*.png
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/crop*
	    { date & echo $slowReplicas; } >> timestamps/cropping_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Cropping, replica $n out of $slowReplicas
	    python3 bb.py crop > offsets.txt
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/cropping_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "enhance" ] 
    then
	mkdir -p enhanced/normalized
	mkdir -p enhanced/equalized
	mkdir -p enhanced/uniform
	mkdir -p enhanced/modulated
	rm -rf enhanced/*/*.png
	rm -rf enhanced/*.png
	if [ "$timestamps" = true ]
	then
	    rm -f timestamps/enhance*
	    { date & echo $slowReplicas; } >> timestamps/enhancement_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Enhancing, replica $n out of $slowReplicas	    
	    zsh enhance.sh
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/enhancement_end_time.txt
	fi
	break
    fi
done
# these are separate loops to ensure correct order in case phases are picked out of order
for arg in $req
do
    if [ "$arg" = "scale" ] 
    then
	mkdir -p scaled/enhanced
	mkdir -p scaled/original
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/scal*
	    { date & echo $slowReplicas; } >> timestamps/scaling_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Scaling, replica $n out of $slowReplicas	    	    
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`	
		convert -resize ${width}x cropped/$dataset.png scaled/original/$dataset.png	
		convert -resize ${width}x enhanced/$dataset.png scaled/enhanced/$dataset.png
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/scaling_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "pre" ] # preproc annotations
    then
	if [ "$timestamps" = true ]
	then
	    rm -f timestamps/preprocess*
	    { date & echo $fastReplicas; } >> timestamps/preprocessing_start_time.txt
	fi
	for n in $(seq $fastReplicas)
	do
	    echo Preproc, replica $n out of $fastReplicas	    	    	    
	    python3 radius.py > radius.dat	    
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`	
		python3 overlap.py $dataset 
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $fastReplicas; } >> timestamps/preprocessing_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "ext" ] 
    then
	mkdir -p individual/squares
	mkdir -p individual/original
	mkdir -p individual/enhanced
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/extract*
	    { date & echo $slowReplicas; } >> timestamps/extraction_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Extracting, replica $n out of $slowReplicas
	    rm -rf individual/*/*.png
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		python3 extract.py ${dataset} 
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/extraction_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "post" ] 
    then
	mkdir -p composite/enhanced
	mkdir -p composite/original
	rm -rf composite/*/*.png
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/post*
	    { date & echo $slowReplicas; } >> timestamps/postprocessing_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Postprocessing, replica $n out of $slowReplicas
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		convert -background none individual/enhanced/${dataset}_*.png +append composite/enhanced/${dataset}.png
		convert -background none individual/original/${dataset}_*.png +append composite/original/${dataset}.png	
		for kind in "${classes[@]}"
		do
		    convert -background none individual/original/*_${kind}_*.png +append composite/original/${kind}.png
		    convert -background none individual/enhanced/*_${kind}_*.png +append composite/enhanced/${kind}.png
		    convert -background none individual/original/${dataset}_${kind}_*.png +append composite/original/${dataset}_${kind}.png
		    convert -background none individual/enhanced/${dataset}_${kind}_*.png +append composite/enhanced/${dataset}_${kind}.png
		done
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/postprocessing_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "char" ]
    then
	start=80
	end=99
	step=1
	listing=`python -c "print(' '.join([str(x) for x in range($start, $end + 1, $step)]))"`
	echo Using quantiles $listing
	quantiles=($(echo $listing | tr ' ' '\n')) 
	mkdir -p thresholds
	rm -f thresholds/*.txt
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/char*
	    { date & echo $slowReplicas; } >> timestamps/characterization_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Characterizing, replica $n out of $slowReplicas
	    rm -f ruleperf.txt # reset
	    for q in "${quantiles[@]}"
	    do
		python3 rules.py 0.$q > thresholds/thr_$q.txt
		for kind in "${classes[@]}"
		do
		    python3 threshold.py $kind $q >> ruleperf.txt
		done
	    done
	    python3 ruleperf.py > best.txt
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/characterization_end_time.txt
	fi
	best=`head -n 1 best.txt | awk '{print $1}'` # just use the first if there are many
	cp thresholds/thr_$best.txt thresholds.txt
	echo Examined quantiles were $quantiles
	echo The BEST quantile was $best
	break
    fi
done
mkdir -p thresholded
for arg in $req
do
    if [ "$arg" = "thr" ] 
    then
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/thr*
	    { date & echo $slowReplicas; } >> timestamps/thresholding_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Thresholding, replica $n out of $slowReplicas	    
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		python3 threshold.py $dataset
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/thresholding_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "ca" ] 
    then
	if [ "$timestamps" = true ]
	then
	    rm -f timestamps/autom*
	    { date & echo $slowReplicas; } >> timestamps/automata_start_time.txt
	fi
	for n in $(seq $slowReplicas)
	do
	    echo Automata, replica $n out of $slowReplicas	    
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		python3 automaton.py $dataset > automaton/${dataset}.log
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $slowReplicas; } >> timestamps/automata_end_time.txt
	fi
	echo Creating GIFs
	rm -rf automaton/frames # force clear so as not to affect the GIF
	mkdir -p automaton/frames
	for file in `ls -1 orthomosaics/*.tiff`
	do
	    dataset=`basename $file .tiff`
	    python3 automaton.py $dataset GIF # make the GIFs (the method is deterministic) 
	done
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "eval" ] 
    then
	mkdir -p output/air/original
	mkdir -p output/air/automaton
	mkdir -p output/air/enhanced
	mkdir -p output/air/thresholded
	if [ "$timestamps" = true ]
	then
	    rm -f timestamps/eval*
	    { date & echo $fastReplicas; } >> timestamps/evaluation_start_time.txt
	fi
	for n in $(seq $fastReplicas)
	do
	    echo Evaluating, replica $n out of $fastReplicas	
	    rm results.txt # redo the result file
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		python3 test.py $dataset >> results.txt 
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $fastReplicas; } >> timestamps/evaluation_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "cover" ] 
    then
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/cover*
	    { date & echo $fastReplicas; } >> timestamps/coverage_start_time.txt
	fi
	for n in $(seq $fastReplicas)
	do
	    echo Computing coverage, replica $n out of $fastReplicas		    
	    python3 counts.py > coverage.txt
	    python3 coverage.py
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $fastReplicas; } >> timestamps/coverage_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "forecast" ] 
    then
	mkdir -p output/ground/original
	mkdir -p output/ground/automaton
	mkdir -p output/ground/enhanced
	mkdir -p output/ground/thresholded
	if [ "$timestamps" = true ]
	then	
	    rm -f timestamps/forecast*
	    { date & echo $fastReplicas; } >> timestamps/forecasting_start_time.txt
	fi
	for n in $(seq $fastReplicas)
	do
	    echo Forecasting, replica $n out of $fastReplicas		    	    
	    rm ground.txt # redo the forecast result file
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
	    python3 test.py $dataset ground >> ground.txt 
	    done
	done
	if [ "$timestamps" = true ]
	then
	    { date & echo $fastReplicas; } >> timestamps/forecasting_end_time.txt
	fi
	break
    fi
done
for arg in $req
do
    if [ "$arg" = "update" ] # update the manuscript
    then
	ec=`awk '{print $2}' trees.dat | sort | uniq | grep -v kind`
        eclasses=($(echo $ec)) 
	for expc in "${eclasses[@]}"
	do
	    color=`echo ${rgb[$expc]}`
	    grep $expc trees.dat | tail -n +2 | awk -v color=$color '{print $4" "$3" "color}' > exp_$expc.dat
	done
	python3 bb.py > bb.plot
	for kind in "${classes[@]}" # count the samples 
	do
	    echo $kind
	    ls -lh individual/enhanced/*_${kind}_*.png | wc -l
	done
	mkdir -p individual/thresholded
	mkdir -p individual/automaton
	mkdir -p ground/individual/thresholded
	mkdir -p ground/individual/automaton	
	mkdir -p ground/individual/squares
	mkdir -p ground/individual/original
	mkdir -p ground/individual/enhanced
	for file in `ls -1 orthomosaics/*.tiff`
	do 
	    dataset=`basename $file .tiff`
	    python3 grayscale.py $dataset
	    python3 extract.py ${dataset} post
	    python3 validate.py $dataset
	    python3 histogram.py ${dataset} 
	    python3 chandiff.py ${dataset} 
	    python3 test.py $dataset images 
	done
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
	mkdir -p histograms
	mkdir -p projections
	python3 projections.py # illustrations for the manuscript
	mkdir -p collages/original
	mkdir -p collages/enhanced
	mkdir -p collages/thresholded
	python3 collages.py # the pixel collages for the manuscript
	mkdir -p examples/squares
	mkdir -p examples/enhanced
	mkdir -p examples/original
	mkdir -p examples/thresholded
	mkdir -p examples/automaton
	python3 examples.py 4 4
	mkdir -p examples/ground/squares
	mkdir -p examples/ground/enhanced
	mkdir -p examples/ground/original
	mkdir -p examples/ground/thresholded
	mkdir -p examples/ground/automaton	
	python3 examples.py 1 5 ground 
	python3 confusion.py results.txt tex > results.tex # format the results in LaTeX
	fgrep "% CM" results.tex | tail -n +2 > conf.tex
	fgrep "% STATS" results.tex > perf.tex
	for kind in "${classes[@]}"
	do	
	    grep $kind coverage.txt | awk -v k=$kind '{print $1" "$3" "k}' | sed 's/jun60/0/g;s/jul90/1/g;s/jul100/2/g;s/aug90/3/g;s/aug100/4/g' > coverage/$kind.txt
	done
	grep black coverage.txt | awk -v k=$kind '{print $1" "$3" "k}' | sed 's/jun60/0/g;s/jul90/1/g;s/jul100/2/g;s/aug90/3/g;s/aug100/4/g' > coverage/background.txt	
	cat coverage/green.txt | awk '{print $1" "$2" "0}' | sort -g > coverage/g.txt	
	cat coverage/g.txt coverage/yellow.txt | awk '{a[$1] += $2; if ($3 != "yellow"){b[$1] = $2}}END{for (x in a) {print x" "a[x]" "b[x]}}' | sort -g > coverage/gy.txt
	cat coverage/gy.txt coverage/red.txt | awk '{a[$1] += $2; if ($3 != "red"){b[$1] = $2}}END{for (x in a) {print x" "a[x]" "b[x]}}' | sort -g > coverage/gyr.txt
	cat coverage/gyr.txt coverage/leafless.txt | awk '{a[$1] += $2; if ($3 != "leafless"){b[$1] = $2}}END{for (x in a) {print x" "a[x]" "b[x]}}' | sort -g > coverage/gyrl.txt
	cat coverage/gyrl.txt coverage/background.txt | awk '{a[$1] += $2; if ($3 != "background"){b[$1] = $2}}END{for (x in a) {print x" "a[x]" "b[x]}}' | sort -g > coverage/all.txt
	gnuplot coverage.plot
	zsh figures.sh # figure files for the manuscript
	break
    fi
done
