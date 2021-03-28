# main command
root=$PWD

for grp in "1000K" "1200K"; do
    for j in $(seq 1 10); do
        qsub runPlotPC-md.csh ${grp} ${j}
    done
done
#end