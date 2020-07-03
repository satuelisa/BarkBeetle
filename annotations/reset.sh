#!/bin/zsh
purge=$1
for file in `ls -1 *.raw`;
do
    dataset=`basename $file .raw`	
    grep -v $purge ${dataset}.annot > tmp
    mv tmp ${dataset}.annot
    grep -v $purge ${dataset}.raw > tmp
    mv tmp ${dataset}.raw
done

