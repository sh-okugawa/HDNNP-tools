# main command
root=$PWD

for k in 2 10; do
    for i in "50" "100" "200" "300" "500"; do
        folder="d"${k}"n"${i}
        for j in $(seq 1 1 10); do
            dir=${root}/${folder}/${j}/predict-phono3py
            cd ${dir}
            python phono3pyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
            qsub predictionRun.sh
        done
    done
done
#end
