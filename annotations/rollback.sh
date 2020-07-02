#!/bin/zsh

for file in `ls -1 *.annot`;
do
    dataset=`basename $file .annot`	
    grep -v \- ${dataset}.annot | grep -v \# | awk '{print $2" "$3" "$4}' > ${dataset}.raw
done
