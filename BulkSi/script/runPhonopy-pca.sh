# main command
root=$PWD

for i in "p10" "p15" "p20" "p30" "noPCA"; do
    folder="d20n50-PCA/"${i}
    for j in $(seq 1 10); do
        dir=${root}/${folder}/${j}/predict-phonopy
        cd ${dir}
        python phonopyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
        hdnnpy predict
        python phonopyRun.py --prefix Crystal --dim 2 2 2 --poscar POSCAR-unitcell --mesh 2 2 2
    done
done