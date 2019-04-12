#/bin/bash

for i in `ls *_31-50.csv`
do
    j="${i/31-50/1-30}"
    k="${i/31-50/1-50}"
    cat $j >> $k
    tail -n +2 $i >> $k
done
