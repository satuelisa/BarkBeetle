fastReplicas=30 # the only purpose of the replicas is the time measurement
slowReplicas=3 # slower phases are repeated fewer times
width=1000 # to which width to scale down the images for the final phases 
declare -a classes=("green" "yellow" "red" "leafless")
req=($(echo $@ | tr ' ' '\n'))
all=`grep "\$arg" process.sh | grep '==' | grep -v 'process' | grep -v 'all' | cut -c 21-30 | awk -F '"' '{print $1}'`
echo Available $all
for arg in "${req}"
do
    if [ "$arg" == "all" ] 
    then
	req=($(echo "all" $all | tr ' ' '\n'))
	req=`echo $all | tr ' ' '\n'`
	break
    fi    
done
echo Requested:
for arg in "${req[@]}"
do
    echo "*" $arg
done
mkdir -p timestamps
for arg in "${req[@]}"
do
    if [ "$arg" == "crop" ] 
    then
	mkdir -p cropped
	rm -rf cropped/*.png
	rm -f timestamps/crop*
	{ date & echo $slowReplicas; } >> timestamps/cropping_start_time.txt	
	for n in $(seq $slowReplicas)
	do
	    echo Cropping, replica $n out of $slowReplicas
	    python3 bb.py > bb.plot
	done
	{ date & echo $slowReplicas; } >> timestamps/cropping_end_time.txt
	grep '# crop' bb.plot > offsets.txt
	break
    fi
done
for arg in "${req[@]}"
do
    if [ "$arg" == "enhance" ] 
    then
	rm -f timestamps/enhance*
	mkdir -p enhanced/normalized
	mkdir -p enhanced/equalized
	mkdir -p enhanced/uniform
	mkdir -p enhanced/modulated
	rm -rf enhanced/*/*.png
	rm -rf enhanced/*.png
	{ date & echo $slowReplicas; } >> timestamps/enhancement_start_time.txt	
	for n in $(seq $slowReplicas)
	do
	    echo Enhancing, replica $n out of $slowReplicas	    
	    bash enhance.sh
	done
	{ date & echo $slowReplicas; } >> timestamps/enhancement_end_time.txt
	break
    fi
done
# these are separate loops to ensure correct order in case phases are picked out of order
for arg in "${req[@]}" 
do
    if [ "$arg" == "scale" ] 
    then
	mkdir -p scaled/enhanced
	mkdir -p scaled/original
	rm -f timestamps/scal*
	{ date & echo $slowReplicas; } >> timestamps/scaling_start_time.txt		
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
	{ date & echo $slowReplicas; } >> timestamps/scaling_end_time.txt
	break
    fi
done
for arg in "${req[@]}" 
do
    if [ "$arg" == "pre" ] # preproc annotations
    then
	rm -f timestamps/preprocess*
	{ date & echo $fastReplicas; } >> timestamps/preprocessing_start_time.txt 	
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
	{ date & echo $fastReplicas; } >> timestamps/preprocessing_end_time.txt	 
	break
    fi
done
for arg in "${req[@]}" 
do
    if [ "$arg" == "ext" ] 
    then
	mkdir -p individual/squares
	mkdir -p individual/original
	mkdir -p individual/enhanced
	rm -f timestamps/extract*
	{ date & echo $slowReplicas; } >> timestamps/extraction_start_time.txt
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
	{ date & echo $slowReplicas; } >> timestamps/extraction_end_time.txt	    
	break
    fi
done
for arg in "${req[@]}" 
do
    if [ "$arg" == "post" ] 
    then
	mkdir -p composite/enhanced
	mkdir -p composite/original
	rm -rf composite/*/*.png
	rm -f timestamps/post*
	{ date & echo $slowReplicas; } >> timestamps/postprocessing_start_time.txt	
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
	{ date & echo $slowReplicas; } >> timestamps/postprocessing_end_time.txt
	break
    fi
done
for arg in "${req[@]}"
do
    if [ "$arg" == "char" ]
    then
	start=80
	end=99
	step=1
	listing=`python -c "print(' '.join([str(x) for x in range($start, $end + 1, $step)]))"`
	echo Using quantiles $listing
	quantiles=($(echo $listing | tr ' ' '\n'))	
	mkdir -p thresholds
	rm -f thresholds/*.txt
	rm -f timestamps/char*
	{ date & echo $slowReplicas; } >> timestamps/characterization_start_time.txt
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
	{ date & echo $slowReplicas; } >> timestamps/characterization_end_time.txt
	best=`head -n 1 best.txt | awk '{print $1}'` # just use the first if there are many
	cp thresholds/thr_$best.txt thresholds.txt
	break
    fi
done
mkdir -p thresholded
for arg in "${req[@]}" 
do
    if [ "$arg" == "thr" ] 
    then
	rm -f timestamps/thr*
	{ date & echo $slowReplicas; } >> timestamps/thresholding_start_time.txt
	for n in $(seq $slowReplicas)
	do
	    echo Thresholding, replica $n out of $slowReplicas	    
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		python3 threshold.py $dataset
	    done
	done
	{ date & echo $slowReplicas; } >> timestamps/thresholding_end_time.txt
	break
    fi
done
for arg in "${req[@]}" 
do
    if [ "$arg" == "ca" ] 
    then
	rm -f timestamps/autom*
	{ date & echo $slowReplicas; } >> timestamps/automata_start_time.txt
	for n in $(seq $slowReplicas)
	do
	    echo Automata, replica $n out of $slowReplicas	    
	    for file in `ls -1 orthomosaics/*.tiff`
	    do
		dataset=`basename $file .tiff`
		python3 automaton.py $dataset > automaton/${dataset}.log
	    done
	done
	{ date & echo $slowReplicas; } >> timestamps/automata_end_time.txt
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
for arg in "${req[@]}" 
do
    if [ "$arg" == "eval" ] 
    then
	mkdir -p output/air/original
	mkdir -p output/air/automaton
	mkdir -p output/air/enhanced
	mkdir -p output/air/thresholded
	rm -f timestamps/eval*
	{ date & echo $fastReplicas; } >> timestamps/evaluation_start_time.txt
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
	{ date & echo $fastReplicas; } >> timestamps/evaluation_end_time.txt
	break
    fi
done
for arg in "${req[@]}" 
do
    if [ "$arg" == "cover" ] 
    then
	rm -f timestamps/cover*
	{ date & echo $fastReplicas; } >> timestamps/coverage_start_time.txt
	for n in $(seq $fastReplicas)
	do
	    echo Computing coverage, replica $n out of $fastReplicas		    
	    python3 counts.py > coverage.txt
	    python3 coverage.py
	done
	{ date & echo $fastReplicas; } >> timestamps/coverage_end_time.txt	    
	break
    fi
done
for arg in "${req[@]}" 
do
    if [ "$arg" == "forecast" ] 
    then
	mkdir -p output/ground/original
	mkdir -p output/ground/automaton
	mkdir -p output/ground/enhanced
	mkdir -p output/ground/thresholded
	rm -f timestamps/forecast*
	{ date & echo $fastReplicas; } >> timestamps/forecasting_start_time.txt
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
	{ date & echo $fastReplicas; } >> timestamps/forecasting_end_time.txt
	break
    fi
done
for arg in "${req[@]}" 
do
    if [ "$arg" == "update" ] # update the manuscript
    then
	for kind in "${classes[@]}" # count the samples 
	do
	    echo $kind
	    ls -lh individual/enhanced/*_${kind}_*.png | wc -l
	done
	echo Examined quantiles were $quantiles
	echo The BEST quantile was $best
	mkdir -p individual/thresholded
	mkdir -p individual/automaton
	for file in `ls -1 orthomosaics/*.tiff`
	do # include the thresholded and the automata versions of the samples
	    dataset=`basename $file .tiff`
	    python3 grayscale.py $dataset 
	    python3 extract.py ${dataset} post
	    python3 validate.py $dataset
	    python3 histogram.py ${dataset} # the channel histograms 
	    python3 chandiff.py ${dataset} # the channel-difference histograms 
	    python3 test.py $dataset images  # annotate the results
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
	python3 examples.py # the examples of the samples for the manuscript
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
	bash figures.sh # figure files for the manuscript
	break
    fi
done
