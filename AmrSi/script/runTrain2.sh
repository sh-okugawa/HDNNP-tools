# main command
root=$PWD

for i in "1500-103040"; do
    for j in $(seq 11 20); do
        dir=${root}/amr216/${i}smpl/${j}
        cd ${dir}
        qsub run.csh
    done
done