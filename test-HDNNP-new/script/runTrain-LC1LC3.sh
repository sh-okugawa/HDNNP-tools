# main command
root=$PWD

for j in $(seq 1 5); do
    dir=${root}/1000K-LC3/mix/3000smpl/${j}
    cd ${dir}
    qsub run.csh
done

for j in $(seq 1 5); do
    dir=${root}/1000K-LC1/1500smpl/${j}
    cd ${dir}
    qsub run.csh
done

#end

