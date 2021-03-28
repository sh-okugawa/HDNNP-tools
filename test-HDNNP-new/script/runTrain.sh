# main command
root=$PWD

for j in $(seq 11 20); do
    dir=${root}/small/${j}
    cd ${dir}
    qsub run.csh
done
#end

