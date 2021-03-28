# main command
root=$PWD

for i in "p10" "p15" "p20" "p30" "noPCA"; do
    folder="d20n50-PCA/"${i}
    for j in $(seq 1 10); do
        dir=${root}/${folder}/${j}
        cd ${dir}
        qsub run.csh
    done
done
#end
