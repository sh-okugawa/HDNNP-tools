# main command
root=$PWD

for i in "1000K0.99" "1000K1.0" "1000K1.01"; do
    for j in $(seq 1 10); do
        dir=${root}/${i}/${j}/predict-phonopy
        cd ${dir}
        python phonopyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
        hdnnpy predict
        python phonopyRun.py --prefix Crystal --dim 2 2 2 --poscar POSCAR-unitcell --mesh 2 2 2
    done
done
#end
