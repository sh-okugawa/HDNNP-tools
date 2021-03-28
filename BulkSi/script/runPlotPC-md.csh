#!/bin/csh
#$ -cwd
#$ -V -S /bin/bash
#$ -N Plot-PCPC2
#$ -o stdout
#$ -e stderr
#$ -q all.q
#$ -pe smp 24

PIPENV_PIPFILE=$HOME/HDNNP/Pipfile
pipenv run python PlotPC-batch-md.py $1 $2