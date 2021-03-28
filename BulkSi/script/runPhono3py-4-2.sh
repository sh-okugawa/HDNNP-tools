# main command
root=$PWD

dir=${root}/1000K-LC7/0.95/1/predict-phono3py-4
cd ${dir}
echo phono3pyRun /1000K-LC7/0.95/1
python phono3pyRun.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2 --mesh 11 11 11 > out.txt
