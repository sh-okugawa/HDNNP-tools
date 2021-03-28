#!/bin/csh
#$ -cwd
#$ -V -S /bin/bash
#$ -N plotSF-amrSi
#$ -o stdout
#$ -e stderr
#$ -q all.q
#$ -pe x24 24

# for deactivate OpenMP
export OMP_NUM_THREADS=1
root=$PWD
MPIROOT=/usr/local/openmpi-1.8.8/
export PATH=$MPIROOT/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPIROOT/lib
export MANPATH=$MANPATH:$MPIROOT/share/man

PIPENV_PIPFILE=$HOME/HDNNP/Pipfile
pipenv run mpirun -np 24 python plotRMSE-amr216-SF2.py