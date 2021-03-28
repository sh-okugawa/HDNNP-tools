# main command
root=$PWD
dir=${root}/1000K-LC7/0.95/1/predict-phono3py-4
cd ${dir}
python phono3pyPrep.py --prefix Crystal --poscar POSCAR-unitcell --dim 2 2 2
qsub predictionRun.sh
