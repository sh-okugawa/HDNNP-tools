# main command
root=$PWD

for j in $(seq 11 20); do
    dir=${root}/1000K-LC7/mix/3500smpl/${j}/predict-phono3py
    cd ${dir}
    echo small/${j}
    python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
done