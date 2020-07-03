#!/bin/zsh

for file in `ls -1 *.annot`;
do
    dataset=`basename $file .annot`	
    grep -v \- ${dataset}.annot | grep -v \# | awk -v ds=${dataset} '{print ds" "$2" "$3" "$4}' > ${dataset}.raw
done
