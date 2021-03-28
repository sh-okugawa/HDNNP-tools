# main command
root=$PWD

for i in $(seq 1 10); do
    for j in $(seq 1 10); do
        dir=${root}/1000K-LC7/mix/${i}/${j}
        cd ${dir}
        qsub run.csh
    done
done
#end

