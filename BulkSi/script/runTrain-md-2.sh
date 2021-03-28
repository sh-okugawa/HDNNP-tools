# main command
root=$PWD

for i in "1000K0.99" "1000K1.0" "1000K1.01"; do
    for j in $(seq 1 10); do
        dir=${root}/${i}/${j}
        cd ${dir}
        qsub run.csh
    done
done
#end

