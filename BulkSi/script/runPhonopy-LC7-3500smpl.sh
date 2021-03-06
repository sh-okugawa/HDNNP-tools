# main command
root=$PWD

for j in $(seq 1 10); do
    dir=${root}/1000K-LC7/mix/3500smpl/${j}/predict-phonopy
    cd ${dir}
    python phonopyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
    hdnnpy predict
    python phonopyRun.py --prefix Crystal --dim 2 2 2 --poscar POSCAR-unitcell --mesh 2 2 2
done
#end