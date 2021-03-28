# main command
root=$PWD

for j in $(seq 1 1 10); do
    dir=${root}/d20n50/${j}/predict-phono3py2
    cd ${dir}
    python phono3pyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
    qsub predictionRun.sh
done
#end
