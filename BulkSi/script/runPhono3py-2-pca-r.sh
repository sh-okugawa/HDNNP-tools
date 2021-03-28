# main command
root=$PWD

for i in "p15/4"; do
    folder="d20n50-"${i}
    dir=${root}/${folder}/predict-phono3py
    cd ${dir}
    echo ${folder}/${j}
    python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
done