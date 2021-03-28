# main command
root=$PWD

for j in $(seq 21 30); do
    dir=${root}/1000K-LC7/mix/3500smpl/${j}
    cd ${dir}
    qsub run.csh
done
#end

