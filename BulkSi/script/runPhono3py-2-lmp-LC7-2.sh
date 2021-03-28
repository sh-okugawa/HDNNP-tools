# main command
root=$PWD

for i in $(seq 8 10); do
    for j in $(seq 1 10); do
        dir=${root}/1000K-LC7/mix/${i}/${j}/predict-phono3py
        cd ${dir}
        echo phono3pyRun /1000K-LC7/mix/${i}/${j}
        python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
   done
done
