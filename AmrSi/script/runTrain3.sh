# main command
root=$PWD

for i in "org" "SMZ"; do
    for j in $(seq 1 10); do
        dir=${root}/amr216/1500-103040smpl/SymF/SF/${i}/${j}
        cd ${dir}
        qsub run.csh
    done
done