# main command
root=$PWD

for j in $(seq 1 5); do
    dir=${root}/1000K-LC3/mix/3000smpl/${j}/predict-phono3py
    cd ${dir}
    echo small/${j}
    python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
done

for j in $(seq 1 5); do
    dir=${root}/1000K-LC1/1500smpl/${j}/predict-phono3py
    cd ${dir}
    echo small/${j}
    python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
done