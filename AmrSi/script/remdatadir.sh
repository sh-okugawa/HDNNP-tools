#!/bin/bash
dirs=`find . -maxdepth 1 -mindepth 1 -type d`
for dir in $dirs; do
    #echo $dir
    subdirs=`find $dir -maxdepth 1 -mindepth 1 -type d`
    for sub in $subdirs; do
        sn=`basename ${sub}`
        if [ $sn = "2" -o  $sn = "3" -o  $sn = "4" -o  $sn = "5" -o  $sn = "6" ]; then
            echo $sub
            rm -rf $sub/data
        elif [ $sn = "7" -o  $sn = "8" -o  $sn = "9" -o  $sn = "10" ]; then
            echo $sub
            rm -rf $sub/data
        elif [ $sn = "12" -o  $sn = "13" -o  $sn = "14" -o  $sn = "15" -o  $sn = "16" ]; then
            echo $sub
            rm -rf $sub/data
        elif [ $sn = "17" -o  $sn = "18" -o  $sn = "19" -o  $sn = "20" ]; then
            echo $sub
            rm -rf $sub/data
        elif [ $sn = "22" -o  $sn = "23" -o  $sn = "24" -o  $sn = "25" -o  $sn = "26" ]; then
            echo $sub
            rm -rf $sub/data
        elif [ $sn = "27" -o  $sn = "28" -o  $sn = "29" -o  $sn = "30" ]; then
            echo $sub
            rm -rf $sub/data
        elif [ $sn = "32" -o  $sn = "33" -o  $sn = "34" -o  $sn = "35" -o  $sn = "36" ]; then
            echo $sub
            rm -rf $sub/data
        elif [ $sn = "37" -o  $sn = "38" -o  $sn = "39" -o  $sn = "40" ]; then
            echo $sub
            rm -rf $sub/data
        fi
    done
done