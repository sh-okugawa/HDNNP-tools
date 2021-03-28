# main command
root=$PWD

for i in "1000K" "1200K"; do
    for j in $(seq 1 10); do
        dir=${root}/${i}/${j}/predict-phono3py
        cd ${dir}
        python phono3pyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
        qsub predictionRun.sh
    done
done
#end