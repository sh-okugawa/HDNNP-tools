# main command
root=$PWD

for i in "p10" "p15" "p20" "p30" "noPCA"; do
    folder="d20n50-PCA/"${i}
    for j in $(seq 1 10); do
        dir=${root}/${folder}/${j}/predict-phono3py
        cd ${dir}
        echo ${folder}/${j}
        python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
    done
done