# main command
root=$PWD

for j in $(seq 1 10); do
    dir=${root}/d20n50-newPCA/${j}/predict-phono3py
    cd ${dir}
    echo phono3pyRun /d20n50-newPCA/${j}
    python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
done