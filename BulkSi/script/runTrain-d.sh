# main command
root=$PWD

for k in 2 10; do
    for i in "50" "100" "200" "300" "500"; do
        folder="d"${k}"n"${i}
        for j in $(seq 1 1 10); do
            dir=${root}/${folder}/${j}
            cd ${dir}
            qsub run.csh
        done
    done
done
#end
