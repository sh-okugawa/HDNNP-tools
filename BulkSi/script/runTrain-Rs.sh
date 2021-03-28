# main command
root=$PWD

for j in $(seq 1 10); do
    dir=${root}/1000K-LC7/Rs/mix/3/${j}
    cd ${dir}
    qsub run.csh
done
#end

