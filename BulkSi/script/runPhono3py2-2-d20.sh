# main command
root=$PWD

for j in $(seq 1 1 10); do
    dir=${root}/d20n50/${j}/predict-phono3py2
    cd ${dir}
    echo ${folder}/${j}
    python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
done