# main command
root=$PWD

for j in $(seq 1 10); do
    dir=${root}/d20n50-newPCA/${j}/predict-phono3py
    cd ${dir}
    python phono3pyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
    qsub predictionRun.sh
done