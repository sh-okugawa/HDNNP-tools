# main command
root=$PWD

for j in $(seq 1 10); do
    dir=${root}/amr216/300smpl/${j}
    cd ${dir}
    qsub run.csh
done
#end

