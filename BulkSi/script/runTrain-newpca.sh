# main command
root=$PWD

for j in $(seq 1 10); do
    dir=${root}/d20n50-newPCA/${j}
    cd ${dir}
    qsub run.csh
done
#end
