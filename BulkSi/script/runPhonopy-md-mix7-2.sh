# main command
root=$PWD

for i in "0.95" "0.97" "0.99" "1.0" "1.01" "1.03" "1.05"; do
    for j in $(seq 1 10); do
        dir=${root}/1000K-LC7/${i}/${j}/predict-phonopy
        cd ${dir}
        python phonopyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
        hdnnpy predict
        python phonopyRun.py --prefix Crystal --dim 2 2 2 --poscar POSCAR-unitcell --mesh 2 2 2
    done
done
#end
