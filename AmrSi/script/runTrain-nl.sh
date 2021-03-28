# main command
root=$PWD

for i in "2" "4" "5"; do
    for j in $(seq 1 5); do
        dir=${root}/amr216/300smpl/40-${i}/${j}
        cd ${dir}
        qsub run.csh
    done
done

for i in "100" "200"; do
    for j in "2" "3" "4" "5"; do
        for k in $(seq 1 5); do
            dir=${root}/amr216/300smpl/${i}-${j}/${k}
            cd ${dir}
            qsub run.csh
        done
    done
done
#end