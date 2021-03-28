# main command
root=$PWD

for j in $(seq 11 20); do
    dir=${root}/1000K-LC7/mix/3500smpl/${j}/predict-phono3py
    cd ${dir}
    python phono3pyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
    qsub predictionRun.sh
done