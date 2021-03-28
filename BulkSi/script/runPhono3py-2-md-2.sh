# main command
root=$PWD

for i in "1000K0.99" "1000K1.0" "1000K1.01"; do
    for j in $(seq 1 10); do
        dir=${root}/${i}/${j}/predict-phono3py
        cd ${dir}
        echo ${i}/${j}
        python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
    done
done
#end