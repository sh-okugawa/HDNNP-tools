# main command
root=$PWD

for i in "0.95" "0.97" "0.99" "1.0" "1.01" "1.03" "1.05"; do
    for j in $(seq 1 10); do
        dir=${root}/1000K-LC7/${i}/${j}
        cd ${dir}
        qsub run.csh
    done
done
#end

